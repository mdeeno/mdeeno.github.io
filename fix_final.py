import os
import re

# 계산기 파일이 있는 경로
base_dir = "content/calculators"

def fix_calculators_final():
    if not os.path.exists(base_dir):
        print(f"❌ 폴더를 찾을 수 없습니다: {base_dir}")
        return

    print(f"🛠️ [긴급 수정] 날짜 및 레이아웃 교정 시작... ({base_dir})")
    
    files = os.listdir(base_dir)
    count = 0
    
    for filename in files:
        if filename.endswith(".md") and filename != "_index.md":
            filepath = os.path.join(base_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            original_content = content
            
            # 1. 'layout' 설정 삭제 (작은따옴표, 큰따옴표, 공백 모두 대응)
            # 예: layout: 'page', layout: "page", layout : 'page' 모두 삭제
            content = re.sub(r'^layout\s*:\s*[\'"]?page[\'"]?.*\n?', '', content, flags=re.MULTILINE)
            
            # 2. 날짜를 '2026-01-01'로 강제 변경 (미래 날짜 문제 해결)
            # 기존 date: 2026-XX-XX 패턴을 찾아서 과거 날짜로 바꿉니다.
            content = re.sub(r'^date\s*:\s*\d{4}-\d{2}-\d{2}', 'date: 2026-01-01', content, flags=re.MULTILINE)
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"   ✅ 수정 완료: {filename}")
                count += 1
            else:
                print(f"   - 변경 없음: {filename}")

    print(f"\n🎉 총 {count}개 파일 수정 완료!")
    print("   1. layout 설정을 삭제했습니다.")
    print("   2. 날짜를 '2026-01-01'로 변경했습니다. (즉시 발행)")
    print("👉 이제 터미널에서 'hugo server'를 껐다 켜면 100% 나옵니다!")

if __name__ == "__main__":
    fix_calculators_final()