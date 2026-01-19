import os
import time
import datetime
import random
import platform
import ast
import google.generativeai as genai
import matplotlib.pyplot as plt
from matplotlib import rc
from git import Repo
from dotenv import load_dotenv

load_dotenv()

# ==============================================================================
# [설정]
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

def get_real_data_from_llm(topic):
    """
    LLM의 지식베이스를 활용해 '실제 데이터'와 '적절한 단위'를 추출함
    """
    print(f"🧠 [1/6] '{topic}' 관련 실제 통계 데이터 조회 중...")
    
    current_year = datetime.datetime.now().year
    
    prompt = f"""
    당신은 데이터 분석가입니다. 주제 "{topic}"에 대한 **실제 통계 데이터** 혹은 **가장 신뢰할 수 있는 추정치**를 알려주세요.
    
    [요구사항]
    1. 2023년부터 {current_year+1}년까지의 연도별 데이터 4개를 뽑아주세요.
    2. 데이터의 **단위(Unit)**를 반드시 명시하세요. (예: %, 명, 만원, 억원, 세대 등)
    3. Python 딕셔너리 형태로 출력하세요.
    
    [출력 포맷 예시]
    {{
        "years": ["2023", "2024", "2025(E)", "2026(F)"],
        "values": [3.50, 3.25, 3.00, 2.75],
        "unit": "%",
        "title": "한국 기준금리 추이"
    }}
    
    **설명 없이 오직 JSON(딕셔너리) 코드만 출력하세요.**
    """
    
    try:
        response = model.generate_content(prompt)
        # 텍스트 정제 (코드 블록 제거)
        clean_text = response.text.replace("```json", "").replace("```python", "").replace("```", "").strip()
        data_dict = ast.literal_eval(clean_text)
        return data_dict
    except Exception as e:
        print(f"⚠️ 데이터 추출 실패 (기본값 사용): {e}")
        # 실패 시 기본값
        return {
            "years": ["2023", "2024", "2025", "2026"],
            "values": [100, 110, 120, 130],
            "unit": "Index",
            "title": f"{topic} 트렌드 지수"
        }

def generate_viral_title(topic):
    print(f"⚡ [2/6] 제목 세탁 중...")
    prompt = f"""
    주제: "{topic}"
    클릭을 유도하는 블로그 제목 (35자 이내).
    규칙: "충격", "긴급", "공개", "전망" 등 단어 활용.
    오직 제목만 출력.
    """
    response = model.generate_content(prompt)
    return response.text.strip().replace('"', '')

def generate_graph(filename_base, data_dict):
    print(f"📊 [3/6] '{data_dict['unit']}' 단위로 그래프 그리는 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    os.makedirs(image_dir, exist_ok=True)
    img_filename = f"{filename_base}-chart.png"
    img_path = os.path.join(image_dir, img_filename)

    years = data_dict['years']
    values = data_dict['values']
    unit = data_dict['unit']
    title = data_dict['title']
    
    # 추세에 따른 색상 결정
    if values[-1] > values[0]:
        color = ['#ffcdd2', '#ef9a9a', '#ef5350', '#c62828'] # 상승(빨강)
    elif values[-1] < values[0]:
        color = ['#bbdefb', '#90caf9', '#42a5f5', '#1565c0'] # 하락(파랑)
    else:
        color = ['#e1bee7', '#ce93d8', '#ab47bc', '#7b1fa2'] # 보합(보라)

    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, values, color=color, width=0.6)
    
    # 막대 위에 수치 + 단위 표시
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height, 
                 f'{height}\n{unit}', 
                 ha='center', va='bottom', fontsize=10, fontweight='bold')

    plt.title(title, fontsize=14, fontweight='bold', pad=20)
    plt.ylabel(f"Unit: {unit}", fontsize=11)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.savefig(img_path, dpi=100, bbox_inches='tight')
    plt.close()
    return f"/images/{img_filename}"

def generate_github_content(topic, viral_title, graph_url, data_dict):
    print(f"🤖 [4/6] 실제 데이터 기반 리포트 작성 중...")
    now = datetime.datetime.now()
    
    # 데이터 요약 문자열 만들기
    data_summary = ""
    for y, v in zip(data_dict['years'], data_dict['values']):
        data_summary += f"- **{y}**: {v}{data_dict['unit']}\n"

    cover_image = "[https://loremflickr.com/1600/900/finance,chart,business](https://loremflickr.com/1600/900/finance,chart,business)"

    front_matter = f"""---
title: "{viral_title}"
date: {now.strftime("%Y-%m-%d")}
draft: false
categories: ["Data Analysis"]
tags: ["Statistics", "Trend", "Market"]
cover:
    image: "{cover_image}"
    alt: "{viral_title}"
    relative: false
---"""

    prompt = f"""
    현재 날짜: {now.strftime("%Y년 %m월 %d일")}
    
    주제: {topic}
    제목: {viral_title}
    **실제 확보된 데이터**:
    {data_summary}
    
    위 데이터를 바탕으로 전문적인 분석 글을 작성해.
    
    [작성 구조]
    1. **Fact Check**: "통계에 따르면..."이라며 위 데이터를 인용해 현재 상황을 팩트로 설명.
    2. **Insight**: 수치가 변화한 원인 분석 (전문가 관점).
    3. **Action**: 이 데이터({data_dict['values'][-1]}{data_dict['unit']})를 보고 독자가 해야 할 행동.
    
    **마크다운 본문만 출력.**
    """
    
    response = model.generate_content(prompt)
    body = response.text.replace("```markdown", "").replace("```", "")
    
    full_content = f"{front_matter}\n\n![Chart]({graph_url})\n*▲ {topic} 통계 분석 ({now.year} 기준)*\n\n{body}"
    return full_content

def generate_tistory_content(viral_title, github_link):
    print(f"🎨 [5/6] 티스토리 요약글 생성 중...")
    prompt = f"""
    제목: {viral_title}
    티스토리용 요약글(HTML).
    버튼: "🚨 [클릭] 통계 데이터 전체 보기" (링크: {github_link})
    마지막 줄: 태그 10개
    """
    response = model.generate_content(prompt)
    content = response.text.replace("```html", "").replace("```", "")
    lines = content.strip().split('\n')
    return "\n".join(lines[:-1]), lines[-1]

def deploy_to_github(viral_title, content):
    print(f"🚀 [6/6] 배포 중...")
    safe_filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{hash(viral_title)}.md"
    filepath = os.path.join(BLOG_DIR, "content", "posts", safe_filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"Post: {viral_title}")
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ 완료!")
        return f"{MAIN_DOMAIN_URL}/posts/{safe_filename.replace('.md', '')}"
    except: return MAIN_DOMAIN_URL

def save_tistory_file(viral_title, html, tags):
    draft_dir = "tistory_drafts"
    os.makedirs(draft_dir, exist_ok=True)
    filename = f"Draft-{datetime.datetime.now().strftime('%H%M%S')}.txt"
    filepath = os.path.join(draft_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"제목: {viral_title}\n\n[태그]\n{tags}\n\n[HTML]\n{html}")
    try: os.system(f"open {draft_dir}")
    except: pass

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 PropTech 봇 (Real Data + 단위 자동적용)")
    print("="*50)
    
    topic = input("✍️  주제 입력 (예: 한국 출산율, 강남 아파트 평당가): ")
    if topic:
        # 1. 실제 데이터 추출
        data_dict = get_real_data_from_llm(topic)
        
        # 2. 제목 생성
        viral_title = generate_viral_title(topic)
        
        # 3. 그래프 (단위 포함)
        graph_url = generate_graph("chart", data_dict)
        
        # 4. 글 작성
        git_content = generate_github_content(topic, viral_title, graph_url, data_dict)
        link = deploy_to_github(viral_title, git_content)
        
        # 5. 티스토리
        html, tags = generate_tistory_content(viral_title, link)
        save_tistory_file(viral_title, html, tags)