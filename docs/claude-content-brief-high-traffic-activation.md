# Claude Content Brief: High Traffic Blog Activation

Date: 2026-06-19
Repository: `mdeeno.github.io`
Channel: `https://tech.mdeeno.com`

## Objective

Create and rewrite content that increases qualified organic traffic for M-DEENO and sends readers to the free diagnosis flow at `https://mdeeno.com/member`.

Do not write generic real-estate commentary. Every article must connect a search intent to one measurable reconstruction risk and one conversion action.

## Content Rules

- Main topic must be one of: `재건축 분담금`, `비례율`, `공사비`, `이주비`, `DSR`, `LTV`, `단지명 + 재건축 리스크`.
- Each article needs one clear reader problem in the first 150 words.
- Include at least one simple formula or scenario table.
- Include three internal links:
  - One calculator page under `/calculators/`
  - One related reconstruction/market article
  - One complex page under `/complex/` when a district or complex is mentioned
- Include two CTAs to `https://mdeeno.com/member` with UTM:
  - `utm_source=blog`
  - `utm_medium=post_body` or `cta`
  - `utm_campaign=organic_growth`
- Add front matter `faq` with exactly 3 Q/A pairs.
- Do not add `robotsNoIndex: true` unless the article is intentionally excluded from search.

## First Assignment

Draft three pillar pages:

1. `재건축 분담금 계산 완벽 가이드`
   - Target intent: "재건축 분담금 계산"
   - Include formula: 추가분담금 = 조합원 분양가 - 권리가액
   - Link to DSR calculator and at least one contribution-risk article.

2. `비례율 90% 이하이면 조합원 분담금은 얼마나 늘어날까`
   - Target intent: "비례율 분담금"
   - Explain 100%, 95%, 90%, 85% scenarios.
   - Include a table by 종전자산 5억/8억/10억.

3. `공사비 900만 원 시대 재건축 생존 전략`
   - Target intent: "공사비 900만 원 재건축"
   - Explain construction cost, interest, general sale price, and delay risks.
   - Link to loan interest calculator and related cost-risk posts.

## Rewrite Assignment

Pick five existing noindexed April/May posts and rewrite only if they can become evergreen cluster support pages. Recommended candidates:

- `공사비 800만 원 시대`
- `공사비 900만 원 시대`
- `목동 재건축 분담금`
- `분당 재건축 분담금`
- `은마아파트 재건축 분담금`

Rewrite target:

- Remove short-term market noise.
- Keep only durable explanation, formulas, scenarios, and decision checklists.
- Add FAQ front matter.
- Recommend removing `robotsNoIndex: true` only after the article is rewritten into an evergreen search page.

## Quality Bar

A finished article should answer:

- What changed?
- Why does it change my 분담금?
- Which number should I check first?
- What should I calculate now?
- Why should I use M-DEENO now?

Avoid:

- Unsupported price claims.
- Excessive buzzwords.
- Broad market forecasts without a direct 분담금 mechanism.
- Duplicating the same CTA sentence in every paragraph.

## Delivery Format

Return edited Markdown files or patches. Keep filenames Korean-friendly and slug-safe. Put drafts under `content/posts/reconstruction/` unless the article is clearly a market issue.
