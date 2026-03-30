# mdeeno.github.io CHANGELOG

블로그 세부 변경사항 기록.

---

## 2026-03

### 2026-03-30
**[100명 SEO 테스트] P0/P1 수정 + 중복 삭제**
- 100명 페르소나 SEO 테스트 1차 루프 실행 (200건 평가)
- P0: UTM 이중 utm_campaign 4건 수정 (3/26 포스트), 정치인 포스트 UTM 누락 5건 보정
- P0: "AI가 분석한" 이미지 캡션 17건 → "M-DEENO 시뮬레이션" 교체
- P1-1: 중복 CTA 557개 포스트에서 제거 (4,542줄 삭제)
- P1-4: AI 문구 823건 수정 (문장 패턴 2종 + "데이터 랩" 210건 + 이모지 611건)
- P1-5: 카테고리 오분류 18건 (reconstruction→strategy) 이동
- P1-6: 중복/불필요 포스트 28건 삭제 (macOS " 2.md" 8 + _aut 7 + _manual 13)
- 테스트 결과: SEO 100%, CTA 100%, 가독성 97.5%, 신뢰도 92.5%, UTM 98%
- 면책조항은 Hugo partial(post_disclaimer.html)이 전 포스트에 자동 삽입 확인
- 잔여 P1: 과장 표현(폭탄/폭등 71%), H2 위계 부족 5건 — posting-engine 템플릿 레벨 개선 대상

**[콘텐츠] 포스트 769개 일괄 정리**
- _auto 중복 파일 215개 삭제 (비_auto 파일 유지, 554개 잔존)
- description == title이던 357개 포스트 description을 본문 기반 재생성 (120~160자)
- frontmatter 더블쿼트 통일 + categories 디렉토리 매핑 (reconstruction→재건축/재개발, market→시장 분석 등)
- 깨진 blockquote(> **>) 58개, 미닫힌 bracket 35개, 줄바꿈된 frontmatter 37개 수정
- mdeeno.com/member CTA 링크 UTM 일괄 추가 (utm_source=blog&utm_medium=post_cta&utm_campaign=auto_post)
- 면책조항: Hugo partial(post_disclaimer.html)이 single.html에서 자동 삽입 확인 → 본문 추가 불필요
- 관련: content/posts/**, scripts/bulk_cleanup.py

### 2026-03-27
**[UX/접근성] 404 페이지 생성 + 색상 대비 잔여분 수정**
- 커스텀 404.html 생성 (홈으로 돌아가기 + 계산기 CTA + 보조 링크, 모바일 반응형)
- static/css/custom.css: logo #6b7684→#4e5968, --md-muted→#4b5563, --md-subtle→#6b7280, disclosure #ccc→#6b7280
- lab-style.css: 다크 배경 #777/#666/#888→#9ca3af (WCAG AA 대비)
- post_views.html: 인라인 #888→#4b5563, 폰트 13px 보장
- CTA 링크 전체 점검: mdeeno.com/member UTM 파라미터 일관성 확인 완료

**[접근성] 20인 페르소나 테스트 Round 2 — 색상 대비 개선**
- caption/설명 텍스트 #6b7684 → #4e5968 (WCAG AA 대비비 6.8:1)
- 관련: custom-typography.css, custom.css

**[접근성/UX] 10인 페르소나 타겟 테스트 P0+P1 수정**
- 메뉴 "전체 리포트" → "전체 글 보기" (이투자 혼동 해소)
- CTA 버튼 green → brand blue (#1e40af) 통일 (calc-cta-btn, calc-cta-box)
- 모바일 테이블 폰트 14px → 15px (65세+ 가독성)
- 테이블 td white-space: nowrap 제거 (72세 가로 스크롤 장벽 해소)

**[설정/전환율] 카카오 공유 SDK 키 설정 + 홈페이지 CTA UTM 파라미터 추가**
- `hugo.toml`에 `kakao_js_key` 파라미터 추가 (카카오 공유 SDK JavaScript 키)
- 블로그 홈페이지 CTA 3곳에 `utm_campaign`, `utm_content` 파라미터 추가 (hero / mvp-strip / premium-band)
- 퍼널 유입 경로별 전환 추적 정밀화
- 관련 파일: `hugo.toml`, `layouts/index.html`

### 2026-03-25 (16)
**[카카오 채널 CTA 포스트 본문 삽입 + 다크모드 제거]**
- 668개 포스트에 카카오 채널 인라인 CTA 삽입 (5번째 H2 앞 배치)
- 카카오 옐로우(#FEE500) 기반 인라인 스타일 + CSS 클래스 추가
- 다크모드 시스템 차단 (hugo.toml disableThemeToggle, color-scheme: light)
- 표 테두리 강화(#e2e8f0), 행 호버(#eff6ff), 모바일 반응형 개선
- 포스트 내 링크 호버 효과 추가 (.post-content a:not([class]))
- CTA 버튼 색상 보호 (.post-content a:not([class]) 셀렉터)
- 관련 파일: `static/css/custom.css`, `hugo.toml`, `layouts/partials/extend_head.html`, `content/posts/**`

### 2026-03-24 (15)
**[CTA 카테고리별 차별화 + Related Posts 자동 렌더링]**
- top_cta.html / cta_auto.html: 5개 카테고리별 CTA 문구 분기 (재건축/시장/전략/세금/기본)
- related_posts.html 생성: Hugo Related API로 포스트 하단 관련 글 3개 자동 렌더링
- single.html에 related_posts 파셜 삽입
- 관련 파일: `layouts/partials/cta_auto.html`, `layouts/partials/top_cta.html`, `layouts/partials/related_posts.html`, `layouts/_default/single.html`

### 2026-03-24 (14)
**[SEO 강화: Sitemap 복구 + FAQ Schema + Hugo Minify]**
- sitemap.xml: outputs 설정 추가로 1,429 URL 색인 가능하도록 복구
- faq_schema.html: 72개 포스트에 FAQPage JSON-LD 자동 삽입
- hugo.toml: minifyOutput=true 설정으로 CSS/HTML/JS 압축 활성화
- 관련 파일: `hugo.toml`, `layouts/partials/faq_schema.html`, `layouts/partials/extend_head.html`

### 2026-03-24 (13)
**[SEO 일괄 개선: alt태그 + _auto 슬러그 마이그레이션 + 내부링크]**
- 38개 포스트 차트 alt 태그: generic "M-DEENO 시장 전망 분석 차트" → title 기반 키워드 alt로 변환
- 217개 _auto 파일명 제거 + Hugo aliases 추가 (기존 URL 301 redirect 보장)
- 415개 파일에서 921개 내부 링크 _auto 참조 업데이트
- Hugo 빌드 검증 완료 (1175 aliases 정상 생성)
- 관련 스크립트: `posting-engine/batch_improve_posts.py`

### 2026-03-22 (12)
**[FAQ 줄넘김 전체 수정]**
- 268개 포스트 FAQ 질문(Q)과 답변(A) 사이 빈 줄 누락 일괄 수정
- `fix_faq_linebreak.py` 스크립트로 일괄 처리
- 관련 파일: `content/posts/**/*.md`

### 2026-03-22 (11)
**[Google Search Console 인증 메타태그 추가]**
- `hugo.toml`에 `[params.analytics.google] SiteVerificationTag` 설정
- PaperMod 테마 `head.html`이 자동으로 `<meta name="google-site-verification">` 렌더링
- 관련 파일: `hugo.toml`

### 2026-03-22 (10)
**[404개 포스트 OG 이미지 생성 및 삽입]**
- 브랜드 카드형 OG 이미지 404개 자동 생성 (`static/images/og/`)
- 카테고리별 악센트 컬러, M-DEENO 로고, mdeeno.com URL 포함
- 각 포스트 front matter에 `image:` 필드 자동 삽입
- 관련 파일: `static/images/og/og-*.png`, `content/posts/**/*.md`

### 2026-03-21 (9)
**[면책조항 + 저작권 표시 Hugo partial로 복구]**
- `post_disclaimer.html` partial 신규 생성
- 모든 포스트 하단에 면책조항 + © 저작권 자동 표시
- 마크다운 인라인 방식 → 템플릿 일괄 관리로 전환
- 관련 파일: `layouts/partials/post_disclaimer.html`, `layouts/_default/single.html`, `static/css/custom.css`

### 2026-03-21 (8)
**[내부 링크 450개 포스트 일괄 삽입 + Hugo 관련글 위젯 제거]**
- internal_linker (Jaccard 유사도) 포스트당 3개 내부 링크 추가 (총 1,350개)
- Hugo `related_posts.html` 위젯 제거 — internal_linker로 통일
- cleanup/internal_linker 충돌 해결: cleanup rule 9 제거
- SEO 내부 링크 최소 3개 요구사항 충족
- 관련 파일: `layouts/_default/single.html`, 450개 포스트

### 2026-03-21 (7)
**[수동 HTML CTA 제거 + 로고 크기 통일 + OG 이미지 교체]**
- 인라인 스타일 CTA div 22개 제거 (Hugo 자동 CTA로 대체)
- 로고 크기 MVP와 통일: Desktop 24px, Mobile 20px
- OG 이미지 로고4(심볼 파랑 + 텍스트 검정)로 교체
- 관련 파일: `hugo.toml`, `static/css/custom.css`, `static/og-image.png`, 21개 포스트

### 2026-03-21 (6)
**[M-DEENO 브랜드 로고 적용]**
- 헤더: PaperMod label.icon으로 로고4 이미지 적용 (iconHeight 28)
- 파비콘: 심볼 crop 기반 16/32px + ICO + apple-touch-icon
- OG 이미지: 1200x630 소셜 공유 썸네일
- 관련 파일: `hugo.toml`, `static/logo.png`, `static/favicon*`, `static/og-image.png`

### 2026-03-21 (5)
**[포스트 정리 2차 — 잔여 불필요 요소 일괄 제거]**
- 면책문구 160개 제거 (※ 본 리포트는..., 📢 면책 조항 등 전 변형)
- 인라인 계산기 링크 블록 제거 (📉 이주비 대출 한도...)
- 고아 `</div>` 태그 제거
- 깨진 마크다운 링크 수정 (`- [- [` → `- [`)
- "핵심 정리" 섹션을 "함께 읽으면 좋은 글" 앞으로 순서 교정
- trailing `---` 제거
- 450개 파일, 4,259줄 제거
- 도구: `posting-engine/cleanup_posts.py`

### 2026-03-21 (4)
**[Phase 3: 450개 포스트 도입부+결론부 리라이트]**
- 밋밋한 도입부("~에 대해 알아보겠습니다") → "공포 후킹 → 공감 → 본론 약속" 구조로 교체
- 결론부 없는 포스트에 "핵심 정리" 섹션 추가 (M-DEENO 자연스러운 언급)
- 도입부 인라인 스타일 CTA 블록 제거 (layouts 자동 삽입으로 대체)
- 본론/FAQ/관련글/front matter는 건드리지 않음
- 관련 파일: `content/posts/**/*.md`
- 도구: `posting-engine/rewrite_intros.py`

### 2026-03-21 (3)
**[Phase 2: 블로그 UI 리디자인 — toss/브런치 수준 UX]**
- CTA 파셜 인라인 스타일 → CSS 클래스 전환 (`blog-cta--top`, `blog-cta--bottom`)
- 홈페이지: 히어로 여백 확대, 카드 멀티레이어 그림자, 프리미엄 밴드 그래디언트
- 포스트 카드: 텍스트 크기 증가 (1rem), 부드러운 호버 애니메이션
- lab-card/lab-formula-box: 좌측 컬러 보더 + 그래디언트 배경
- FAQ details: 좌측 파란 보더, open 시각 피드백
- 관련 포스트 위젯: 카드형 디자인, 호버 배경 효과
- TOC/계산기 CTA: 그림자/패딩 업그레이드
- 다크모드 토글 비활성화 (`disableThemeToggle = true`)
- 관련 파일: `static/css/custom.css`, `assets/css/extended/*.css`, `layouts/partials/*.html`, `hugo.toml`

### 2026-03-21 (2)
**[블로그 인라인 색상 전수 수정 — 450개 파일]**
- `color:#fff` 제거 후 CSS 관리로 전환 (2,187건)
- CTA 버튼 `color:#fff` 복원 (507건, 어두운 배경 전용)
- `color:#888` → `#6b7280` WCAG AA 대비 준수 (90건)
- `color:#2c3e50/#7f8c8d/#495057` → 브랜드 색상 통일 (34건)
- 다크모드 H2/H3 색상: `#93c5fd/#bfdbfe` → `#60a5fa` (대비 강화)
- 관련 파일: `content/posts/**/*.md`, `static/css/custom.css`

### 2026-03-21
**[블로그 모바일 가독성 전면 개선 — 50~60대 타겟]**
- iOS Safari 자동줌 방지: 검색 input font-size 16px 이상
- 모바일 인라인 CTA 버튼 강제 풀폭 (display:block, min-height 48px)
- 차트 캡션/small 태그 최소 14px 보장
- H2/H3/table/post-title 600px breakpoint 폰트 상향
- 홈 히어로/MVP strip/premium band 폰트 확대
- 포스트 카드 제목, stat 라벨 확대
- 모든 CTA min-height 48~52px 보장
- 관련 파일: `static/css/custom.css`, `assets/css/extended/custom-typography.css`, `content/_index.md`

**[블로그 CTA/FAQ 가시성 개선]**
- FAQ 섹션 스타일링 추가 (파란색 헤딩, details/summary 카드 디자인)
- 차트 래퍼(lab-graph-wrapper) 폴백 스타일
- CTA 블록 다크모드 오버라이드
- 인라인 스타일 CTA 블록에 브랜드 컬러 적용
- FAQ 구조 정규화 (h3/h4 strong 상속)
- 관련 파일: `assets/css/extended/custom-typography.css`, `assets/css/extended/custom.css`

### 2026-03-20 (3)
**[SEO]** 블로그 FAQ 섹션 일괄 추가 (배치 3)
- 대상: 69개 포스트 (market 30, niche 19, reconstruction 20)
- 완료: 67개 (Unicode 파일명 이슈로 2개 스킵)
- 스킵 파일: 월세-수익률-폭발-임박-평택화성포천, 무인-스터디카페-폐업률-40%
- 각 포스트에 Q1/Q2/Q3 형식의 FAQ 3개 삽입
- 삽입 위치: "함께 읽으면 좋은 글" 섹션 직전
- 관련 커밋: 배치 3-1~3-3

### 2026-03-20 (2)
**[전환율]** 블로그 CTA 전환율 개선 작업
- B-1: cta_auto.html / mdeeno_cpa.html CTA 카피 강화 ("공사비 10% → 분담금 70% 증가" 후킹)
- B-2: top_cta.html 신규 생성, single.html에 상단 CTA 배너 자동 삽입
- B-3: AI 분석 데이터 태그 321개 파일에서 일괄 제거
- B-4: CTA 미포함 포스트 76개에 인라인 CTA 삽입
- Hugo 빌드 검증 통과, 금지 용어 0건

### 2026-03-20
**[품질]** 블로그 전체 포스팅 품질 감사 및 일괄 수정 (456 파일)
- Prop-Logic™ → M-DEENO 분석 엔진 치환 (240건, "엔진 엔진" 중복 55건 포함 수정)
- 깨진 이미지 참조 제거: 본문 410건 + front matter image 321건
- 깨진 내부 링크 수정: 자동 88건 + 수동 3건 (괄호 포함 URL)
- HTML 고아 닫힘 태그 제거: 136건
- 짧은/잘린 포스트: draft 처리 120건, 미완성 문장 트림 31건
- Hugo 빌드 검증 통과 (1789 pages, 0 errors)

**[CTA]** 블로그 CTA 통일 — A안(공포 후킹) 적용 (378 파일)
- 사전 신청 폼, 출시 알림, 분담금 정밀 진단 등 6개 패턴 → 통일 CTA로 교체
- 새 CTA: "공사비 10% 오르면, 내 분담금은 최대 7배 뜁니다" + "내 분담금 무료 분석하기"

### 2026-03-18
**[SEO]** 내부 링크 409개 포스트에 일괄 삽입 + FAQ 6개 추가
- "함께 읽으면 좋은 글" 섹션: 36개 → 445/451개 (Jaccard 유사도 기반 관련 글 3개씩)
- FAQ 섹션: 6개 포스트에 추가 (나머지는 Gemini 쿼터 리셋 후 추가 예정)
- 관련 파일: content/posts 하위 409개 .md 파일

### 2026-03-17 (2)
**[모바일 반응형]** 480px 브레이크포인트 강화
- `static/css/custom.css`: 히어로/스탯/MVP스트립/프리미엄밴드/포스트카드/기사콘텐츠 등 480px 여백·폰트 축소
- `assets/css/extended/custom.css`: CTA 블록(mvp-cta, landing-cta, calc-cta) 480px 패딩·폰트 최적화
- 관련 파일: 2개 CSS 파일, +53줄

### 2026-03-17
**[SEO]** Schema.org 구조화 데이터 + 이미지 lazy loading 추가
- 포스트 페이지에 Article JSON-LD 구조화 데이터 삽입 (검색 리치 결과 대응)
- 마크다운 이미지 render hook으로 lazy loading 자동 적용 (LCP/CLS 개선)
- 관련 파일: `layouts/partials/extend_head.html`, `layouts/_default/_markup/render-image.html`

**[접근성]** 고령층 접근성 개선 — CTA 버튼/폰트 크기 확대
- CTA 버튼 패딩 확대 (13px 20px → 16px 24px), min-height: 44px 추가
- 모바일 포스트 제목 크기 24px → 26px
- 계산기 버튼 패딩 확대 (12px → 14px 24px), 히어로 버튼 통일
- cta_auto.html 인라인 스타일 동기화
- 관련 파일: `assets/css/extended/custom.css`, `assets/css/lab-style.css`, `layouts/partials/cta_auto.html`

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

