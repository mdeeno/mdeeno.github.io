import os
import time
import datetime
import random
import platform
import ast
import urllib.parse
import json
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

# 🔥 [수익화 설정] 본인의 오픈채팅방 링크나 리더스CPA/핀다/토스 링크를 넣으세요!
KAKAO_OPEN_CHAT_URL = "https://open.kakao.com/o/YOUR_LINK_HERE" 

# 🔥 [이미지 설정] AI 이미지 생성 기능 끄기 (True=켜기, False=끄기)
# 현재 이미지 서버(Pollinations) 과부하 방지를 위해 False 권장
USE_AI_IMAGE = False

# 성능 좋은 모델 하나만 사용 (원샷 처리를 위해)
MODEL_CANDIDATES = ['gemini-2.0-flash-exp', 'gemini-2.5-flash']
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def generate_one_shot(prompt):
    """
    [원샷 전략] 한 번의 호출로 기획+집필+요약을 끝냅니다. (API 차단 방지)
    """
    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            # JSON 모드 강제
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
    print(f"🚀 [1/1] '{topic}' 분석 및 글 작성 중 (원샷 통합 호출)...")
    
    # 🔥 [핵심 프롬프트 수정]
    # 1. search_keyword: 추상적 단어 금지, 구체적 행정동/아파트명 요구
    # 2. Tone & Formatting: 블로그 말투, 이모지, 짧은 문단 강제
    prompt = f"""
    Act as a Famous Real Estate Blogger (Power Blogger). Analyze: "{topic}".
    
    You must output a single VALID JSON object with these exact keys:
    1. "viral_title": A click-bait Korean title focusing on Profit/ROI (Use emojis).
    2. "search_keyword": A SPECIFIC Korean 'Dong' (neighborhood) or 'Station' name for Naver Land search (e.g., "시흥 장현지구", "안산 고잔동", "반포 래미안"). 
       - CRITICAL: Do NOT use abstract words like "undervalued" or "investment". Must be a location name.
    3. "roi_data": {{ "years": [2023, 2024, 2025, 2026], "values": [index numbers], "unit": "Index", "title": "Chart Title" }}
    4. "image_prompts": ["Cover Image Prompt", "Mid-Content Image Prompt"]
    5. "blog_body_markdown": The full blog post body in Korean Markdown.
       
       [CRITICAL WRITING STYLE RULES]
       1. **Tone**: Engaging, Professional yet Friendly (Blog Style). NOT academic. Use phrases like "여러분!", "지금 놓치면 후회합니다!".
       2. **Formatting**: 
          - Use **Bold** for key phrases frequently.
          - Use Emojis (💰, 🚀, 🏗️, ✅, ⚠️, 👋) at the start of paragraphs or headers.
          - Use Bullet points (`*`) or Numbered lists (`1.`) for readability.
       3. **Paragraphs**: Keep paragraphs SHORT (max 3-4 lines). Add line breaks often to avoid "Wall of Text".
       4. **Length**: Long-form (min 2000 characters) to maximize AdSense revenue.
       5. **Structure**: 
          - Intro (Hook) 
          - Section 1: Money Flow (Why invest here?)
          - Section 2: Data Analysis
          - Section 3: Target Spot (3 specific areas with pros/cons)
          - Section 4: Action Plan
       6. **Placeholder**: Put `[[MID_IMAGE]]` exactly between Section 2 and 3.

    6. "tistory_teaser": HTML summary for Tistory (3 bullet points + CTA button).
    
    Output JSON ONLY. No markdown code blocks.
    """
    
    result = generate_one_shot(prompt)
    if not result: return None
    
    try:
        clean_json = result.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return data
    except Exception as e:
        print(f"⚠️ JSON 파싱 실패: {e}")
        # 실패 시 비상용 더미 데이터 반환
        return {
            "viral_title": f"{topic} 분석 리포트",
            "search_keyword": "부동산 시세",
            "roi_data": {"years": [2023,2024,2025,2026], "values": [100,110,120,130], "unit":"Index", "title":"전망"},
            "image_prompts": ["city skyline", "blueprint"],
            "blog_body_markdown": "내용 생성에 실패했습니다. (API 오류)",
            "tistory_teaser": "<p>요약 생성 실패</p>"
        }

def generate_graph(filename_base, data_dict):
    print(f"📊 그래프 생성 중 (로컬)...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    if not os.path.exists(image_dir): os.makedirs(image_dir)
        
    img_filename = f"{filename_base}-{int(time.time())}.png"
    img_path = os.path.join(image_dir, img_filename)

    plt.figure(figsize=(10, 6))
    plt.bar(data_dict['years'], data_dict['values'], color='#d32f2f')
    plt.title(data_dict['title'])
    plt.savefig(img_path)
    plt.close()
    return f"/images/{img_filename}"

def create_final_content(data, graph_url):
    print(f"🤖 콘텐츠 조립 중...")
    
    now = datetime.datetime.now()
    
    # 이미지 처리 (사용 안 함 설정 시 건너뜀)
    if USE_AI_IMAGE:
        prompts = data.get('image_prompts', ["city", "building"])
        encoded_cover = urllib.parse.quote(prompts[0])
        encoded_mid = urllib.parse.quote(prompts[1] if len(prompts)>1 else prompts[0])
        cover_image = f"https://image.pollinations.ai/prompt/{encoded_cover}?width=1600&height=900&nologo=true"
        mid_image = f"https://image.pollinations.ai/prompt/{encoded_mid}?width=800&height=500&nologo=true"
    else:
        cover_image = None
        mid_image = None
    
    body = data['blog_body_markdown']
    
    if USE_AI_IMAGE and mid_image:
        if "[[MID_IMAGE]]" in body:
            body = body.replace("[[MID_IMAGE]]", f"\n![분석 이미지]({mid_image})\n")
        else:
            paragraphs = body.split('\n\n')
            insert_idx = len(paragraphs) // 2
            paragraphs.insert(insert_idx, f"\n![분석 이미지]({mid_image})\n")
            body = "\n\n".join(paragraphs)
    else:
        # 이미지를 안 쓸 때는 표식([[MID_IMAGE]])만 조용히 제거
        body = body.replace("[[MID_IMAGE]]", "")

    keyword = data.get('search_keyword', '부동산')
    
    # 🔥 [수익화 Footer] - 링크 키워드를 구체적으로 적용
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

[👉 네이버 부동산에서 '{keyword}' 실시간 매물 보러가기](https://search.naver.com/search.naver?query={keyword})
"""

    front_matter = f"""---
title: "{data['viral_title']}"
date: {now.strftime("%Y-%m-%d")}
draft: false
categories: ["Investment Strategy"]
tags: ["Real Estate", "ROI", "Money"]
"""
    if cover_image:
        front_matter += f"""cover:
    image: "{cover_image}"
    alt: "{data['viral_title']}"
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
    print("🔥 PropTech 봇 (월 500 수익화 최종 완결판)")
    print("   * 가독성 UP: 블로그 말투 + 짧은 문단 + 이모지")
    print("   * 링크 정확도 UP: 추상적 키워드 제외, 구체적 지명 사용")
    print("   * 차단 방지: API 원샷 호출")
    print("="*50)
    
    topic = input("✍️  분석할 주제 입력: ")
    if topic:
        data = process_topic_one_shot(topic)
        if data:
            graph_url = generate_graph("chart", data['roi_data'])
            full_content = create_final_content(data, graph_url)
            link = deploy_to_github(data['viral_title'], full_content)
            save_tistory_file(data['viral_title'], data['tistory_teaser'], link)
            print("\n🎉 발행 완료! (월 500만원을 향해 달립시다)")
        else:
            print("❌ 생성 실패. 잠시 후 다시 시도하세요.")
    else:
        print("❌ 실행을 중단합니다.")