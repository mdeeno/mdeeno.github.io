---
title: '🏠 부동산 취득세 계산기 (2026년 기준)'
date: 2026-01-26
layout: 'page'
summary: '집 살 때 필수! 1주택자부터 다주택자까지 취득세 자동 계산'
---

## 🧾 취득세, 미리 준비 안 하면 낭패!

부동산을 살 때는 집값만 있으면 안 됩니다. 집값의 **1.1% ~ 12%**에 달하는 취득세를 현금으로 준비해야 등기를 칠 수 있습니다.

- **1주택자:** 1% ~ 3% (비교적 저렴)
- **2주택자:** 1% ~ 8% (조정지역 여부에 따라 다름)
- **다주택자/법인:** 최대 12% (중과세 폭탄 주의!)

---

### 🧮 주택 취득세 계산기

<style>
  .calc-box-tax { background: #f3f0ff; padding: 25px; border-radius: 12px; margin-top: 20px; border: 1px solid #d0bfff; }
  .calc-btn-tax { width: 100%; padding: 15px; background: #7950f2; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-tax:hover { background: #6741d9; }
</style>

<div class="calc-box-tax">
  <div class="calc-row">
    <label class="calc-label">매수 금액 (만원)</label>
    <input type="number" id="taxPrice" class="calc-input" placeholder="예: 60000">
  </div>
  <div class="calc-row">
    <label class="calc-label">취득 후 주택 수</label>
    <select id="taxCount" class="calc-input">
      <option value="1">1주택 (무주택자 매수)</option>
      <option value="2">2주택 (비조정지역/일시적)</option>
      <option value="multi">3주택 이상 / 조정 2주택</option>
    </select>
  </div>
  <button class="calc-btn-tax" onclick="calcTax()">세금 확인하기</button>

  <div id="taxResult" class="result-area" style="border-color: #7950f2;">
    <h3>💸 납부 예상 세액</h3>
    <p>취득세율: <span id="taxRateRes">0</span> %</p>
    <p>총 납부액: <strong id="taxTotal" style="color: #5f3dc4; font-size: 24px;">0</strong> 원</p>
    <p style="font-size: 12px; color: #888;">* 지방교육세, 농어촌특별세 포함 대략적 수치입니다.</p>
  </div>
</div>

<script>
function calcTax() {
  const price = Number(document.getElementById('taxPrice').value) * 10000;
  const count = document.getElementById('taxCount').value;

  if(!price) { alert("금액을 입력해주세요."); return; }

  let baseRate = 0.01; // 기본 1%

  if (count === 'multi') {
    baseRate = 0.08; // 다주택 중과 (보수적으로 8% 설정, 최대 12%)
  } else if (count === '2') {
    baseRate = 0.01; // 비조정 2주택 가정
    if (price >= 600000000 && price <= 900000000) {
        // 6억~9억 구간 사선형 세율
        baseRate = (price * 2 / 300000000 - 3) / 100;
    } else if (price > 900000000) {
        baseRate = 0.03;
    }
  } else {
    // 1주택자
    if (price <= 600000000) baseRate = 0.01;
    else if (price <= 900000000) baseRate = (price * 2 / 300000000 - 3) / 100;
    else baseRate = 0.03;
  }
  
  // 농특세, 지방교육세 포함 (약식: 세율 + 0.1~0.4% 정도 추가되나 단순화를 위해 10% 가산)
  let finalTax = price * baseRate * 1.1; 

  document.getElementById('taxRateRes').innerText = (baseRate * 100).toFixed(2);
  document.getElementById('taxTotal').innerText = Math.floor(finalTax).toLocaleString();
  document.getElementById('taxResult').style.display = 'block';
}
</script>
