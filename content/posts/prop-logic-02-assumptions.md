---
title: 'Prop-Logic: 시뮬레이션 엔진의 5대 핵심 변수와 로직'
date: 2026-02-05T17:02:00+09:00
categories: ['Prop-Logic']
weight: 2
---
<div class="lab-stepper">
<a href="/posts/prop-logic-01-intro/" class="lab-step-dot done">1</a>
<a href="/posts/prop-logic-02-assumptions/" class="lab-step-dot active">2</a>
<a href="/posts/prop-logic-03-limitations/" class="lab-step-dot done">3</a>
<a href="/posts/prop-logic-04-engine/" class="lab-step-dot done">4</a>
</div>
<div class="lab-step-labels">
<div class="lab-step-label">연구 개요</div>
<div class="lab-step-label active">로직 설계</div>
<div class="lab-step-label">한계 고지</div>
<div class="lab-step-label">시뮬 실행</div>
</div>


<div class="lab-formula-box" style="text-align: left; border-left: 5px solid #0056b3; padding: 15px; margin-bottom: 30px;">
    <small style="color: #3898ff; font-weight: bold;">CHAPTER 02 / 04</small>
    <p style="margin: 5px 0 0 0; font-size: 0.95rem;"><strong>Part 2.</strong> 엔진의 핵심 변수와 로직 설계</p>
</div>

### 🧪 연구 로직의 구성

본 엔진은 다음 5가지 독립 변수의 상호작용을 통해 사업성을 산출합니다.

1. **연면적(GFA)**: 용적률에 따른 총 개발 규모
2. **평당 공사비**: 시공사 계약의 핵심 변수
3. **기타사업비율**: 금융 비용 및 운영비
4. **종전자산가액**: 조합원의 기여 자산 평가액
5. **예상 분양가**: 시장 상황에 따른 매출액

$$Total Cost = (GFA \times Cost_{pyeong}) \times (1 + Ratio_{other})$$

<div style="text-align: center; margin-top: 50px; padding-top: 20px; border-top: 1px dashed #eee;">
    <a href="/posts/prop-logic-03-limitations/" class="lab-btn">NEXT: 📌 연구의 한계 및 법적 고지 보러가기 ▶</a>
    <br><br>
    <a href="/posts/prop-logic-01-intro/" style="color: #888; text-decoration: none; font-size: 0.9rem;">◀ 연구 개요(HUB)로 돌아가기</a>
</div>

---
> **※ 본 글은 PropTech Lab의 정비사업·부동산 의사결정 구조 연구 과정에서 정리된 사례 분석 리포트의 일부입니다.**
> 
> 실제 사업 조건, 지역, 시점에 따라 결과는 달라질 수 있습니다.