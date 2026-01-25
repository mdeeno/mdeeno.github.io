import os
import re

# 1. 계산기 파일 경로
base_dir = "content/calculators"

# 2. 글로벌 CSS 경로 (모바일 폰트 조절용)
css_dir = "assets/css/extended"
css_file = os.path.join(css_dir, "custom.css")

# 🔥 [수정된 CSS] 'button' 태그 앞에 '.calc-container'를 붙여서 범위 제한
# 이렇게 하면 헤더에 있는 야간모드 버튼은 영향을 받지 않습니다.
corrected_calc_css = """
<style>
/* 1. 계산기 박스 */
div[class*="calc-box"], .calc-container {
    background-color: #ffffff !important;
    padding: 20px !important;
    border-radius: 16px !important;
    margin-top: 20px !important;
    border: 1px solid #e0e0e0 !important;
    box-shadow: 0 5px 15px rgba(0,0,0,0.05) !important;
    color: #333333 !important;
}

/* 2. 라벨 */
label, .calc-label {
    display: block !important;
    margin-bottom: 5px !important;
    font-weight: bold !important;
    font-size: 15px !important;
    color: #212529 !important;
}

/* 3. 입력창 */
input, select, .calc-input {
    width: 100% !important;
    padding: 12px !important;
    margin-bottom: 15px !important;
    background-color: #f8f9fa !important;
    color: #000000 !important;
    border: 1px solid #ced4da !important;
    border-radius: 8px !important;
    font-size: 16px !important; 
    line-height: 1.5 !important;
}

/* 4. 버튼 (범위 제한: .calc-container 안에 있는 버튼만!) */
.calc-container button, div[class*="calc-box"] button {
    width: 100% !important;
    padding: 15px !important;
    background-color: #212529 !important;
    color: #ffffff !important;
    font-size: 16px !important;
    font-weight: bold !important;
    border: none !important;
    border-radius: 10px !important;
    cursor: pointer !important;
    margin-top: 5px !important;
}

/* 5. 결과창 */
div[id$="Result"], .result-area {
    margin-top: 20px !important;
    padding: 20px !important;
    background-color: #f1f3f5 !important;
    border-radius: 12px !important;
    border-left: 5px solid #00C853 !important;
    color: #333333 !important;
    display: none;
}
</style>
"""

# 🔥 [모바일 최적화 CSS] 제목 폰트 줄이기 & 버튼 강제 축소
mobile_optimization_css = """
/* 모바일 화면 (폭 768px 이하) 설정 */
@media screen and (max-width: 768px) {
    /* 1. 포스팅 제목 크기 축소 (기존 40px -> 24px) */
    .post-title {
        font-size: 24px !important;
        line-height: 1.3 !important;
    }
    
    /* 2. 본문 제목 h1, h2 크기 축소 */
    .post-content h1 { font-size: 22px !important; }
    .post-content h2 { font-size: 20px !important; }
    
    /* 3. 계산기 제목 축소 */
    h1 { font-size: 24px !important; }
}

/* 4. 야간모드 버튼 강제 축소 (혹시 모를 오류 방지) */
#theme-toggle {
    width: auto !important;
    padding: 0 !important;
    background: transparent !important;
}
"""

def fix_design_final():
    # 1. 계산기 파일 내부 CSS 수정
    if os.path.exists(base_dir):
        print(f"🛠️ 계산기 CSS 범위 수정 중... ({base_dir})")
        files = os.listdir(base_dir)
        for filename in files:
            if filename.endswith(".md") and filename != "_index.md":
                filepath = os.path.join(base_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 기존 스타일 태그 삭제 후 새것으로 교체
                new_content = re.sub(r'<style>.*?</style>', corrected_calc_css, content, flags=re.DOTALL)
                
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
        print("   ✅ 계산기 버튼 스타일 격리 완료 (헤더 버튼 보호)")

    # 2. 글로벌 CSS 파일 생성 (모바일 폰트 조절)
    if not os.path.exists(css_dir):
        os.makedirs(css_dir)
    
    with open(css_file, 'w', encoding='utf-8') as f:
        f.write(mobile_optimization_css)
    
    print(f"🛠️ 모바일 최적화 CSS 생성 완료 ({css_file})")
    print("   ✅ 모바일 제목 폰트 크기: 24px로 축소")
    print("   ✅ 야간모드 버튼 크기: 정상화")
    print("\n👉 터미널에서 'hugo server'를 재시작하면 바로 적용됩니다!")

if __name__ == "__main__":
    fix_design_final()