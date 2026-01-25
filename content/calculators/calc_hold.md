---
title: '🏠 보유세(재산세+종부세) 계산기'
date: 2026-01-26
layout: 'page'
summary: '나는 매년 얼마를 내야 할까? 공시가격 기준 보유세 예측'
---

## 😰 가만히 있어도 나가는 돈, 보유세

집을 가지고만 있어도 매년 6월 1일 기준으로 세금이 부과됩니다.

1.  **재산세:** 모든 주택 소유자가 냅니다. (7월, 9월 반반 납부)
2.  **종합부동산세(종부세):** 공시가격 합계가 일정 금액(1주택 12억, 다주택 9억)을 넘으면 추가로 내는 부자세(?)입니다.

---

### 🧮 보유세 간편 계산기 (1주택자 기준)

<style>
  .calc-box-hold { background: #f8f0fc; padding: 25px; border-radius: 12px; margin-top: 20px; border: 1px solid #eebefa; }
  .calc-btn-hold { width: 100%; padding: 15px; background: #be4bdb; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-hold:hover { background: #ae3ec9; }
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
