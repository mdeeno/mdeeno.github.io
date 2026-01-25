import os
import re
import sys
import time
from datetime import datetime, timedelta

# ==============================================================================
# [설정] 파일 정보
# ==============================================================================
INPUT_FILE = "input.txt"
BLOG_DIR = os.getcwd() 

def parse_gem_output(text):
    print("🔍 젬(Gem) 결과물 파싱 시작...")
    
    # 0. 젬이 출력한 텍스트에서 보이지 않는 특수문자나 불필요한 공백 제거
    text = text.strip()
    
    data = {}

    # 1. 파일 정보 추출 (정규식 유연하게 수정)
    path_match = re.search(r"경로[:\s]+([^\n\r]+)", text)
    file_match = re.search(r"파일명[:\s]+([^\n\r]+)", text)
    
    data['target_dir'] = path_match.group(1).strip() if path_match else "content/posts/analysis/"
    raw_filename = file_match.group(1).strip() if file_match else f"manual-post-{int(time.time())}.md"
    
    # 접미사 _manual 처리
    if ".md" in raw_filename and "_manual" not in raw_filename:
        name_part, ext_part = os.path.splitext(raw_filename)
        data['filename'] = f"{name_part}_manual{ext_part}"
    else:
        data['filename'] = raw_filename

    # 2. 본문 추출 (--- 기호를 기점으로 끝까지 긁기)
    # 코드 블록(```)이 있든 없든 상관없이 '---'로 시작하는 구간을 찾습니다.
    content_match = re.search(r"---.*", text, re.DOTALL)
    
    if content_match:
        raw_content = content_match.group(0).strip()
        
        # 3단계(티스토리)나 4단계(명령어)가 시작되면 그 전까지만 자름
        split_markers = ["3단계", "티스토리", "4단계", "배포 명령어", "5단계"]
        for marker in split_markers:
            if marker in raw_content:
                raw_content = raw_content.split(marker)[0].strip()
        
        # 앞뒤에 붙은 마크다운 코드 블록 표시 제거
        raw_content = raw_content.replace("```markdown", "").replace("```", "").strip()
        
        # 🔥 [서버 시차 해결] 날짜 강제 보정 (무조건 어제 날짜)
        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        # date: YYYY-MM-DD 형식을 찾아서 교체
        raw_content = re.sub(r'date:\s*\d{4}-\d{2}-\d{2}', f'date: {yesterday}', raw_content)
        
        data['main_content'] = raw_content
        print(f"✅ 본문 파싱 성공 (저장될 날짜: {yesterday})")
    else:
        print("❌ 오류: '---'로 시작하는 본문을 찾을 수 없습니다. input.txt 내용을 확인하세요.")
        return None

    # 3. 티스토리 HTML 추출
    html_match = re.search(r"(<div.*</div>|<h2.* 태그:.*)", text, re.DOTALL)
    if html_match:
        raw_html = html_match.group(1).strip()
        raw_html = raw_html.replace("```html", "").replace("```", "").strip()
        data['tistory_content'] = raw_html
    else:
        data['tistory_content'] = "티스토리 내용을 찾지 못했습니다."

    return data

def save_files(data):
    if not data: return

    # 메인 포스팅 저장
    full_path_dir = os.path.join(BLOG_DIR, data['target_dir'])
    if not os.path.exists(full_path_dir): os.makedirs(full_path_dir)
    full_path_file = os.path.join(full_path_dir, data['filename'])
    
    with open(full_path_file, 'w', encoding='utf-8') as f:
        f.write(data['main_content'])
    print(f"🎉 [블로그 생성] {full_path_file}")

    # 티스토리 저장
    tistory_dir = os.path.join(BLOG_DIR, "tistory_drafts")
    if not os.path.exists(tistory_dir): os.makedirs(tistory_dir)
    tistory_path = os.path.join(tistory_dir, f"Tistory-{data['filename'].replace('.md', '.txt')}")
    with open(tistory_path, 'w', encoding='utf-8') as f:
        f.write(data['tistory_content'])
    print(f"🎉 [티스토리 생성] {tistory_path}")

    print("\n" + "="*50)
    print("🚀 [배포 명령어]")
    print(f"git add .\ngit commit -m 'Manual Post: {data['filename']}'\ngit push origin main")
    print("="*50)

if __name__ == "__main__":
    if not os.path.exists(INPUT_FILE):
        print(f"❌ {INPUT_FILE} 파일이 없습니다.")
        sys.exit()
        
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        raw_text = f.read()
        
    if not raw_text.strip():
        print("❌ input.txt가 비어있습니다.")
        sys.exit()
        
    parsed_data = parse_gem_output(raw_text)
    save_files(parsed_data)