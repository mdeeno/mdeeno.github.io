import os
import time
import datetime
import random
import platform
import ast
import urllib.parse
import json
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

# 🚨 API 호출 절약을 위해 가장 성능 좋은 모델 하나만 집중 공략
MODEL_CANDIDATES = [
    'gemini-2.0-flash-exp',
    'gemini-2.5-flash',
]
# ==============================================================================

genai.configure(api_key=GEMINI_API_KEY)

def generate_with_backoff(prompt):
    """
    [API 절약 모드] 
    호출 횟수를 줄였으므로, 한 번 실패하면 조금 더 길게(60초) 쉽니다.
    """
    for model_name in MODEL_CANDIDATES:
        try:
            model = genai.GenerativeModel(model_name)
            # JSON 응답을 강제하기 위한 설정
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            error_msg = str(e)
            if "429" in error_msg or "Resource exhausted" in error_msg:
                print(f"   ⏳ [서버 과부하] {model_name} 대기 중... (60초 휴식)")
                time.sleep(60)
                try:
                    print(f"   🔄 [재시도] 다시 시도합니다...")
                    response = model.generate_content(prompt)
                    return response.text
                except:
                    continue
            continue
    return None

def set_korean_font():
    if platform.system() == "Darwin":
        try:
            rc('font', family='AppleGothic')
            plt.rcParams['axes.unicode_minus'] = False 
        except: pass

def get_all_metadata_at_once(topic):
    """
    🔥 [핵심] 4번의 질문을 1번으로 압축합니다.
    (데이터, 제목, 이미지 프롬프트, 티스토리 요약을 한 방에 받음)
    """
    print(f"🧠 [1/3] '{topic}' 기획안 작성 중 (통합 API 호출)...")
    current_year = datetime.datetime.now().year
    
    prompt = f"""
    Act as a Real Estate Expert. Analyze the topic: "{topic}".
    
    Return a JSON object containing ALL the following information:
    1. "roi_data": Trend data (2023-{current_year+1}) with years, values(index/roi), unit, title.
    2. "viral_title": A click-bait style Korean title about Profit/ROI.
    3. "image_keywords": 2 English prompts (1 for cover: city/construction, 1 for mid-content: blueprint/graph).
    4. "tistory_teaser": A HTML summary (3 bullet points + call to action).
    
    Output Format (JSON Only):
    {{
        "roi_data": {{
            "years": ["2023", "2024", "2025", "2026"],
            "values": [10, 20, 30, 40],
            "unit": "ROI(%)",
            "title": "Title Here"
        }},
        "viral_title": "Korean Title Here",
        "image_keywords": ["Cover Prompt English", "Mid Prompt English"],
        "tistory_teaser": "<h3>Title</h3><ul><li>Point 1</li><li>Point 2</li></ul>..."
    }}
    NO MARKDOWN. JUST JSON STRING.
    """
    
    result = generate_with_backoff(prompt)
    
    # 실패 시 기본값 (프로그램 죽음 방지)
    default_data = {
        "roi_data": {
            "years": ["2023", "2024", "2025", "2026"],
            "values": [100, 110, 120, 130],
            "unit": "Index",
            "title": f"{topic} 전망"
        },
        "viral_title": f"[투자분석] {topic}: 심층 분석 리포트",
        "image_keywords": ["modern city skyline", "architectural blueprint"],
        "tistory_teaser": f"<h3>{topic} 분석</h3><p>상세 내용은 블로그에서 확인하세요.</p>"
    }

    if not result:
        print("⚠️ API 호출 실패. 기본값을 사용합니다.")
        return default_data

    try:
        clean_json = result.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean_json)
        return data
    except Exception as e:
        print(f"⚠️ JSON 파싱 실패({e}). 기본값을 사용합니다.")
        return default_data

def generate_graph(filename_base, data_dict):
    print(f"📊 [2/3] 그래프 생성 중 (로컬 작업)...")
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

def generate_blog_post(topic, metadata, graph_url):
    print(f"🤖 [3/3] 본문 작성 중 (2번째 API 호출)...")
    
    # 60초 강제 휴식 (연속 호출 방지)
    print("   ⏳ 안전한 API 사용을 위해 30초 대기합니다...")
    time.sleep(30)

    viral_title = metadata['viral_title']
    roi_data = metadata['roi_data']
    img_prompts = metadata['image_keywords']
    
    # 이미지 URL 생성
    encoded_cover = urllib.parse.quote(img_prompts[0])
    encoded_mid = urllib.parse.quote(img_prompts[1]) if len(img_prompts) > 1 else urllib.parse.quote("architecture")
    
    cover_image = f"https://image.pollinations.ai/prompt/{encoded_cover}?width=1600&height=900&nologo=true"
    mid_image_url = f"https://image.pollinations.ai/prompt/{encoded_mid}?width=800&height=500&nologo=true"

    now = datetime.datetime.now()
    data_summary = f"Trends: {roi_data['years']} -> {roi_data['values']}"

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
    Act as a Real Estate Consultant. Topic: {topic}
    Title: {viral_title}
    Data: {data_summary}
    Mid-Image: {mid_image_url}
    
    Write a high-quality blog post in Korean (Markdown).
    
    [Rules]
    1. Insert `{mid_image_url}` between Section 2 and 3.
    2. Use search links: `[👉 네이버 부동산 시세 확인](https://search.naver.com/search.naver?query={topic}+시세)`
    3. Structure: Money Flow -> Data Verification -> Target Spot -> Action Plan.
    
    Output ONLY Markdown body.
    """
    
    result = generate_with_backoff(prompt)
    
    if not result:
        body = "⚠️ 내용 생성에 실패했습니다. (API 한도 초과). 나중에 다시 시도해주세요."
    else:
        body = result.replace("```markdown", "").replace("```", "")

    return f"{front_matter}\n\n![Chart]({graph_url})\n*▲ {topic} 데이터 분석 ({now.year} 기준)*\n\n{body}"

def deploy_to_github(viral_title, content):
    print(f"🚀 배포 및 저장 중...") 
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
        print("✅ 깃허브 배포 완료!")
        return f"{MAIN_DOMAIN_URL}/posts/{safe_filename.replace('.md', '')}"
    except Exception as e:
        print(f"❌ 깃허브 배포 실패: {e}")
        return MAIN_DOMAIN_URL

def save_tistory_file(viral_title, html_content):
    draft_dir = "tistory_drafts"
    os.makedirs(draft_dir, exist_ok=True)
    filename = f"Report-{datetime.datetime.now().strftime('%H%M%S')}.txt"
    filepath = os.path.join(draft_dir, filename)
    
    # 링크 버튼 추가
    final_html = html_content
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(f"제목: {viral_title}\n\n[HTML 소스]\n{final_html}")
    try: os.system(f"open {draft_dir}")
    except: pass

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 PropTech 봇 (API 절약형 통합 모드)")
    print("   * 5번 질문할 것을 2번으로 줄여서 차단을 방지합니다.")
    print("="*50)
    
    topic = input("✍️  분석할 주제 입력: ")
    if topic:
        # 1. 통합 메타데이터 생성 (1번 호출)
        metadata = get_all_metadata_at_once(topic)
        
        # 2. 그래프 생성 (API 안 씀)
        graph_url = generate_graph("chart", metadata['roi_data'])
        
        # 3. 본문 생성 (2번 호출)
        full_content = generate_blog_post(topic, metadata, graph_url)
        
        # 4. 배포
        post_link = deploy_to_github(metadata['viral_title'], full_content)
        
        # 5. 티스토리 파일 저장 (이미 1번 단계에서 만들었음)
        # 링크만 업데이트해서 저장
        final_teaser = metadata['tistory_teaser'] + f'\n<br><a href="{post_link}" style="background:blue;color:white;padding:10px;">👉 리포트 전문 보기</a>'
        save_tistory_file(metadata['viral_title'], final_teaser)
        
        print("\n🎉 모든 작업이 완료되었습니다!")
    else:
        print("❌ 실행을 중단합니다.")