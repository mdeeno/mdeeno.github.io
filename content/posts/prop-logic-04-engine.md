---
title: '📊 Prop-Logic v1.1: 내 아파트 재건축, 추가 분담금은 얼마일까?'
date: 2026-02-05T19:00:00+09:00
categories: ['Prop-Logic']
weight: 1
math: true
showPostNavLinks: false
---

<div class="lab-stepper">
  <a href="/posts/prop-logic-01-intro/" class="lab-step-dot done">1</a>
  <a href="/posts/prop-logic-02-assumptions/" class="lab-step-dot done">2</a>
  <a href="/posts/prop-logic-03-limitations/" class="lab-step-dot done">3</a>
  <a href="/posts/prop-logic-04-engine/" class="lab-step-dot active">4</a>
</div>
<div class="lab-step-labels">
  <div class="lab-step-label">연구 개요</div>
  <div class="lab-step-label">로직 설계</div>
  <div class="lab-step-label">한계 고지</div>
  <div class="lab-step-label active">시뮬 실행</div>
</div>

<div class="lab-formula-box">
  <h2 class="color-blue">💻 Prop-Logic Laboratory</h2>
  <p class="lab-p1">공사비 변화에 따른 사업 안정성 체험 시뮬레이터</p>
  <p class="lab-p3">도시공학 및 정비사업 사업성 검토에서 실제 사용되는 수익·비용 구조를 기반으로 설계되었습니다.</p>
</div>

### 🧪 시뮬레이터 개요 및 목적

본 시뮬레이터는 '**공사비 변화**'가 '**조합원 분담금**'에 '**어떤 영향**'을
주는지를 한눈에 체감할 수 있도록 설계되었습니다.

'**실제 정비사업 실무**'에서 사용되는 '**사업성 검토 구조**'를 바탕으로,  
'**일반 조합원**'도 이해할 수 있도록 '**핵심 가정만 단순화**'해 반영했습니다.
<br>

<small>※ 현재 평균 기준(Base 시나리오) 설명</small><br>
본 시뮬레이터의 ‘**현재 평균 기준**’ 시나리오는  
'**서울 외곽**' 및 '**수도권 주요 주거지**'의
'**일반적인 재건축 사업 구조**'를 기준점으로 삼고 있습니다.

초고가 하이엔드 단지나 지방 소규모 사업장이 아닌,  
'**조합원 분담금**'에 대한 '**불확실성**'과 '**논쟁이 가장 자주 발생하는 구간**'을 상정한 시나리오입니다.

<div class="lab-formula-box">
  <h2>Prop-Logic:<br> 우리 단지 사업안전도 분석기</h2>
  <div class="lab-formula-text">
    <!-- $$R = \frac{V_{after} - C_{total}}{V_{before}} \times 100$$ -->
    $$점수(R) = \frac{분양수익 - 총공사비}{종전자산가치} \times 100$$
  </div>
  <p class="lab-formula-caption">* <strong>점수(R)가 100 미만</strong>으로 떨어지면<br> 
  내가 내야 할 돈(추가 분담금)이 생길 가능성이 커집니다.</p>
</div>

<div class="lab-engine-container">
  <h3 style="text-align: center;">📊 실시간 구조 분석 엔진 v1.1</h3>
  <div class="lab-input-group">
    <p><span>1️⃣ 우리 단지 정보 입력</span></p>
    <div class="lab-grid">
      <div>
        <label class="lab-label">건축 연면적 (평)</label>
        <input type="number" id="input-building-area" value="5000" class="lab-input">
      </div>
      <div>
        <label class="lab-label">종전자산 평가액 (억원)</label>
        <input type="number" id="input-asset-value" value="250" class="lab-input">
      </div>
      <p style="font-size: 0.75rem; color: #888;">* 가치(종전자산): 현재 단지 내 땅과 건물의 전체 평가액입니다.</p>
    </div>
  <hr>
    <div style="display: flex; justify-content: space-between;">
      <label><span>2️⃣ 평당 공사비 설정 (만원)</span></label>
      <input type="number" id="input-cost-number" value="900" style="width: 80px; height: 40px; margin-left: 20px; padding: 8px; border: 1px solid #8d8d8d; border-radius: 6px; text-align: right; font-weight: bold; background: #ffffff; color: #888;">
    </div>
    <input type="range" id="input-cost-slider" min="500" max="1500" step="10" value="900" style="width: 100%; cursor: pointer;">
  </div>
</div>

<!-- 모바일 UX 분리용 간격 -->
<div class="lab-mobile-spacer"></div>
<div class="lab-input-group lab-scenario-card">
  <p class="lab-label lab-subtle-label">📍 시장 환경 시나리오 (가정 비교)</p>
  <div class="lab-grid-3 scenario-grid">
    <label class="scenario-option">
      <input type="radio" name="market-scenario" value="base" checked onchange="updateScenario()">
    <span>현재 평균 기준</span> <br>
    </label>
    <label class="scenario-option">
      <input type="radio" name="market-scenario" value="stress" onchange="updateScenario()">
      <span>최악의 상황 가정</span> <br>
    </label>
    <label class="scenario-option">
      <input type="radio" name="market-scenario" value="high" onchange="updateScenario()">
      <span>분양가 최고 구간</span> <br>
    </label>
  </div>
  
<div class="scenario-guide">
  <ul class="lab-small-text" style="list-style: none; padding-left: 0;">
    <li><strong>현재 평균</strong> · 수도권 일반적 사업 구조</li>
    <li><strong>최악 가정</strong> · 금리·공사비 리스크 동시 발생</li>
    <li><strong>최고 구간</strong> · 고분양가 + 고사양으로 공사비·리스크 동반 상승</li>
  </ul>
  <p class="lab-accent-text" style="margin-top: 10px;">
    ※ 실제 조합 회의에서는 이 세 가정을 동시에 검토합니다.
  </p>
</div>

<div class="lab-formula-box lab-result-focus">
  <p class="lab-subtitle">📊 사업 안정성 점수</p>
  <div class="lab-score-display">
    <span id="output-proportion-ratio">115.00</span><span class="lab-p1"> 점</span>
  </div>
  <p id="output-status-message" class="lab-p1" style="margin-top: 15px;"></p>
  <p class="lab-small-text" style="margin-top: 10px; opacity: 0.8;">
  ※ 분양 수익은 유효 분양 가능 면적(eff)을 반영한 추정치입니다.<br>
  ※ 본 결과는 일반분양가·용적률을 고정한 상태에서 공사비 변화만을 반영한 시뮬레이션입니다.
  </p>
  <p id="output-detail-description" class="lab-p1 color-red"></p>
</div>

<!-- CTA -->
<div class="lab-cta-section">
  <p class="lab-p3 color-orange" style="margin-bottom: 8px;">
    이 점수는 ‘판단의 출발점’일 뿐입니다.
  </p>
  <p class="lab-small-text" style="margin-bottom: 14px;">
    * 실제 단지 여건에 따라 결과는 크게 달라질 수 있습니다.
  </p>
  <a href="javascript:generateMailLink('soft')" class="lab-btn">
    🔍 우리 단지 조건으로 한 번 더 검토해보기
  </a>
</div>
<br>
<p class="lab-small-text">
* 가구 수 및 지분 구조를 단순화한 평균 추정치입니다. <br>
* 100점 아래로 내려가면 추가 분담금 발생 가능성이 생깁니다.
</p>

<script>

async function calc() {
  const data = {
    area: document.getElementById('input-building-area').value,
    asset_value: document.getElementById('input-asset-value').value,
    cost: document.getElementById('input-cost-number').value,
    scenario: document.querySelector('input[name="market-scenario"]:checked').value
  };

  // 서버로 데이터 전송 (공식은 서버 안에 있음)
  try {
    const response = await fetch("https://prop-logic-engine.onrender.com/v1/calc", {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(data)
    });
  
    if (!response.ok) throw new Error('Network response was not ok');
    const result = await response.json();

    // 1. 점수 출력 및 색상 적용
    const ratioEl = document.getElementById('output-proportion-ratio');
    ratioEl.innerText = result.score;
    ratioEl.style.color = result.color;

    // 2. 상태 메시지 및 상세 설명 업데이트
    const statusMsgEl = document.getElementById('output-status-message');
    statusMsgEl.innerText = result.status;
    statusMsgEl.style.color = result.color;

    document.getElementById('output-detail-description').innerText = result.description;
    
    // 3. CTA 버튼 문구 동적 업데이트 (서버에서 결정된 멘트)
    const ctaBtnText = document.getElementById('dynamicCtaText');
    if (ctaBtnText) {
      ctaBtnText.innerText = result.cta_text;
    }
  } catch (error) {
    // 4. 에러 발생 시 처리 (서버 다운, 네트워크 단절 등)
    console.error('시뮬레이션 호출 실패:', error);
    
    const statusMsgEl = document.getElementById('output-status-message');
    if (statusMsgEl) {
      statusMsgEl.innerText = "🚨 시스템 점검 중입니다.";
      statusMsgEl.style.color = "#e74c3c";
    }
    
    const descEl = document.getElementById('output-detail-description');
    if (descEl) {
      descEl.innerText = "잠시 후 다시 시도하거나 관리자에게 문의하세요.";
    }
  }
}

// 4. 시나리오 제어 및 CTA 합성
function updateScenario() {
  const radio = document.querySelector('input[name="market-scenario"]:checked');
  if (!radio) return;
  
  calc(); 
}

// 5. 초기화 및 이벤트 바인딩 (DOM 로드 후 실행 보장)
function init() {
  const ids = ['input-cost-slider', 'input-cost-number', 'input-building-area', 'input-asset-value'];
  
  ids.forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('input', (e) => {
        // 슬라이더-숫자창 실시간 동기화
        if (id === 'input-cost-slider') document.getElementById('input-cost-number').value = e.target.value;
        if (id === 'input-cost-number') document.getElementById('input-cost-slider').value = e.target.value;
        calc();
      });
    }
  });

  calc(); // 첫 실행
}

// 페이지 로드가 완전히 끝난 후 실행
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}

// 메일 링크 생성 함수
function generateMailLink(type = "soft") {
  const score = document.getElementById('output-proportion-ratio').innerText;
  const level = type === "hard" ? "정밀 검증 요청" : "1차 구조 검토 요청";
  const body = encodeURIComponent(
    `[요청 유형] ${level}\n안정성 점수: ${score}점\n현재 설정 기준으로 분석을 요청합니다.`
  );
  window.location.href =
    `mailto:mdeeno.official@gmail.com?subject=[Prop-Logic 분석]&body=${body}`;
}
</script>

<hr>
<p class="lab-subtitle">📌 주의사항</p>
<p> 재건축/재개발 정비사업에서 <span>'공사비 10만원'</span>의 차이는 우리 집의 <span>'천만 원'</span>을 결정짓습니다.</p>
<p>위 수치는 사용자님의 입력값에 기초한 산술적 시뮬레이션이며, 실제 사업성 판단은 단지의 대지 지분, 용적률, 일반분양가 등 전문가의 정밀한 변수 해석이 수반되어야 합니다.</p>

<div style="text-align: center; margin-top: 50px;">
<p>👉 우리 단지, 이 조건으로 괜찮을까?</p>

<!-- 하단 CTA : 시나리오/점수 기반 동적 CTA -->
<a href="javascript:generateMailLink('hard')" class="lab-btn lab-btn-cta">
  <span id="dynamicCtaText">점수 기준으로 전문가 검증하기</span>
</a>

---

> **※ 본 글은 PropTech Lab의 정비사업·부동산 의사결정 구조 연구 과정에서 정리된 사례 분석 리포트의 일부입니다.**
>
> 실제 사업 조건, 지역, 시점에 따라 결과는 달라질 수 있습니다.
