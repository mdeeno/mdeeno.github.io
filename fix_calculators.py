import os
import re # 정규표현식 모듈 추가

base_dir = "content/calculators"

def fix_files():
    if not os.path.exists(base_dir):
        print(f"❌ '{base_dir}' 폴더를 찾을 수 없습니다.")
        return

    print(f"🛠️ 계산기 파일 강력 수정 시작... ({base_dir})")
    
    files = os.listdir(base_dir)
    count = 0
    
    for filename in files:
        if filename.endswith(".md") and filename != "_index.md":
            filepath = os.path.join(base_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            new_lines = []
            modified = False
            
            for line in lines:
                # 🔥 수정된 부분: 작은따옴표('), 큰따옴표(") 모두 잡아냄
                if re.search(r'layout:\s*[\'"]page[\'"]', line):
                    modified = True
                    continue # 이 줄은 저장하지 않고 건너뜀 (삭제)
                new_lines.append(line)
            
            if modified:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.writelines(new_lines)
                print(f"   ✅ 수정 완료: {filename}")
                count += 1
            else:
                print(f"   - 변경 없음 (이미 삭제됨): {filename}")

    print(f"\n🎉 총 {count}개의 파일에서 'layout' 설정을 강제 삭제했습니다.")
    print("👉 2단계(안내문구 수정)를 진행하고 서버를 재시작하세요!")

if __name__ == "__main__":
    fix_files()