#!/usr/bin/env python3
"""
M-DEENO 블로그 포스트 품질 소급 수정 스크립트
5가지 문제를 일괄 수정합니다.

Usage:
    python3 fix_post_quality.py --dry-run   # 수정 대상 건수 확인만
    python3 fix_post_quality.py             # 실제 수정 실행
"""

import os
import re
import glob
import argparse
from pathlib import Path


def split_frontmatter(content: str):
    """frontmatter(--- ... ---)와 본문을 분리합니다.
    frontmatter 종료 라인(--- 또는 ---<!-- ... -->)까지 포함합니다.
    Returns: (frontmatter_with_closing, body) or None if no frontmatter.
    """
    if not content.startswith("---"):
        return None

    # Find second ---
    first_end = content.index("\n", 0)
    second_start = content.index("---", first_end)
    # Find end of the closing --- line (may have <!-- inline-links-inserted --> etc)
    closing_line_end = content.index("\n", second_start)

    frontmatter = content[: closing_line_end + 1]  # includes the \n after ---
    body = content[closing_line_end + 1 :]

    return frontmatter, body


def fix_issue1_frontmatter_blank_lines(frontmatter: str, body: str):
    """Issue 1: frontmatter 직후 빈 줄 2개 이상 → 1개만 유지"""
    count = 0
    # body가 \n\n\n 으로 시작하면 (빈 줄 2개 이상)
    # \n으로만 시작하는 부분을 제거하고 \n 하나만 유지
    original_body = body
    body = re.sub(r"^\n{2,}", "\n", body)
    if body != original_body:
        count = 1
    return frontmatter, body, count


def fix_issue2_ai_analysis_duplicate(body: str):
    """Issue 2: 'AI 분석 AI 분석' 또는 'AI 분석 M-DEENO AI 분석' 중복 수정"""
    count = 0

    # Pattern: 'AI 분석 M-DEENO AI 분석' → 'AI 분석'
    new_body = body.replace("AI 분석 M-DEENO AI 분석", "AI 분석")
    count += body.count("AI 분석 M-DEENO AI 분석")
    body = new_body

    # Pattern: 'AI 분석 AI 분석' → 'AI 분석'
    new_body = body.replace("AI 분석 AI 분석", "AI 분석")
    count += body.count("AI 분석 AI 분석")
    body = new_body

    return body, count


def fix_issue3_cta_blank_lines(body: str):
    """Issue 3: </div> 이후 빈 줄 3개 이상 → 최대 1개, --- 앞 빈 줄 3개 이상 → 최대 1개"""
    count = 0

    # </div> 뒤에 빈 줄 3개 이상 → 2개(\n\n = 빈 줄 1개)로 축소
    pattern = r"(</div>)\s*\n(\n{2,})"
    matches = re.findall(pattern, body)
    count += len(matches)
    body = re.sub(pattern, r"\1\n\n", body)

    # --- (구분선, frontmatter 아님) 앞에 빈 줄 3개 이상 → 최대 1개
    pattern2 = r"\n{3,}(---)\s*$"
    matches2 = re.findall(pattern2, body, re.MULTILINE)
    count += len(matches2)
    body = re.sub(r"\n{3,}(---)\s*$", r"\n\n---", body, flags=re.MULTILINE)

    return body, count


def fix_issue4_consecutive_blank_lines(body: str):
    """Issue 4: 본문에서 연속 빈 줄 3개 이상 → 2개(=빈 줄 1개)로 축소
    3개 이상 연속 \n → \n\n 으로 (콘텐츠 줄 사이 빈 줄 하나 유지)
    """
    count = 0
    # \n\n\n\n 이상 (빈 줄 2개+) → \n\n (빈 줄 1개)
    original = body
    body = re.sub(r"\n{3,}", "\n\n", body)
    # Count how many replacements (approximate)
    count = len(re.findall(r"\n{3,}", original))
    return body, count


def fix_issue5_alt_text_duplicate(body: str):
    """Issue 5: 이미지 alt text에서 'AI 분석 AI 분석' 중복 수정
    이미 Issue 2에서 전체 텍스트 치환으로 처리되지만, 명시적으로 alt text도 확인
    """
    count = 0
    pattern = r"(!\[.*?)AI 분석 AI 분석(.*?\])"
    matches = re.findall(pattern, body)
    count = len(matches)
    body = re.sub(pattern, r"\1AI 분석\2", body)
    return body, count


def process_file(filepath: str, dry_run: bool = True):
    """파일 하나를 처리합니다. 수정 건수와 변경 여부를 반환합니다."""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    result = split_frontmatter(content)
    if result is None:
        return {"changed": False, "issues": {}}

    frontmatter, body = result
    original_content = content
    issues = {}

    # Issue 1: frontmatter 직후 빈 줄
    frontmatter, body, c1 = fix_issue1_frontmatter_blank_lines(frontmatter, body)
    if c1:
        issues["issue1"] = c1

    # Issue 2: AI 분석 중복 (Issue 5도 여기서 처리됨)
    body, c2 = fix_issue2_ai_analysis_duplicate(body)
    if c2:
        issues["issue2"] = c2

    # Issue 5: alt text AI 분석 중복 (Issue 2에서 이미 처리되었지만 확인)
    body, c5 = fix_issue5_alt_text_duplicate(body)
    if c5:
        issues["issue5"] = c5

    # Issue 4: 연속 빈 줄 3개 이상 (Issue 3보다 먼저 처리하면 Issue 3 패턴이 사라짐)
    # Issue 3을 먼저 처리 후 Issue 4로 나머지 정리
    # → Issue 3: CTA~면책 과도한 빈 줄
    body, c3 = fix_issue3_cta_blank_lines(body)
    if c3:
        issues["issue3"] = c3

    # Issue 4: 전체 연속 빈 줄 정리
    body, c4 = fix_issue4_consecutive_blank_lines(body)
    if c4:
        issues["issue4"] = c4

    new_content = frontmatter + body
    changed = new_content != original_content

    if changed and not dry_run:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(new_content)

    return {"changed": changed, "issues": issues}


def main():
    parser = argparse.ArgumentParser(description="블로그 포스트 품질 소급 수정")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="수정하지 않고 대상 건수만 확인",
    )
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    posts_dir = os.path.join(base_dir, "content", "posts")

    files = glob.glob(os.path.join(posts_dir, "**", "*.md"), recursive=True)
    files = [f for f in files if not f.endswith("_index.md")]
    files.sort()

    total_files = len(files)
    changed_files = 0
    total_issues = {
        "issue1": 0,
        "issue2": 0,
        "issue3": 0,
        "issue4": 0,
        "issue5": 0,
    }

    mode = "DRY-RUN" if args.dry_run else "FIX"
    print(f"[{mode}] 대상 파일: {total_files}개")
    print("=" * 60)

    for filepath in files:
        result = process_file(filepath, dry_run=args.dry_run)
        if result["changed"]:
            changed_files += 1
            rel_path = os.path.relpath(filepath, base_dir)
            issue_summary = ", ".join(
                f"{k}:{v}" for k, v in result["issues"].items()
            )
            if args.dry_run:
                print(f"  수정 필요: {rel_path} ({issue_summary})")
        for k, v in result["issues"].items():
            total_issues[k] = total_issues.get(k, 0) + v

    print("=" * 60)
    print(f"\n[결과 요약]")
    print(f"  전체 파일:   {total_files}개")
    print(f"  변경 파일:   {changed_files}개")
    print(f"  미변경 파일: {total_files - changed_files}개")
    print()
    print("[이슈별 수정 건수]")
    print(f"  Issue 1 (frontmatter 빈 줄):        {total_issues['issue1']}건")
    print(f"  Issue 2 (AI 분석 중복):              {total_issues['issue2']}건")
    print(f"  Issue 3 (CTA 과도한 빈 줄):          {total_issues['issue3']}건")
    print(f"  Issue 4 (연속 빈 줄 3+):             {total_issues['issue4']}건")
    print(f"  Issue 5 (alt text AI 분석 중복):     {total_issues['issue5']}건")
    total_all = sum(total_issues.values())
    print(f"  ---")
    print(f"  총 수정:                             {total_all}건")


if __name__ == "__main__":
    main()
