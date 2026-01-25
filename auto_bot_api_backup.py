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
# [설정 & 상수 관리 영역] - 사용자님의 원본을 한 줄도 삭제하지 않았습니다.
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

CALC_MENU_STR = "\n".join([f"- If discussing loans: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['dsr', 'interest']])
CALC_MENU_STR += "\n".join([f"- If discussing buying taxes: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['tax', 'fee']])
CALC_MENU_STR += "\n".join([f"- If discussing selling: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['transfer']])

# 🔥 [모델 설정]
MODEL_CANDIDATES = [
    'gemini-2.0-flash-exp',
    'gemini-flash-latest',
    'gemini-exp-1206',
    'gemini-2.0-flash-lite-preview-02-05',
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
    system_name = platform.system()
    if system_name == "Darwin":
        rc('font', family='AppleGothic')
        plt.rcParams['axes.unicode_minus'] = False 
    elif system_name == "Windows":
        rc('font', family='Malgun Gothic')
        plt.rcParams['axes.unicode_minus'] = False 
    else:
        try: rc('font', family='NanumGothic') 
        except: pass

def generate_one_shot(prompt):
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
            if text.strip().startswith("{") and not text.strip().endswith("}"):
                return json.loads(text.strip() + "}")
        except: pass
    return None

def process_topic_one_shot(topic):
    now = datetime.datetime.now()
    # 🕒 서버 시차 해결 (배포 즉시 반영을 위해 '어제' 날짜 사용)
    safety_date = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    current_date_str = now.strftime("%B %Y")
    current_year = now.year
    
    print(f"🚀 [Gemini API] '{topic}' 분석 시작 (V4.0 개조식 적용)...")
    
    # 🔥 [V4.0 지침 반영] 개조식 및 모바일 가독성 프롬프트 업데이트
    prompt = f"""
    Role: Senior Real Estate Investment Analyst.
    Task: Write a high-quality blog post about "{topic}".
    
    # 🛑 STRICT RULES (V4.0)
    1. BULLET POINTS ONLY: No long prose. Use bullet points (*) and short phrases.
    2. MOBILE READY: Max 2 lines per paragraph. Ensure empty lines between sections.
    3. SUMMARY TABLE: Include a Markdown Table comparing TOP 3 items at the start of Body.
    4. NO GREETINGS: Do NOT start with "Hello". Start directly with a Hook.
    5. DATA SAFETY: Use price ranges (e.g. "8억 중반 ~ 9억 초반") + "(Market Estimate)".

    Format: Output ONLY a single valid JSON object.
    JSON Keys:
    "viral_title", "category", "search_keyword", "roi_data", "calculator_type", "blog_body_markdown", "tistory_teaser"
    
    (Apply V4.0 개조식 스타일 to blog_body_markdown)
    Internal Links to include:
    {CALC_MENU_STR}
    """
    
    result = generate_one_shot(prompt)
    if not result: return None
    
    data = clean_json_response(result)
    return data, safety_date

def generate_graph(filename_base, data_dict):
    print(f"📊 [Matplotlib] 차트 생성 중...")
    set_smart_font()
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    if not os.path.exists(image_dir): os.makedirs(image_dir)
    img_filename = f"{filename_base}-{int(time.time())}.png"
    img_path = os.path.join(image_dir, img_filename)
    
    years = data_dict.get('years', [])
    values = data_dict.get('values', [])
    title = data_dict.get('title', 'Price Trend')
    
    plt.figure(figsize=(10, 6))
    plt.bar(years, values, color=COLOR_PRIMARY, width=0.6)
    plt.plot(years, values, color=COLOR_LINE, marker='o', linewidth=2)
    plt.title(title)
    plt.savefig(img_path)
    plt.close()
    return f"/images/{img_filename}"

def create_final_content(data, graph_url, post_date):
    print(f"✍️ [Editor] 포스팅 조립 중...")
    body = data.get('blog_body_markdown', '')
    keyword = data.get('search_keyword', '부동산')
    title = data.get('viral_title', '부동산 리포트')
    category = data.get('category', '부동산 분석')
    calc_type = data.get('calculator_type', 'none')
    
    encoded_keyword = urllib.parse.quote(keyword)
    naver_land_url = f"https://new.land.naver.com/search?sk={encoded_keyword}"

    calculator_btn = ""
    if calc_type in CALCULATOR_MAP and calc_type != 'none':
        info = CALCULATOR_MAP[calc_type]
        calculator_btn = f"""
<div style="margin-top: 30px; margin-bottom: 30px; text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef;">
    <p style="margin-bottom: 10px; font-weight: bold; color: #495057;">👇 이 매물, 내 조건으로 계산해보기</p>
    <a href="{MAIN_DOMAIN_URL}{info['url']}" target="_blank" style="display: inline-block; background-color: {COLOR_BTN_BG}; color: white; padding: 15px 30px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
        🧮 <strong>{info['text']} 돌려보기</strong>
    </a>
</div>"""

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
{calculator_btn}
<a href="{naver_land_url}" target="_blank">👉 <strong>네이버 부동산에서 '{keyword}' 시세 확인하기</strong></a>
<br><hr><small>📢 <strong>면책 조항</strong><br>본 포스팅은 정보 제공용이며, 투자의 책임은 투자자 본인에게 있습니다.</small>"""

    return f"{front_matter}\n\n![전망 차트]({graph_url})\n*▲ AI 분석 데이터 ({post_date} 기준)*\n\n{body}{footer}"

def deploy_to_github(title, content, category_kr, post_date):
    print(f"🚀 [Git] 배포 시작...") 
    folder = CATEGORY_FOLDER_MAP.get(category_kr, "tips")
    target_dir = os.path.join(BLOG_DIR, "content", "posts", folder)
    if not os.path.exists(target_dir): os.makedirs(target_dir)

    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    filename = f"{post_date}-{safe_title}_auto.md"
    filepath = os.path.join(target_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f: f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"Auto Post: {title}")
        repo.remote(name='origin').push()
        return f"{MAIN_DOMAIN_URL}/posts/{folder}/{filename.replace('.md', '')}"
    except Exception as e:
        print(f"❌ 배포 실패: {e}")
        return MAIN_DOMAIN_URL

def save_tistory_snippet(title, teaser, link):
    draft_dir = "tistory_drafts"
    if not os.path.exists(draft_dir): os.makedirs(draft_dir)
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    path = os.path.join(draft_dir, f"Tistory-{safe_title}_auto.txt")
    html = f"""<div style="font-size: 16px; line-height: 1.8;"><h2>{title}</h2><br>{teaser}<br><br>
    <div style="text-align: center;"><a href="{link}" target="_blank" style="display: inline-block; background-color: {COLOR_TISTORY}; color: white; padding: 15px 40px; text-decoration: none; font-weight: bold; border-radius: 8px;">👉 리포트 전문 보기</a></div></div>"""
    with open(path, "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    print("\n🔥 PropTech API Bot V18.0 (원본 로직 완벽 복구 및 V4.0 이식)")
    topic = input("\n✍️ 주제 입력: ")
    if topic:
        data, s_date = process_topic_one_shot(topic)
        if data:
            graph_url = generate_graph("chart", data.get('roi_data', {}))
            content = create_final_content(data, graph_url, s_date)
            link = deploy_to_github(data.get('viral_title'), content, data.get('category'), s_date)
            save_tistory_snippet(data.get('viral_title'), data.get('tistory_teaser'), link)
            print(f"🎉 발행 완료! ({s_date})")