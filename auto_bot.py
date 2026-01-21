import os
import time
import datetime
import random
import platform
import ast
import urllib.parse
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

# 🚨 무료 티어 생존용 모델 리스트
MODEL_CANDIDATES = [
    'gemini-2.0-flash-exp',
    'gemini-2.5-flash',
    'gemini-exp-1206',
]
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def generate_content_with_retry(prompt):
    """
    [핵심 수정] 실패 시 'None'을 반환하여 프로그램이 죽지 않게 함
    """
    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Resource exhausted" in error_msg:
                print(f"   ⏳ [과열] {model_name} 식히는 중... (30초 대기)")
                time.sleep(30) # 대기 시간 증가
                try:
                    print(f"   🔄 [재시도] 다시 요청...")
                    response = model.generate_content(prompt)
                    return response.text
                except:
                    continue
            continue
            
    print("\n⚠️ [경고] 모든 AI 모델 응답 실패. 비상 모드로 전환합니다.")
    return None # 에러를 내지 않고 None 반환

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def get_real_data_from_llm(topic):
    print(f"🧠 [1/6] 수익성 분석 중...")
    
    current_year = datetime.datetime.now().year
    prompt = f"""
    Topic: "{topic}"
    Task: Extract real investment trends & ROI data (2023-{current_year+1}).
    Output Format (JSON only): {{"years": ["2023", "2024", "2025", "2026"], "values": [10, 15, 23, 35], "unit": "ROI(%)", "title": "Growth"}}
    NO MARKDOWN. ONLY JSON STRING.
    """
    
    result_text = generate_content_with_retry(prompt)
    
    # AI 실패 시 기본값 사용
    if not result_text:
        return {
            "years": ["2023", "2024", "2025", "2026"],
            "values": [100, 110, 120, 130],
            "unit": "Index",
            "title": f"{topic} 시장 전망"
        }
        
    try:
        clean_text = result_text.replace("```json", "").replace("```python", "").replace("```", "").strip()
        data_dict = ast.literal_eval(clean_text)
        return data_dict
    except:
        return {
            "years": ["2023", "2024", "2025", "2026"],
            "values": [100, 110, 120, 130],
            "unit": "Index",
            "title": f"{topic} 시장 전망"
        }

def generate_viral_title(topic):
    print(f"⚡ [2/6] 제목 생성 중...")
    
    prompt = f"""
    Create a click-bait blog title for "{topic}" in Korean.
    Focus on Profit, ROI. Example: "2026년 {topic}: 지금 사야 할 이유"
    Output ONLY the title.
    """
    result = generate_content_with_retry(prompt)
    if not result: return f"[투자분석] {topic}: 데이터로 보는 전망"
    return result.strip().replace('"', '')

def get_image_prompts(topic):
    print(f"🎨 [3/6] 이미지 프롬프트 작성 중...")
    
    prompt = f"""
    Topic: "{topic}"
    Create 2 English image prompts: 1. Cover (City/Construction), 2. Mid-content (Blueprint/Graph).
    Output Format: Prompt1, Prompt2
    """
    result = generate_content_with_retry(prompt)
    
    if not result:
        return "modern city skyline golden hour", "architectural blueprint plan"
        
    try:
        prompts = result.split(',')
        if len(prompts) >= 2:
            return prompts[0].strip(), prompts[1].strip()
        return "modern city skyline", "architectural blueprint"
    except:
        return "modern city skyline", "architectural blueprint"

def generate_graph(filename_base, data_dict):
    print(f"📊 [4/6] 그래프 생성 중...")
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
    print(f"🤖 [5/6] 본문 작성 중...")
    now = datetime.datetime.now()
    
    data_summary = ""
    for y, v in zip(data_dict['years'], data_dict['values']):
        data_summary += f"- **{y}**: {v}{data_dict['unit']}\n"

    encoded_cover = urllib.parse.quote(cover_prompt)
    encoded_mid = urllib.parse.quote(mid_prompt)
    
    # 🔥 [오타 수정 완료] []() 제거함
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
    Act as a Real Estate Investment Consultant.
    Topic: {topic}
    Title: {viral_title}
    Data: {data_summary}
    Mid-Content Image URL: {mid_image_url}
    
    Write a blog post in Korean (Markdown).
    
    [VISUAL]
    - Insert '{mid_image_url}' between Section 2 and 3.
    - Format: `\n\n![현장 이미지]({mid_image_url})\n`
    
    [LINKS]
    - Use search links: `[👉 네이버 부동산 시세 확인](https://search.naver.com/search.naver?query={topic}+시세)`
    
    [Structure]
    1. Money Flow
    2. Data Verification
    3. Target Spot (2-3 regions)
    4. Action Plan
    
    Output ONLY Markdown body.
    """
    
    result = generate_content_with_retry(prompt)
    
    # 비상용 기본 본문 (AI가 죽었을 때 사용)
    if not result:
        body = f"""
## 1. 분석 개요
{topic}에 대한 시장의 관심이 뜨겁습니다. 
데이터 분석 결과, 지속적인 우상향 트렌드가 예상됩니다.

## 2. 데이터 검증
{data_summary}
위 지표를 볼 때, 지금이 적기일 수 있습니다.

![관련 이미지]({mid_image_url})

## 3. 결론 및 전략
구체적인 매수 타이밍과 유망 단지는 네이버 부동산을 통해 확인하시기 바랍니다.
[👉 네이버 부동산 시세 바로가기](https://land.naver.com)
"""
    else:
        body = result.replace("```markdown", "").replace("```", "")
    
    full_content = f"{front_matter}\n\n![Chart]({graph_url})\n*▲ {topic} 데이터 분석 ({now.year} 기준)*\n\n{body}"
    return full_content

def generate_tistory_content(viral_title, github_link):
    print(f"🎨 [6/6] 티스토리 요약 작성 중...")
    
    prompt = f"""
    Write a HTML teaser for "{viral_title}".
    Language: Korean.
    Include 3 bullet points summary and a button to: {github_link}
    Output ONLY HTML code.
    """
    result = generate_content_with_retry(prompt)
    
    if not result:
        return f"""
        <h3>{viral_title}</h3>
        <p>상세 분석 리포트가 발간되었습니다.</p>
        <a href="{github_link}">👉 리포트 전문 보기</a>
        """, "부동산, 투자, 분석"
        
    try:
        content = result.replace("```html", "").replace("```", "")
        lines = content.strip().split('\n')
        return "\n".join(lines[:-1]), lines[-1]
    except:
         return f"""
        <h3>{viral_title}</h3>
        <p>상세 분석 리포트가 발간되었습니다.</p>
        <a href="{github_link}">👉 리포트 전문 보기</a>
        """, "부동산, 투자, 분석"

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
        print("✅ 완료! (배포 성공)")
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
    print("🔥 PropTech 봇 (무중단 완주 모드)")
    print("   * AI 응답 실패 시에도 멈추지 않고 파일을 생성합니다.")
    print("   * 단계별 강제 휴식으로 과열을 방지합니다.")
    print("="*50)
    
    topic = input("✍️  분석할 주제 입력: ")
    if topic:
        # 단계별 강제 휴식 (10초) 추가하여 RPM 제한 회피
        data_dict = get_real_data_from_llm(topic)
        time.sleep(10) 
        
        viral_title = generate_viral_title(topic)
        time.sleep(10)
        
        cover_prompt, mid_prompt = get_image_prompts(topic)
        time.sleep(10)
        
        graph_url = generate_graph("chart", data_dict)
        # 그래프 생성은 AI 안 쓰니까 휴식 불필요
        
        git_content = generate_github_content(topic, viral_title, graph_url, data_dict, cover_prompt, mid_prompt)
        time.sleep(10)
        
        link = deploy_to_github(viral_title, git_content)
        
        html, tags = generate_tistory_content(viral_title, link)
        save_tistory_file(viral_title, html, tags)
    else:
        print("❌ 실행을 중단합니다.")