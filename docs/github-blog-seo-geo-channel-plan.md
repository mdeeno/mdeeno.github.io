# GitHub Blog SEO/GEO Channel Plan

Updated: 2026-06-19

## Current Finding

The GitHub Pages blog at `tech.mdeeno.com` already has the right base SEO/GEO infrastructure:

- Production robots.txt with crawling allowed.
- Canonical URLs.
- Google/Naver verification.
- Sitemap excluding `robotsNoIndex: true` pages.
- Article, Organization, Breadcrumb, and FAQ structured data.
- `llms.txt` output for AI crawler discovery.
- App funnel links to `mdeeno.com/member` with UTM tracking.

The main traffic blocker was content-level indexing. Many posts were intentionally set to `robotsNoIndex: true`; that is useful for old or off-topic content, but it also blocked recent high-intent M-DEENO posts about reconstruction contribution risk from Google/Naver discovery and the sitemap.

## Changes Applied

Opened 23 recent, high-intent market posts for indexing. These posts are directly tied to M-DEENO's core funnel: reconstruction contribution risk, construction cost, interest rate, DSR/LTV, jeonse pressure, and project delay.

Kept noindex on older or lower-fit posts to avoid expanding low-quality crawl surface.

Aligned `llms.txt` with SEO policy by excluding pages marked `robotsNoIndex: true`. This keeps generative discovery focused on indexable, higher-confidence pages.

Fixed FAQ JSON-LD extraction so CTA HTML and disclaimers are not pulled into `acceptedAnswer`.

## Operating Strategy

Use the GitHub blog as the top-of-funnel channel, not as a generic real-estate magazine.

Priority content clusters:

1. `재건축 분담금`
2. `공사비 800만/900만/1000만 원`
3. `비례율`
4. `이주비/DSR/LTV`
5. `단지명 + 분담금 리스크`
6. `전세가 상승 + 이주 + 분담금`

Publishing rule:

- Publish 3 new indexable posts per week.
- Each post must target one concrete search intent and one funnel CTA.
- Keep old or weak posts noindexed unless they are rewritten into a core cluster.
- Add 3 internal links from each new post: one calculator, one related risk article, one complex page.
- Add one app CTA above the first H2 and one near the final FAQ.

Measurement:

- GA4 event: `blog_to_mvp_click`
- UTM source: `blog`
- Primary weekly metric: blog sessions to `/member`
- Secondary metrics: indexed URL count, top query impressions, CTR, CTA click rate

## Next Review Checklist

- Confirm the 23 reopened posts appear in Google Search Console sitemap coverage.
- Submit `https://tech.mdeeno.com/sitemap.xml` after deploy.
- Inspect `https://tech.mdeeno.com/llms.txt` after deploy.
- Use Rich Results Test on 3 sample posts with FAQ schema.
- Rewrite five noindexed April/May posts into evergreen pillar pages only if they match a core cluster.
