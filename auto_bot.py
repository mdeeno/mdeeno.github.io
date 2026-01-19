import os
import time
import datetime
import random
import platform
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib import rc
from git import Repo
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# ==============================================================================
# [설정 영역]
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_DIR = os.getenv("BLOG_DIR")
MAIN_DOMAIN_URL = "https://tech.mdeeno.com"
MODEL_NAME = 'gemini-flash-latest'
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def generate_viral_title(topic):
    """제목 세탁기: 클릭을 부르는 제목으로 변환"""
    print(f"⚡ [1/6] 제목을 자극적으로 세탁하는 중...")
    prompt = f"""
    주제: "{topic}"
    
    이 주제를 블로그 제목으로 쓸 건데, 사람들이 클릭을 안 하고는 못 배기게 **'자극적이고 논란이 될만한'** 제목으로 바꿔줘.
    
    [규칙]
    1. 물음표(?)나 느낌표(!) 적극 사용.
    2. "충격", "긴급", "폭등", "아직도", "피눈물" 같은 단어 사용.
    3. 길이는 35자 이내.
    4. 예시: "GTX 분석" -> "GTX 개통 임박? 지금 안 사면 벼락거지 확정입니다"
    
    **오직 바뀐 제목만 출력해 (따옴표 제외).**
    """
    response = model.generate_content(prompt)
    viral_title = response.text.strip().replace('"', '')
    print(f"   👉 변경된 제목: {viral_title}")
    return viral_title

def generate_graph(topic, filename_base):
    print("📊 [2/6] 데이터 분석 그래프 그리는 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    os.makedirs(image_dir, exist_ok=True)
    img_filename = f"{filename_base}-chart.png"
    img_path = os.path.join(image_dir, img_filename)

    # 현재 연도 자동 인식
    current_year = datetime.datetime.now().year
    years = [str(current_year-3), str(current_year-2), str(current_year-1), str(current_year)+'(Now)']
    values = [100, random.randint(110, 130), random.randint(140, 170), random.randint(190, 230)]
    
    plt.figure(figsize=(10, 6))
    plt.bar(years, values, color=['#b0bec5', '#90a4ae', '#ff7043', '#d84315'], width=0.6)
    
    plt.title(f"Market Trend: {topic}", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Growth Index (Base=100)", fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.savefig(img_path, dpi=100, bbox_inches='tight')
    plt.close()
    return f"/images/{img_filename}"

def generate_github_content(original_topic, viral_title, graph_url):
    print(f"🤖 [3/6] 현재 시점(Today) 기준으로 글 작성 중...")
    
    # 🔥 [핵심] 컴퓨터의 현재 날짜를 가져와서 봇에게 주입
    now = datetime.datetime.now()
    today_str = now.strftime("%Y년 %m월 %d일")
    current_year = now.year
    
    cover_image = "https://loremflickr.com/1600/900/city,money,luxury"

    front_matter = f"""---
title: "{viral_title}"
date: {now.strftime("%Y-%m-%d")}
draft: false
categories: ["Insight", "Market Analysis"]
tags: ["Investment", "Real Estate", "{current_year} Trend"]
cover:
    image: "{cover_image}"
    alt: "{viral_title}"
    caption: "Data Analysis Lab"
    relative: false
    hidden: false
---"""

    prompt = f"""
    **[시점 고정 명령]**
    오늘 날짜: **{today_str}**
    
    너는 지금 **{today_str}** 현재를 살고 있는 '냉철한 데이터 분석가'다.
    모든 분석과 제언은 **오늘({today_str})**을 기준으로 작성되어야 한다.
    
    [절대 금지]
    - 오늘보다 과거의 날짜(예: {current_year-1}년, {current_year-2}년)를 미래처럼 예측하지 마라.
    - 예: "{current_year-2}년 말에 사세요" (X) -> "{current_year-2}년에 샀어야 했습니다" (O)
    - 예: "{current_year}년 전망은..." (O)
    
    [작성 주제]
    원래 주제: {original_topic}
    제목: {viral_title}
    
    [글 구조]
    1. **Intro**: "{today_str} 기준, 최신 데이터가 업데이트되었습니다."로 시작.
    2. **Body**:
       - 과거 데이터와 현재 데이터를 비교하며 상승세를 증명.
       - "위 그래프를 보세요. 지금 지표가 가리키는 방향은 명확합니다."
       - 문단은 짧게, **핵심은 굵게**.
    3. **Action Plan**:
       - 독자가 **오늘 당장** 실행해야 할 3가지 행동 강령.
       - "지금이 막차입니다." 같은 긴박함 조성.
    
    **Front Matter 제외하고 본문 마크다운만 출력.**
    """
    
    response = model.generate_content(prompt)
    body = response.text.replace("```markdown", "").replace("```", "")
    
    full_content = f"{front_matter}\n\n![Market Chart]({graph_url})\n*▲ {original_topic} 시장 데이터 추이 ({today_str} 기준)*\n\n{body}"
    return full_content

def generate_tistory_content(viral_title, github_link):
    print(f"🎨 [4/6] 티스토리용 요약글 생성 중...")
    
    prompt = f"""
    제목: {viral_title}
    
    티스토리용 '궁금증 유발형' 요약글 (HTML).
    1. 핵심 정보(지역, 종목)는 가리고 "블로그 본문에서 공개"라고 유도.
    2. 버튼: "🚨 [클릭] 비공개 리포트 전체 보기" (링크: {github_link})
    3. 버튼 스타일: 빨간색, 큼직하게.
    4. 마지막 줄에 태그 10개(쉼표 구분).
    """
    
    response = model.generate_content(prompt)
    content = response.text.replace("```html", "").replace("```", "")
    
    lines = content.strip().split('\n')
    tags = lines[-1]
    html_body = "\n".join(lines[:-1])
    
    return html_body, tags

def deploy_to_github(viral_title, content):
    print(f"🚀 [5/6] 깃허브 배포 중...")
    safe_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{hash(viral_title)}.md"
    filepath = os.path.join(BLOG_DIR, "content", "posts", safe_filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"New Post: {viral_title}")
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ 배포 완료!")
        return f"{MAIN_DOMAIN_URL}/posts/{safe_filename.replace('.md', '')}"
    except:
        return MAIN_DOMAIN_URL

def save_tistory_file(viral_title, html, tags):
    print(f"💾 [6/6] 티스토리 파일 저장 중...")
    draft_dir = "tistory_drafts"
    os.makedirs(draft_dir, exist_ok=True)
    filename = f"Draft-{datetime.datetime.now().strftime('%H%M%S')}.txt"
    filepath = os.path.join(draft_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"제목: {viral_title}\n\n[태그]\n{tags}\n\n[HTML 본문]\n{html}")
    
    print(f"✨ 저장 완료: {filepath}")
    try: os.system(f"open {draft_dir}")
    except: pass

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 PropTech 파워블로거 봇 (Real-Time 동기화)")
    print("="*50)
    
    original_topic = input("✍️  주제 입력: ")
    
    if original_topic:
        viral_title = generate_viral_title(original_topic)
        # 파일명은 URL 안전하게
        safe_title = viral_title.replace(" ", "-").replace("?", "").replace("!", "")
        graph_url = generate_graph(viral_title, "graph")
        git_content = generate_github_content(original_topic, viral_title, graph_url)
        link = deploy_to_github(viral_title, git_content)
        html, tags = generate_tistory_content(viral_title, link)
        save_tistory_file(viral_title, html, tags)
    else:
        print("❌ 주제를 입력하세요.")