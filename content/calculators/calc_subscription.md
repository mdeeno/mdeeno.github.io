---
title: '🏆 아파트 청약 가점 계산기'
date: 2026-01-01
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

<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1.05rem;font-weight:700;color:#1e40af;margin:0 0 8px;">청약 가점이 낮아도 재건축 투자가 가능할까요?</p>
  <p style="font-size:0.9rem;color:#374151;margin:0 0 14px;">M-DEENO 리스크 진단으로 재건축 조합원 입장에서의 리스크를 확인해 보세요.</p>
  <a href="https://mdeeno.com/member?utm_source=blog&utm_medium=calc_cta&utm_campaign=calc_subscription" target="_blank" rel="noopener noreferrer"
     style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">
    재건축 리스크 무료 진단 →
  </a>
</div>

<p style="font-size:12px;color:#888;margin-top:16px;">※ 본 계산기는 참고용이며, 실제 가점은 청약홈(applyhome.co.kr)에서 정확한 산정 기준을 확인하시기 바랍니다.</p>
