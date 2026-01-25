import os
import time
import datetime
import random
import platform
import urllib.parse
import json
import warnings
import re

# 🔥 [설정] 경고 메시지 무시
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

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

# 💰 [수익화 링크] 나중에 애드픽 가입하면 여기를 바꾸세요.
KAKAO_OPEN_CHAT_URL = "https://open.kakao.com/o/YOUR_LINK_HERE" 

# ⚙️ [시스템 설정]
USE_AI_IMAGE = False 

# 🔥 [핵심] 사용자님 API 리스트에 있는 '확실한 모델'만 사용
MODEL_CANDIDATES = [
    'gemini-2.0-flash',       # 1순위: 정식 버전 (가장 안정적)
    'gemini-2.0-flash-lite',  # 2순위: 라이트 (속도 빠름, 쿼리 여유 많음)
    'gemini-2.5-flash'        # 3순위: 최신 버전
]

# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def generate_one_shot(prompt):
    """Gemini API 호출 (안정적인 모델 순서대로 시도)"""
    for model_name in MODEL_CANDIDATES:
        try:
            # print(f"   🤖 시도 중: {model_name}...") # 디버깅용 로그
            model = genai.GenerativeModel(model_name)
            
            # 2.0 모델은 temperature를 낮춰야 JSON 실수가 적음
            response = model.generate_content(
                prompt,
                generation_config={"temperature": 0.4}
            )
            return response.text
        except Exception as e:
            error_msg = str(e)
            
            # 과부하(429) 걸리면 잠시 쉬었다가 다음 모델로 (Lite로 넘어가면 해결됨)
            if "429" in error_msg or "Resource exhausted" in error_msg:
                print(f"   ⏳ [과부하] {model_name} 패스 -> 다음 모델로 전환합니다.")
                time.sleep(2) # 짧게 대기 후 바로 다음 모델 시도
                continue
            
            # 그 외 에러(404 등)는 즉시 다음 모델로
            continue
    return None

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def clean_json_response(text):
    """JSON 파싱 에러 방지 (강력한 복구 기능)"""
    try:
        # 1. 마크다운 제거
        clean_text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except json.JSONDecodeError:
        try:
            # 2. 정규식으로 { } 구간만 강제 추출 (앞뒤 잡다한 말 제거)
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if match:
                extracted = match.group(1)
                # 3. 2.0 모델이 자주 틀리는 "마지막 쉼표" 제거 수술
                extracted = re.sub(r',\s*}', '}', extracted)
                return json.loads(extracted)
        except: pass
    return None

def process_topic_one_shot(topic):
    print(f"🚀 [Gemini] '{topic}' 수익화 분석 시작...")
    
    # 🔥 [핵심 수정] 가독성(Readability) 극대화 지침 추가
    prompt = f"""
    Role: Real Estate Power Blogger.
    Task: Analyze "{topic}" and write a blog post.
    
    Format: Output ONLY a single valid JSON object. No intro text.

    JSON Keys required:
    1. "viral_title": Provocative Korean title with emojis.
    2. "search_keyword": Specific Korean location (e.g. "가락동 헬리오시티").
    3. "roi_data": {{ "years": [2024, 2025, 2026, 2027], "values": [100, 115, 130, 150], "title": "Price Trend" }}
    4. "blog_body_markdown": Korean blog post content (Markdown).
       [EXTREMELY IMPORTANT STYLE RULES]
       - **Short Paragraphs**: Max 2-3 lines per paragraph. NO WALL OF TEXT.
       - **Line Breaks**: Add empty lines between every paragraph.
       - **Bullet Points**: Use lists (`*`) frequently for easy reading.
       - **Bold**: Highlight key phrases like **"2026년 착공"**, **"2배 상승"**.
       - **Emojis**: Use emojis (💰, 🚀, ✅) at the start of sections.
       - Structure: Hook -> Money Flow -> [[MID_IMAGE]] -> Analysis -> Action Plan.
    5. "tistory_teaser": Short HTML summary.
    """
    
    result = generate_one_shot(prompt)
    if not result: return None
    
    # JSON 복구 시도
    data = clean_json_response(result)
    
    if not data:
        print("⚠️ 분석 실패 (AI가 올바른 데이터를 주지 않았습니다).")
        # 실패 시 봇 꺼짐 방지용 더미 데이터
        return {
            "viral_title": f"🚨 {topic} 긴급 분석 리포트",
            "search_keyword": topic,
            "roi_data": {"years": [2024,2025], "values": [100,100], "title":"준비중"},
            "blog_body_markdown": f"## {topic}\n\n죄송합니다. 현재 데이터를 분석할 수 없습니다.",
            "tistory_teaser": "<p>분석 실패</p>"
        }
    return data

def generate_graph(filename_base, data_dict):
    print(f"📊 [Matplotlib] 차트 생성 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    if not os.path.exists(image_dir): os.makedirs(image_dir)
        
    img_filename = f"{filename_base}-{int(time.time())}.png"
    img_path = os.path.join(image_dir, img_filename)

    years = data_dict.get('years', ['2024', '2025'])
    values = data_dict.get('values', [100, 110])
    title = data_dict.get('title', '시장 전망')

    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, values, color='#FF5252', width=0.6)
    plt.plot(years, values, color='#D32F2F', marker='o', linewidth=2)
    plt.title(title)
    plt.savefig(img_path)
    plt.close()
    return f"/images/{img_filename}"

def create_final_content(data, graph_url):
    print(f"✍️ [Editor] 포스팅 조립 중...")
    now = datetime.datetime.now()
    
    body = data.get('blog_body_markdown', '')
    keyword = data.get('search_keyword', '부동산')
    title = data.get('viral_title', '부동산 리포트')
    
    if not USE_AI_IMAGE:
        body = body.replace("[[MID_IMAGE]]", "")

    # 네이버 부동산 지도 링크
    encoded_keyword = urllib.parse.quote(keyword)
    naver_land_url = f"https://new.land.naver.com/search?sk={encoded_keyword}"

    # 수익화 Footer
    footer = f"""
\n
---
### 🛑 {keyword} 투자, 아직도 고민만 하시나요?

부동산은 **타이밍**이 생명입니다.
내 자금으로 가능한 **최고의 매물**이 무엇인지 지금 바로 확인하세요.

📉 **신용점수 영향 없는** 안심 한도 조회
👉 **[💰 나의 대출 한도 1분 조회하기]({KAKAO_OPEN_CHAT_URL})**

🚀 **실시간 매물 호가 확인**
[👉 **네이버 부동산에서 '{keyword}' 보기**]({naver_land_url})
"""

    front_matter = f"""---
title: "{title}"
date: {now.strftime("%Y-%m-%d")}
draft: false
categories: ["Investment Strategy"]
tags: ["{keyword}", "부동산투자", "재테크"]
image: "{graph_url}"
---
"""
    
    # 🔥 [수정됨] 제목 중복 제거 완료 (본문에서 '# Title' 제거)
    return f"{front_matter}\n\n![전망 차트]({graph_url})\n*▲ AI 분석 데이터 ({now.year}년 기준)*\n\n{body}\n{footer}"

def deploy_to_github(title, content):
    print(f"🚀 [Git] 깃허브 배포 시작...") 
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    safe_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    filepath = os.path.join(BLOG_DIR, "content", "posts", safe_filename)
    
    with open(filepath, 'w', encoding='utf-8') as f: 
        f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"New Post: {title}")
        origin = repo.remote(name='origin')
        origin.push()
        
        post_url = f"{MAIN_DOMAIN_URL}/posts/{safe_filename.replace('.md', '')}"
        print(f"✅ [Success] 배포 완료! \n🔗 링크: {post_url}")
        return post_url
    except Exception as e:
        print(f"❌ [Error] 깃허브 배포 실패: {e}")
        return MAIN_DOMAIN_URL

def save_tistory_snippet(title, teaser, link):
    draft_dir = "tistory_drafts"
    if not os.path.exists(draft_dir): os.makedirs(draft_dir)
    
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    filename = f"Tistory-{safe_title}.txt"
    path = os.path.join(draft_dir, filename)
    
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"<h2>{title}</h2>\n{teaser}\n<a href='{link}'>전문 보기</a>")
    print(f"📂 [Tistory] 초안 저장 완료")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔥 PropTech 수익화 봇 V2.7 (제목 중복 수정 완료)")
    print("   ✅ 블로그 제목이 두 번 나오는 현상 수정")
    print("   ✅ 사용자 API 최적화 모델 유지")
    print("="*60)
    
    topic = input("\n✍️  분석할 부동산 주제/지역을 입력하세요: ")
    
    if topic:
        data = process_topic_one_shot(topic)
        if data:
            roi_data = data.get('roi_data', {})
            graph_url = generate_graph("chart", roi_data)
            full_content = create_final_content(data, graph_url)
            link = deploy_to_github(data.get('viral_title'), full_content)
            save_tistory_snippet(data.get('viral_title'), data.get('tistory_teaser'), link)
            print(f"\n🎉 성공! 글이 아주 깔끔하게 올라갈 겁니다.")
        else:
            print("❌ 실패. (모든 모델이 응답하지 않습니다)")
    else:
        print("❌ 주제 입력 안됨.")