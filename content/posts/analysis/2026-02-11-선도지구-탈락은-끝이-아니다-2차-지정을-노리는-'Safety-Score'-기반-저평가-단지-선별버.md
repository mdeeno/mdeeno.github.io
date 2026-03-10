---
title: "선도지구 탈락은 끝이 아니다: 2차 지정을 노리는 'Safety Score' 기반 저평가 단지 선별법"
date: 2026-02-11 22:49:41
draft: false
categories:
- 재건축/재개발
tags:
- 1기 신도시 선도지구
- 재건축 사업성
- 분당 재건축
- 일산 재건축
- 평촌 재건축 시세
description: '선도지구 탈락은 끝이 아니다: 2차 지정을 노리는 ''Safety Score'' 기반 저평가 단지 선별법'
image: https://raw.githubusercontent.com/mdeeno/mdeeno.github.io/main/static/images/chart-1770904196.png
---

![전망 차트](https://raw.githubusercontent.com/mdeeno/mdeeno.github.io/main/static/images/chart-1770904196.png)
_▲ AI 분석 데이터 (2026-02-11 22:49:41 기준)_

---

<div class="lab-card">
1기 신도시 선도지구 발표 직후, 탈락 단지들의 실망 매물이 쏟아지며 단기 시세 조정이 불가피해졌습니다. 하지만 이는 역설적으로 2차 지정을 노리는 투자자들에게 최적의 진입 시점이 될 수 있습니다. 본 포스팅에서는 'Safety Score'를 통해 2차 지정 가능성이 높은 저평가 우량 단지를 분석합니다.
</div>

### 선도지구 탈락 단지의 단기 시세 하락 리스크 점검

선도지구에서 제외된 단지들은 당분간 **매수 심리 위축**과 **매물 적체** 현상을 겪을 가능성이 매우 높습니다.

- 기대감이 선반영되었던 호가가 빠지며 급매물이 출현할 수 있는 시기입니다.
- 특히 통합 재건축 동의율이 낮았던 단지는 투자 우선순위에서 밀려 하락폭이 더 클 수 있습니다.
- 하지만 정부의 2차, 3차 지정 로드맵이 확고하므로 **일시적 가격 눌림목**을 활용해야 합니다.

### 투자자를 위한 Safety Score (사업 안정성) 산출 공식

단순히 가격이 싸다고 매수하는 것은 위험합니다. 2차 지정을 선점하기 위해서는 **사업 안정성 점수**를 따져봐야 합니다.

<div class="lab-formula-box">
Safety Score = (평균 대지 지분 ÷ 현재 용적률) × 통합 재건축 참여 가구 수
</div>

- **평균 대지 지분**: 지분이 높을수록 향후 추가 분담금 경계선에서 자유롭습니다.
- **용적률**: 현재 용적률이 180% 이하인 단지가 사업성 확보에 절대적으로 유리합니다.
- **통합 규모**: 3,000세대 이상의 대단지 통합 재건축일수록 정부의 가산점 부여 확률이 높습니다.

### 실제 단지별 시세 및 사업성 비교 분석

현재 시장에서 주목받는 주요 단지들의 84㎡ 기준 현황을 비교해 보겠습니다.

- **분당 시범삼성/한양 (선도지구 선정)**: 현재 호가 **16억~17.5억 원**. 이미 높은 프리미엄이 형성되어 추격 매수 시 수익률이 제한적일 수 있습니다.
- **일산 마두동 백마 1, 2단지 (2차 유력 후보)**: 현재 호가 **7.2억~8.3억 원**. 선도지구 탈락 후 소폭 조정 중이나, 역세권 입지와 높은 동의율로 2차 지정 가능성이 매우 높습니다.
- **평촌 귀인동 현대 4차 (저평가 구간)**: 현재 호가 **9.5억~10.5억 원**. 학원가 인접성에도 불구하고 사업 속도에 대한 우려로 저평가되어 있으나, 대지 지분이 양호하여 Safety Score가 높게 나타납니다.

### 2차 지정을 노리는 투자자의 행동 전략

지금은 공포에 팔 때가 아니라, **동의율 80% 이상**을 달성한 탈락 단지를 리스트업할 때입니다.

- 단기적으로는 가격이 하락하겠으나, 2025년 하반기 2차 지정 공고 시점에 다시 전고점을 돌파할 것입니다.
- 취득세와 보유세 부담을 고려하여 실거주 요건을 채울 수 있는 단지를 우선순위에 두십시오.
- 특히 지자체별 배점 기준에서 '주민 동의율' 배점이 가장 높으므로, 단지 내 커뮤니티 활성화 정도를 반드시 확인해야 합니다.

<script>
  async function submitBlogLead() {
    const email = document.getElementById('blog-lead-email').value.trim();
    const btn = document.getElementById('blog-lead-btn');
    if (!email) return alert('이메일을 입력해주세요.');
    btn.innerText = '전송 중...';
    btn.disabled = true;
    try {
      const res = await fetch('https://mdeeno.com/api/waitlist', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: email, source: window.location.pathname })
      });
      if (!res.ok) throw new Error('서버 오류: ' + res.status);
      alert('✅ 사전 신청이 완료되었습니다!');
      document.getElementById('blog-lead-email').value = '';
    } catch (err) {
      alert('오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    } finally {
      btn.innerText = '사전 신청';
      btn.disabled = false;
    }
  }
</script>

---

> **※ 본 글은 M-DEENO의 부동산 의사결정 연구 노트입니다.**

---

### 🛑 1기 신도시 선도지구, 재건축 사업성, 분당 재건축, 일산 재건축, 평촌 재건축 시세 투자, 고민되시나요?

부동산은 **타이밍**입니다.
내 자금 상황에 맞는 **최적의 매물**을 지금 확인하세요.



{{< mdeeno_cpa type="loan" >}}

{{< ad_cpa type="finance" >}}
