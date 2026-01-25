---
title: '📉 DSR & 내 집 마련 대출 한도 계산기'
date: 2026-01-26
layout: 'page'
summary: '내 연봉으로 얼마까지 대출이 나올까? DSR 40% 규제 완벽 분석'
---

## 🧐 DSR이 도대체 뭔가요?

**DSR(총부채원리금상환비율)**은 쉽게 말해 **"네가 버는 돈 중에서 빚 갚는 데 얼마를 쓰니?"**라는 비율입니다.

- **DSR 40%의 의미:** 연봉이 5,000만 원이라면, 1년에 갚는 원금+이자가 2,000만 원을 넘으면 안 된다는 뜻입니다.
- **왜 중요한가요?:** 은행은 이 DSR 비율을 칼같이 지킵니다. 아무리 집값이 비싸도 내 DSR 한도가 꽉 차면 10원도 빌릴 수 없습니다.

## 💡 대출 한도를 늘리는 꿀팁

1.  **마이너스 통장 정리:** 쓰지 않는 마통이라도 한도만큼 빚으로 잡힙니다. 당장 없애세요.
2.  **만기를 길게:** 대출 기간을 30년보다 40년, 50년으로 늘리면 1년에 갚는 돈이 줄어들어 DSR이 낮아집니다.

---

### 🧮 DSR & 한도 계산기

<style>
  .calc-box { background: #f1f3f5; padding: 25px; border-radius: 12px; margin-top: 20px; }
  .calc-row { margin-bottom: 15px; }
  .calc-label { font-weight: bold; display: block; margin-bottom: 5px; }
  .calc-input { width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-size: 16px; }
  .calc-btn { width: 100%; padding: 15px; background: #228be6; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn:hover { background: #1c7ed6; }
  .result-area { margin-top: 20px; padding: 20px; background: #fff; border-radius: 8px; display: none; border: 2px solid #228be6; }
</style>

<div class="calc-box">
  <div class="calc-row">
    <label class="calc-label">1. 연소득 (세전/만원)</label>
    <input type="number" id="dsrIncome" class="calc-input" placeholder="예: 5000">
  </div>
  <div class="calc-row">
    <label class="calc-label">2. 기존 대출의 연간 상환액 (만원)</label>
    <input type="number" id="dsrExisting" class="calc-input" placeholder="예: 500 (신용대출, 할부 등)">
  </div>
  <div class="calc-row">
    <label class="calc-label">3. 새로 받을 대출 금액 (만원)</label>
    <input type="number" id="dsrNewLoan" class="calc-input" placeholder="예: 30000">
  </div>
  <div class="calc-row">
    <label class="calc-label">4. 대출 금리 (%)</label>
    <input type="number" id="dsrRate" class="calc-input" placeholder="예: 4.0">
  </div>
  <div class="calc-row">
    <label class="calc-label">5. 대출 기간 (년)</label>
    <input type="number" id="dsrYear" class="calc-input" placeholder="예: 40">
  </div>
  <button class="calc-btn" onclick="calcDSR()">내 DSR 확인하기</button>

  <div id="dsrResult" class="result-area">
    <h3>📊 계산 결과</h3>
    <p>예상 DSR: <strong id="dsrValue" style="color: #d6336c; font-size: 24px;">0</strong> %</p>
    <p id="dsrComment"></p>
  </div>
</div>

<script>
function calcDSR() {
  const income = Number(document.getElementById('dsrIncome').value);
  const existing = Number(document.getElementById('dsrExisting').value);
  const newLoan = Number(document.getElementById('dsrNewLoan').value);
  const rate = Number(document.getElementById('dsrRate').value) / 100;
  const year = Number(document.getElementById('dsrYear').value);

  if(!income || !newLoan) { alert('연소득과 대출금액을 입력해주세요.'); return; }

  // 원리금 균등 상환 기준 연 상환액 계산
  const monthlyRate = rate / 12;
  const totalMonths = year * 12;
  const monthlyPayment = (newLoan * monthlyRate * Math.pow(1+monthlyRate, totalMonths)) / (Math.pow(1+monthlyRate, totalMonths) - 1);
  const yearlyPayment = monthlyPayment * 12;

  const totalYearlyRepayment = existing + yearlyPayment;
  const dsr = (totalYearlyRepayment / income) * 100;

  document.getElementById('dsrValue').innerText = dsr.toFixed(2);
  const comment = document.getElementById('dsrComment');
  document.getElementById('dsrResult').style.display = 'block';

  if(dsr <= 40) {
    comment.innerHTML = "✅ <strong>안전합니다!</strong> 은행 대출 승인 가능성이 높습니다.";
    comment.style.color = "green";
  } else if(dsr <= 50) {
    comment.innerHTML = "⚠️ <strong>주의 단계입니다.</strong> 2금융권 이용이나 한도 감액이 필요할 수 있습니다.";
    comment.style.color = "#f59f00";
  } else {
    comment.innerHTML = "🚨 <strong>위험합니다!</strong> 대출이 거절될 확률이 매우 높습니다. 대출 기간을 늘리거나 금액을 줄이세요.";
    comment.style.color = "red";
  }
}
</script>
