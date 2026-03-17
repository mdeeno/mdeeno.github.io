# mdeeno.github.io CHANGELOG

블로그 세부 변경사항 기록.

---

## 2026-03

### 2026-03-17
**[SEO]** 테마 중복 포스트 150개 삭제 — keyword cannibalization 제거
- 42개 중복 클러스터 식별 (분담금 5억, 은마 재건축, 이주비 대출, 로또 청약 등)
- 클러스터당 대표 1개 보존, 나머지 삭제 (592개 → 442개)
- Google HCU 대응 + 검색 순위 집중 효과 기대
- 삭제 로그: `content/posts/deletion-log-2026-03-17.txt`

### 2026-03-13
**[랜딩]** 히어로 문구 고통점 기반 교체 + AdSense 6/15 자동 활성화 구조 추가
- Hero H1: "내 아파트 수익성" → "재건축 추가분담금, 우리 단지는 감당 가능할까요?"
- Hero sub: 공사비 상승 고통점 기반 문구로 교체
- CTA 3곳 통일: "내 단지 리스크 분석하기" (hero / mvp-strip / premium-band)
- AdSense: hugo.toml에 publisher_id / slot_id / active_date 파라미터 추가
- `adsense_slot.html` partial 신규 생성 (Hugo now >= 2026-06-15 조건)
- 광고 위치: index.html (포스트 섹션 아래), single.html (본문 뒤)
- 6/15 이전 빌드: HTML에 광고 코드 없음 (Hugo 빌드 시점 결정)
- 관련 파일: `layouts/index.html`, `layouts/_default/single.html`, `layouts/partials/adsense_slot.html`, `layouts/partials/extend_head.html`, `hugo.toml`

### 2026-03-12
**[UX]** 블로그 CTA 역할 명확화 (430 + 53개 일괄)
- Form CTA (430개): 계산기 버튼 최상단 이동 → 이메일 폼은 구분선 아래 "리포트 출시 알림 이메일 등록"으로 분리
- "사전 신청"/"베타 신청" → "출시 알림 신청"으로 통일
- Gradient CTA (53개): 버튼 텍스트 "무료 리스크 분析 시작" → "무료 분담금 계산 시작"
- 관련 파일: `content/posts/**/*.md`

### 2026-03-10
**[전환]** 전체 포스트 CTA 자동 삽입 (인트로 + 마무리) — 530개 포스트 일괄 적용
- `layouts/_default/single.html` 신규: 모든 포스트에 CTA 자동 주입
- `layouts/partials/cta_auto.html`: 포스트 slug 기반 utm_content 추적
- `mdeeno_cpa.html` shortcode: UTM 파라미터 추가

**[SEO/UX]** 관련 포스트 위젯 + 카테고리별 계산기 컨텍스트 링크
- `related_posts.html`: 태그 기반 관련 포스트 4개 자동 표시
- `calc_cta.html`: 카테고리에 따라 관련 계산기 자동 연결
- `hugo.toml`: related content 설정 추가

**[디자인]** 홈페이지 전면 리디자인 — 라이트 모드, 네이비/블루 팔레트, 검색 중심 UX
- 다크 계열 → 라이트 모드 전환
- 검색창을 홈 핵심 요소로 배치

**[타이포그래피]** 아티클 가독성 전면 개선 — Pretendard 폰트 적용
- 폰트 교체, 줄간격·자간·본문 너비 최적화
- 포스트 푸터·TOC·모바일 가독성 개선

**[SEO]** 포스트 타이틀에서 M-DEENO 브랜딩 제거 (64개 포스트)
- 검색 노출 자연스럽게 개선

**[분석]** GoatCounter 페이지 뷰 카운터 추가
- 포스트별 조회수 표시 + 홈페이지 방문자 통계

**[안정성]** CJK 한자 잔존 문자 전수 수정 (206개 파일 YAML 정규화)
- 분析→분석 등 한자 잔류 문자 전체 교체
- YAML frontmatter 따옴표 정규화

### 2026-03-09
**[디자인]** 홈페이지 리디자인 — MVP CTA 중심 + 가치 제안 밴드 추가
- SaaS 제품 CTA를 홈 상단 핵심으로 배치

**[안정성]** CJK 析 문자 전체 소스 파일 정리 + 카테고리 정규화

### 2026-03-08
**[디자인]** 카드형 홈페이지 리디자인 + 카테고리 정리
- 포스트 목록을 카드 레이아웃으로 전환

**[분석]** GA4 추적 연결 (G-77C1K4JKYP)

**[품질]** 중복 재건축 포스트 10건 삭제

**[인프라]** PaperMod 테마 git submodule로 연결 (GitHub Actions 빌드 수정)

### 2026-03-07
**[퍼널]** SaaS 퍼널 연결 — CTA 컴포넌트, 레이아웃 주입, 보안 수정
- 블로그 → SaaS 제품 유입 경로 완성

**[콘텐츠]** 490+ 포스트 대량 추가
- 261개 포스트 태그 포맷 수정 (SEO 최적화)

### 2026-03-06
**[퍼널]** SaaS 퍼널 CTA 컴포넌트 추가 + 레이아웃 삽입 + 보안 수정

---

## 2026-02

### 2026-02-22
**[UX]** 랜딩페이지 반응형 수정
**[퍼널]** prop-logic → mdeeno.com 페이지 연결

### 2026-02-17
**[SEO]** 네이버 서치어드바이저 소유권 인증
**[SEO]** 스키마 언어 ko-KR로 수정, robot.txt 추가
**[버그픽스]** heal.html 무한 재귀 문제 해결
**[CPA]** 기존 포스팅 CPA 예약코드 작성 (6월 론칭 시 활성화 예정)

---

## 히스토리

