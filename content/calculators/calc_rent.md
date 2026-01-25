---
title: '🔄 전월세 전환율 계산기'
date: 2026-01-26
layout: 'page'
summary: '전세 3억을 월세로 바꾸면 얼마? 법정 전환율 계산'
---

## 🔄 전세 ↔ 월세, 얼마가 적당할까?

임대차 계약 갱신 시 보증금을 올리거나 내릴 때, 법정 **전월세 전환율**을 꼭 확인해야 합니다.

- **법정 전환율:** 기준금리 + 2.0% (주택임대차보호법 기준)
- 집주인이 터무니없는 월세를 요구한다면? 이 계산기로 반박하세요!

---

### 🧮 전환 계산기

<style>
  .calc-box-rent { background: #e6fcf5; padding: 25px; border-radius: 12px; margin-top: 20px; border: 1px solid #96f2d7; }
  .calc-btn-rent { width: 100%; padding: 15px; background: #20c997; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-rent:hover { background: #12b886; }
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
