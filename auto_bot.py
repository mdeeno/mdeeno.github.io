import os
import time
import datetime
import random
import platform
import ast
import urllib.parse
import json
import warnings

# 경고 메시지 무시
warnings.simplefilter(action='ignore', category=FutureWarning)

import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib import rc
from git import Repo
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# [설정 영역]
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_DIR = os.getenv("BLOG_DIR")
MAIN_DOMAIN_URL = "https://tech.mdeeno.com"

# 🔥 [수익화 설정] 일단 본인의 오픈채팅방 링크를 넣으세요. (애드픽 가입 전까지)
KAKAO_OPEN_CHAT_URL = "https://open.kakao.com/o/YOUR_LINK_HERE" 

# 🔥 [이미지 설정] AI 이미지 생성 기능 끄기 (서버 안정화 전까지 False 유지)
USE_AI_IMAGE = False

MODEL_CANDIDATES = ['gemini-2.0-flash-exp', 'gemini-2.5-flash']
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def generate_one_shot(prompt):
    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Resource exhausted" in error_msg:
                print(f"   ⏳ [서버 과부하] {model_name} 잠시 대기... (60초)")
                time.sleep(60)
                try:
                    response = model.generate_content(prompt)
                    return response.text
                except: continue
            continue
    return None

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def process_topic_one_shot(topic):
    print(f"🚀 [1/1] '{topic}' 분석 및 글 작성 중...")
    
    prompt = f"""
    Act as a Famous Real Estate Blogger. Analyze: "{topic}".
    
    Output a single VALID JSON object:
    1. "viral_title": Click-bait Korean title (Use emojis).
    2. "search_keyword": A SPECIFIC Korean location name for Naver Real Estate search (e.g., "위례동", "잠실 엘스"). 
       - CRITICAL: Must be a specific 'Dong' or 'Complex' name.
    3. "roi_data": {{ "years": [2023, 2024, 2025, 2026], "values": [index numbers], "unit": "Index", "title": "Chart Title" }}
    4. "image_prompts": ["Cover Image Prompt", "Mid-Content Image Prompt"]
    5. "blog_body_markdown": Full blog post in Korean Markdown.
       [STYLE RULES]
       - Tone: Friendly, Professional, Blog Style ("여러분!", "지금이 기회입니다!").
       - Formatting: Use **Bold**, Emojis (💰, 🚀, ✅), and short paragraphs.
       - Length: Long-form (min 2000 chars).
       - Structure: Hook -> Money Flow -> Data -> Target Spot -> Action Plan.
       - Placeholder: Put `[[MID_IMAGE]]` between Section 2 and 3.
    6. "tistory_teaser": HTML summary.
    
    Output JSON ONLY.
    """
    
    result = generate_one_shot(prompt)
    if not result: return None
    
    try:
        clean_json = result.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return data
    except Exception as e:
        print(f"⚠️ JSON 파싱 실패: {e}")
        return {
            "viral_title": f"{topic} 분석 리포트",
            "search_keyword": "서울 아파트",
            "roi_data": {"years": [2023,2024,2025,2026], "values": [100,110,120,130], "unit":"Index", "title":"전망"},
            "image_prompts": ["city", "building"],
            "blog_body_markdown": "내용 생성 실패",
            "tistory_teaser": "<p>실패</p>"
        }

def generate_graph(filename_base, data_dict):
    print(f"📊 그래프 생성 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    if not os.path.exists(image_dir): os.makedirs(image_dir)
        
    img_filename = f"{filename_base}-{int(time.time())}.png"
    img_path = os.path.join(image_dir, img_filename)

    years = data_dict.get('years', ['2024', '2025'])
    values = data_dict.get('values', [100, 110])
    title = data_dict.get('title', '시장 전망')

    plt.figure(figsize=(10, 6))
    plt.bar(years, values, color='#d32f2f')
    plt.title(title)
    plt.savefig(img_path)
    plt.close()
    return f"/images/{img_filename}"

def create_final_content(data, graph_url):
    print(f"🤖 콘텐츠 조립 중...")
    now = datetime.datetime.now()
    
    if USE_AI_IMAGE:
        prompts = data.get('image_prompts', ["city", "building"])
        if not prompts: prompts = ["city", "building"]
        encoded_cover = urllib.parse.quote(prompts[0])
        encoded_mid = urllib.parse.quote(prompts[1] if len(prompts)>1 else prompts[0])
        cover_image = f"https://image.pollinations.ai/prompt/{encoded_cover}?width=1600&height=900&nologo=true"
        mid_image = f"https://image.pollinations.ai/prompt/{encoded_mid}?width=800&height=500&nologo=true"
    else:
        cover_image = None
        mid_image = None
    
    body = data.get('blog_body_markdown', '내용 없음')
    
    if USE_AI_IMAGE and mid_image:
        if "[[MID_IMAGE]]" in body:
            body = body.replace("[[MID_IMAGE]]", f"\n![분석 이미지]({mid_image})\n")
        else:
            paragraphs = body.split('\n\n')
            insert_idx = len(paragraphs) // 2
            paragraphs.insert(insert_idx, f"\n![분석 이미지]({mid_image})\n")
            body = "\n\n".join(paragraphs)
    else:
        body = body.replace("[[MID_IMAGE]]", "")

    keyword = data.get('search_keyword', '부동산')
    
    # 🔥 [핵심 수정] 네이버 부동산(Land) 전용 URL 생성
    # 예: https://new.land.naver.com/search?sk=위례동%20아파트
    encoded_keyword = urllib.parse.quote(keyword)
    naver_land_url = f"https://new.land.naver.com/search?sk={encoded_keyword}"

    footer = f"""
\n
---
### 🔒 [VIP 리포트] '{keyword}' 투자 지도 (Coming Soon)
현재 **구체적인 진입 타이밍**과 **히든 매물**이 담긴 시크릿 리포트를 제작 중입니다.
AI가 분석한 심층 데이터가 곧 공개됩니다.

* 🔔 **[알림 신청] 리포트 무료 배포 시작 시 알림 받기 (준비중)**

---
### 💡 혹시 **투자금**이 부족하신가요?
정부 지원 **저금리 대출**이나 **내 한도**가 궁금하다면?
(조회해도 신용등급 영향 없습니다)

👉 **[내게 맞는 최저금리 상품 1분 만에 확인하기]({KAKAO_OPEN_CHAT_URL})**

[👉 네이버 부동산에서 '{keyword}' 실시간 매물 보러가기]({naver_land_url})
"""

    title = data.get('viral_title', '부동산 분석')
    front_matter = f"""---
title: "{title}"
date: {now.strftime("%Y-%m-%d")}
draft: false
categories: ["Investment Strategy"]
tags: ["Real Estate", "ROI", "Money"]
"""
    if cover_image:
        front_matter += f"""cover:
    image: "{cover_image}"
    alt: "{title}"
    relative: false
"""
    front_matter += "---"

    return f"{front_matter}\n\n![Chart]({graph_url})\n*▲ 데이터 분석 ({now.year} 기준)*\n\n{body}\n{footer}"

def deploy_to_github(title, content):
    print(f"🚀 깃허브 배포 중...") 
    safe_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{hash(title)}.md"
    filepath = os.path.join(BLOG_DIR, "content", "posts", safe_filename)
    
    with open(filepath, 'w', encoding='utf-8') as f: f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"Post: {title}")
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ 배포 완료!")
        return f"{MAIN_DOMAIN_URL}/posts/{safe_filename.replace('.md', '')}"
    except Exception as e:
        print(f"❌ 배포 실패: {e}")
        return MAIN_DOMAIN_URL

def save_tistory_file(title, html_content, link):
    draft_dir = "tistory_drafts"
    if not os.path.exists(draft_dir): os.makedirs(draft_dir)
    filename = f"Report-{datetime.datetime.now().strftime('%H%M%S')}.txt"
    
    final_html = html_content + f'<br><br><a href="{link}" style="padding:15px; background:#d32f2f; color:white; text-decoration:none; font-weight:bold; border-radius:10px;">👉 리포트 전문 확인하기 (무료)</a>'
    
    with open(os.path.join(draft_dir, filename), "w", encoding="utf-8") as f:
        f.write(f"제목: {title}\n\n[HTML 소스]\n{final_html}")
    try: os.system(f"open {draft_dir}")
    except: pass

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 PropTech 봇 (네이버 부동산 링크 완벽 수정)")
    print("   * 이제 '네이버 부동산' 지도 검색으로 바로 연결됩니다.")
    print("   * 수익화 링크는 애드픽/오픈채팅 중 편한 걸로 나중에 바꾸세요.")
    print("="*50)
    
    topic = input("✍️  분석할 주제 입력: ")
    if topic:
        data = process_topic_one_shot(topic)
        if data:
            viral_title = data.get('viral_title', topic)
            roi_data = data.get('roi_data', {})
            tistory_teaser = data.get('tistory_teaser', '<p>요약 정보가 없습니다.</p>')
            
            graph_url = generate_graph("chart", roi_data)
            full_content = create_final_content(data, graph_url)
            link = deploy_to_github(viral_title, full_content)
            save_tistory_file(viral_title, tistory_teaser, link)
            
            print("\n🎉 발행 완료!")
        else:
            print("❌ 생성 실패.")
    else:
        print("❌ 실행을 중단합니다.")