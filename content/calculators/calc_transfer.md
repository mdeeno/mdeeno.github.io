---
title: '💸 양도소득세 계산기 (2026년 최신)'
date: 2026-01-01
summary: '집 팔 때 세금 폭탄 피하는 법! 1세대 1주택 비과세 체크까지'
---

## 🏠 집 팔 때 남는 게 있을까?

재건축 사업에서 **현금청산을 선택하거나 조합원 지위를 매도**할 때도 양도소득세가 발생합니다. 청산 금액과 원래 취득가액의 차이에 세금이 부과되므로, 실제 수익을 계산하려면 반드시 사전 시뮬레이션이 필요합니다.

- 관련 분석: [재건축 현금청산: 내 집 뺏기는 걸까, 돈 버는 기회일까?](/posts/reconstruction/)
- 관련 분석: [재건축 10년의 여정: 수익률을 가르는 결정적 단계는?](/posts/reconstruction/)

양도세는 **'번 만큼 내는 세금'**입니다. 5억에 사서 10억에 팔았다면, 차익 5억에 대해 세금을 냅니다.

- **1세대 1주택 비과세:** 2년 이상 보유(조정지역은 거주)하고 12억 원 이하에 팔면 세금이 **0원**입니다.
- **장기보유특별공제:** 오래 가지고 있을수록 세금을 깎아줍니다. (최대 80%)

---

### 🧮 양도세 간편 계산기



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

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">청산 vs 보유, 내 단지는 어떤 선택이 유리할까요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO Prop-Logic™ 엔진이 양도세·분담금·수익성을 종합 시뮬레이션합니다.</p>
  <a href="https://mdeeno.com/member" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    청산·보유 비교 분석 시작 →
  </a>
</div>
