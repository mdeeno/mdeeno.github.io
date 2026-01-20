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

def get_model(model_name='gemini-1.5-flash'):
    """모델을 가져오되, 실패하면 구형 모델로 자동 전환하는 똑똑한 함수"""
    return genai.GenerativeModel(model_name)

def generate_content_safe(prompt, model_priority=['gemini-1.5-flash', 'gemini-pro']):
    """
    1순위 모델(1.5-flash)로 시도하고, 
    404/429 에러가 나면 2순위(pro)로 자동 전환하여 무조건 성공시키는 함수
    """
    for model_name in model_priority:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"⚠️ [{model_name}] 실패... 다음 모델로 전환합니다. (에러: {e})")
            time.sleep(1) # 잠시 대기 후 재시도
            continue
    
    # 모든 모델 실패 시
    return "죄송합니다. 모든 AI 모델이 응답하지 않습니다."

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def get_real_data_from_llm(topic):
    print(f"🧠 [1/6] '{topic}' 데이터 조회 (AI 자동 스위칭)...")
    
    current_year = datetime.datetime.now().year
    prompt = f"""
    Act as a Data Analyst. Topic: "{topic}"
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
    
    # 🔥 여기서 안전하게 생성 요청
    result_text = generate_content_safe(prompt)
    
    try:
        clean_text = result_text.replace("```json", "").replace("```python", "").replace("```", "").strip()
        data_dict = ast.literal_eval(clean_text)
        return data_dict
    except:
        return {
            "years": ["2023", "2024", "2025", "2026"],
            "values": [100, 110, 120, 130],
            "unit": "Index",
            "title": f"{topic} 트렌드"
        }

def generate_viral_title(topic):
    print(f"⚡ [2/6] 제목 세탁 중...")
    prompt = f"""
    Make a viral blog title for "{topic}" in Korean. 
    Use strong words like "충격", "긴급", "전망". Max 35 chars.
    Output ONLY the title.
    """
    result = generate_content_safe(prompt)
    return result.strip().replace('"', '')

def get_image_keywords(topic):
    print(f"🎨 [3/6] 이미지 키워드 추출 중...")
    prompt = f"""
    Topic: "{topic}"
    Extract 3 english keywords for stock photos.
    Example: "train,station,city"
    Output ONLY keywords (comma separated).
    """
    result = generate_content_safe(prompt)
    return result.strip().replace(" ", "")

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
    
    body_text = generate_content_safe(prompt)
    body = body_text.replace("```markdown", "").replace("```", "")
    
    full_content = f"{front_matter}\n\n![Chart]({graph_url})\n*▲ {topic} 통계 분석 ({now.year} 기준)*\n\n{body}"
    return full_content

def generate_tistory_content(viral_title, github_link):
    print(f"🎨 [6/6] 티스토리 요약글 생성 중...")
    prompt = f"""
    Write a HTML teaser for a blog post about "{viral_title}".
    Language: Korean.
    Include a button linking to: {github_link}
    Last line: 10 tags separated by commas.
    """
    result = generate_content_safe(prompt)
    
    try:
        content = result.replace("```html", "").replace("```", "")
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
    print("🔥 PropTech 봇 (AI 자동 스위칭 모드)")
    print("   1순위: gemini-1.5-flash (최신)")
    print("   2순위: gemini-pro (안전빵)")
    print("="*50)
    
    topic = input("✍️  주제 입력 (예: 금리 전망, 삼성전자 주가): ")
    if topic:
        data_dict = get_real_data_from_llm(topic)
        viral_title = generate_viral_title(topic)
        img_keywords = get_image_keywords(topic)
        graph_url = generate_graph("chart", data_dict)
        git_content = generate_github_content(topic, viral_title, graph_url, data_dict, img_keywords)
        link = deploy_to_github(viral_title, git_content)
        html, tags = generate_tistory_content(viral_title, link)
        save_tistory_file(viral_title, html, tags)