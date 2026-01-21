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

# 🚨 생존 전략: 무료 가능성이 높은 순서대로 '후보군'을 편성
MODEL_CANDIDATES = [
    'gemini-2.0-flash-exp',        
    'gemini-flash-latest',         
    'gemini-exp-1206',             
    'gemini-2.0-flash-lite-preview-02-05',
    'gemini-2.5-flash-lite-preview-09-2025'
]
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def generate_content_with_survival(prompt):
    """모델 서바이벌 실행 함수"""
    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            continue 
    print("\n❌ 모든 모델이 응답하지 않습니다.")
    raise Exception("All models failed")

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def get_real_data_from_llm(topic):
    print(f"🧠 [1/6] '{topic}' 수익성 분석 중...")
    time.sleep(1) 
    
    current_year = datetime.datetime.now().year
    prompt = f"""
    Topic: "{topic}"
    Task: Extract real investment trends & ROI data (2023-{current_year+1}).
    
    Output Format (JSON only):
    {{
        "years": ["2023", "2024", "2025(E)", "2026(F)"],
        "values": [10, 15, 23, 35],
        "unit": "ROI(%)",
        "title": "Investment Growth Projection"
    }}
    NO MARKDOWN. ONLY JSON STRING.
    """
    try:
        result_text = generate_content_with_survival(prompt)
        clean_text = result_text.replace("```json", "").replace("```python", "").replace("```", "").strip()
        data_dict = ast.literal_eval(clean_text)
        return data_dict
    except Exception as e:
        print(f"⚠️ 데이터 추출 실패 (기본값 사용): {e}")
        return {
            "years": ["2023", "2024", "2025", "2026"],
            "values": [100, 115, 135, 150],
            "unit": "Index",
            "title": f"{topic} 가치 상승 전망"
        }

def generate_viral_title(topic):
    print(f"⚡ [2/6] '돈 되는' 제목 뽑는 중...")
    time.sleep(1)
    
    # 🔥 수익화 핵심: 제목부터 '이익'을 강조하도록 변경
    prompt = f"""
    Act as a Real Estate Investment Consultant.
    Create a highly clickable, profit-focused blog title for "{topic}" in Korean.
    
    Rules:
    1. Focus on 'Profit', 'Timing', 'Undervalued', 'ROI'.
    2. Professional but Persuasive (Money-making tone).
    3. Example: "2026년 {topic}: 지금 사야 할 저평가 단지 TOP 3 분석"
    4. No vague titles. Be specific.
    
    Output ONLY the title.
    """
    try:
        result = generate_content_with_survival(prompt)
        return result.strip().replace('"', '')
    except:
        return f"[투자전략] {topic}: 수익률 극대화 분석"

def get_image_keywords(topic):
    print(f"🎨 [3/6] 이미지 키워드 추출 중...")
    time.sleep(1)
    prompt = f"""
    Topic: "{topic}"
    Extract 3 english keywords for stock photos.
    Keywords: luxury apartment, construction site, money graph, skyline.
    Output ONLY keywords (comma separated).
    """
    try:
        result = generate_content_with_survival(prompt)
        return result.strip().replace(" ", "")
    except:
        return "city,apartment,money"

def generate_graph(filename_base, data_dict):
    print(f"📊 [4/6] '{data_dict['unit']}' 그래프 생성 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    os.makedirs(image_dir, exist_ok=True)
    img_filename = f"{filename_base}-chart.png"
    img_path = os.path.join(image_dir, img_filename)

    years = data_dict['years']
    values = data_dict['values']
    unit = data_dict['unit']
    title = data_dict['title']
    
    # 상승장은 붉은색(Red) 계열로 강렬하게
    color = ['#ffcdd2', '#ef9a9a', '#ef5350', '#d32f2f'] 

    plt.figure(figsize=(10, 6))
    bars = plt.bar(years, values, color=color, width=0.6)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, height, 
                 f'{height}\n{unit}', 
                 ha='center', va='bottom', fontsize=12, fontweight='bold')

    plt.title(title, fontsize=16, fontweight='bold', pad=20)
    plt.ylabel(f"Unit: {unit}", fontsize=12)
    plt.grid(axis='y', linestyle='--', alpha=0.3)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    
    plt.savefig(img_path, dpi=100, bbox_inches='tight')
    plt.close()
    return f"/images/{img_filename}"

def generate_github_content(topic, viral_title, graph_url, data_dict, img_keywords):
    print(f"🤖 [5/6] 투자 리포트(수익화 버전) 작성 중...")
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
categories: ["Investment Strategy"]
tags: ["Real Estate", "ROI", "Trend"]
cover:
    image: "{cover_image}"
    alt: "{viral_title}"
    relative: false
---"""

    # 🔥 여기가 핵심: '돈이 되는' 글쓰기 프롬프트
    prompt = f"""
    Act as a Top-tier Real Estate Investment Consultant (Salary: $500k/year).
    Topic: {topic}
    Title: {viral_title}
    Data:
    {data_summary}
    
    Write a high-value investment report in Korean (Markdown).
    
    [Tone & Style]
    - Persuasive, Confident, Insightful. (Like a paid consulting report)
    - Focus on 'Money Flow', 'Undervalued Assets', 'Timing'.
    - Use specific examples of regions or apartment names (Real or Representative) to increase credibility.
    
    [Structure]
    1. **Money Flow (돈의 흐름)**: Where is the liquidity moving? Why this topic now?
    2. **Data Verification (데이터 검증)**: Analyze the chart. Prove the growth potential.
    3. **Target Spot (유망 지역/단지)**: Suggest 2-3 specific regions or apartment types that will benefit the most. (Be specific! e.g., 'Bundang Sibeom', 'GTX-A Line Yongin', etc.)
    4. **Action Plan (투자 전략)**: Buy/Hold/Sell strategy.
    
    Output ONLY Markdown body.
    """
    
    try:
        result = generate_content_with_survival(prompt)
        body = result.replace("```markdown", "").replace("```", "")
    except:
        body = "내용 생성 중 오류가 발생했습니다."
    
    full_content = f"{front_matter}\n\n![Chart]({graph_url})\n*▲ {topic} 투자 가치 분석 ({now.year} 기준)*\n\n{body}"
    return full_content

def generate_tistory_content(viral_title, github_link):
    print(f"🎨 [6/6] 티스토리 요약글 생성 중...")
    time.sleep(1)
    prompt = f"""
    Write a HTML teaser for an investment blog post about "{viral_title}".
    Language: Korean.
    Tone: Engaging, Money-focused.
    Include a button linking to: {github_link} ("투자 리포트 확인하기")
    Last line: 10 tags separated by commas.
    """
    try:
        result = generate_content_with_survival(prompt)
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
        repo.index.commit(f"Investment Report: {viral_title}")
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ 완료!")
        return f"{MAIN_DOMAIN_URL}/posts/{safe_filename.replace('.md', '')}"
    except: return MAIN_DOMAIN_URL

def save_tistory_file(viral_title, html, tags):
    draft_dir = "tistory_drafts"
    os.makedirs(draft_dir, exist_ok=True)
    filename = f"Report-{datetime.datetime.now().strftime('%H%M%S')}.txt"
    filepath = os.path.join(draft_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"제목: {viral_title}\n\n[태그]\n{tags}\n\n[HTML]\n{html}")
    try: os.system(f"open {draft_dir}")
    except: pass

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 PropTech 봇 (수익화 컨설턴트 모드)")
    print("   * 목표: 월 500만원 가치의 고품질 투자 리포트 생성")
    print("="*50)
    
    topic = input("✍️  분석할 주제 입력: ")
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