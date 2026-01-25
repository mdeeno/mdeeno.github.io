---
title: "💰 대출 이자 계산기 (월 상환액)"
date: 2026-01-26
layout: "page"
summary: "매달 얼마씩 갚아야 할까? 원리금 균등 vs 원금 균등 비교"
---

## 🏦 이자 갚는 방식, 뭐가 다를까?
대출을 받을 때 가장 고민되는 것이 **"어떻게 갚느냐"**입니다.

1.  **원리금 균등 상환 (가장 추천 👍):**
    * 매달 내는 돈(원금+이자)이 **똑같습니다.**
    * 계획적인 지출 관리가 가능해서 직장인에게 가장 유리합니다.
2.  **원금 균등 상환:**
    * 처음엔 많이 내고, 갈수록 적게 냅니다.
    * 총 이자는 제일 적지만, 초반 부담이 너무 큽니다.
3.  **만기 일시 상환:**
    * 이자만 내다가 마지막에 원금을 한방에 갚습니다. (전세 대출 등)

---

### 🧮 월 상환액 계산기 (원리금 균등 기준)
<style>
  .calc-box { background: #e3fafc; padding: 25px; border-radius: 12px; margin-top: 20px; }
  .calc-btn-int { width: 100%; padding: 15px; background: #0c8599; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-int:hover { background: #0b7285; }
</style>

<div class="calc-box">
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
    <h3>📊 매월 갚아야 할 돈</h3>
    <p>월 상환액: <strong id="intMonthly" style="color: #0c8599; font-size: 24px;">0</strong> 원</p>
    <p>총 이자액: <span id="intTotal">0</span> 만원</p>
    <p style="font-size: 14px; color: #666;">(원리금 균등 상환 기준)</p>
  </div>
</div>

<script>
function calcInterest() {
  const loan = Number(document.getElementById('intLoan').value) * 10000;
  const rate = Number(document.getElementById('intRate').value) / 100 / 12;
  const months = Number(document.getElementById('intYear').value) * 12;

  if(!loan || !rate) { alert('값을 입력해주세요.'); return; }

  // 원리금 균등 공식
  const monthlyPay = (loan * rate * Math.pow(1 + rate, months)) / (Math.pow(1 + rate, months) - 1);
  const totalPay = monthlyPay * months;
  const totalInterest = totalPay - loan;

  document.getElementById('intMonthly').innerText = Math.round(monthlyPay).toLocaleString();
  document.getElementById('intTotal').innerText = Math.round(totalInterest / 10000).toLocaleString();
  document.getElementById('intResult').style.display = 'block';
}
</script>