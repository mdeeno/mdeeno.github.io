---
title: '🤝 부동산 중개수수료(복비) 계산기'
date: 2026-01-26
layout: 'page'
summary: '매매/전세 계약 전 필수 확인! 법정 중개보수 상한요율 계산'
---

## 🏠 복비, 호구 잡히지 마세요!

중개수수료는 **'상한요율'** 내에서 협의하는 것이 원칙입니다. 법적으로 정해진 최대 금액을 미리 알고 가야 당당하게 협의할 수 있습니다.

- **매매:** 거래 금액에 따라 0.4% ~ 0.7% (최대 0.9%)
- **임대차(전월세):** 거래 금액에 따라 0.3% ~ 0.5% (최대 0.8%)
- **오피스텔:** 주거용은 매매 0.5%, 임대차 0.4%

---

### 🧮 중개보수 계산기 (주택 기준)

<style>
  .calc-box-fee { background: #fff0f6; padding: 25px; border-radius: 12px; margin-top: 20px; border: 1px solid #fcc2d7; }
  .calc-btn-fee { width: 100%; padding: 15px; background: #e64980; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-fee:hover { background: #be4bdb; }
</style>

<div class="calc-box-fee">
  <div class="calc-row">
    <label class="calc-label">거래 종류</label>
    <select id="feeType" class="calc-input">
      <option value="buy">매매/교환</option>
      <option value="rent">전세/월세</option>
    </select>
  </div>
  <div class="calc-row">
    <label class="calc-label">거래 금액 (만원)</label>
    <input type="number" id="feeAmount" class="calc-input" placeholder="예: 50000 (5억)">
  </div>
  <button class="calc-btn-fee" onclick="calcFee()">복비 계산하기</button>

  <div id="feeResult" class="result-area" style="border-color: #e64980;">
    <h3>🤝 최대 중개보수</h3>
    <p>상한요율: <span id="feeRate">0</span> %</p>
    <p>최대 수수료: <strong id="feeMax" style="color: #c2255c; font-size: 24px;">0</strong> 원</p>
    <p style="font-size: 12px; color: #888;">* 부가세 별도, 시/도 조례에 따라 일부 차이 가능</p>
  </div>
</div>

<script>
function calcFee() {
  const type = document.getElementById('feeType').value;
  const amount = Number(document.getElementById('feeAmount').value) * 10000;
  
  if(!amount) { alert("금액을 입력해주세요."); return; }

  let rate = 0;
  let limit = 0;

  if (type === 'buy') { // 매매
    if (amount < 50000000) { rate = 0.6; limit = 250000; }
    else if (amount < 200000000) { rate = 0.5; limit = 800000; }
    else if (amount < 900000000) { rate = 0.4; }
    else if (amount < 1200000000) { rate = 0.5; }
    else if (amount < 1500000000) { rate = 0.6; }
    else { rate = 0.7; }
  } else { // 임대차
    if (amount < 50000000) { rate = 0.5; limit = 200000; }
    else if (amount < 100000000) { rate = 0.4; limit = 300000; }
    else if (amount < 600000000) { rate = 0.3; }
    else if (amount < 1200000000) { rate = 0.4; }
    else if (amount < 1500000000) { rate = 0.5; }
    else { rate = 0.6; }
  }

  let fee = amount * (rate / 100);
  if (limit > 0 && fee > limit) fee = limit;

  document.getElementById('feeRate').innerText = rate;
  document.getElementById('feeMax').innerText = Math.floor(fee).toLocaleString();
  document.getElementById('feeResult').style.display = 'block';
}
</script>
