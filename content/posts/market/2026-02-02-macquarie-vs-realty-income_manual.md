---
title: '은퇴자 배당주 대결! 맥쿼리인프라 vs 리얼티인컴(O) 수익률 및 안정성 완벽 비교'
date: 2026-02-01
draft: false
categories: ['부동산 분석']
tags: ['맥쿼리인프라', '리얼티인컴', '은퇴설계', '배당주투자', '월배당']
description: '한국과 미국을 대표하는 배당주 1등, 맥쿼리인프라와 리얼티인컴을 정밀 비교합니다. 2026년 최신 배당 수익률과 은퇴자를 위한 최적의 포트폴리오 전략을 공개합니다.'
image: '/images/macquarie-vs-realty-income.png'
---

## 💰 "매달 꼬박꼬박 들어오는 월세 같은 배당, 누구를 선택할까요?"

- 한국 도로 통행료를 받을까(맥쿼리), 미국 편의점 월세를 받을까(리얼티)?
- 금리 하락기, 어떤 종목이 더 강력한 주가 상승 탄력을 보여줄까요?
- 15% 배당소득세? ISA와 연금저축을 활용한 절세 끝판왕 전략은?

---

### 📊 2026년 한·미 배당 대장주 핵심 비교

| 구분 | 맥쿼리인프라 (088980) | 리얼티인컴 (O) |
| :

---

| :

---

| :

---

|
| **자산 성격** | 국내 유료도로, 교량, 데이터센터 | 미국·유럽 상업용 부동산(리테일) |
| **배당 주기** | 연 2회 (반기 배당) | **연 12회 (월배당)** |
| **2026 예상 수익률** | **약 6.6% ~ 6.8%** | **약 5.3% ~ 5.5%** |
| **배당 성장성** | 자산 만기에 따른 변동성 존재 | 600개월 이상 배당 지급 및 성장 |
| **세금 혜택** | ISA 계좌 활용 시 극대화 | 연금저축/IRP 내 국내상장 ETF로 절세 |

---

### 🚀 은퇴자를 위한 1등 배당주 정밀 분석

#### 🥇 [수익률 대장] 맥쿼리인프라 (Macquarie Korea Infrastructure Fund)

- **분석:** 국내 최대 상장 인프라 펀드로, 정부와의 실시협약을 통해 안정적인 수입을 보장받습니다. 최근 하남 데이터센터 및 동부간선도로 지하화 사업 등 신규 자산을 편입하며 포트폴리오를 확장 중입니다.
- **현재 시세:** **11,250원 내외 (2026년 2월 기준)**
- **투자 포인트:** 6% 중후반의 높은 배당 수익률이 강점입니다. 특히 2026년부터 신규 자산의 현금흐름이 온전하게 반영되면서 배당금(DPS) 상승이 기대됩니다.

#### 🥈 [안정성 대장] 리얼티인컴 (Realty Income Corporation)

- **분석:** 'The Monthly Dividend Company®'라는 별칭답게 월배당의 상징입니다. 세븐일레븐, 월그린 등 경기 불황에도 강한 우량 임차인을 보유하고 있어 배당 컷(Dividend Cut) 리스크가 매우 낮습니다.
- **현재 시세:** **약 $57 ~ $60 (주당)**
- **투자 포인트:** 배당 수익률은 맥쿼리보다 낮지만, '달러 자산'이라는 강력한 헤지 수단이 됩니다. 환율 변동에 대비한 자산 배분 차원에서 은퇴자에게 필수적인 종목입니다.

---

### 🧮 은퇴 후 현금흐름 계산기

배당 소득이 일정 금액(2,000만 원)을 넘으면 금융소득종합과세 대상이 됩니다. 미리 계산해 보세요.

- [💰 배당 소득 포함 내 연봉별 세금 계산하기](https://tech.mdeeno.com/calculators/calc_dsr/)
- [💸 양도세 및 배당소득 절세 전략 확인하기](https://tech.mdeeno.com/calculators/calc_transfer/)

---

### 💡 결론: '맥쿼리 6 : 리얼티 4'의 황금 비율을 추천합니다

2026년 시장 상황에서 맥쿼리인프라는 **높은 원화 인컴**을, 리얼티인컴은 **안정적인 달러 인컴과 월 복리 효과**를 제공합니다. 은퇴자라면 국내 ISA 계좌를 통해 맥쿼리인프라를 담아 절세 혜택을 누리고, 연금 계좌에서는 리얼티인컴 비중이 높은 ETF를 편입하여 과세이연 효과를 극대화하는 전략이 유효합니다.

<small>본 분석은 2026년 2월 시장 데이터를 기반으로 작성되었으며, 종목 추천이 아닌 정보 제공을 목적으로 합니다. 모든 투자의 책임은 본인에게 있습니다.</small>

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

> **※ 본 분석은 M-DEENO의 정비사업 및 부동산 구조 연구를 위해 공개 자료와 가정값을 기반으로 정리된 시뮬레이션 사례입니다.**
>
> 개별 단지의 사업성 판단이나 투자 결정의 최종 근거로 사용하기에는 추가 검토가 필요합니다.

{{< mdeeno_cpa type="loan" >}}

{{< ad_cpa type="finance" >}}
