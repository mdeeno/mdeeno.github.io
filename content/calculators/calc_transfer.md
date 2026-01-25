---
title: '💸 양도소득세 계산기 (2026년 최신)'
date: 2026-01-26
layout: 'page'
summary: '집 팔 때 세금 폭탄 피하는 법! 1세대 1주택 비과세 체크까지'
---

## 🏠 집 팔 때 남는 게 있을까?

양도세는 **'번 만큼 내는 세금'**입니다. 5억에 사서 10억에 팔았다면, 차익 5억에 대해 세금을 냅니다.

- **1세대 1주택 비과세:** 2년 이상 보유(조정지역은 거주)하고 12억 원 이하에 팔면 세금이 **0원**입니다.
- **장기보유특별공제:** 오래 가지고 있을수록 세금을 깎아줍니다. (최대 80%)

---

### 🧮 양도세 간편 계산기

<style>
  .calc-box-trans { background: #fff5f5; padding: 25px; border-radius: 12px; margin-top: 20px; border: 1px solid #ffc9c9; }
  .calc-btn-trans { width: 100%; padding: 15px; background: #fa5252; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-trans:hover { background: #e03131; }
</style>

<div class="calc-box-trans">
  <div class="calc-row">
    <label class="calc-label">취득 가액 (만원)</label>
    <input type="number" id="buyPrice" class="calc-input" placeholder="예: 50000 (5억)">
  </div>
  <div class="calc-row">
    <label class="calc-label">양도 가액 (만원)</label>
    <input type="number" id="sellPrice" class="calc-input" placeholder="예: 80000 (8억)">
  </div>
  <div class="calc-row">
    <label class="calc-label">보유 기간</label>
    <select id="holdYear" class="calc-input">
      <option value="1">1년 미만 (70% 중과)</option>
      <option value="2">2년 미만 (60% 중과)</option>
      <option value="3">2년 이상 (일반세율)</option>
    </select>
  </div>
  <button class="calc-btn-trans" onclick="calcTransfer()">세금 계산하기</button>

  <div id="transResult" class="result-area" style="border-color: #fa5252;">
    <h3>💸 양도세 결과</h3>
    <p>양도 차익: <span id="profit">0</span> 만원</p>
    <p>예상 납부세액: <strong id="finalTax" style="color: #c92a2a; font-size: 24px;">0</strong> 원</p>
    <p style="font-size: 12px; color: #888;">* 필요경비, 기본공제(250만) 포함 약식 계산입니다.</p>
  </div>
</div>

<script>
function calcTransfer() {
  const buy = Number(document.getElementById('buyPrice').value) * 10000;
  const sell = Number(document.getElementById('sellPrice').value) * 10000;
  const hold = document.getElementById('holdYear').value;

  if(!buy || !sell) { alert("금액을 입력해주세요."); return; }

  const profit = sell - buy - 2500000; // 기본공제 250만 차감
  if (profit <= 0) {
    document.getElementById('profit').innerText = "0";
    document.getElementById('finalTax').innerText = "0";
    document.getElementById('transResult').style.display = 'block';
    return;
  }

  let tax = 0;
  
  if (hold === "1") {
    tax = profit * 0.77; // 지방세 포함 77%
  } else if (hold === "2") {
    tax = profit * 0.66; // 지방세 포함 66%
  } else {
    // 일반세율 (6~45%) + 지방세 10%
    let baseTax = 0;
    if (profit <= 14000000) baseTax = profit * 0.06;
    else if (profit <= 50000000) baseTax = profit * 0.15 - 1260000;
    else if (profit <= 88000000) baseTax = profit * 0.24 - 5760000;
    else if (profit <= 150000000) baseTax = profit * 0.35 - 15440000;
    else if (profit <= 300000000) baseTax = profit * 0.38 - 19940000;
    else if (profit <= 500000000) baseTax = profit * 0.40 - 25940000;
    else if (profit <= 1000000000) baseTax = profit * 0.42 - 35940000;
    else baseTax = profit * 0.45 - 65940000;
    
    tax = baseTax * 1.1;
  }

  document.getElementById('profit').innerText = Math.round((sell-buy)/10000).toLocaleString();
  document.getElementById('finalTax').innerText = Math.floor(tax).toLocaleString();
  document.getElementById('transResult').style.display = 'block';
}
</script>
