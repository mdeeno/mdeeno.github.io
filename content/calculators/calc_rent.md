---
title: '🔄 전월세 전환율 계산기'
date: 2026-01-01
summary: '전세 3억을 월세로 바꾸면 얼마? 법정 전환율 계산'
---

## 🔄 전세 ↔ 월세, 얼마가 적당할까?

임대차 계약 갱신 시 보증금을 올리거나 내릴 때, 법정 **전월세 전환율**을 꼭 확인해야 합니다.

- **법정 전환율:** 기준금리 + 2.0% (주택임대차보호법 기준)
- 집주인이 터무니없는 월세를 요구한다면? 이 계산기로 반박하세요!

---

### 🧮 전환 계산기



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



<div class="calc-box-rent">
  <div class="calc-row">
    <label class="calc-label">전환할 보증금 액수 (만원)</label>
    <input type="number" id="rentDeposit" class="calc-input" placeholder="예: 10000 (1억을 월세로)">
  </div>
  <div class="calc-row">
    <label class="calc-label">적용 전환율 (%)</label>
    <input type="number" id="rentRate" class="calc-input" placeholder="예: 5.0 (보통 4~6%)">
  </div>
  <button class="calc-btn-rent" onclick="calcRent()">월세 얼마?</button>

  <div id="rentResult" class="result-area" style="border-color: #20c997;">
    <h3>🔄 전환 결과</h3>
    <p>보증금 <strong>1억</strong>을 줄이면,</p>
    <p>월세는 <strong id="rentMonthly" style="color: #087f5b; font-size: 24px;">0</strong> 원 늘어납니다.</p>
  </div>
</div>

<script>
function calcRent() {
  const deposit = Number(document.getElementById('rentDeposit').value) * 10000;
  const rate = Number(document.getElementById('rentRate').value) / 100;

  if(!deposit) { alert("금액을 입력해주세요."); return; }

  // 연 이자 / 12개월
  const monthlyRent = (deposit * rate) / 12;

  document.getElementById('rentMonthly').innerText = Math.round(monthlyRent).toLocaleString();
  document.getElementById('rentResult').style.display = 'block';
}
</script>

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">전월세 전환 후 대출 한도가 궁금하신가요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO 리스크 진단으로 내 단지의 자금 계획을 시뮬레이션해 보세요.</p>
  <a href="https://mdeeno.com/member?utm_source=blog&utm_medium=calc_cta&utm_campaign=calc_rent" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    재건축 리스크 무료 진단 →
  </a>
</div>

<p style="font-size:12px;color:#888;margin-top:16px;">※ 본 계산기는 참고용이며, 실제 전환율은 한국은행 기준금리 변동 및 지역 관행에 따라 달라질 수 있습니다.</p>
