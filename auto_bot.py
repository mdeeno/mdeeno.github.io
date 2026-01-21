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
# [설정 영역]
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_DIR = os.getenv("BLOG_DIR")
MAIN_DOMAIN_URL = "https://tech.mdeeno.com"
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def find_working_model():
    """
    [최종 수정] 딴눈 팔지 않고 오직 '1.5-flash'만 찾아서 연결합니다.
    """
    print("🔍 [시스템] 무료 혜자 모델(1.5 Flash) 연결 중...", end=" ")
    try:
        # 내 API 키로 쓸 수 있는 모델 리스트 가져오기
        my_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        
        # 1.5 Flash가 있는지 확인 (가장 정확한 이름 매칭)
        target_model = 'models/gemini-1.5-flash'
        
        if target_model in my_models:
            print(f"성공! 👉 [{target_model}]")
            return target_model
        
        # 혹시 이름이 조금 다를 경우를 대비해 검색
        for m in my_models:
            if 'gemini-1.5-flash' in m:
                print(f"성공! 👉 [{m}]")
                return m

        print("\n⚠️ 목록에서 못 찾았지만, 강제로 연결을 시도합니다.")
        return 'models/gemini-1.5-flash'
            
    except Exception as e:
        print(f"\n⚠️ 모델 탐색 에러(무시하고 진행): {e}")
        return 'models/gemini-1.5-flash'

# 모델 확정
ACTIVE_MODEL_NAME = find_working_model()
model = genai.GenerativeModel(ACTIVE_MODEL_NAME)

def set_korean_font():
    """맥북 한글 폰트 설정"""
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def get_real_data_from_llm(topic):
    print(f"🧠 [1/6] '{topic}' 데이터 분석 중...")
    time.sleep(1) 
    
    current_year = datetime.datetime.now().year
    prompt = f"""
    You are a Data Analyst. Topic: "{topic}"
    Extract real statistical data (2023-{current_year+1}).
    
    Output Format (JSON only):
    {{
        "years": ["2023", "2024", "2025(E)", "2026(F)"],
        "values": [1.5, 2.0, 2.5, 3.0],
        "unit": "%",
        "title": "Exact Title of Chart"
    }}
    NO MARKDOWN. JUST JSON STRING.
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.replace("```json", "").replace("```python", "").replace("```", "").strip()
        data_dict = ast.literal_eval(clean_text)
        return data_dict
    except Exception as e:
        print(f"⚠️ 데이터 추출 실패 (기본값 사용): {e}")
        return {
            "years": ["2023", "2024", "2025", "2026"],
            "values": [100, 110, 120, 130],
            "unit": "Index",
            "title": f"{topic} 트렌드"
        }

def generate_viral_title(topic):
    print(f"⚡ [2/6] 제목 세탁 중...")
    time.sleep(1)
    prompt = f"""
    Make a viral blog title for "{topic}" in Korean. 
    Use strong words like "충격", "긴급", "전망". Max 35 chars.
    Output ONLY the title.
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip().replace('"', '')
    except:
        return f"충격 전망! {topic}의 미래"

def get_image_keywords(topic):
    print(f"🎨 [3/6] 이미지 키워드 추출 중...")
    time.sleep(1)
    prompt = f"""
    Topic: "{topic}"
    Extract 3 english keywords for stock photos.
    Example: "train,station,city"
    Output ONLY keywords (comma separated).
    """
    try:
        response = model.generate_content(prompt)
        return response.text.strip().replace(" ", "")
    except:
        return "business,finance,tech"

def generate_graph(filename_base, data_dict):
    print(f"📊 [4/6] '{data_dict['unit']}' 단위로 그래프 그리는 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    os.makedirs(image_dir, exist_ok=True)
    img_filename = f"{filename_base}-chart.png"
    img_path = os.path.join(image_dir, img_filename)

    years = data_dict['years']
    values = data_dict['values']
    unit = data_dict['unit']
    title = data_dict['title']
    
    if values[-1] > values[0]:
        color = ['#ffcdd2', '#ef9a9a', '#ef5350', '#c62828'] 
    elif values[-1] < values[0]:
        color = ['#bbdefb', '#90caf9', '#42a5f5', '#1565c0'] 
    else:
        color = ['#e1bee7', '#ce93d8', '#ab47bc', '#7b1fa2'] 

    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, values, color=color, width=0.6)
    
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

def generate_github_content(topic, viral_title, graph_url, data_dict, img_keywords):
    print(f"🤖 [5/6] 리포트 작성 중...")
    time.sleep(1)
    now = datetime.datetime.now()
    
    data_summary = ""
    for y, v in zip(data_dict['years'], data_dict['values']):
        data_summary += f"- **{y}**: {v}{data_dict['unit']}\n"

    cover_image = f"[https://loremflickr.com/1600/900/](https://loremflickr.com/1600/900/){img_keywords}"

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
    Act as a Professional Data Analyst.
    Topic: {topic}
    Title: {viral_title}
    Data:
    {data_summary}
    
    Write a blog post in Korean (Markdown).
    Structure:
    1. **Fact Check**: Explain the data objectively.
    2. **Insight**: Why is this happening?
    3. **Action Plan**: What should the reader do NOW?
    
    Output ONLY Markdown body.
    """
    
    try:
        response = model.generate_content(prompt)
        body = response.text.replace("```markdown", "").replace("```", "")
    except:
        body = "내용 생성 중 오류가 발생했습니다."
    
    full_content = f"{front_matter}\n\n![Chart]({graph_url})\n*▲ {topic} 통계 분석 ({now.year} 기준)*\n\n{body}"
    return full_content

def generate_tistory_content(viral_title, github_link):
    print(f"🎨 [6/6] 티스토리 요약글 생성 중...")
    time.sleep(1)
    prompt = f"""
    Write a HTML teaser for a blog post about "{viral_title}".
    Language: Korean.
    Include a button linking to: {github_link}
    Last line: 10 tags separated by commas.
    """
    try:
        response = model.generate_content(prompt)
        content = response.text.replace("```html", "").replace("```", "")
        lines = content.strip().split('\n')
        return "\n".join(lines[:-1]), lines[-1]
    except:
        return "<p>내용을 확인하세요.</p>", "태그1, 태그2"

def deploy_to_github(viral_title, content):
    print(f"🚀 [7/7] 배포 중...") 
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
    print("🔥 PropTech 봇 (1.5 Flash 강제 고정)")
    print("="*50)
    
    if ACTIVE_MODEL_NAME:
        topic = input("✍️  주제 입력: ")
        if topic:
            data_dict = get_real_data_from_llm(topic)
            viral_title = generate_viral_title(topic)
            img_keywords = get_image_keywords(topic)
            graph_url = generate_graph("chart", data_dict)
            git_content = generate_github_content(topic, viral_title, graph_url, data_dict, img_keywords)
            link = deploy_to_github(viral_title, git_content)
            html, tags = generate_tistory_content(viral_title, link)
            save_tistory_file(viral_title, html, tags)
    else:
        print("❌ 실행을 중단합니다.")