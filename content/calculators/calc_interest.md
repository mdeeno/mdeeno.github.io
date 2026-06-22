---
title: "💰 대출 이자 계산기 — 거치식·원리금균등"
date: 2026-01-01
lastmod: 2026-06-22
summary: "이자만 납부하는 거치식과 원리금균등 방식의 월 납부액·총이자를 비교합니다"
---

## 재건축 이주비 후불이자, 얼마나 쌓일까?

이주비 이자는 조합·금융기관 협약에 따라 월납, 후불 또는 지원 방식으로 달라집니다. 후불은 이자 납부 시점을 미루는 것이므로 최종 부담 주체와 정산 방식을 약정서에서 확인해야 합니다.

아래 계산기로 이주비 대출의 총 이자 부담을 미리 시뮬레이션해 보세요.

- 관련 분석: [재건축 이주비 대출 이자 계산 — 금리·기간별 비용표](/posts/reconstruction/재건축-이주비-대출-억-단위-이자-부담-피하려면-m-deeno의-2024-정비사업-자금-데이터-분ᄉ/)
- 한도 확인: [재건축 이주비 대출 한도 — DSR·LTV 확인 순서](/posts/reconstruction/2026-03-17-이주비-대출-0원-재건축-조합원이-입주-전-반드시-체크할-3가지/)

---

## 이자 갚는 방식, 뭐가 다를까?
대출을 받을 때 가장 고민되는 것이 **"어떻게 갚느냐"**입니다.

1.  **원리금 균등 상환:**
    * 매달 내는 돈(원금+이자)이 **똑같습니다.**
    * 납부액이 일정하지만 개인에게 가장 유리한지는 현금흐름에 따라 다릅니다.
2.  **원금 균등 상환:**
    * 처음엔 많이 내고, 갈수록 적게 냅니다.
    * 원금이 빠르게 줄어 총이자가 상대적으로 적고 초기 납부액이 큽니다.
3.  **만기 일시 상환:**
    * 매월 이자만 내고 만기에 원금을 상환합니다. 이자 후불 약정은 납부 시점과 계산 방식을 별도로 확인해야 합니다.

---

### 🧮 월 납부액·총이자 계산기


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



<div class="calc-box">
  <div class="calc-row">
    <label class="calc-label">상환 방식</label>
    <select id="intMode" class="calc-input">
      <option value="interestOnly">이자만 납부·원금 만기상환</option>
      <option value="amortizing">원리금 균등상환</option>
    </select>
  </div>
  <div class="calc-row">
    <label class="calc-label">대출 금액 (만원)</label>
    <input type="number" id="intLoan" class="calc-input" placeholder="예: 20000">
  </div>
  <div class="calc-row">
    <label class="calc-label">연 이자율 (%)</label>
    <input type="number" id="intRate" class="calc-input" placeholder="예: 4.5">
  </div>
  <div class="calc-row">
    <label class="calc-label">대출 기간 (년)</label>
    <input type="number" id="intYear" class="calc-input" placeholder="예: 30">
  </div>
  <button class="calc-btn-int" onclick="calcInterest()">계산하기</button>

  <div id="intResult" class="result-area" style="border-color: #0c8599;">
    <h3>📊 계산 결과</h3>
    <p><span id="intMonthlyLabel">월 납부액</span>: <strong id="intMonthly" style="color: #0c8599; font-size: 24px;">0</strong> 원</p>
    <p>총 이자액: <span id="intTotal">0</span> 만원</p>
    <p id="intNote" style="font-size: 14px; color: #666;"></p>
  </div>
</div>

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">이자 계산 결과가 예상보다 많나요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO 정밀 리포트는 이주비 이자·공사비 상승·분담금을 통합 시뮬레이션합니다.</p>
  <a href="https://mdeeno.com/member?utm_source=blog&utm_medium=calculator_cta&utm_campaign=inline_link" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    재건축 리스크 정밀 분석 →
  </a>
</div>

<script>
function calcInterest() {
  const mode = document.getElementById('intMode').value;
  const loan = Number(document.getElementById('intLoan').value) * 10000;
  const rate = Number(document.getElementById('intRate').value) / 100 / 12;
  const months = Number(document.getElementById('intYear').value) * 12;

  if(!loan || rate < 0 || !months) { alert('대출 금액, 금리와 기간을 확인해주세요.'); return; }

  let monthlyPay;
  let totalInterest;

  if(mode === 'interestOnly') {
    monthlyPay = loan * rate;
    totalInterest = monthlyPay * months;
    document.getElementById('intMonthlyLabel').innerText = '월 이자';
    document.getElementById('intNote').innerText = '원금 전액을 계속 사용하고 이자를 매월 단순 납부하는 가정입니다.';
  } else {
    monthlyPay = rate === 0
      ? loan / months
      : (loan * rate * Math.pow(1 + rate, months)) / (Math.pow(1 + rate, months) - 1);
    totalInterest = monthlyPay * months - loan;
    document.getElementById('intMonthlyLabel').innerText = '월 상환액';
    document.getElementById('intNote').innerText = '원리금 균등상환 가정입니다.';
  }

  document.getElementById('intMonthly').innerText = Math.round(monthlyPay).toLocaleString();
  document.getElementById('intTotal').innerText = Math.round(totalInterest / 10000).toLocaleString();
  document.getElementById('intResult').style.display = 'block';
}
</script>
