#!/usr/bin/env python3
"""
Rewrite top 15 reconstruction-related blog posts using Gemini API.
"""

import os
import time
import re

from google import genai
from google.genai import types

# --- Config ---
GEMINI_API_KEY = "REDACTED_GEMINI_KEY"
BASE_DIR = "/Users/suhun/Desktop/document/mdeeno.github.io/content/posts/reconstruction"

TARGET_FILES = [
    "2026-03-06-재건축-분담금-폭탄,-내-아파트는-안전할까-M-DEENO가-분석한-수익성-임계점_auto.md",
    "2026-03-06-재건축-10년의-여정,-수익률을-가르는-결정적-단계는-(M-DEENO-데이터-랩-분석)_auto.md",
    "2026-03-07-내-집이-빚더미로-재개발-분담금-폭탄-피하는-M-DEENO의-데이터-기반-생존-전략_auto.md",
    "2026-03-07-내-집이-빚더미로-재건축-'분담금-대출'-리스크와-M-DEENO의-수익성-방어-전략_auto.md",
    "2026-03-07-내-집의-가치를-결정하는-'재개발-보상금',-M-DEENO-데이터로-본-손해-안-보는-법_auto.md",
    "2026-03-07-내-집이-황금알을-낳기까지,-재개발-절차-10단계-완벽-가이드-(ft.-한남3·성수)_auto.md",
    "2026-03-07-재개발-수익률,-뜬구름-잡는-소리에-속지-마세요-M-DEENO의-데이터-기반-절차-가이드_auto.md",
    "2026-03-07-공사비-1,000만-원-시대,-내-집-재개발-분담금-'폭탄'-피하는-3가지-핵심-지표_auto.md",
    "2026-03-08-서울-재개발-예정지,-상위-1%만-아는-'옥석-가리기'...-M-DEENO-Prop-Logic™-분석-결과_auto.md",
    "2026-03-08-재개발-분담금-5억-시대-M-DEENO가-분석한-추가-분담금-리스크와-생존-전략_auto.md",
    "2026-03-08-재개발-이주비,-대출-규제-속에서-내-집-지키는-법-M-DEENO-데이터-분석-보고서_auto.md",
    "2026-03-08-재개발-투자,-언제-들어가야-돈이-될까-M-DEENO가-분석한-단계별-수익-임계점_auto.md",
    "2026-03-08-은마-재건축,-'희망-고문'-끝날까-M-DEENO가-분석한-2024년-사업성-시뮬레이션_auto.md",
    "2026-03-08-재개발-보상금,-'이것'-모르면-수억-원-손해-M-DEENO가-분석한-구역별-보상-가이드_auto.md",
    "2026-03-08-재개발-입주권,-'로또'일까-'폭탄'일까-M-DEENO가-분석한-2024-정비사업-투자-공식_auto.md",
]

REWRITE_PROMPT_TEMPLATE = """You are rewriting a Korean real estate blog post about reconstruction/정비사업 for M-DEENO.

ORIGINAL TITLE: {title}

ORIGINAL BODY:
{body}

REWRITE RULES:
1. Follow this narrative arc: 충격(shock) → 분석(analysis) → 비교(comparison) → 전략(strategy) → 행동(action)
2. First use of technical terms must include explanation in parentheses:
   - 비례율(사업 수익성이 높을수록 올라가는 지수로, 100% 이하면 조합원 추가 분담금이 발생)
   - 종전자산(재건축 전 내 아파트의 감정평가 금액)
   - 관리처분(이주·철거 직전 단계로, 분담금이 확정되는 시점)
   - 권리가액(비례율을 적용한 내 실질 지분 가치)
   - 도정법(도시 및 주거환경정비법)
3. Content ratio: data/numbers 30%, strategy/interpretation 40%, action guidance 30%
4. Include TWO CTAs with this HTML block after the intro and before the conclusion:
<div style="margin:32px 0;padding:20px 28px;background:linear-gradient(135deg,#eff6ff,#dbeafe);border:2px solid #2563eb;border-radius:12px;text-align:center;">
  <p style="font-size:1rem;font-weight:700;color:#1e40af;margin:0 0 8px;">📊 내 단지 추가분담금 리스크 무료 분석</p>
  <a href="https://mdeeno.com/member" target="_blank" style="display:inline-block;padding:12px 28px;background:#2563eb;color:#fff;font-weight:700;border-radius:8px;text-decoration:none;">내 단지 추가분담금 리스크를 무료로 계산해보세요 →</a>
</div>
5. NO phrases: "이 글에서는", "지금부터 설명드리겠습니다", "마지막으로 정리해보겠습니다", "함께 살펴보겠습니다", "이번 포스팅에서는"
6. Start the first sentence by directly addressing the reader's pain point with a specific number
7. Length: 1500~2500 Korean words
8. Use ### for section headings, 2-4 sentences per paragraph
9. Include FAQ section at the end with 3 Q&As
10. Tone: professional but accessible, like an experienced real estate consultant
11. Include at least 3 internal links to related posts on the blog using markdown links like [text](/posts/reconstruction/filename/)

Output ONLY the rewritten markdown body (no front matter). Start directly with the first sentence.
"""


def parse_file(filepath):
    """Parse a Hugo markdown file into front matter, body, and trailing HTML."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract front matter (between first and second ---)
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None, content, ""

    front_matter = "---" + parts[1] + "---"
    body_and_rest = parts[2]

    # Identify trailing HTML blocks to preserve
    # Look for lead_gen form, script tags, or "함께 읽으면 좋은 글" section
    # We'll preserve everything from {{< mdeeno_cpa or the lead gen div onward

    # Find the position of preserved blocks
    preserve_markers = [
        r'\{\{<\s*mdeeno_cpa',
        r'<div style="margin:40px 0;padding:25px;background:#f0f7ff',
        r'## 함께 읽으면 좋은 글',
        r'<script>',
    ]

    preserve_start = len(body_and_rest)
    for marker in preserve_markers:
        match = re.search(marker, body_and_rest)
        if match and match.start() < preserve_start:
            preserve_start = match.start()

    body = body_and_rest[:preserve_start].strip()
    trailing = body_and_rest[preserve_start:]

    # Extract title from front matter
    title_match = re.search(r'^title:\s*["\']?(.+?)["\']?\s*$', front_matter, re.MULTILINE)
    title = title_match.group(1) if title_match else "재건축 관련 포스트"

    return front_matter, body, trailing, title


def rewrite_with_gemini(client, title, body):
    """Call Gemini API to rewrite the post body with retry on rate limit."""
    prompt = REWRITE_PROMPT_TEMPLATE.format(title=title, body=body[:8000])  # limit input

    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-flash-latest",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.7,
                    max_output_tokens=8192,
                )
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                # Parse retry delay from error if available
                wait = 60 * (attempt + 1)
                import re as _re
                m = _re.search(r'retryDelay.*?(\d+)s', err_str)
                if m:
                    wait = int(m.group(1)) + 5
                print(f"  Rate limited, waiting {wait}s before retry {attempt+1}/3...")
                time.sleep(wait)
            else:
                raise
    raise Exception("Max retries exceeded")


def main():
    client = genai.Client(api_key=GEMINI_API_KEY)

    updated = []
    skipped = []

    for i, filename in enumerate(TARGET_FILES):
        filepath = os.path.join(BASE_DIR, filename)

        if not os.path.exists(filepath):
            print(f"[{i+1}/15] SKIP (not found): {filename}")
            skipped.append(filename)
            continue

        print(f"\n[{i+1}/15] Processing: {filename[:60]}...")

        try:
            result = parse_file(filepath)
            if result[0] is None:
                print(f"  -> SKIP: could not parse front matter")
                skipped.append(filename)
                continue

            front_matter, body, trailing, title = result
            print(f"  Title: {title}")
            print(f"  Body length: {len(body)} chars")

            new_body = rewrite_with_gemini(client, title, body)
            print(f"  New body length: {len(new_body)} chars")

            # Write back: front matter + newline + new body + trailing HTML
            new_content = front_matter + "\n\n" + new_body + "\n\n" + trailing

            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)

            print(f"  -> UPDATED successfully")
            updated.append(filename)

        except Exception as e:
            print(f"  -> ERROR: {e}")
            skipped.append(filename)

        # Rate limit protection
        if i < len(TARGET_FILES) - 1:
            print(f"  Sleeping 10 seconds...")
            time.sleep(10)

    print("\n" + "="*60)
    print(f"SUMMARY: {len(updated)} updated, {len(skipped)} skipped")
    print("\nUpdated files:")
    for f in updated:
        print(f"  ✓ {f}")
    if skipped:
        print("\nSkipped files:")
        for f in skipped:
            print(f"  ✗ {f}")


if __name__ == "__main__":
    main()
