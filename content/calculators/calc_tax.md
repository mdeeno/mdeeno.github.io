---
title: '🏠 부동산 취득세 계산기 (2026년 기준)'
date: 2026-01-01
summary: '집 살 때 필수! 1주택자부터 다주택자까지 취득세 자동 계산'
---

## 🧾 취득세, 미리 준비 안 하면 낭패!

재건축 아파트를 매수할 때는 **취득세를 현금으로 즉시 납부**해야 합니다. 관리처분인가 이후 조합원 지위 양수도 시에도 취득세가 발생합니다.

- 관련 분석: [재건축 분담금 폭탄, 내 아파트는 안전할까?](/posts/reconstruction/)
- 관련 분석: [재건축 용적률의 비밀: 분담금 0원이 가능할까?](/posts/reconstruction/)

부동산을 살 때는 집값만 있으면 안 됩니다. 집값의 **1.1% ~ 12%**에 달하는 취득세를 현금으로 준비해야 등기를 칠 수 있습니다.

- **1주택자:** 1% ~ 3% (비교적 저렴)
- **2주택자:** 1% ~ 8% (조정지역 여부에 따라 다름)
- **다주택자/법인:** 최대 12% (중과세 폭탄 주의!)

---

### 🧮 주택 취득세 계산기



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



<div class="calc-box-tax">
  <div class="calc-row">
    <label class="calc-label">매수 금액 (만원)</label>
    <input type="number" id="taxPrice" class="calc-input" placeholder="예: 60000">
  </div>
  <div class="calc-row">
    <label class="calc-label">취득 후 주택 수</label>
    <select id="taxCount" class="calc-input">
      <option value="1">1주택 (무주택자 매수)</option>
      <option value="2">2주택 (비조정지역/일시적)</option>
      <option value="multi">3주택 이상 / 조정 2주택</option>
    </select>
  </div>
  <button class="calc-btn-tax" onclick="calcTax()">세금 확인하기</button>

  <div id="taxResult" class="result-area" style="border-color: #7950f2;">
    <h3>💸 납부 예상 세액</h3>
    <p>취득세율: <span id="taxRateRes">0</span> %</p>
    <p>총 납부액: <strong id="taxTotal" style="color: #5f3dc4; font-size: 24px;">0</strong> 원</p>
    <p style="font-size: 12px; color: #888;">* 지방교육세, 농어촌특별세 포함 대략적 수치입니다.</p>
  </div>
</div>

<script>
function calcTax() {
  const price = Number(document.getElementById('taxPrice').value) * 10000;
  const count = document.getElementById('taxCount').value;

  if(!price) { alert("금액을 입력해주세요."); return; }

  let baseRate = 0.01; // 기본 1%

  if (count === 'multi') {
    baseRate = 0.08; // 다주택 중과 (보수적으로 8% 설정, 최대 12%)
  } else if (count === '2') {
    baseRate = 0.01; // 비조정 2주택 가정
    if (price >= 600000000 && price <= 900000000) {
        // 6억~9억 구간 사선형 세율
        baseRate = (price * 2 / 300000000 - 3) / 100;
    } else if (price > 900000000) {
        baseRate = 0.03;
    }
  } else {
    // 1주택자
    if (price <= 600000000) baseRate = 0.01;
    else if (price <= 900000000) baseRate = (price * 2 / 300000000 - 3) / 100;
    else baseRate = 0.03;
  }
  
  // 농특세, 지방교육세 포함 (약식: 세율 + 0.1~0.4% 정도 추가되나 단순화를 위해 10% 가산)
  let finalTax = price * baseRate * 1.1; 

  document.getElementById('taxRateRes').innerText = (baseRate * 100).toFixed(2);
  document.getElementById('taxTotal').innerText = Math.floor(finalTax).toLocaleString();
  document.getElementById('taxResult').style.display = 'block';
}
</script>

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">취득세 외에도 분담금·이주비 부담이 걱정되시나요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO 정밀 리포트는 재건축 전 과정의 비용을 통합 시뮬레이션합니다.</p>
  <a href="https://mdeeno.com/member?utm_source=blog&utm_medium=calculator_cta&utm_campaign=inline_link" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    재건축 비용 통합 분석 →
  </a>
</div>
