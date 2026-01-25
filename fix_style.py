import os
import re

# 계산기 파일 경로
base_dir = "content/calculators"

# 🔥 [강력한 CSS] 다크모드 무시하고 '흰색 카드' 스타일로 강제 적용
# 입력창 폰트 16px 강제 (모바일/PC 가독성 확보) + 텍스트 검정색 강제
universal_css = """
<style>
/* 1. 계산기 박스 (화이트 카드 스타일 강제) */
div[class*="calc-box"], .calc-container {
    background-color: #ffffff !important;
    padding: 30px !important;
    border-radius: 16px !important;
    margin-top: 20px !important;
    border: 1px solid #e0e0e0 !important;
    box-shadow: 0 10px 25px rgba(0,0,0,0.05) !important;
    color: #333333 !important; /* 텍스트는 무조건 검정 */
}

/* 2. 라벨 (제목) */
label, .calc-label {
    display: block !important;
    margin-bottom: 8px !important;
    font-weight: bold !important;
    font-size: 16px !important;
    color: #212529 !important;
}

/* 3. 입력창 & 드롭다운 (핵심 수정) */
input, select, .calc-input {
    width: 100% !important;
    padding: 14px !important;
    margin-bottom: 20px !important;
    background-color: #f8f9fa !important; /* 아주 연한 회색 */
    color: #000000 !important; /* 글자색 검정 강제 (다크모드 상속 방지) */
    border: 1px solid #ced4da !important;
    border-radius: 8px !important;
    font-size: 16px !important; /* 글자 크기 키움 (깨알 글씨 방지) */
    line-height: 1.5 !important;
    appearance: auto !important; /* 드롭다운 화살표 복구 */
    -webkit-appearance: auto !important;
}

/* 입력창 선택 시 강조 */
input:focus, select:focus {
    outline: none !important;
    border-color: #00C853 !important;
    background-color: #ffffff !important;
    box-shadow: 0 0 0 4px rgba(0, 200, 83, 0.1) !important;
}

/* 드롭다운 옵션 (글자 잘 보이게) */
option {
    background-color: #ffffff !important;
    color: #000000 !important;
    font-size: 16px !important;
}

/* 4. 버튼 (크고 누르기 쉽게 통일) */
button, [class^="calc-btn"] {
    width: 100% !important;
    padding: 18px !important;
    background-color: #212529 !important; /* 진한 검정 버튼 */
    color: #ffffff !important;
    font-size: 18px !important;
    font-weight: bold !important;
    border: none !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 10px !important;
}
button:hover, [class^="calc-btn"]:hover {
    background-color: #000000 !important;
    transform: translateY(-2px);
}

/* 5. 결과창 */
div[id$="Result"], .result-area {
    margin-top: 30px !important;
    padding: 25px !important;
    background-color: #f1f3f5 !important;
    border-radius: 12px !important;
    border-left: 6px solid #00C853 !important;
    color: #333333 !important;
    display: none; /* 기본 숨김 */
}
</style>
"""

def apply_universal_style():
    if not os.path.exists(base_dir):
        print(f"❌ 폴더를 찾을 수 없습니다: {base_dir}")
        return

    print(f"🎨 디자인 긴급 수선 시작... ({base_dir})")
    
    files = os.listdir(base_dir)
    count = 0
    
    for filename in files:
        if filename.endswith(".md") and filename != "_index.md":
            filepath = os.path.join(base_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 기존 <style>...</style> 블록을 찾아서 제거하고 새 스타일로 교체
            # 정규식: <style> 태그와 그 사이의 모든 내용(dotall)을 찾음
            new_content = re.sub(r'<style>.*?</style>', universal_css, content, flags=re.DOTALL)
            
            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"   ✅ 디자인 적용 완료: {filename}")
                count += 1
            else:
                # 스타일 태그가 없으면 맨 아래에 추가 (혹시 몰라서)
                if "<style>" not in content:
                    with open(filepath, 'a', encoding='utf-8') as f:
                        f.write("\n" + universal_css)
                    print(f"   ✅ 디자인 신규 추가: {filename}")
                    count += 1
                else:
                    print(f"   - 변경 없음: {filename}")

    print(f"\n🎉 총 {count}개 계산기 디자인을 '화이트 카드' 스타일로 통일했습니다.")
    print("👉 입력창이 검정 글씨로 잘 보이고, 폰트도 커졌습니다.")
    print("👉 'hugo server'를 재시작해서 확인해보세요!")

if __name__ == "__main__":
    apply_universal_style()