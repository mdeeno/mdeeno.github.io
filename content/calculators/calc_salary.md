---
title: '💵 연봉 실수령액 계산기 (2026년 기준)'
date: 2026-01-26
layout: 'page'
summary: '연봉 5천만원이면 실제로는 얼마 받을까? 세금 뗀 월급 확인'
---

## 💸 내 월급, 왜 이것밖에 안 들어왔지?

연봉 계약서에 적힌 금액과 통장에 찍히는 금액은 다릅니다. 바로 **'원천징수'** 때문이죠.

- **국민연금 (4.5%):** 나중에 돌려받는 돈이지만 당장은 떼어갑니다.
- **건강보험 (약 3.5%):** 병원비 혜택을 위한 필수 보험료입니다.
- **고용보험 (0.9%):** 실업급여의 재원이 됩니다.
- **소득세:** 버는 만큼 내는 세금입니다.

보통 연봉의 **약 10% ~ 18%** 정도가 공제되고 입금됩니다. 아래 계산기로 정확한 실수령액을 확인해보세요.

---

### 🧮 연봉 실수령액 계산기

<style>
  .calc-box-sal { background: #fff9db; padding: 25px; border-radius: 12px; margin-top: 20px; }
  .calc-btn-sal { width: 100%; padding: 15px; background: #fab005; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-sal:hover { background: #f08c00; }
</style>

<div class="calc-box-sal">
  <div class="calc-row">
    <label class="calc-label">계약 연봉 (만원)</label>
    <input type="number" id="salTotal" class="calc-input" placeholder="예: 5000">
  </div>
  <div class="calc-row">
    <label class="calc-label">부양 가족 수 (본인 포함)</label>
    <input type="number" id="salFamily" class="calc-input" value="1">
  </div>
  <button class="calc-btn-sal" onclick="calcSalary()">실수령액 확인</button>

  <div id="salResult" class="result-area" style="border-color: #fab005;">
    <h3>💰 예상 월 수령액</h3>
    <p><strong id="salMonthly" style="color: #e67700; font-size: 28px;">0</strong> 원</p>
    <hr>
    <p>국민연금: <span id="valPension">0</span> 원</p>
    <p>건강보험: <span id="valHealth">0</span> 원</p>
    <p>소득세(예상): <span id="valTax">0</span> 원</p>
    <p style="font-size: 12px; color: #888;">* 2025~2026년 요율 기준 단순 추정치입니다.</p>
  </div>
</div>

<script>
function calcSalary() {
  const salary = Number(document.getElementById('salTotal').value) * 10000;
  if(!salary) { alert('연봉을 입력해주세요.'); return; }

  // 2025-2026 추정 요율 (간이 계산)
  const pension = Math.min(salary * 0.045, 265500 * 12); // 상한액 고려(대략)
  const health = salary * 0.03545;
  const care = health * 0.1295;
  const employ = salary * 0.009;
  
  // 소득세 간이 세율 (누진세 단순화 적용)
  let taxRate = 0;
  if(salary < 30000000) taxRate = 0.02;
  else if(salary < 50000000) taxRate = 0.04;
  else if(salary < 88000000) taxRate = 0.08;
  else taxRate = 0.12;

  const tax = salary * taxRate; 
  
  const totalDeduct = pension + health + care + employ + tax;
  const netYearly = salary - totalDeduct;
  const netMonthly = netYearly / 12;

  document.getElementById('salMonthly').innerText = Math.round(netMonthly).toLocaleString();
  document.getElementById('valPension').innerText = Math.round(pension/12).toLocaleString();
  document.getElementById('valHealth').innerText = Math.round((health+care)/12).toLocaleString();
  document.getElementById('valTax').innerText = Math.round(tax/12).toLocaleString();
  
  document.getElementById('salResult').style.display = 'block';
}
</script>
