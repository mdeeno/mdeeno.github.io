import os
import time
import datetime
import random
import platform
import urllib.parse
import json
import warnings
import re
import matplotlib.font_manager as fm

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
# [설정 & 상수 관리 영역] - 360줄 원본 로직 100% 보존
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_DIR = os.getenv("BLOG_DIR")
MAIN_DOMAIN_URL = "https://tech.mdeeno.com"
USE_AI_IMAGE = False 

# 🎨 디자인 설정
COLOR_PRIMARY = "#FF5252"
COLOR_LINE = "#D32F2F"       
COLOR_BTN_BG = "#00C853"
COLOR_TISTORY = "#D32F2F"    

# 📂 카테고리 매핑
CATEGORY_FOLDER_MAP = {
    "부동산 분석": "analysis",
    "청약 정보": "subscription",
    "투자 꿀팁": "tips",
    "시장 전망": "outlook",
    "세금/정책": "policy"
}

# 🧮 계산기 매핑 (9종 전체 보존)
CALCULATOR_MAP = {
    "dsr": {"url": "/calculators/calc_dsr/", "text": "📉 DSR & 대출 한도 계산기"},
    "interest": {"url": "/calculators/calc_interest/", "text": "💰 대출 이자 계산기"},
    "fee": {"url": "/calculators/calc_fee/", "text": "🤝 중개보수(복비) 계산기"},
    "tax": {"url": "/calculators/calc_tax/", "text": "🏠 취득세 계산기"},
    "transfer": {"url": "/calculators/calc_transfer/", "text": "💸 양도소득세 계산기"},
    "hold": {"url": "/calculators/calc_hold/", "text": "🏠 보유세(재산세+종부세) 계산기"},
    "sub": {"url": "/calculators/calc_subscription/", "text": "🏆 청약 가점 계산기"},
    "rent": {"url": "/calculators/calc_rent/", "text": "🔄 전월세 전환율 계산기"},
    "salary": {"url": "/calculators/calc_salary/", "text": "💵 연봉 실수령액 계산기"}
}

# 🔗 프롬프트 주입용 링크 메뉴 (자동 생성)
CALC_MENU_STR = "\n".join([f"- [{v['text']}]({MAIN_DOMAIN_URL}{v['url']})" for k, v in CALCULATOR_MAP.items()])

# 🔥 [모델 설정] - 1.5 버전 삭제 및 고성능 모델 원복
MODEL_CANDIDATES = [
    'gemini-2.0-flash-exp',       # 1순위: 성능 최우선
    'gemini-flash-latest',        # 2순위: 2.0 쿼터 초과 시 대타
    'gemini-exp-1206',            
    'gemini-pro-latest'
]

genai.configure(api_key=GEMINI_API_KEY)

# 안전 설정 해제
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

def set_smart_font():
    """운영체제에 맞는 한글 폰트를 자동으로 설정합니다."""
    system_name = platform.system()
    if system_name == "Darwin":
        rc('font', family='AppleGothic')
    elif system_name == "Windows":
        rc('font', family='Malgun Gothic')
    else:
        try: rc('font', family='NanumGothic') 
        except: pass
    plt.rcParams['axes.unicode_minus'] = False 

def generate_one_shot(prompt):
    """Gemini API를 호출하여 텍스트를 생성합니다."""
    for model_name in MODEL_CANDIDATES:
        try:
            print(f"   ... 🧠 모델 가동 중: {model_name}")
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={"temperature": 0.3},
                safety_settings=SAFETY_SETTINGS
            )
            return response.text
        except Exception as e:
            print(f"   ⚠️ {model_name} 실패: {e}")
            time.sleep(1)
            continue
    return None

def clean_json_response(text):
    """API 응답에서 JSON 데이터만 추출하여 파싱합니다."""
    try:
        clean_text = text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_text)
    except json.JSONDecodeError:
        try:
            match = re.search(r'(\{.*\})', text, re.DOTALL)
            if match:
                extracted = match.group(1)
                extracted = re.sub(r',\s*}', '}', extracted)
                return json.loads(extracted)
        except: pass
    return None

def process_topic_one_shot(topic):
    """주제를 받아 전체 분석 프로세스를 실행하고 데이터를 반환합니다."""
    now = datetime.datetime.now()
    
    # 🕒 [핵심 수정] 시:분:초(%H:%M:%S)까지 포함하여 정렬 순서 강제 고정
    # 어제 날짜로 하되, 현재 시간을 붙여서 겹치지 않게 함
    yesterday = now - datetime.timedelta(days=1)
    safety_date = yesterday.strftime("%Y-%m-%d %H:%M:%S")
    current_year = now.year
    
    print(f"🚀 [Gemini API] '{topic}' 분석 시작 (V28.0 초단위 정렬 패치)...")
    
    # 🔥 [V28.0 프롬프트] 
    prompt = f"""
    Role: Senior Real Estate Investment Analyst (Top-tier Expert).
    Task: Write a high-quality, professional blog post about "{topic}".
    
    # 🛑 CRITICAL RULES
    1. CLICKABLE LINKS: You MUST use Markdown link format `[Text](URL)` for all internal calculators.
    2. BULLET POINTS ONLY: No long prose. Use (*) for all analysis sections.
    3. SUMMARY TABLE: Mandatory Markdown Table at the start of Body.
    4. NO GREETINGS: Start directly with a Hook.
    5. DATA SAFETY: Use realistic price ranges.
    
    Format: Output ONLY a single valid JSON object.
    JSON Keys:
    - "viral_title": Provocative Korean title.
    - "category": Choose ONE from ["부동산 분석", "청약 정보", "투자 꿀팁", "시장 전망", "세금/정책"].
    - "search_keyword": Topic-related keyword.
    - "roi_data": {{"years": [{current_year-2}, {current_year-1}, {current_year}, {current_year+1}], "values": [4 realistic index numbers], "title": "Price Trend Forecast"}}
    - "calculator_type": Choose ONE best match from ['dsr', 'interest', 'fee', 'tax', 'transfer', 'hold', 'sub', 'rent', 'salary'].
    - "blog_body_markdown": Korean Markdown content (Insert CLICKABLE links from the menu below).
    - "tistory_teaser": HTML Teaser content.
    
    # 🧮 CALCULATOR MENU (USE THESE LINKS EXACTLY):
    {CALC_MENU_STR}
    """
    
    result = generate_one_shot(prompt)
    if not result: return None
    
    data = clean_json_response(result)
    return data, safety_date

def generate_graph(filename_base, data_dict):
    """Matplotlib을 사용하여 차트를 생성합니다."""
    print(f"📊 [Matplotlib] 차트 생성 중...")
    set_smart_font()
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    if not os.path.exists(image_dir): os.makedirs(image_dir)
    
    img_filename = f"{filename_base}-{int(time.time())}.png"
    img_path = os.path.join(image_dir, img_filename)
    
    years = data_dict.get('years', [])
    values = data_dict.get('values', [])
    title = data_dict.get('title', 'Price Trend')
    
    # 🛑 차트 데이터 누락 방지
    if not years or len(values) < 2:
        print("   ⚠️ 차트 데이터 누락 감지 -> 기본 데이터로 보정합니다.")
        years = [2024, 2025, 2026, 2027]
        values = [100, 105, 110, 115]
    
    plt.figure(figsize=(10, 6))
    plt.bar(years, values, color=COLOR_PRIMARY, width=0.6, alpha=0.7)
    plt.plot(years, values, color=COLOR_LINE, marker='o', linewidth=2)
    plt.title(title)
    plt.savefig(img_path)
    plt.close()
    return f"/images/{img_filename}"

def create_final_content(data, graph_url, post_date):
    """Markdown 본문 조립 (시간 포함 날짜 적용)"""
    print(f"✍️ [Editor] 포스팅 조립 중...")
    body = data.get('blog_body_markdown', '')
    keyword = data.get('search_keyword', '부동산')
    title = data.get('viral_title', '부동산 리포트')
    category = data.get('category', '부동산 분석')
    calc_type = data.get('calculator_type', 'none')
    
    if not USE_AI_IMAGE:
        body = body.replace("[[MID_IMAGE]]", "")

    encoded_keyword = urllib.parse.quote(keyword)
    naver_land_url = f"https://new.land.naver.com/search?sk={encoded_keyword}"

    calculator_btn = ""
    if calc_type in CALCULATOR_MAP:
        info = CALCULATOR_MAP[calc_type]
        calculator_btn = f"""
<div style="margin: 30px 0; text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef;">
    <p style="margin-bottom: 10px; font-weight: bold; color: #495057;">👇 이 매물, 내 조건으로 계산해보기</p>
    <a href="{MAIN_DOMAIN_URL}{info['url']}" target="_blank" style="display: inline-block; background-color: {COLOR_BTN_BG}; color: white; padding: 15px 30px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        🧮 <strong>{info['text']} 돌려보기</strong>
    </a>
</div>"""

    # 🔥 [중요] Front Matter의 date 필드에 '시:분:초'가 포함됩니다.
    front_matter = f"""---
title: "{title}"
date: {post_date}
draft: false
categories: ["{category}"]
tags: ["{keyword}", "부동산투자", "재테크"]
description: "{title}"
image: "{graph_url}"
---
"""
    footer = f"""\n
---
### 🛑 {keyword} 투자, 아직도 고민만 하시나요?

부동산은 **타이밍**이 생명입니다.
내 자금으로 가능한 **최고의 매물**이 무엇인지 지금 바로 확인하세요.

{calculator_btn}

📉 **대출 가능 여부 확인**
👉 <a href="{MAIN_DOMAIN_URL}/calculators/calc_dsr/" target="_blank"><strong>💰 내 연봉으로 대출 한도 셀프 계산하기 (DSR 계산기)</strong></a>

🚀 **실시간 매물 호가 확인**
<a href="{naver_land_url}" target="_blank">👉 <strong>네이버 부동산에서 '{keyword}' 시세/실거래가 확인하기 (클릭)</strong></a>

<br><hr><small>📢 **면책 조항 (Disclaimer)**<br>
본 포스팅은 부동산 데이터 분석에 기초한 정보 제공을 목적으로 하며, 투자의 법적 책임은 투자자 본인에게 있습니다.</small>"""

    return f"{front_matter}\n\n![전망 차트]({graph_url})\n*▲ AI 분석 데이터 ({post_date} 기준)*\n\n{body}{footer}"

def deploy_to_github(title, content, category_kr, post_date):
    """Git 배포"""
    print(f"🚀 [Git] 배포 시작...") 
    folder = CATEGORY_FOLDER_MAP.get(category_kr, "tips")
    target_dir = os.path.join(BLOG_DIR, "content", "posts", folder)
    if not os.path.exists(target_dir): os.makedirs(target_dir)

    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    # 파일명은 깔끔하게 날짜만 (YYYY-MM-DD)
    filename_date = post_date.split(' ')[0]
    filename = f"{filename_date}-{safe_title}_auto.md"
    filepath = os.path.join(target_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"Auto Post: {title}")
        repo.remote(name='origin').push()
        post_url = f"{MAIN_DOMAIN_URL}/posts/{folder}/{filename.replace('.md', '')}"
        print(f"✅ 배포 성공! URL: {post_url}")
        return post_url
    except Exception as e:
        print(f"❌ 배포 실패: {e}")
        return MAIN_DOMAIN_URL

def save_tistory_snippet(title, teaser, link):
    """티스토리 요약본 저장"""
    draft_dir = "tistory_drafts"
    if not os.path.exists(draft_dir): os.makedirs(draft_dir)
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    path = os.path.join(draft_dir, f"Tistory-{safe_title}_auto.txt")
    
    html = f"""
    <div style="font-size: 16px; line-height: 1.8;">
        <h2>{title}</h2><br>
        {teaser}
        <br><br>
        <div style="text-align: center; margin-top: 20px;">
            <a href="{link}" target="_blank" style="display: inline-block; background-color: {COLOR_TISTORY}; color: white; padding: 15px 40px; text-decoration: none; font-weight: bold; border-radius: 8px; font-size: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                👉 리포트 전문(Full) 무료로 보기
            </a>
        </div>
    </div>"""
    with open(path, "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔥 PropTech API Bot V28.0 (1.5 삭제 & 초단위 정렬 패치)")
    print("   ✅ UI 뒤죽박죽 해결: 날짜에 시:분:초 포함")
    print("   ✅ 1.5 모델 삭제: 사용자 요청 반영 완료")
    print("="*60)
    
    topic = input("\n✍️ 분석 주제 입력: ")
    if topic:
        data, s_date = process_topic_one_shot(topic)
        if data:
            graph_url = generate_graph("chart", data.get('roi_data', {}))
            full_content = create_final_content(data, graph_url, s_date)
            link = deploy_to_github(data.get('viral_title'), full_content, data.get('category'), s_date)
            save_tistory_snippet(data.get('viral_title'), data.get('tistory_teaser'), link)
            print(f"🎉 모든 작업 완료! (날짜: {s_date})")