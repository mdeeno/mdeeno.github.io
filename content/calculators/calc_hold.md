---
title: '🏠 보유세(재산세+종부세) 계산기'
date: 2026-01-01
summary: '나는 매년 얼마를 내야 할까? 공시가격 기준 보유세 예측'
---

## 😰 가만히 있어도 나가는 돈, 보유세

집을 가지고만 있어도 매년 6월 1일 기준으로 세금이 부과됩니다.

1.  **재산세:** 모든 주택 소유자가 냅니다. (7월, 9월 반반 납부)
2.  **종합부동산세(종부세):** 공시가격 합계가 일정 금액(1주택 12억, 다주택 9억)을 넘으면 추가로 내는 부자세(?)입니다.

---

### 🧮 보유세 간편 계산기 (1주택자 기준)



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



<div class="calc-box-hold">
  <div class="calc-row">
    <label class="calc-label">공시가격 (만원)</label>
    <input type="number" id="pubPrice" class="calc-input" placeholder="예: 90000 (9억)">
  </div>
  <button class="calc-btn-hold" onclick="calcHold()">보유세 확인</button>

  <div id="holdResult" class="result-area" style="border-color: #be4bdb;">
    <h3>🧾 연간 예상 납부액</h3>
    <p>재산세: <span id="resTax1">0</span> 원</p>
    <p>종부세: <span id="resTax2">0</span> 원</p>
    <hr>
    <p>총 보유세: <strong id="totalHold" style="color: #862e9c; font-size: 24px;">0</strong> 원</p>
  </div>
</div>

<script>
function calcHold() {
  const price = Number(document.getElementById('pubPrice').value) * 10000;
  if(!price) { alert("공시가격을 입력해주세요."); return; }

  // 1주택자 기준 약식 계산
  // 1. 재산세 (공정시장가액비율 60% 가정)
  const taxBase = price * 0.6;
  let propertyTax = 0;
  
  if(taxBase <= 60000000) propertyTax = taxBase * 0.0005; // 특례세율 적용
  else if(taxBase <= 150000000) propertyTax = 30000 + (taxBase-60000000)*0.0007;
  else if(taxBase <= 300000000) propertyTax = 93000 + (taxBase-150000000)*0.001;
  else propertyTax = 243000 + (taxBase-300000000)*0.0025; // 일반세율

  // 도시지역분, 지방교육세 등 포함 (약 1.4배 보정)
  const finalPropertyTax = propertyTax * 1.4;

  // 2. 종부세 (1주택 공제 12억)
  let jongbuTax = 0;
  if (price > 1200000000) {
    const jBase = (price - 1200000000) * 0.6;
    if (jBase <= 300000000) jongbuTax = jBase * 0.005;
    else jongbuTax = jBase * 0.007; // 간이 적용
  }

  document.getElementById('resTax1').innerText = Math.round(finalPropertyTax).toLocaleString();
  document.getElementById('resTax2').innerText = Math.round(jongbuTax).toLocaleString();
  document.getElementById('totalHold').innerText = Math.round(finalPropertyTax + jongbuTax).toLocaleString();
  document.getElementById('holdResult').style.display = 'block';
}
</script>
