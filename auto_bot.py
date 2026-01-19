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
MODEL_NAME = 'gemini-flash-latest' # 안전하고 빠른 모델
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def set_korean_font():
    """맥북 한글 폰트 설정"""
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def generate_graph(topic, filename_base):
    """전문가 느낌의 차트 생성 (색상 변경)"""
    print("📊 [1/5] 데이터 분석 그래프 그리는 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    os.makedirs(image_dir, exist_ok=True)
    img_filename = f"{filename_base}-chart.png"
    img_path = os.path.join(image_dir, img_filename)

    years = ['2023', '2024', '2025(E)', '2026(F)']
    # 우상향 그래프 데이터
    values = [100, random.randint(110, 130), random.randint(140, 170), random.randint(180, 220)]
    
    plt.figure(figsize=(10, 6))
    # 강렬한 붉은색 계열 (상승장 느낌)
    plt.bar(years, values, color=['#ffcdd2', '#e57373', '#f44336', '#b71c1c'], width=0.6)
    
    plt.title(f"Market Value Projection: {topic}", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Growth Index (Base=100)", fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.savefig(img_path, dpi=100, bbox_inches='tight')
    plt.close()
    return f"/images/{img_filename}"

def generate_github_content(topic, graph_url):
    """깃허브용: 독자를 낚는 '매운맛' 글쓰기"""
    print(f"🤖 [2/5] 깃허브용 심층 분석 글 작성 중...")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    cover_image = "https://loremflickr.com/1600/900/city,building,finance"

    front_matter = f"""---
title: "{topic}"
date: {today}
draft: false
categories: ["Real Estate Analysis", "PropTech"]
tags: ["Investment", "Data", "Trend"]
cover:
    image: "{cover_image}"
    alt: "{topic}"
    caption: "AI Data Analysis Lab"
    relative: false
    hidden: false
---"""

    # 🔥 [핵심] 프롬프트 대폭 수정: 가독성, 체류시간, 클릭 유도
    prompt = f"""
    당신은 월 1,000만 원 수익을 내는 '독설가 스타일의 부동산 데이터 전문가'입니다.
    주제 '{topic}'에 대해 블로그 글을 작성하세요.
    
    [작성 스타일 가이드]
    1. **서론 (Hook)**:
       - 독자의 불안 심리나 호기심을 자극하며 시작하세요. (예: "아직도 여기에 투자 안 하셨나요?", "이 데이터 보고도 안 움직이면 바보입니다.")
       - 글 최상단에 **[3줄 요약]** 박스를 만드세요 (인용구 > 사용).
    
    2. **본문 (Body)**:
       - **문단은 짧게** 끊으세요. (3~4줄마다 엔터 두 번). 그래야 광고가 잘 들어갑니다.
       - 중요한 단어는 반드시 **굵게(Bold)** 처리하세요.
       - "위 그래프를 보세요" 라고 말하며 데이터를 근거로 제시하세요.
       - 중간중간 "💡 **전문가의 팁:**" 섹션을 넣어 꿀팁을 주세요.
    
    3. **결론 (Action)**:
       - 뜬구름 잡지 말고, **"지금 당장 해야 할 행동"**을 1, 2, 3 번호로 매겨서 알려주세요.
       - 마지막엔 "더 늦기 전에 선점하세요." 같은 멘트로 마무리하세요.
    
    **Front Matter는 출력하지 말고, 본문 마크다운만 작성하세요.**
    """
    
    response = model.generate_content(prompt)
    body = response.text.replace("```markdown", "").replace("```", "")
    
    full_content = f"{front_matter}\n\n![Market Chart]({graph_url})\n*▲ {topic} 성장 예측 시뮬레이션 (AI 분석)*\n\n{body}"
    return full_content

def generate_tistory_content(topic, github_link):
    """티스토리용: 궁금하게 만들어서 클릭 유도"""
    print(f"🎨 [3/5] 티스토리용 낚시성 원고 생성 중...")
    
    prompt = f"""
    주제 '{topic}'에 대해 티스토리 블로그용 **'요약형 미끼 글'**을 HTML로 작성하세요.
    
    [작성 전략]
    1. 핵심 결론을 알려줄 듯 말 듯 궁금증을 유발하세요.
    2. "이 분석의 **풀버전 데이터**와 **투자 유망 리스트**는 본문에서 공개합니다."라는 멘트 필수.
    3. 전체 스타일: `<div style="font-family: sans-serif; line-height: 1.8;">` 적용.
    4. **매우 크고 눈에 띄는 버튼**을 만드세요.
       - 버튼 링크: {github_link}
       - 버튼 텍스트: "👉 (클릭) AI가 분석한 '비공개 데이터' 전체 보기"
       - 버튼 스타일: 빨간색 배경(#d32f2f), 흰색 글씨, 폰트 크기 18px, 굵게, 중앙 정렬, 패딩 15px.
    
    [태그 생성]
    HTML 코드 끝난 뒤, 맨 마지막 줄에 **검색 잘 되는 태그 10개** (쉼표 구분) 작성.
    """
    
    response = model.generate_content(prompt)
    content = response.text.replace("```html", "").replace("```", "")
    
    lines = content.strip().split('\n')
    tags = lines[-1]
    html_body = "\n".join(lines[:-1])
    
    return html_body, tags

def deploy_to_github(topic, content):
    """깃허브 배포"""
    print(f"🚀 [4/5] 깃허브에 배포 중...")
    safe_title = topic.replace(" ", "-").replace("?", "").replace("/", "")
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    filepath = os.path.join(BLOG_DIR, "content", "posts", filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"New Post: {topic}")
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ 배포 완료!")
        return f"{MAIN_DOMAIN_URL}/posts/{filename.replace('.md', '').lower()}"
    except:
        return MAIN_DOMAIN_URL

def save_tistory_file(topic, html, tags):
    """티스토리 원고 저장"""
    print(f"💾 [5/5] 티스토리 파일 저장 중...")
    draft_dir = "tistory_drafts"
    os.makedirs(draft_dir, exist_ok=True)
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{topic.replace(' ', '-')}.txt"
    filepath = os.path.join(draft_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"주제: {topic}\n\n[태그]\n{tags}\n\n[HTML]\n{html}")
    
    print(f"✨ 저장 완료: {filepath}")
    try: os.system(f"open {draft_dir}")
    except: pass

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 PropTech 파워블로거 시스템 (매운맛 버전)")
    print("="*50)
    topic = input("✍️  글 주제 입력: ")
    if topic:
        safe = topic.replace(" ", "-").replace("?", "")
        url = generate_graph(topic, safe)
        git_content = generate_github_content(topic, url)
        link = deploy_to_github(topic, git_content)
        html, tags = generate_tistory_content(topic, link)
        save_tistory_file(topic, html, tags)