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

# 가장 안전한 모델 (최신 Flash)
MODEL_NAME = 'gemini-flash-latest'
# ==============================================================================

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(MODEL_NAME)

def set_korean_font():
    """맥북 한글 폰트 깨짐 방지 설정 (AppleGothic)"""
    system_name = platform.system()
    if system_name == "Darwin": # 맥북일 경우
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except:
            pass

def generate_graph(topic, filename_base):
    """주제에 어울리는 전문적인 차트 생성"""
    print("📊 [1/5] 데이터 분석 그래프 그리는 중...")
    
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    os.makedirs(image_dir, exist_ok=True)
    
    img_filename = f"{filename_base}-chart.png"
    img_path = os.path.join(image_dir, img_filename)

    years = ['2023', '2024', '2025(E)', '2026(F)']
    values = [random.randint(40, 60), random.randint(65, 85), random.randint(90, 110), random.randint(120, 150)]
    
    plt.figure(figsize=(10, 6))
    plt.bar(years, values, color=['#cfd8dc', '#90a4ae', '#546e7a', '#263238'], width=0.6)
    
    plt.title(f"Growth Projection: {topic}", fontsize=14, fontweight='bold', pad=20)
    plt.ylabel("Index / Market Value", fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.5)
    
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.savefig(img_path, dpi=100, bbox_inches='tight')
    plt.close()
    
    return f"/images/{img_filename}"

def generate_github_content(topic, graph_url):
    """깃허브용 마크다운 본문 생성"""
    print(f"🤖 [2/5] 깃허브용 심층 분석 글 작성 중...")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    cover_image = "https://loremflickr.com/1600/900/architecture,city,modern"

    front_matter = f"""---
title: "{topic}"
date: {today}
draft: false
categories: ["PropTech", "Urban Insight"]
tags: ["Data", "Analysis", "Future"]
cover:
    image: "{cover_image}"
    alt: "{topic}"
    caption: "AI Data Analysis"
    relative: false
    hidden: false
---"""

    prompt = f"""
    당신은 월 500만 원 수익을 내는 '도시공학 석사 출신 프롭테크 전문가'입니다.
    주제 '{topic}'에 대해 깃허브 기술 블로그에 올릴 **전문적인 마크다운 글**을 써주세요.
    
    [작성 전략]
    1. 서론: 충격적인 통계나 질문으로 시작.
    2. 본문: 소제목(##) 3개 이상. 논리적 근거 제시.
    3. 데이터 언급: "상단 그래프를 보시면(Refer to the chart above)" 멘트 필수.
    4. 결론: 향후 전망 및 제언.
    5. 말투: 신뢰감 있는 해요체.
    
    **Front Matter는 쓰지 마세요. 본문만 작성하세요.**
    """
    
    response = model.generate_content(prompt)
    body = response.text.replace("```markdown", "").replace("```", "")
    
    full_content = f"{front_matter}\n\n![Data Chart]({graph_url})\n*▲ {topic} 시장 성장 예측 시뮬레이션*\n\n{body}"
    return full_content

def generate_tistory_content(topic, github_link):
    """티스토리용 HTML 본문 + 해시태그 생성"""
    print(f"🎨 [3/5] 티스토리용 HTML 및 해시태그 생성 중...")
    
    prompt = f"""
    주제 '{topic}'에 대해 티스토리 블로그에 올릴 **대중 친화적인 글**을 HTML 형식으로 작성해 주세요.
    
    [HTML 스타일 가이드]
    1. 전체를 `<div style="font-family: 'Apple SD Gothic Neo', sans-serif; line-height: 1.8; color: #333;">` 로 감쌀 것.
    2. 소제목은 `<h3>` 태그를 쓰고 `style="border-left: 5px solid #263238; padding-left: 10px; margin-top: 30px;"` 스타일 적용.
    3. 중요 문장은 `<span style="background-color: #eee; font-weight: bold; padding: 2px 5px;">` 로 강조.
    4. 글 마지막에 깃허브 원문으로 가는 **크고 예쁜 버튼** 추가 (링크: {github_link}).
       - 버튼 멘트: "📊 더 깊이 있는 데이터 분석 원문 보러가기"
       - 버튼 스타일: 중앙 정렬, 검은색 배경, 흰색 글씨, 둥근 모서리.
    
    [추가 요청]
    HTML 코드 작성이 끝나면, 맨 마지막 줄에 이 글에 어울리는 **검색 유입용 태그 10개**를 작성해줘.
    - 조건: 해시태그(#) 기호 제외.
    - 조건: 쉼표(,)로 구분.
    """
    
    response = model.generate_content(prompt)
    content = response.text.replace("```html", "").replace("```", "")
    
    lines = content.strip().split('\n')
    tags = lines[-1]
    html_body = "\n".join(lines[:-1])
    
    return html_body, tags

def deploy_to_github(topic, content):
    """깃허브 배포"""
    print(f"🚀 [4/5] 깃허브에 먼저 배포 중...")
    
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
        print("✅ 깃허브 배포 완료!")
        post_url = f"{MAIN_DOMAIN_URL}/posts/{filename.replace('.md', '').lower()}"
        return post_url
    except Exception as e:
        print(f"❌ 배포 실패: {e}")
        return MAIN_DOMAIN_URL

def save_tistory_file(topic, html, tags):
    """티스토리 원고를 별도 텍스트 파일로 저장"""
    print(f"💾 [5/5] 티스토리 원고 파일로 저장 중...")
    
    # 저장할 폴더 (없으면 생성)
    draft_dir = "tistory_drafts"
    os.makedirs(draft_dir, exist_ok=True)
    
    # 파일명 생성
    safe_title = topic.replace(" ", "-").replace("?", "")
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.txt"
    filepath = os.path.join(draft_dir, filename)
    
    # 파일 쓰기
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("=" * 50 + "\n")
        f.write(f"📌 주제: {topic}\n")
        f.write("=" * 50 + "\n\n")
        
        f.write("[ 1. 티스토리 태그 (복사해서 '태그' 란에 붙여넣기) ]\n")
        f.write("-" * 50 + "\n")
        f.write(tags)
        f.write("\n" + "-" * 50 + "\n\n\n")
        
        f.write("[ 2. HTML 본문 (복사해서 'HTML 모드'에 붙여넣기) ]\n")
        f.write("-" * 50 + "\n")
        f.write(html)
        f.write("\n" + "-" * 50 + "\n")
        
    print(f"✨ 저장 완료! 아래 파일을 열어서 복사/붙여넣기 하세요.")
    print(f"📂 파일 위치: {filepath}")
    
    # 맥북에서 폴더 자동으로 열어주기 (선택사항)
    try:
        os.system(f"open {draft_dir}")
    except:
        pass

if __name__ == "__main__":
    print("\n" + "="*60)
    print("🏗️  PropTech 고퀄리티 반자동 시스템 (파일 저장 기능 추가)")
    print("="*60)
    
    topic = input("✍️  글 주제를 입력하세요: ")
    
    if topic:
        safe_title = topic.replace(" ", "-").replace("?", "")
        
        # 1. 그래프 생성
        graph_url = generate_graph(topic, safe_title)
        
        # 2. 깃허브 글 생성 및 배포
        github_content = generate_github_content(topic, graph_url)
        post_link = deploy_to_github(topic, github_content)
        
        # 3. 티스토리용 HTML 생성
        tistory_html, tistory_tags = generate_tistory_content(topic, post_link)
        
        # 4. 파일로 저장
        save_tistory_file(topic, tistory_html, tistory_tags)

    else:
        print("❌ 주제를 입력하지 않았습니다.")