import os
import time
import datetime
import random
import platform
import ast
import urllib.parse # URL 인코딩용 추가
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

def get_image_prompts(topic):
    """
    [핵심 변경] 단순 키워드가 아니라, AI 그림 생성용 '영어 묘사(Prompt)'를 만듭니다.
    """
    print(f"🎨 [3/6] AI 이미지 생성 프롬프트 작성 중...")
    time.sleep(1)
    prompt = f"""
    Topic: "{topic}"
    Create 2 detailed English image prompts for an AI image generator.
    
    1. Cover Image: A wide, cinematic shot of a modern futuristic city skyline or construction site, golden hour lighting, photorealistic, 8k.
    2. Mid Image: A close-up of a modern apartment complex or architectural blueprint plan on a desk, professional photography style.
    
    Output Format (Comma separated):
    Prompt1, Prompt2
    """
    try:
        result = generate_content_with_survival(prompt)
        prompts = result.split(',')
        if len(prompts) >= 2:
            return prompts[0].strip(), prompts[1].strip()
        else:
            return "modern city skyline photorealistic", "modern architecture blueprint photorealistic"
    except:
        return "modern city skyline photorealistic", "modern architecture blueprint photorealistic"

def generate_graph(filename_base, data_dict):
    print(f"📊 [4/6] '{data_dict['unit']}' 그래프 생성 중...")
    set_korean_font()
    
    image_dir = os.path.join(BLOG_DIR, "static", "images")
    if not os.path.exists(image_dir):
        os.makedirs(image_dir)
        
    img_filename = f"{filename_base}-{int(time.time())}.png"
    img_path = os.path.join(image_dir, img_filename)

    years = data_dict['years']
    values = data_dict['values']
    unit = data_dict['unit']
    title = data_dict['title']
    
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

def generate_github_content(topic, viral_title, graph_url, data_dict, cover_prompt, mid_prompt):
    print(f"🤖 [5/6] 투자 리포트(AI 이미지 적용) 작성 중...")
    time.sleep(1)
    now = datetime.datetime.now()
    
    data_summary = ""
    for y, v in zip(data_dict['years'], data_dict['values']):
        data_summary += f"- **{y}**: {v}{data_dict['unit']}\n"

    # 🔥 [핵심] Pollinations AI를 사용하여 '그려낸' 이미지 URL 생성
    # 프롬프트를 URL 인코딩하여 주소로 만듭니다.
    encoded_cover = urllib.parse.quote(cover_prompt)
    encoded_mid = urllib.parse.quote(mid_prompt)
    
    cover_image = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){encoded_cover}?width=1600&height=900&nologo=true"
    mid_image_url = f"[https://image.pollinations.ai/prompt/](https://image.pollinations.ai/prompt/){encoded_mid}?width=800&height=500&nologo=true"

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

    prompt = f"""
    Act as a Top-tier Real Estate Investment Consultant.
    Topic: {topic}
    Title: {viral_title}
    Data: {data_summary}
    Mid-Content Image URL: {mid_image_url}
    
    Write a high-value investment report in Korean (Markdown).
    
    [VISUAL INSTRUCTION]
    - You MUST insert the 'Mid-Content Image URL' provided above exactly BETWEEN 'Section 2. Data Verification' and 'Section 3. Target Spot'.
    - Use this markdown format: `\n\n![현장 분석 이미지]({mid_image_url})\n*▲ {topic} 관련 현장 및 인프라 시뮬레이션*\n\n`
    
    [CRITICAL RULES FOR LINKS]
    1. NEVER invent specific URLs for apartments.
    2. Use 'Search Query Links': `[👉 (Name) 네이버 부동산 시세 확인](https://search.naver.com/search.naver?query=(Name)+부동산+시세)`
    
    [Formatting]
    1. Short Paragraphs (Mobile optimization).
    2. Use Blockquotes (`>`) for key insights.
    
    [Structure]
    1. **Money Flow**
    2. **Data Verification**
    3. **Target Spot** (Suggest 2-3 specific regions)
    4. **Action Plan**
    
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
        print("✅ 완료! (고양이 동상은 이제 안녕! 👋)")
        return f"{MAIN_DOMAIN_URL}/posts/{safe_filename.replace('.md', '')}"
    except Exception as e:
        print(f"❌ 배포 실패: {e}")
        return MAIN_DOMAIN_URL

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
    print("🔥 PropTech 봇 (AI 이미지 생성 버전)")
    print("   * 더 이상 랜덤 이미지가 아닙니다.")
    print("   * 주제에 맞는 '그림'을 AI가 직접 그립니다.")
    print("="*50)
    
    topic = input("✍️  분석할 주제 입력: ")
    if topic:
        data_dict = get_real_data_from_llm(topic)
        viral_title = generate_viral_title(topic)
        # 이미지 키워드 대신 '프롬프트(묘사)'를 가져옵니다
        cover_prompt, mid_prompt = get_image_prompts(topic)
        
        graph_url = generate_graph("chart", data_dict)
        git_content = generate_github_content(topic, viral_title, graph_url, data_dict, cover_prompt, mid_prompt)
        link = deploy_to_github(viral_title, git_content)
        html, tags = generate_tistory_content(viral_title, link)
        save_tistory_file(viral_title, html, tags)
    else:
        print("❌ 실행을 중단합니다.")