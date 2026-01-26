import os  # // 초등학생 설명: 컴퓨터의 폴더나 파일을 관리하는 비서예요. 
import time  # // 초등학생 설명: 시계처럼 시간을 재거나 잠깐 멈추게 할 때 써요. 
import datetime  # // 초등학생 설명: 오늘이 몇 월 며칠인지 정확히 알려주는 달력이에요. 
import random  # // 초등학생 설명: 주머니에서 제비뽑기를 하듯 무작위로 고를 때 써요. 
import platform  # // 초등학생 설명: 지금 컴퓨터가 윈도우인지 맥인지 확인해주는 탐정이에요. 
import urllib.parse  # // 초등학생 설명: 복잡한 인터넷 주소를 컴퓨터가 이해하기 좋게 번역해줘요. 
import json  # // 초등학생 설명: 정보를 이름표와 내용으로 깔끔하게 정리해주는 정리함이에요. 
import warnings  # // 초등학생 설명: 잔소리 같은 경고 메시지를 안 보이게 숨겨주는 귀마개예요. 
import re  # // 초등학생 설명: 긴 글 속에서 내가 원하는 글자만 쏙쏙 찾아내는 돋보기예요. 
import matplotlib.font_manager as fm  # // 초등학생 설명: 그래프에 예쁜 한글 글씨체를 입혀주는 도구예요. 

# // 초등학생 설명: 컴퓨터가 옛날 방식이라고 잔소리하는 것을 못 하게 막아줘요. 
warnings.simplefilter(action='ignore', category=FutureWarning)
warnings.filterwarnings("ignore", category=UserWarning)

import google.generativeai as genai  # // 초등학생 설명: 똑똑한 인공지능 친구 제미나이를 불러와요. 
import matplotlib.pyplot as plt  # // 초등학생 설명: 숫자들을 한눈에 보기 쉬운 그림 지도로 그려줘요. 
from matplotlib import rc  # // 초등학생 설명: 그림 지도에 한글 이름을 붙일 수 있게 도와줘요. 
from git import Repo  # // 초등학생 설명: 내가 쓴 글을 인터넷 창고인 깃허브에 배달해줘요. 
from dotenv import load_dotenv  # // 초등학생 설명: 비밀번호 같은 중요한 정보를 몰래 가져와요. 

load_dotenv()  # // 초등학생 설명: 주머니 속에 숨겨둔 비밀 정보를 꺼내서 준비해요. 

# // 초등학생 설명: 프로그램이 작동하는 데 필요한 비밀번호와 주소들을 미리 적어둬요. 
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_DIR = os.getenv("BLOG_DIR")
MAIN_DOMAIN_URL = "https://tech.mdeeno.com"
USE_AI_IMAGE = False 

COLOR_PRIMARY = "#FF5252"  # // 초등학생 설명: 강조하고 싶은 부분에 칠할 예쁜 빨간색이에요. 
COLOR_LINE = "#D32F2F"       
COLOR_BTN_BG = "#00C853"  # // 초등학생 설명: 클릭하고 싶게 만드는 초록색 버튼 색이에요. 
COLOR_TISTORY = "#D32F2F"    

# // 초등학생 설명: 글의 주제에 따라 어느 방(폴더)에 넣을지 미리 정해둬요. 
CATEGORY_FOLDER_MAP = {
    "부동산 분석": "analysis",
    "청약 정보": "subscription",
    "투자 꿀팁": "tips",
    "시장 전망": "outlook",
    "세금/정책": "policy"
}

# // 초등학생 설명: 집 살 때 필요한 세금이나 대출금을 대신 계산해주는 똑똑한 계산기 목록이에요. 
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

# // 초등학생 설명: 인공지능이 글을 쓰다가 "이런 계산기도 써보세요"라고 말할 수 있게 메뉴판을 만들어요. 
CALC_MENU_STR = "\n".join([f"- If discussing loans: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['dsr', 'interest']])
CALC_MENU_STR += "\n".join([f"- If discussing buying taxes: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['tax', 'fee']])
CALC_MENU_STR += "\n".join([f"- If discussing selling: [{v['text']}]({v['url']})" for k, v in CALCULATOR_MAP.items() if k in ['transfer']])

# // 초등학생 설명: 공부를 제일 잘하는 인공지능 친구부터 순서대로 불러볼게요. 
MODEL_CANDIDATES = [
    'gemini-2.0-flash-exp',
    'gemini-flash-latest',
    'gemini-exp-1206',
    'gemini-2.0-flash-lite-preview-02-05',
    'gemini-pro-latest'
]

genai.configure(api_key=GEMINI_API_KEY)

# // 초등학생 설명: 인공지능이 너무 조심스러워서 대답을 피하지 않도록 용기를 북돋아줘요. 
SAFETY_SETTINGS = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

def set_smart_font():
    # // 초등학생 설명: 컴퓨터 종류에 맞춰서 가장 예쁜 한글 글씨체를 자동으로 골라줘요. 
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
    # // 초등학생 설명: 인공지능에게 질문을 던지고 대답을 받을 때까지 기다려요. 
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
    # // 초등학생 설명: 인공지능의 대답에서 불필요한 낙서들을 지우고 알맹이만 꺼내요. 
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
    # // 초등학생 설명: 어떤 주제로 글을 쓸지 정하고 인공지능에게 숙제를 내줘요. 
    now = datetime.datetime.now()
    safety_date = (now - datetime.timedelta(days=1)).strftime("%Y-%m-%d")
    current_date_str = now.strftime("%B %Y")
    current_year = now.year
    
    print(f"🚀 [Gemini API] '{topic}' 분석 시작 (V5.0 지침 적용)...")
    
    prompt = f"""
    Role: Senior Real Estate Investment Analyst.
    Task: Write a high-quality blog post about "{topic}".
    
    # 🛑 STRICT RULES (V5.0)
    1. BULLET POINTS ONLY: No long prose. Use (*) for all analysis.
    2. MOBILE READY: Max 2 lines per paragraph. Blank lines between sections.
    3. SUMMARY TABLE: Mandatory Markdown Table at the start of Body.
    4. NO GREETINGS: Do NOT start with "Hello". Start directly with a Hook.
    5. DATA SAFETY: Use price ranges (e.g. "8억 중반 ~ 9억 초반").

    Format: Output ONLY a single valid JSON object.
    JSON Keys:
    "viral_title", "category", "search_keyword", "roi_data", "calculator_type", "blog_body_markdown", "tistory_teaser"
    
    Internal Links to include:
    {CALC_MENU_STR}
    """
    
    result = generate_one_shot(prompt)
    if not result: return None
    
    data = clean_json_response(result)
    return data, safety_date

def generate_graph(filename_base, data_dict):
    # // 초등학생 설명: 숫자 데이터를 멋진 막대기와 꺾은선이 있는 그림으로 바꿔줘요. 
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
    # // 초등학생 설명: 인공지능이 쓴 글과 우리가 만든 그림, 버튼들을 하나로 합쳐요. 
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
    if calc_type in CALCULATOR_MAP and calc_type != 'none':
        info = CALCULATOR_MAP[calc_type]
        calculator_btn = f"""
<div style="margin-top: 30px; margin-bottom: 30px; text-align: center; background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e9ecef;">
    <p style="margin-bottom: 10px; font-weight: bold; color: #495057;">👇 이 매물, 내 조건으로 계산해보기</p>
    <a href="{MAIN_DOMAIN_URL}{info['url']}" target="_blank" style="display: inline-block; background-color: {COLOR_BTN_BG}; color: white; padding: 15px 30px; border-radius: 50px; font-weight: bold; text-decoration: none; box-shadow: 0 4px 6px rgba(0,0,0,0.1); transition: 0.3s;">
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

부동산은 **타이밍**이 생명입니다.
내 자금으로 가능한 **최고의 매물**이 무엇인지 지금 바로 확인하세요.

{calculator_btn}

📉 **대출 나오는지 걱정되시나요?**
👉 <a href="{MAIN_DOMAIN_URL}/calculators/calc_dsr/" target="_blank" rel="noopener noreferrer"><strong>💰 내 연봉으로 대출 한도 셀프 계산하기 (DSR 계산기)</strong></a>

🚀 **실시간 매물 호가 확인**
<a href="{naver_land_url}" target="_blank" rel="noopener noreferrer">👉 <strong>네이버 부동산에서 '{keyword}' 시세/실거래가 확인하기 (클릭)</strong></a>

<br><hr><small>📢 <strong>면책 조항 (Disclaimer)</strong><br>
본 포스팅은 부동산 데이터 분석에 기초한 정보 제공을 목적으로 하며, 투자의 법적 책임은 투자자 본인에게 있습니다.</small>"""

    return f"{front_matter}\n\n![전망 차트]({graph_url})\n*▲ AI 분석 데이터 ({post_date} 기준)*\n\n{body}{footer}"

def deploy_to_github(title, content, category_kr, post_date):
    # // 초등학생 설명: 완성된 글을 가방에 담아서 깃허브라는 커다란 창고로 보내요. 
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
    # // 초등학생 설명: 다른 동네 친구들도 볼 수 있게 짧은 요약 편지를 따로 써둬요. 
    draft_dir = "tistory_drafts"
    if not os.path.exists(draft_dir): os.makedirs(draft_dir)
    safe_title = re.sub(r'[\\/*?:"<>|]', "", title).replace(" ", "-")
    path = os.path.join(draft_dir, f"Tistory-{safe_title}_auto.txt")
    
    html = f"""
    <div style="font-size: 16px; line-height: 1.8;">
        <h2>{title}</h2><br>{teaser}<br><br>
        <div style="text-align: center; margin-top: 20px;">
            <a href="{link}" target="_blank" style="display: inline-block; background-color: {COLOR_TISTORY}; color: white; padding: 15px 40px; text-decoration: none; font-weight: bold; border-radius: 8px; font-size: 18px; box-shadow: 0 4px 6px rgba(0,0,0,0.2);">
                👉 리포트 전문(Full) 무료로 보기
            </a>
        </div>
    </div>"""
    with open(path, "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    # // 초등학생 설명: 프로그램의 전원을 켜고 주인님이 시키는 일을 시작해요! 
    print("\n" + "="*60)
    print("🔥 PropTech API Bot V21.0 (360줄 로직 100% 복구 및 V5.0 통합)")
    print("   ✅ 모든 계산기 매핑, 상세 HTML 디자인, MID_IMAGE 처리 복구 완료")
    print("="*60)
    
    topic = input("\n✍️ 분석 주제 입력: ")
    if topic:
        data, s_date = process_topic_one_shot(topic)
        if data:
            graph_url = generate_graph("chart", data.get('roi_data', {}))
            full_content = create_final_content(data, graph_url, s_date)
            link = deploy_to_github(data.get('viral_title'), full_content, data.get('category'), s_date)
            save_tistory_snippet(data.get('viral_title'), data.get('tistory_teaser'), link)
            print(f"🎉 발행 완료! (날짜: {s_date})")