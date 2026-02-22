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

<div style="padding: 24px; background-color: #f8f9fa; border-left: 6px solid #ff4d4f; border-radius: 8px; margin: 30px 0; box-shadow: 0 4px 6px rgba(0,0,0,0.05);">
  <h3 style="margin: 0 0 12px 0; color: #111; font-size: 1.2rem; font-weight: bold;">🚨 Prop-Logic 정식 버전이 출시되었습니다!</h3>
  <p style="margin: 0 0 20px 0; color: #444; line-height: 1.6; font-size: 0.95rem; word-break: keep-all;">
    기존 블로그에서 제공하던 시뮬레이터가 <strong>최신 데이터와 고도화된 로직을 탑재하여 M-DEENO 공식 플랫폼으로 통합</strong>되었습니다.<br><br>
    이제 아래 공식 플랫폼에서 단 1분 만에 <strong>무료로 우리 단지의 분담금 리스크를 진단</strong>하고, 총회 제출용 <strong>상세 시나리오 리포트</strong>까지 즉시 확인해 보세요.
  </p>
  <div style="text-align: center;">
    <a href="https://mdeeno.com/mvp" target="_blank" rel="noopener noreferrer" style="display: inline-block; padding: 16px 32px; background-color: #ff4d4f; color: #fff; text-decoration: none; font-weight: bold; border-radius: 8px; font-size: 1.1rem; transition: background-color 0.2s; box-shadow: 0 4px 6px rgba(255, 77, 79, 0.3);">
      👉 우리 단지 분담금 리스크 무료 진단하기
    </a>
  </div>
</div>

---

> **※ 본 글은 M-DEENO의 정비사업·부동산 의사결정 구조 연구 과정에서 정리된 사례 분석 리포트의 일부입니다.**
>
> 실제 사업 조건, 지역, 시점에 따라 결과는 달라질 수 있습니다.

{{< mdeeno_cpa type="loan" >}}
