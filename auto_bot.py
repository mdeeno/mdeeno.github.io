import os
import re
import sys
import time

# ==============================================================================
# [설정] 수동 입력 파일명
# ==============================================================================
INPUT_FILE = "input.txt"
BLOG_DIR = os.getcwd() 

def parse_gem_output(text):
    print("🔍 젬(Gem) 결과물 파싱 시작...")
    
    data = {}

    # 1. 파일 경로 및 이름 추출 (단순 검색으로 변경)
    # 복잡한 정규식 대신, 단순하게 줄별로 검사해서 찾습니다.
    lines = text.split('\n')
    for line in lines:
        if "경로:" in line and "content/posts" in line:
            data['target_dir'] = line.split("경로:")[1].strip()
        if "파일명:" in line and ".md" in line:
            raw_name = line.split("파일명:")[1].strip()
            # 파일명에 _manual 자동 부착 로직
            if "_manual" not in raw_name:
                name_part, ext_part = os.path.splitext(raw_name)
                data['filename'] = f"{name_part}_manual{ext_part}"
            else:
                data['filename'] = raw_name

    # 못 찾았을 경우 기본값
    if 'target_dir' not in data:
        print("⚠️ 경로 자동 인식 실패 -> 기본값(content/posts/analysis/) 사용")
        data['target_dir'] = "content/posts/analysis/"
    
    if 'filename' not in data:
        print("⚠️ 파일명 자동 인식 실패 -> 날짜 기반 생성")
        data['filename'] = f"manual-post-{int(time.time())}_manual.md"

    # 2. 메인 블로그 포스팅 (Markdown) 추출 [알고리즘 개선]
    # 정규식 대신 '위치 기반'으로 찾습니다. (훨씬 강력함)
    
    # 시작점 찾기: 첫 번째 '---' 가 나오는 곳
    start_idx = text.find("---")
    
    # 끝점 찾기: '3단계' 라는 단어가 나오는 곳 (혹은 티스토리 HTML 시작점)
    end_idx = text.find("3단계")
    if end_idx == -1:
        # 3단계라는 말이 없으면 <div 로 시작하는 HTML 앞까지
        end_idx = text.find("<div")
        
    if start_idx != -1 and end_idx != -1:
        raw_content = text[start_idx:end_idx].strip()
        # 혹시 끝에 ``` 가 남아있으면 제거
        raw_content = raw_content.replace("```markdown", "").replace("```", "").strip()
        data['main_content'] = raw_content
        print("✅ 메인 포스팅 본문 추출 성공!")
    else:
        print("❌ 메인 포스팅 내용을 찾을 수 없습니다.")
        print(f"   (Debug: Start={start_idx}, End={end_idx})")
        return None

    # 3. 티스토리 HTML 추출
    # '3단계' 뒤에 있는 <html> 태그 찾기
    tistory_part = text[end_idx:] # 3단계 이후 텍스트만 자름
    
    html_start = tistory_part.find("<div")
    if html_start == -1: html_start = tistory_part.find("<h2")
    
    if html_start != -1:
        raw_html = tistory_part[html_start:].strip()
        # 뒤에 불필요한 텍스트(4단계 등) 자르기
        end_html = raw_html.find("4단계")
        if end_html != -1:
            raw_html = raw_html[:end_html].strip()
            
        raw_html = raw_html.replace("```html", "").replace("```", "").strip()
        data['tistory_content'] = raw_html
        print("✅ 티스토리 HTML 추출 성공!")
    else:
        data['tistory_content'] = ""
        print("⚠️ 티스토리 HTML을 찾지 못했습니다. (빈 파일 생성)")

    return data

def save_files(data):
    if not data: return

    # 1. 메인 포스팅 저장
    full_path_dir = os.path.join(BLOG_DIR, data['target_dir'])
    if not os.path.exists(full_path_dir):
        os.makedirs(full_path_dir)
    
    full_path_file = os.path.join(full_path_dir, data['filename'])
    
    with open(full_path_file, 'w', encoding='utf-8') as f:
        f.write(data['main_content'])
    print(f"🎉 [파일 생성 완료] {full_path_file}")

    # 2. 티스토리 파일 저장
    tistory_dir = os.path.join(BLOG_DIR, "tistory_drafts")
    if not os.path.exists(tistory_dir):
        os.makedirs(tistory_dir)
        
    tistory_filename = f"Tistory-{data['filename'].replace('.md', '.txt')}"
    tistory_path = os.path.join(tistory_dir, tistory_filename)
    
    with open(tistory_path, 'w', encoding='utf-8') as f:
        f.write(data['tistory_content'])
    print(f"🎉 [티스토리 완료] {tistory_path}")

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🔥 PropTech 수동 포스팅 생성기 (V13.1 강력 파싱)")
    print("="*50)
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ '{INPUT_FILE}' 파일이 없습니다.")
        with open(INPUT_FILE, 'w', encoding='utf-8') as f: f.write("")
        print(f"   👉 '{INPUT_FILE}' 생성됨. 여기에 내용을 붙여넣고 다시 실행하세요.")
        sys.exit()
        
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    parsed_data = parse_gem_output(raw_text)
    save_files(parsed_data)
    print("\n🚀 이제 'git push'만 하시면 됩니다!")