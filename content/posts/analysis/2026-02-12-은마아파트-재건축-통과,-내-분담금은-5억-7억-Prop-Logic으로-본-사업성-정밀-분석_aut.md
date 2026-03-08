---
title: 은마아파트 재건축 통과, 내 분담금은 5억? 7억? Prop-Logic으로 본 사업성 정밀 분석
date: 2026-02-12 19:46:31
draft: false
categories:
- 재건축/재개발
tags:
- 은마아파트 재건축
- 은마아파트 분담금
- 대치동 부동산 전망
- 재건축 사업성 분석
- 부동산투자
description: 은마아파트 재건축 통과, 내 분담금은 5억? 7억? Prop-Logic으로 본 사업성 정밀 분석
image: https://raw.githubusercontent.com/mdeeno/mdeeno.github.io/main/static/images/chart-1770979615.png
---

![전망 차트](https://raw.githubusercontent.com/mdeeno/mdeeno.github.io/main/static/images/chart-1770979615.png)
_▲ AI 분석 데이터 (2026-02-12 19:46:31 기준)_

---

대치동 은마아파트 재건축 심의가 드디어 통과되었지만, 소유주들의 표정은 복잡하기만 합니다. 치솟는 공사비와 금리 인상 여파로 인해 과거와는 차원이 다른 **추가 분담금** 공포가 현실화되고 있기 때문입니다.

<div class="lab-card">
은마아파트 재건축은 심의 통과로 큰 산을 넘었으나, 공사비 급증으로 인해 84㎡ 기준 예상 분담금이 당초 예상보다 20~30% 상승할 가능성이 큽니다. 사업 안정성 확보를 위한 정밀한 수지 분석이 필요한 시점입니다.
</div>

### 은마아파트 재건축 현주소와 시세 분석

최근 은마아파트 전용 **84㎡ 실거래가는 약 26억~27억 원** 선을 형성하며 심의 통과 기대감을 반영하고 있습니다. 하지만 이는 인근 신축 단지인 '래미안 대치 팰리스'의 시세와 비교했을 때 여전히 상당한 격차를 보입니다.

- **은마아파트**: 84㎡ 기준 약 26.5억 원 (재건축 추진 중)
- **잠실 주공 5단지**: 82㎡ 기준 약 29억 원 (한강변 고층 재건축 호재)
- **개포 경남**: 96㎡ 기준 약 28억 원 (통합 재건축 추진 및 사업성 우수)

### Prop-Logic으로 분석한 예상 분담금 공식

재건축 사업의 핵심은 '비례율', 즉 **사업 안정성 점수**입니다. 최근 공사비가 평당 800만 원을 넘어서면서 소유주가 부담해야 할 금액은 기하급수적으로 늘고 있습니다.

<div class="lab-formula-box">
예상 분담금 = (조합원 분양가) - (종전 자산 평가액 × 사업 안정성 점수)
</div>

- 현재 은마아파트의 사업 안정성 점수는 약 **90~95%** 수준으로 예측됩니다.
- 일반 분양가가 평당 7,000만 원을 상회하지 못할 경우 분담금은 더 늘어납니다.
- 84㎡ 소유주가 동일 평형을 분양받을 때 최소 **5억 원 이상의 분담금**이 발생할 수 있습니다.

### 주변 단지와의 사업성 비교 분석

대치동 은마와 함께 강남 재건축의 '대어'로 꼽히는 단지들과의 비교는 필수적입니다. 사업 속도와 일반 분양 물량에 따라 수익성이 크게 갈리기 때문입니다.

- **잠실 주공 5단지**: 용도지역 상향을 통해 최고 70층 재건축을 추진하며 사업성을 극대화하고 있습니다.
- **개포 경남·우성·현대**: 통합 재건축을 통해 대단지 프리미엄과 공공기여 최소화를 노리고 있습니다.
- **은마아파트**: 단지 규모는 가장 크지만, 교육 환경 보호 구역 등 규제가 많아 공사비 관리가 최대 관건입니다.

### 투자자가 주의해야 할 리스크 포인트

재건축 심의 통과가 곧 '수익'을 보장하는 시대는 끝났습니다. 분담금 경계선을 넘어서는 순간 실질 수익률은 급격히 하락할 수 있습니다.

- **공사비 증액**: 시공사 선정 과정에서 발생할 수 있는 공사비 갈등은 사업 기간을 늦추는 주범입니다.
- **기부채납 비율**: 서울시와의 협의 과정에서 공공기여 비율이 높아지면 조합원의 몫은 줄어듭니다.
- **금리 변동성**: 이주비 대출 및 사업비 대출 이자는 사업성 점수를 깎아먹는 핵심 요인입니다.

결론적으로 은마아파트는 상징성과 입지 면에서 독보적이지만, **실질 분담금 규모**에 따라 향후 매수세의 향방이 결정될 것입니다.

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
      alert('✅ 베타 신청이 완료되었습니다!');
      document.getElementById('blog-lead-email').value = '';
    } catch (err) {
      alert('오류가 발생했습니다. 잠시 후 다시 시도해주세요.');
    } finally {
      btn.innerText = '베타 신청';
      btn.disabled = false;
    }
  }
</script>

---

> **※ 본 글은 M-DEENO의 부동산 의사결정 연구 노트입니다.**

---

### 🛑 은마아파트 재건축, 은마아파트 분담금, 대치동 부동산 전망, 재건축 사업성 분석 투자, 고민되시나요?

부동산은 **타이밍**입니다.
내 자금 상황에 맞는 **최적의 매물**을 지금 확인하세요.



{{< mdeeno_cpa type="loan" >}}

{{< ad_cpa type="finance" >}}
