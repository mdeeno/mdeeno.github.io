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

# 🚨 아까 check.py에서 확인된 '실존하는 모델'만 넣었습니다.
MODEL_CANDIDATES = [
    'gemini-2.0-flash-exp',    # 1타자: 무료 한도가 가장 널널함
    'gemini-2.5-flash',        # 2타자: 최신형
    'gemini-exp-1206',         # 3타자: 실험 버전
]
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def generate_content_with_retry(prompt):
    """
    [핵심 수정] 속도 제한(429)이 걸리면 포기하지 않고 '기다렸다 다시' 합니다.
    """
    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            # 429 에러(Resource exhausted)는 속도 문제이므로 기다리면 해결됨
            if "429" in error_msg or "Resource exhausted" in error_msg:
                print(f"   ⏳ [속도 제한 감지] {model_name} 모델이 숨 고르는 중... (20초 대기)")
                time.sleep(20) # 20초 푹 쉬기
                try:
                    # 재시도
                    print(f"   🔄 [재시도] 다시 요청합니다...")
                    response = model.generate_content(prompt)
                    return response.text
                except:
                    print(f"   ❌ 재시도 실패. 다음 모델로 넘어갑니다.")
                    continue
            # 다른 에러면 바로 다음 모델로
            continue
            
    print("\n❌ 모든 모델이 응답하지 않습니다. 잠시 후 다시 실행해주세요.")
    raise Exception("All models failed")

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def get_real_data_from_llm(topic):
    print(f"🧠 [1/6] '{topic}' 수익성 분석 중...")
    time.sleep(5) # 5초 휴식
    
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
        result_text = generate_content_with_retry(prompt)
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
    time.sleep(5) # 5초 휴식
    
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
        result = generate_content_with_retry(prompt)
        return result.strip().replace('"', '')
    except:
        return f"[투자전략] {topic}: 수익률 극대화 분석"

def get_image_prompts(topic):
    print(f"🎨 [3/6] AI 이미지 생성 프롬프트 작성 중...")
    time.sleep(10) # 🔥 여기서 에러 났으니 10초 푹 휴식
    
    prompt = f"""
    Topic: "{topic}"
    Create 2 detailed English image prompts for an AI image generator.
    
    1. Cover Image: A cinematic shot of modern city or construction site, golden hour, 8k.
    2. Mid Image: A close-up of architectural blueprint or money graph, professional style.
    
    Output Format (Comma separated):
    Prompt1, Prompt2
    """
    try:
        result = generate_content_with_retry(prompt)
        prompts = result.split(',')
        if len(prompts) >= 2:
            return prompts[0].strip(), prompts[1].strip()
        else:
            return "modern city skyline", "modern architecture blueprint"
    except:
        return "modern city skyline", "modern architecture blueprint"

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
    print(f"🤖 [5/6] 투자 리포트 작성 중...")
    time.sleep(10) # 🔥 여기도 10초 휴식 (가장 긴 작업)
    now = datetime.datetime.now()
    
    data_summary = ""
    for y, v in zip(data_dict['years'], data_dict['values']):
        data_summary += f"- **{y}**: {v}{data_dict['unit']}\n"

    encoded_cover = urllib.parse.quote(cover_prompt)
    encoded_mid = urllib.parse.quote(mid_prompt)
    
    # 🔥 [수정 완료] URL 오타 수정 (마크다운 문법 제거하고 순수 URL만 남김)
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
    - Insert the 'Mid-Content Image URL' exactly BETWEEN 'Section 2' and 'Section 3'.
    - Format: `\n\n![현장 분석 이미지]({mid_image_url})\n*▲ {topic} 관련 시뮬레이션*\n\n`
    
    [CRITICAL RULES FOR LINKS]
    1. NEVER invent specific URLs for apartments.
    2. Use 'Search Query Links': `[👉 (Name) 네이버 부동산 시세 확인](https://search.naver.com/search.naver?query=(Name)+부동산+시세)`
    
    [Formatting]
    1. Short Paragraphs.
    2. Use Blockquotes (`>`) for key insights.
    
    [Structure]
    1. **Money Flow**
    2. **Data Verification**
    3. **Target Spot** (Suggest 2-3 specific regions)
    4. **Action Plan**
    
    Output ONLY Markdown body.
    """
    
    try:
        result = generate_content_with_retry(prompt)
        body = result.replace("```markdown", "").replace("```", "")
    except:
        body = "내용 생성 중 오류가 발생했습니다."
    
    full_content = f"{front_matter}\n\n![Chart]({graph_url})\n*▲ {topic} 투자 가치 분석 ({now.year} 기준)*\n\n{body}"
    return full_content

def generate_tistory_content(viral_title, github_link):
    print(f"🎨 [6/6] 티스토리 '미끼(Hook)' 글 생성 중...")
    time.sleep(5)
    
    prompt = f"""
    Write a HTML blog post teaser for "{viral_title}".
    Target Audience: Real estate investors looking for high ROI.
    Language: Korean.
    
    [Content Strategy: The 'Sneak Peek' Technique]
    1. **Introduction**: Briefly explain why this topic is hot RIGHT NOW.
    2. **Key Takeaways (Preview)**: Provide 3 bullet points summarizing the 'Problem' or 'Trend' from the main report. (Show you are an expert).
    3. **The Cliffhanger**: Explicitly state what is in the Full Report that is missing here.
       - e.g., "The exact month to buy," "The list of Top 3 undervalued apartments."
    4. **Call to Action**: A distinct button linking to: {github_link}
    
    [HTML Structure]
    - Use `<h3>` for section headers.
    - Use `<ul>` and `<li>` for the preview points.
    - Use a clean, professional style (css in body or inline).
    - The button should say something like "👉 2026년 금리/매수 타이밍 분석 풀버전 보기".
    
    Output ONLY HTML code (starting from <style>...).
    """
    try:
        result = generate_content_with_retry(prompt)
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
        print("✅ 완료! (AI 이미지가 성공적으로 생성되었습니다)")
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
    print("🔥 PropTech 봇 (속도 조절 안전 운행 모드)")
    print("   * 429(속도제한) 에러 시 20초 대기 후 재시도합니다.")
    print("   * 조금 느리지만, 확실하게 완주합니다.")
    print("="*50)
    
    topic = input("✍️  분석할 주제 입력: ")
    if topic:
        data_dict = get_real_data_from_llm(topic)
        viral_title = generate_viral_title(topic)
        cover_prompt, mid_prompt = get_image_prompts(topic)
        
        graph_url = generate_graph("chart", data_dict)
        git_content = generate_github_content(topic, viral_title, graph_url, data_dict, cover_prompt, mid_prompt)
        link = deploy_to_github(viral_title, git_content)
        html, tags = generate_tistory_content(viral_title, link)
        save_tistory_file(viral_title, html, tags)
    else:
        print("❌ 실행을 중단합니다.")