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
KAKAO_OPEN_CHAT_URL = "https://open.kakao.com/o/YOUR_LINK_HERE" 
USE_AI_IMAGE = False 

# 🔥 [계산기 매핑 정보]
# AI가 'type'을 선택하면, 그에 맞는 URL과 버튼 멘트를 매칭합니다.
CALCULATOR_MAP = {
    "dsr": {"url": "/calculators/calc_dsr/", "text": "📉 내 연봉으로 이 집 대출 나올까? (DSR 계산기)"},
    "interest": {"url": "/calculators/calc_interest/", "text": "💰 매달 갚아야 할 원리금은 얼마? (이자 계산기)"},
    "fee": {"url": "/calculators/calc_fee/", "text": "🤝 중개수수료(복비) 호구 안 당하는 법 (복비 계산기)"},
    "tax": {"url": "/calculators/calc_tax/", "text": "🏠 집 살 때 취득세, 얼마나 준비해야 할까? (취득세 계산기)"},
    "transfer": {"url": "/calculators/calc_transfer/", "text": "💸 집 팔면 남는 게 있을까? (양도세 계산기)"},
    "hold": {"url": "/calculators/calc_hold/", "text": "🏠 가만히 있어도 나가는 세금 확인 (보유세 계산기)"},
    "sub": {"url": "/calculators/calc_subscription/", "text": "🏆 내 점수로 청약 당첨 가능할까? (가점 계산기)"},
    "rent": {"url": "/calculators/calc_rent/", "text": "🔄 전세↔월세, 적정 금액은 얼마? (전환율 계산기)"},
    "salary": {"url": "/calculators/calc_salary/", "text": "💵 세금 떼고 실제 통장에 꽂히는 돈은? (실수령액 계산기)"},
    "none": {"url": "", "text": ""}
}

MODEL_CANDIDATES = [
    'gemini-2.0-flash',       
    'gemini-2.0-flash-lite',  
    'gemini-2.5-flash'        
]

genai.configure(api_key=GEMINI_API_KEY)

# ... (generate_one_shot, set_korean_font, clean_json_response 함수는 기존과 동일) ...
def generate_one_shot(prompt):
    """Gemini API 호출"""
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
    """차트 폰트 설정"""
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def clean_json_response(text):
    """JSON 파싱 및 복구"""
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
    print(f"🚀 [Gemini] '{topic}' 수익화 분석 시작...")
    
    # 🔥 [V4.5 프롬프트] 구체적인 계산기 타입(type) 선택 요청
    prompt = f"""
    Role: Real Estate Power Blogger.
    Task: Analyze "{topic}" and write a blog post.
    
    Format: Output ONLY a single valid JSON object.

    JSON Keys required:
    1. "viral_title": Provocative Korean title with emojis.
    
    2. "category": Choose ONE from ["부동산 분석", "청약 정보", "투자 꿀팁", "시장 전망", "세금/정책"].
    
    3. "search_keyword": Specific Location + Property Type. NO abstract words like "투자/전망".
    
    4. "roi_data": {{ "years": [2024, 2025, 2026, 2027], "values": [100, 115, 130, 150], "title": "Price Trend" }}
    
    5. "calculator_type": Choose ONE best match from:
       ['dsr', 'interest', 'fee', 'tax', 'transfer', 'hold', 'sub', 'rent', 'salary', 'none'].
       - Example: Buying a house -> 'tax' or 'dsr'. Selling -> 'transfer'. Renting -> 'rent'. Subscription -> 'sub'.
    
    6. "blog_body_markdown": Korean Markdown content.
       - **Hypothetical Simulation**: MUST include a Markdown Table.
       - **Style**: Short paragraphs (2-3 lines), bold keywords, bullet points.
       - Structure: Hook -> Money Flow -> **Simulation Table** -> Analysis -> Action Plan.
       
    7. "tistory_teaser": HTML format text (10-15 lines).
       - **Hook**: Mention the calculator. Ex: "Calculate your exact taxes/limit inside the blog!"
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

    # 🔥 [V4.5] 맞춤형 계산기 버튼 생성
    calculator_btn = ""
    if calc_type in CALCULATOR_MAP and calc_type != 'none':
        info = CALCULATOR_MAP[calc_type]
        calculator_btn = f"""
<div style="margin-top: 30px; margin-bottom: 30px; text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef;">
    <p style="margin-bottom: 10px; font-weight: bold; color: #495057;">👇 내 조건으로 정확하게 계산해보고 싶다면?</p>
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
        🧮 <strong>{info['text']}</strong>
    </a>
    <p style="margin-top: 10px; font-size: 12px; color: #868e96;">(2026년 최신 기준 / 사용자 입력 가능)</p>
</div>
"""

    footer = f"""
\n
---
### 🛑 {keyword} 투자, 아직도 고민만 하시나요?

부동산은 **타이밍**이 생명입니다.
내 자금으로 가능한 **최고의 매물**이 무엇인지 지금 바로 확인하세요.

{calculator_btn}

📉 **신용점수 영향 없는** 안심 한도 조회
👉 <a href="{KAKAO_OPEN_CHAT_URL}" target="_blank" rel="noopener noreferrer"><strong>💰 나의 대출 한도 1분 조회하기 (클릭)</strong></a>

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

def deploy_to_github(title, content):
    print(f"🚀 [Git] 깃허브 배포 시작...") 
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    safe_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    # 🔥 [수정] 포스팅 저장 위치 확인 (calculators 폴더와 섞이지 않게)
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
    print("🔥 PropTech 수익화 봇 V4.5 (계산기 자동 매칭)")
    print("   ✅ 주제에 딱 맞는 계산기(9종 중 택1)를 골라 추천합니다.")
    print("   ✅ 계산기 URL 경로 수정 완료 (/calculators/...)")
    print("   ✅ 기준일 업데이트 안내 문구 추가")
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
            print(f"\n🎉 발행 완료!")
        else:
            print("❌ 실패.")
    else:
        print("❌ 주제 입력 안됨.")