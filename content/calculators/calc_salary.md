---
title: '💵 연봉 실수령액 계산기 (2026년 기준)'
date: 2026-01-01
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

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">실수령액으로 분담금 대출이 가능할까요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO 리스크 진단으로 DSR 한도와 분담금 부담을 통합 분석해 보세요.</p>
  <a href="https://mdeeno.com/member?utm_source=blog&utm_medium=calc_cta&utm_campaign=calc_salary" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    재건축 리스크 무료 진단 →
  </a>
</div>

<p style="font-size:12px;color:#888;margin-top:16px;">※ 본 계산기는 간이 추정치이며, 정확한 세금 계산은 국세청 홈택스 또는 세무사 상담을 통해 확인하시기 바랍니다.</p>
