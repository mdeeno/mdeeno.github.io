---
title: '🏆 아파트 청약 가점 계산기'
date: 2026-01-26
layout: 'page'
summary: '내 점수로 서울 아파트 당첨 가능할까? 무주택/부양가족 점수 산출'
---

## 🎫 청약, 점수가 깡패다!

민간분양 아파트는 **가점제**로 당첨자를 뽑습니다. 84점 만점에 몇 점인지 미리 알아야 전략을 짤 수 있습니다.

- **무주택 기간 (32점):** 길수록 좋습니다. (만 30세부터 산정)
- **부양가족 수 (35점):** 많을수록 깡패입니다. (1명당 5점)
- **청약통장 가입기간 (17점):** 오래 묵힐수록 유리합니다.

---

### 🧮 가점 계산기

<style>
  .calc-box-sub { background: #e7f5ff; padding: 25px; border-radius: 12px; margin-top: 20px; border: 1px solid #74c0fc; }
  .calc-btn-sub { width: 100%; padding: 15px; background: #339af0; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 10px; }
  .calc-btn-sub:hover { background: #1c7ed6; }
</style>

<div class="calc-box-sub">
  <div class="calc-row">
    <label class="calc-label">1. 무주택 기간 (년)</label>
    <select id="subNoHouse" class="calc-input">
      <option value="0">1년 미만 (2점)</option>
      <option value="2">1년~2년 (4점)</option>
      <option value="10">5년~6년 (12점)</option>
      <option value="20">10년~11년 (22점)</option>
      <option value="32">15년 이상 (32점 만점)</option>
    </select>
  </div>
  <div class="calc-row">
    <label class="calc-label">2. 부양 가족 수 (명, 본인제외)</label>
    <select id="subFamily" class="calc-input">
      <option value="5">0명 (5점)</option>
      <option value="10">1명 (10점)</option>
      <option value="15">2명 (15점)</option>
      <option value="20">3명 (20점)</option>
      <option value="25">4명 (25점)</option>
      <option value="30">5명 (30점)</option>
      <option value="35">6명 이상 (35점 만점)</option>
    </select>
  </div>
  <div class="calc-row">
    <label class="calc-label">3. 통장 가입 기간 (년)</label>
    <select id="subBank" class="calc-input">
      <option value="1">6개월~1년 (2점)</option>
      <option value="7">5년~6년 (7점)</option>
      <option value="12">10년~11년 (12점)</option>
      <option value="17">15년 이상 (17점 만점)</option>
    </select>
  </div>
  <button class="calc-btn-sub" onclick="calcSub()">가점 확인하기</button>

  <div id="subResult" class="result-area" style="border-color: #339af0;">
    <h3>🏆 나의 청약 가점</h3>
    <p>총점: <strong id="totalScore" style="color: #1864ab; font-size: 30px;">0</strong> / 84점</p>
    <p id="scoreComment" style="font-weight: bold;"></p>
  </div>
</div>

<script>
function calcSub() {
  const p1 = Number(document.getElementById('subNoHouse').value);
  const p2 = Number(document.getElementById('subFamily').value);
  const p3 = Number(document.getElementById('subBank').value);

  const total = p1 + p2 + p3;
  const comment = document.getElementById('scoreComment');

  document.getElementById('totalScore').innerText = total;
  document.getElementById('subResult').style.display = 'block';

  if(total >= 60) {
    comment.innerHTML = "🎉 서울 인기 단지도 노려볼 만한 <strong>안정권</strong>입니다!";
    comment.style.color = "green";
  } else if(total >= 40) {
    comment.innerHTML = "🤔 비인기 타입이나 <strong>경기/인천권</strong> 당첨 가능성이 있습니다.";
    comment.style.color = "#f59f00";
  } else {
    comment.innerHTML = "😢 가점이 낮습니다. <strong>추첨제</strong> 물량을 공략하세요.";
    comment.style.color = "red";
  }
}
</script>
