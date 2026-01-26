import os
import re

# ==============================================================================
# [설정] 수정할 대상 경로
# ==============================================================================
TARGET_DIR = "content/posts"  # 포스팅이 저장된 폴더
MAIN_DOMAIN_URL = "https://tech.mdeeno.com"

# 🔗 살려낼 링크 매핑 정보 (죽은 텍스트 -> 산 링크)
CALCULATOR_MAP = {
    "DSR & 대출 한도 계산기": "/calculators/calc_dsr/",
    "대출 이자 계산기": "/calculators/calc_interest/",
    "중개보수(복비) 계산기": "/calculators/calc_fee/",
    "취득세 계산기": "/calculators/calc_tax/",
    "양도소득세 계산기": "/calculators/calc_transfer/",
    "보유세(재산세+종부세) 계산기": "/calculators/calc_hold/",
    "청약 가점 계산기": "/calculators/calc_subscription/",
    "전월세 전환율 계산기": "/calculators/calc_rent/",
    "연봉 실수령액 계산기": "/calculators/calc_salary/"
}

def fix_content(content):
    original_content = content
    
    # 1. 🧱 가독성 박살(벽돌) 수정: * 기호 앞에 줄바꿈 강제 삽입
    # 기존에 줄바꿈이 없는 "* "를 "\n\n* "로 변경
    content = re.sub(r'(?<!\n)\n\*\s', '\n\n* ', content)
    
    # 2. 🔗 죽은 링크 심폐소생
    # 예: "[취득세 계산기]" -> "[취득세 계산기](URL)"
    # 예: " 취득세 계산기 " -> " [취득세 계산기](URL) "
    for text, url in CALCULATOR_MAP.items():
        full_url = f"{MAIN_DOMAIN_URL}{url}"
        markdown_link = f"[{text}]({full_url})"
        
        # 이미 잘 된 링크는 건드리지 않음
        if f"({full_url})" in content:
            continue
            
        # 1) 대괄호만 있고 주소 없는 것 고치기 ([텍스트])
        content = content.replace(f"[{text}]", markdown_link)
        
        # 2) 괄호 안의 이상한 텍스트 고치기 (() 텍스트) -> (* 텍스트)
        content = content.replace("() ", "* ")
        content = content.replace("( ) ", "* ")
        
        # 3) 그냥 텍스트만 덜렁 있는 경우 링크 씌우기 (앞뒤 공백 있을 때)
        # 너무 공격적으로 바꾸면 오작동할 수 있으니 주의
        if text in content and markdown_link not in content:
             content = content.replace(text, markdown_link)

    return content

def main():
    print("🚑 [일괄 수정] 포스팅 심폐소생술 시작...")
    count = 0
    
    for root, dirs, files in os.walk(TARGET_DIR):
        for file in files:
            if file.endswith(".md"):
                filepath = os.path.join(root, file)
                
                with open(filepath, 'r', encoding='utf-8') as f:
                    old_content = f.read()
                
                new_content = fix_content(old_content)
                
                if old_content != new_content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"✅ 수정 완료: {file}")
                    count += 1
                else:
                    print(f"PASS (수정 불필요): {file}")

    print(f"\n🎉 총 {count}개의 파일이 정상화되었습니다.")

if __name__ == "__main__":
    main()