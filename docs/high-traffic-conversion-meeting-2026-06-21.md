# 블로그 고트래픽 전환 회의록

- 일시: 2026-06-21
- 대상: `https://tech.mdeeno.com`
- 목표: 검색 유입을 늘리되, 최종적으로 `/member` 리스크 진단 시작을 증가시킨다.
- 참석 관점: Growth, SEO/GEO, Content, Product/Data, Engineering

## 1. 결론

M-DEENO 블로그는 부동산 종합 매거진이 아니라 **재건축 조합원의 분담금 리스크 의사결정 채널**로 운영한다.

향후 14일 동안 다음 순서로 전환한다.

1. Google OAuth를 복구하고 GSC·GA4 기준선을 확보한다.
2. 신규 단지 페이지와 범용 뉴스 자동 발행을 일시 동결한다.
3. 이미 만든 3개 필라를 중심으로 지원 글과 내부 링크를 집중한다.
4. 기존 `noindex` 글은 일괄 해제하지 않고 검색 의도와 품질을 통과한 글만 선별 복구한다.
5. 블로그에서 `/member`로 이동하는 이벤트를 하나의 전환 이벤트로 통일한다.

트래픽의 정의는 페이지뷰가 아니다. 이번 전환의 최종 KPI는 **오가닉 방문자의 리스크 진단 시작 수**다.

## 2. 현재 상태

2026-06-21 저장소 기준:

| 항목 | 현재 값 | 판단 |
|---|---:|---|
| 일반 포스트 | 734개 | 양은 충분함 |
| `noindex` 포스트 | 710개 | 검색 의도 중복 감사 후 8개 추가 제외 |
| 검색 노출 가능한 일반 포스트 | 24개 | 중복을 줄였으며 클러스터 지원 글은 여전히 부족함 |
| 단지 페이지 | 198개 | 전부 색인 가능, 확장보다 품질·성과 확인 우선 |
| FAQ front matter 적용 글 | 27개 | 리치결과 KPI로 사용하지 않음 |
| 핵심 필라 | 3개 | 분담금 계산, 비례율, 공사비 900만 원 |

이미 갖춘 자산:

- 재건축 분담금 필라 3종
- 단지별 분석 198개
- 계산기 9종 이상
- CTA 및 UTM 구조
- `llms.txt`, sitemap, canonical, Article/Breadcrumb 구조화 데이터

핵심 문제는 콘텐츠 부족이 아니라 **색인 가능한 핵심 글의 밀도, 내부 링크 구조, 전환 측정**이다.

## 3. 관점별 논의

### Growth

초기 제안은 색인 페이지를 빠르게 늘리는 것이었다. 그러나 702개를 일괄 해제하면 과거의 광범위한 부동산·경매·세금·청약 글이 사이트의 주제를 다시 흐린다. 검색 노출이 늘어도 `/member` 전환과 무관한 트래픽이 될 가능성이 높다.

결론: 전체 색인 수가 아니라 `분담금`, `비례율`, `공사비`, `이주비`, `단지명 + 재건축` 쿼리 노출을 늘린다.

### SEO/GEO

Google은 대량의 비독창적 자동 생성 페이지를 scaled content abuse로 판단할 수 있다. 현재 198개 단지 페이지는 고유 서술이 보강되어 있지만 템플릿 공통 영역이 크다. 성과 확인 없이 단지를 더 늘리는 것은 위험 대비 효율이 낮다.

Google의 AI 검색도 별도 GEO 기술보다 색인, 검색 품질, 내부 링크, 고유한 정보가 선행 조건이다. 2026년 6월부터 일부 사이트에 생성형 AI 성과 보고서가 제공되기 시작했으므로 GSC에 해당 보고서가 보이면 별도 기준선을 남긴다.

결론: 신규 URL 확대를 멈추고 기존 URL의 고유성, 출처, 링크, 전환 성과를 높인다.

### Content

범용 뉴스 글은 발행 시점의 화제성은 있지만 검색 수명이 짧고 기존 글과 제목·의도가 중복되기 쉽다. 반면 이미 만든 3개 필라는 사용자의 실제 질문과 M-DEENO 진단 흐름에 직접 연결된다.

결론: 다음 14일의 신규 콘텐츠는 3개 필라의 지원 글 6개로 제한한다.

- 재건축 분담금 계산
  - 권리가액과 조합원 분양가로 추가분담금 계산하는 법
  - 관리처분 전 추정분담금이 바뀌는 5가지 변수
- 비례율
  - 비례율 100%·95%·90%가 권리가액에 미치는 차이
  - 비례율이 높아도 분담금이 생기는 경우
- 공사비
  - 공사비 10% 상승이 평형별 부담에 미치는 영향
  - 공사비 검증 전 조합원이 확인할 자료와 질문

각 글은 원본 계산표 또는 시나리오, 공식 출처, 필라 링크, 관련 단지 2개, 계산기 1개, `/member` CTA를 포함해야 한다.

### Product/Data

오늘 GSC·GA4 조회를 시도했으나 Google OAuth refresh token이 만료 또는 취소되어 `invalid_grant`가 발생했다. 현재 성과 기준선 없이 절대 목표를 정하면 근거 없는 숫자가 된다.

또한 CTA 이벤트가 `hero_cta`, `bottom_cta`, `cta_auto_click`, `complex_cta_click` 등으로 분산되어 있다. 분석 시 이를 매번 합산해야 하므로 페이지·위치·클러스터별 비교가 어렵다.

결론: OAuth 복구가 최우선이며, 전환 이벤트를 아래 형태로 통일한다.

```text
event: blog_to_mvp_click
params:
  page_path
  content_type      # pillar | support | complex | calculator | home
  cluster           # contribution | ratio | construction_cost | relocation_loan
  cta_position      # hero | mid | bottom | floating
  destination       # /member
```

기존 이벤트는 호환성을 위해 당분간 유지하되 `blog_to_mvp_click`을 함께 전송한다.

### Engineering

기술 SEO의 기반은 이미 갖춰져 있다. 이번 스프린트에서 새 구조화 데이터나 신규 크롤러 대응 파일을 추가하는 것은 우선순위가 아니다.

FAQ 리치결과는 현재 Google에서 공신력 있는 정부·보건 사이트에 한정된다. 따라서 부동산 블로그에서 FAQ schema 적용 수나 Rich Results Test 통과를 트래픽 KPI로 두지 않는다. FAQ는 독자의 질문을 해결할 때만 본문 콘텐츠로 사용한다.

## 4. 확정 실행안: 14일 스프린트

### Day 0~1: 측정 복구

- [ ] Google OAuth 재인증
- [ ] GSC 28일·90일 기준선 저장
- [ ] GA4 블로그 세션·오가닉 세션·`/member` 이동 수 저장
- [ ] GSC 생성형 AI 성과 보고서 노출 여부 확인
- [ ] sitemap에 포함된 URL 수와 실제 색인 URL 수 비교

### Day 1~3: 구조 정리

- [x] `blog_to_mvp_click` 공통 이벤트 추가
- [x] 홈 히어로의 `양도소득세`, `청약 전략` 링크를 핵심 4개 클러스터로 교체
- [x] 3개 필라에서 지원 글·관련 단지·계산기로 이어지는 링크 구조 설계
- [x] 기존 32개 색인 가능 글의 검색 의도 감사, 중복 8개 `noindex` 전환

### Day 3~10: 콘텐츠 집중

- [ ] 지원 글 6개 발행
- [x] 기존 `noindex` 글 중 재작성 후보 10개만 선정
- [ ] 후보마다 원본성, 출처, 검색 의도, 필라 연결, 전환 경로를 검수
- [ ] 검수 통과 글만 `noindex` 해제
- [x] 198개 단지 중 우선 20개 선정 (`high-traffic-activation-backlog-2026-06-21.md`)

### Day 11~14: 성과 판정

- [ ] 신규·복구 URL 색인 상태 확인
- [ ] 쿼리별 노출·CTR·평균순위 비교
- [ ] 글별 `blog_to_mvp_click`과 진단 시작 연결 확인
- [ ] 성과가 난 클러스터 1개를 다음 30일 집중 주제로 확정

## 5. KPI와 판정 기준

OAuth 복구 후 28일 기준선을 고정하고 아래 상대 목표를 적용한다.

| 단계 | KPI | 30일 목표 |
|---|---|---:|
| 색인 | 선별 신규·복구 URL 색인율 | 90% 이상 |
| 노출 | 핵심 5개 검색군 노출 | 기준선 대비 +50% |
| 유입 | 핵심 검색군 오가닉 클릭 | 기준선 대비 +30% |
| 전환 | 오가닉 방문자의 `/member` 이동률 | 기준선 대비 +50% |
| 사업 | 블로그 기여 리스크 진단 시작 수 | 기준선 대비 +30% |

절대 목표치는 기준선 확인 후 확정한다. 데이터가 없는 상태에서 세션 수나 리드 수를 임의로 약속하지 않는다.

## 6. 중단 기준

다음 작업은 하지 않는다.

- 702개 `noindex` 글 일괄 해제
- 신규 단지 페이지 대량 생성
- 검색 의도 없는 범용 부동산 뉴스 자동 발행
- 제목만 바꾼 유사 글 양산
- FAQ 리치결과를 목적으로 한 FAQ schema 확대
- 페이지뷰만 보고 성공 판정
- 색인 요청 반복으로 품질 문제를 해결하려는 시도

## 7. 담당과 기한

| 담당 | 작업 | 기한 |
|---|---|---|
| Product/Data | OAuth 복구 및 28일·90일 기준선 | 2026-06-22 |
| Engineering | 전환 이벤트 통일, 홈 클러스터 정리 | 2026-06-24 |
| SEO/GEO | 색인 후보 10개·우선 단지 20개 선정 | 2026-06-24 |
| Content | 지원 글 6개 작성·발행 | 2026-07-01 |
| Growth | 첫 성과 리뷰와 다음 집중 클러스터 결정 | 2026-07-05 |

## 8. 공식 근거

- Google, people-first content: https://developers.google.com/search/docs/fundamentals/creating-helpful-content
- Google, spam policies / scaled content abuse: https://developers.google.com/search/docs/essentials/spam-policies
- Google, internal link best practices: https://developers.google.com/search/docs/crawling-indexing/links-crawlable
- Google, AI features and websites: https://developers.google.com/search/docs/appearance/ai-overviews
- Google, generative AI performance reports in Search Console: https://developers.google.com/search/blog/2026/06/gen-ai-performance-reports
- Google, FAQ structured data eligibility: https://developers.google.com/search/docs/appearance/structured-data/faqpage

## 최종 의사결정

이번 스프린트의 우선순위는 다음 한 문장으로 고정한다.

> **측정되지 않는 대량 발행을 멈추고, 재건축 분담금 의도가 강한 3개 클러스터에서 검색 노출과 진단 전환을 동시에 만든다.**
