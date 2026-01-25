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

    # 1. 파일 경로 및 이름 추출
    lines = text.split('\n')
    for line in lines:
        if "경로:" in line and "content/posts" in line:
            data['target_dir'] = line.split("경로:")[1].strip()
        if "파일명:" in line and ".md" in line:
            raw_name = line.split("파일명:")[1].strip()
            if "_manual" not in raw_name:
                name_part, ext_part = os.path.splitext(raw_name)
                data['filename'] = f"{name_part}_manual{ext_part}"
            else:
                data['filename'] = raw_name

    if 'target_dir' not in data:
        print("⚠️ 경로 자동 인식 실패 -> 기본값(content/posts/analysis/) 사용")
        data['target_dir'] = "content/posts/analysis/"
    
    if 'filename' not in data:
        data['filename'] = f"manual-post-{int(time.time())}_manual.md"

    # 2. 메인 블로그 포스팅 (Markdown) 추출
    # 유연한 파싱: '---' 시작점부터 '3단계' 전까지 추출
    start_idx = text.find("---")
    
    # 끝점 찾기 우선순위: 3단계 -> 티스토리 HTML 시작점
    end_idx = text.find("3단계")
    if end_idx == -1: 
        end_idx = text.find("<div") # 3단계 텍스트가 없을 경우 대비
        
    if start_idx != -1 and end_idx != -1:
        raw_content = text[start_idx:end_idx].strip()
        # 코드블록 기호 제거
        raw_content = raw_content.replace("```markdown", "").replace("```", "").strip()
        data['main_content'] = raw_content
        print("✅ 메인 포스팅 본문 추출 성공!")
    else:
        print("❌ 메인 포스팅 내용을 찾을 수 없습니다.")
        return None

    # 3. 티스토리 HTML 추출
    tistory_part = text[end_idx:] 
    html_start = tistory_part.find("<div")
    if html_start == -1: html_start = tistory_part.find("<h2")
    
    if html_start != -1:
        raw_html = tistory_part[html_start:].strip()
        # '4단계' 혹은 '5단계' 전까지만 자르기
        end_html = raw_html.find("4단계")
        if end_html == -1: end_html = raw_html.find("5단계")
        
        if end_html != -1: raw_html = raw_html[:end_html].strip()
        
        raw_html = raw_html.replace("```html", "").replace("```", "").strip()
        data['tistory_content'] = raw_html
        print("✅ 티스토리 HTML 추출 성공!")
    else:
        data['tistory_content'] = ""
        print("⚠️ 티스토리 HTML을 찾지 못했습니다.")

    # 4. 배포 명령어 추출 (5단계)
    cmd_start = text.find("git add")
    if cmd_start != -1:
        cmd_text = text[cmd_start:].strip()
        cmd_text = cmd_text.replace("```bash", "").replace("```", "").strip()
        data['git_command'] = cmd_text
    else:
        # 젬이 명령어를 안 줬을 경우 기본값
        data['git_command'] = 'git add .\ngit commit -m "New Manual Post"\ngit push origin main'

    return data

def save_files(data):
    if not data: return

    # 메인 포스팅 저장
    full_path_dir = os.path.join(BLOG_DIR, data['target_dir'])
    if not os.path.exists(full_path_dir): os.makedirs(full_path_dir)
    full_path_file = os.path.join(full_path_dir, data['filename'])
    with open(full_path_file, 'w', encoding='utf-8') as f: f.write(data['main_content'])
    print(f"🎉 [메인 생성] {full_path_file}")

    # 티스토리 저장
    tistory_dir = os.path.join(BLOG_DIR, "tistory_drafts")
    if not os.path.exists(tistory_dir): os.makedirs(tistory_dir)
    tistory_filename = f"Tistory-{data['filename'].replace('.md', '.txt')}"
    tistory_path = os.path.join(tistory_dir, tistory_filename)
    with open(tistory_path, 'w', encoding='utf-8') as f: f.write(data['tistory_content'])
    print(f"🎉 [티스토리 생성] {tistory_path}")

    # 🔥 [명령어 출력] 사용자 편의 기능
    print("\n" + "="*50)
    print("🚀 [배포 준비 완료] 아래 명령어를 복사해서 실행하세요!")
    print("="*50)
    print(f"\033[92m{data.get('git_command')}\033[0m") # 초록색 출력
    print("="*50 + "\n")

if __name__ == "__main__":
    print("\n🔥 PropTech 수동 포스팅 생성기 (V13.2 Final)")
    
    if not os.path.exists(INPUT_FILE):
        print(f"❌ '{INPUT_FILE}' 파일이 없습니다.")
        with open(INPUT_FILE, 'w', encoding='utf-8') as f: f.write("")
        print(f"   👉 '{INPUT_FILE}' 생성됨. 젬 결과를 붙여넣고 다시 실행하세요.")
        sys.exit()
        
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    parsed_data = parse_gem_output(raw_text)
    save_files(parsed_data)