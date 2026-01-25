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
USE_AI_IMAGE = False 

# 🔥 [폴더 매핑]
CATEGORY_FOLDER_MAP = {
    "부동산 분석": "analysis",
    "청약 정보": "subscription",
    "투자 꿀팁": "tips",
    "시장 전망": "outlook",
    "세금/정책": "policy"
}

# 🔥 [계산기 매핑] - AI가 본문에 심을 수 있게 마크다운 리스트로 준비
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

# 프롬프트에 주입할 "계산기 메뉴판" 생성
CALC_MENU_STR = "\n".join([f"- If discussing loans: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['dsr', 'interest']])
CALC_MENU_STR += "\n".join([f"- If discussing buying taxes: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['tax', 'fee']])
CALC_MENU_STR += "\n".join([f"- If discussing selling: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['transfer']])

MODEL_CANDIDATES = [
    'gemini-2.0-flash',       
    'gemini-2.0-flash-lite',  
    'gemini-2.5-flash'        
]

genai.configure(api_key=GEMINI_API_KEY)

def generate_one_shot(prompt):
    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(
                prompt,
                generation_config={"temperature": 0.4}
            )
            return response.text
        except Exception as e:
            time.sleep(2)
            continue
    return None

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

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
        except: pass
    return None

def process_topic_one_shot(topic):
    print(f"🚀 [Gemini] '{topic}' 자동화 분석 시작 (TOP3 & 내부링크)...")
    
    # 🔥 [V6.0 핵심 프롬프트] TOP 3 강제 + 내부 링크 삽입 명령
    prompt = f"""
    Role: Real Estate Power Blogger.
    Task: Analyze "{topic}" and write a highly engaging blog post.
    
    Format: Output ONLY a single valid JSON object.

    JSON Keys required:
    1. "viral_title": Provocative Korean title with emojis.
    2. "category": Choose ONE from ["부동산 분석", "청약 정보", "투자 꿀팁", "시장 전망", "세금/정책"].
    3. "search_keyword": Specific Location + Property Type.
    4. "roi_data": {{ "years": [2024, 2025, 2026, 2027], "values": [100, 115, 130, 150], "title": "Price Trend" }}
    5. "calculator_type": Choose ONE best match from ['dsr', 'interest', 'fee', 'tax', 'transfer', 'hold', 'sub', 'rent', 'salary', 'none'].
    
    6. "blog_body_markdown": Korean Markdown content.
       - **CRITICAL RULE 1 (TOP 3 Strategy)**: You MUST organize the analysis into a "TOP 3 Recommendation" structure.
         - Do NOT use generic names like "Apartment A".
         - Use specific personas: e.g., "🥇 TOP 1: The Safe Leader (대장주)", "🥈 TOP 2: The New Build (신축)", "🥉 TOP 3: High ROI (재개발/저평가)".
         - Create a Markdown Table summarizing these 3 options (Price, Pros, Cons, Exp. Return).
       
       - **CRITICAL RULE 2 (Internal Linking)**: You MUST insert a Markdown link to a relevant calculator naturally within the text.
         - Use these exact links (Select 1-2 relevant ones):
           {CALC_MENU_STR}
         - Example: "Before buying, check your taxes with the [🏠 취득세 계산기](/calculators/calc_tax/)."
         - Do NOT invent fake links. Use only the provided paths.

       - **Style**: Short paragraphs, bold keywords, engaging tone.
       
    7. "tistory_teaser": HTML format text (10-15 lines).
       - Hook: "Check the TOP 3 list inside!"
    """
    
    result = generate_one_shot(prompt)
    if not result: return None
    
    data = clean_json_response(result)
    
    if not data:
        print("⚠️ 분석 실패.")
        return None
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
    category = data.get('category', '부동산 분석')
    calc_type = data.get('calculator_type', 'none')
    
    if not USE_AI_IMAGE:
        body = body.replace("[[MID_IMAGE]]", "")

    encoded_keyword = urllib.parse.quote(keyword)
    naver_land_url = f"https://new.land.naver.com/search?sk={encoded_keyword}"

    # 1. 맞춤형 계산기 버튼 (하단용)
    calculator_btn = ""
    if calc_type in CALCULATOR_MAP and calc_type != 'none':
        info = CALCULATOR_MAP[calc_type]
        calculator_btn = f"""
<div style="margin-top: 30px; margin-bottom: 30px; text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef;">
    <p style="margin-bottom: 10px; font-weight: bold; color: #495057;">👇 이 매물, 내 조건으로 계산해보기</p>
    <a href="{MAIN_DOMAIN_URL}{info['url']}" target="_blank" style="
        display: inline-block; 
        background-color: #00C853; 
        color: white; 
        padding: 15px 30px; 
        border-radius: 50px; 
        font-weight: bold; 
        text-decoration: none; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        transition: 0.3s;">
        🧮 <strong>{info['text']} 돌려보기</strong>
    </a>
</div>
"""

    footer_calc_link = f"{MAIN_DOMAIN_URL}/calculators/calc_dsr/"

    footer = f"""
\n
---
### 🛑 {keyword} 투자, 아직도 고민만 하시나요?

부동산은 **타이밍**이 생명입니다.
내 자금으로 가능한 **최고의 매물**이 무엇인지 지금 바로 확인하세요.

{calculator_btn}

📉 **대출 나오는지 걱정되시나요?**
👉 <a href="{footer_calc_link}" target="_blank" rel="noopener noreferrer"><strong>💰 내 연봉으로 대출 한도 셀프 계산하기 (DSR 계산기)</strong></a>

🚀 **실시간 매물 호가 확인**
<a href="{naver_land_url}" target="_blank" rel="noopener noreferrer">👉 <strong>네이버 부동산에서 '{keyword}' 시세/실거래가 확인하기 (클릭)</strong></a>

<br>
<hr>
<small>📢 <strong>면책 조항 (Disclaimer)</strong><br>
본 포스팅은 부동산 데이터 분석에 기초한 정보 제공을 목적으로 하며, 투자의 법적 책임은 투자자 본인에게 있습니다. 투자는 개인의 재정 상황을 고려하여 신중하게 결정하시기 바랍니다.</small>
"""

    front_matter = f"""---
title: "{title}"
date: {now.strftime("%Y-%m-%d")}
draft: false
categories: ["{category}"]
tags: ["{keyword}", "부동산투자", "재테크"]
description: "{title}"
image: "{graph_url}"
---
"""
    return f"{front_matter}\n\n![전망 차트]({graph_url})\n*▲ AI 분석 데이터 ({now.year}년 기준)*\n\n{body}\n{footer}"

def deploy_to_github(title, content, category_kr):
    print(f"🚀 [Git] 깃허브 배포 시작...") 
    folder_name = CATEGORY_FOLDER_MAP.get(category_kr, "tips")
    target_dir = os.path.join(BLOG_DIR, "content", "posts", folder_name)
    if not os.path.exists(target_dir): os.makedirs(target_dir)

    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    safe_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    filepath = os.path.join(target_dir, safe_filename)
    
    with open(filepath, 'w', encoding='utf-8') as f: 
        f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"New Post: {title}")
        origin = repo.remote(name='origin')
        origin.push()
        post_url = f"{MAIN_DOMAIN_URL}/posts/{folder_name}/{safe_filename.replace('.md', '')}"
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
    html = f"""
    <div style="font-size: 16px; line-height: 1.8;">
        <h2>{title}</h2>
        <br>
        {teaser}
        <br><br>
        <div style="text-align: center; margin-top: 20px;">
            <a href="{link}" target="_blank" style="
                display: inline-block;
                background-color: #D32F2F; 
                color: white; 
                padding: 15px 40px; 
                text-decoration: none; 
                font-weight: bold; 
                border-radius: 8px; 
                font-size: 18px;
                box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                👉 리포트 전문(Full) 무료로 보기 & 계산기 사용하기
            </a>
            <p style="color: #666; font-size: 14px; margin-top: 10px;">
                (클릭 시 광고 없이 원본 사이트로 이동합니다)
            </p>
        </div>
    </div>
    """
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"📂 [Tistory] 티저 저장 완료")

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🔥 PropTech 수익화 봇 V6.0 (자동화의 끝판왕)")
    print("   ✅ 본문 구조 강제: 무조건 'TOP 3' 형식으로 작성")
    print("   ✅ 문맥 인식 링크: 세금 얘기엔 세금계산기, 대출 얘기엔 DSR계산기 자동 삽입")
    print("   ✅ 수정할 필요 없는 완벽한 초안 생성")
    print("="*60)
    
    topic = input("\n✍️  분석할 부동산 주제/지역을 입력하세요: ")
    if topic:
        data = process_topic_one_shot(topic)
        if data:
            roi_data = data.get('roi_data', {})
            graph_url = generate_graph("chart", roi_data)
            full_content = create_final_content(data, graph_url)
            link = deploy_to_github(data.get('viral_title'), full_content, data.get('category'))
            save_tistory_snippet(data.get('viral_title'), data.get('tistory_teaser'), link)
            print(f"\n🎉 발행 완료!")
        else:
            print("❌ 실패.")
    else:
        print("❌ 주제 입력 안됨.")