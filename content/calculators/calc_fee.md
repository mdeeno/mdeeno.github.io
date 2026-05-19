---
title: '🤝 부동산 중개수수료(복비) 계산기'
date: 2026-01-01
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

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">중개보수 외에 취득세·양도세도 궁금하신가요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO 리스크 진단으로 재건축 비용을 종합 분석해 보세요.</p>
  <a href="https://mdeeno.com/member?utm_source=blog&utm_medium=calc_cta&utm_campaign=calc_fee" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    재건축 리스크 무료 진단 →
  </a>
</div>

<p style="font-size:12px;color:#888;margin-top:16px;">※ 본 계산기는 참고용이며, 실제 중개보수는 시/도 조례 및 중개사와의 협의에 따라 달라질 수 있습니다.</p>
