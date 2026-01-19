import os
import time
import datetime
import google.generativeai as genai
import pyperclip
from git import Repo
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains # <--- 여기 수정됨!

# ==============================================================================
# [설정 영역]
# ==============================================================================
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
BLOG_DIR = os.getenv("BLOG_DIR")
TISTORY_WRITE_URL = os.getenv("TISTORY_WRITE_URL")
MAIN_DOMAIN_URL = "https://tech.mdeeno.com"
# ==============================================================================

# Gemini 설정
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-latest')

def generate_full_post(topic):
    """[깃허브용] 전문가 분석 글 작성 (Markdown)"""
    print(f"🤖 [1/4] '{topic}' 심층 분석 중... (Gemini가 글 쓰는 중)")
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    
    prompt = f"""
    당신은 도시공학 석사 출신의 프롭테크 전문가입니다.
    주제 '{topic}'에 대해 전문적인 기술 블로그 글을 Markdown 형식으로 작성해 주세요.
    
    [작성 조건]
    1. 맨 위에 아래 Front Matter를 반드시 포함하세요.
    ---
    title: "{topic}"
    date: {today}
    draft: false
    categories: ["PropTech", "Urban Planning"]
    ---
    2. 서론 - 본론(소제목 ## 사용) - 결론 - 3줄 요약 구조로 작성하세요.
    3. 구체적인 수치나 예시를 들어 전문성을 보여주세요.
    4. 글자 수는 공백 포함 2000자 이상으로 풍부하게 작성하세요.
    """
    response = model.generate_content(prompt)
    return response.text.replace("```markdown", "").replace("```", "")

def generate_summary_post(topic, link):
    """[티스토리용] 요약 및 유입 글 작성 (HTML)"""
    print(f"🤖 [2/4] 티스토리용 요약본 작성 중...")
    
    prompt = f"""
    주제 '{topic}'에 대해 티스토리 블로그 독자를 위한 '핵심 요약' 글을 HTML 형식으로 작성해 주세요.
    
    [작성 조건]
    1. 흥미로운 제목과 서론으로 시작하세요.
    2. 핵심 내용 3가지를 <ul>, <li> 태그로 요약하세요.
    3. 글의 마지막에 아래 내용을 포함하여 깃허브 블로그로 유도하는 버튼을 만드세요.
       - 멘트: "더 자세한 데이터 분석과 그래프는 제 기술 블로그에서 확인하실 수 있습니다."
       - 버튼 코드: 
       <div style="text-align: center; margin: 30px 0;">
           <a href="{link}" target="_blank" style="background-color: #333; color: white; padding: 15px 30px; text-decoration: none; border-radius: 10px; font-weight: bold; font-size: 16px;">📊 [전문 분석 리포트 보러가기]</a>
       </div>
    4. 전체 내용을 <div> 태그 하나로 감싸주세요.
    """
    response = model.generate_content(prompt)
    return response.text.replace("```html", "").replace("```", "")

def deploy_to_github(topic, content):
    """깃허브 배포 및 URL 반환"""
    print(f"🚀 [3/4] 깃허브(2호점)에 글 업로드 중...")
    
    safe_title = topic.replace(" ", "-").replace("?", "").replace("/", "")
    filename = f"{datetime.datetime.now().strftime('%Y-%m-%d')}-{safe_title}.md"
    filepath = os.path.join(BLOG_DIR, "content", "posts", filename)
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
        
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add('--all')
        repo.index.commit(f"New Post: {topic}")
        origin = repo.remote(name='origin')
        origin.push()
        print("✅ 깃허브 배포 성공!")
        post_url = f"{MAIN_DOMAIN_URL}/posts/{filename.replace('.md', '').lower()}"
        return post_url
    except Exception as e:
        print(f"❌ Git 배포 중 오류 발생: {e}")
        return MAIN_DOMAIN_URL

def post_to_tistory(topic, html_content):
    """티스토리 자동 발행 (맥북 크롬 제어)"""
    print(f"🌏 [4/4] 티스토리(본점)에 요약글 발행 준비...")
    
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        print("❌ 실행된 크롬을 찾을 수 없습니다! 터미널에서 크롬을 디버깅 모드로 먼저 켜주세요.")
        return

    print("   -> 티스토리 에디터로 이동합니다.")
    driver.get(TISTORY_WRITE_URL)
    time.sleep(5)

    try:
        title_area = driver.switch_to.active_element
        title_area.send_keys(f"[도시공학 이슈] {topic} (핵심 요약)")
        time.sleep(1)
    except:
        print("⚠️ 제목 입력 실패 (직접 입력해주세요)")

    try:
        pyperclip.copy(html_content)
        actions = ActionChains(driver)
        actions.key_down(Keys.TAB).key_up(Keys.TAB).perform()
        time.sleep(1)
        actions.key_down(Keys.COMMAND).send_keys('v').key_up(Keys.COMMAND).perform()
        print("🎉 작성 완료! 티스토리 화면에서 내용을 확인하고 '발행' 버튼을 눌러주세요.")
        
    except Exception as e:
        print(f"❌ 본문 입력 오류: {e}")

if __name__ == "__main__":
    print("="*50)
    print("🏗️  PropTech 블로그 자동화 시스템 가동")
    print("="*50)
    
    topic = input("✍️  오늘의 블로그 주제를 입력하세요: ")
    
    if topic:
        full_content = generate_full_post(topic)
        post_url = deploy_to_github(topic, full_content)
        print(f"🔗 깃허브 글 링크 생성됨: {post_url}")
        
        summary_html = generate_summary_post(topic, post_url)
        post_to_tistory(topic, summary_html)
    else:
        print("❌ 주제가 입력되지 않았습니다.")