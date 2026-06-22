---
title: '📉 DSR 계산기 — 연소득 대비 원리금 상환액'
date: 2026-01-01
lastmod: 2026-06-22
summary: '연소득과 기존·신규 대출의 연간 원리금으로 예상 DSR을 계산합니다'
---

## 이주비 이후 신규 대출 여력을 확인하세요

금융위원회 최신 정책 문답상 중도금·이주비 대출은 DSR 직접 적용 대상에서 제외됩니다. 다만 이주비 실행 후 다른 DSR 적용 대출을 신규로 받을 때 기존 이주비의 원리금이 반영될 수 있습니다.

아래 계산기는 일반 대출의 예상 DSR을 확인하는 도구입니다. 이주비 승인액을 계산하거나 금융기관의 승인을 예측하는 도구가 아닙니다.

- 관련 분석: [재건축 이주비 대출 한도 — DSR·LTV 확인 순서](/posts/reconstruction/2026-03-17-이주비-대출-0원-재건축-조합원이-입주-전-반드시-체크할-3가지/)
- 공식 기준: [금융위원회 가계대출 관리 강화 FAQ](https://www.fsc.go.kr/po020201/85518)

---

## DSR이 도대체 뭔가요?

**DSR(총부채원리금상환비율)**은 쉽게 말해 **"네가 버는 돈 중에서 빚 갚는 데 얼마를 쓰니?"**라는 비율입니다.

- **DSR 40%의 의미:** 연소득이 5,000만 원이고 DSR 기준을 40%로 적용한다면 연간 원리금 상환액 한도는 2,000만 원이라는 뜻입니다.
- **주의할 점:** 실제 산정 만기, 스트레스 금리, 포함 부채와 적용 비율은 대출 종류·업권·신청 시점에 따라 다릅니다.

## 신청 전에 확인할 항목

1. 기존 대출의 DSR 산정상 연간 원리금
2. 신규 대출에 적용되는 스트레스 금리와 산정 만기
3. 은행권·비은행권의 적용 기준
4. 이주비·중도금 등 예외 대출이 이후 신규 심사에 반영되는 방식

---

### 🧮 DSR & 한도 계산기



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

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">DSR 계산 후 다음 단계가 필요하신가요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO 정밀 리포트는 내 단지의 이주비 한도·공사비·분담금을 종합 시뮬레이션합니다.</p>
  <a href="https://mdeeno.com/member?utm_source=blog&utm_medium=calculator_cta&utm_campaign=inline_link" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    재건축 리스크 정밀 분석 →
  </a>
</div>

<script>
function calcDSR() {
  const income = Number(document.getElementById('dsrIncome').value);
  const existing = Number(document.getElementById('dsrExisting').value);
  const newLoan = Number(document.getElementById('dsrNewLoan').value);
  const rate = Number(document.getElementById('dsrRate').value) / 100;
  const year = Number(document.getElementById('dsrYear').value);

  if(!income || !newLoan || !year || rate < 0) { alert('연소득, 대출금액, 금리와 기간을 확인해주세요.'); return; }

  // 원리금 균등 상환 기준 연 상환액 계산
  const monthlyRate = rate / 12;
  const totalMonths = year * 12;
  const monthlyPayment = monthlyRate === 0
    ? newLoan / totalMonths
    : (newLoan * monthlyRate * Math.pow(1+monthlyRate, totalMonths)) / (Math.pow(1+monthlyRate, totalMonths) - 1);
  const yearlyPayment = monthlyPayment * 12;

  const totalYearlyRepayment = existing + yearlyPayment;
  const dsr = (totalYearlyRepayment / income) * 100;

  document.getElementById('dsrValue').innerText = dsr.toFixed(2);
  const comment = document.getElementById('dsrComment');
  document.getElementById('dsrResult').style.display = 'block';

  if(dsr <= 40) {
    comment.innerHTML = "현재 입력값 기준 40% 이하입니다. 실제 승인 여부는 금융기관 심사와 스트레스 DSR 적용 결과를 확인하세요.";
    comment.style.color = "green";
  } else if(dsr <= 50) {
    comment.innerHTML = "현재 입력값 기준 40%를 초과합니다. 적용 업권과 대출 종류의 실제 기준을 확인하세요.";
    comment.style.color = "#f59f00";
  } else {
    comment.innerHTML = "현재 입력값 기준 50%를 초과합니다. 신규 대출 전 금융기관의 정식 한도 조회가 필요합니다.";
    comment.style.color = "red";
  }
}
</script>
