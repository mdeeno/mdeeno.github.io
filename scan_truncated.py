"""
블로그 포스트 전수 스캔: 잘린 콘텐츠(비정상적으로 짧은 포스트) 식별
"""

import os
import re
from pathlib import Path

POSTS_DIR = Path("/Users/suhun/Projects/mdeeno/mdeeno.github.io/content/posts/")
REPORT_PATH = Path("/Users/suhun/Projects/mdeeno/mdeeno.github.io/truncated_posts_report.txt")
SHORT_THRESHOLD = 500  # 본문 500자 미만 = 비정상


def extract_body(content: str) -> str:
    """front matter 제거 후 본문 추출, HTML 태그 제거"""
    # front matter 제거 (--- ... ---)
    fm_match = re.match(r"^---\s*\n.*?\n---\s*\n", content, re.DOTALL)
    body = content[fm_match.end():] if fm_match else content

    # HTML 태그 제거
    body = re.sub(r"<[^>]+>", "", body)
    # 마크다운 이미지/링크 문법 제거
    body = re.sub(r"!\[.*?\]\(.*?\)", "", body)
    body = re.sub(r"\[([^\]]*)\]\(.*?\)", r"\1", body)
    # 마크다운 헤딩 기호 제거
    body = re.sub(r"^#+\s*", "", body, flags=re.MULTILINE)
    # 마크다운 강조 제거
    body = re.sub(r"\*{1,3}|_{1,3}", "", body)
    # 공백 정리
    body = body.strip()
    return body


def check_truncation(body: str) -> bool:
    """마지막 실제 텍스트가 마침표/물음표/느낌표로 끝나지 않으면 잘림 의심.
    Hugo shortcode({{...}})와 빈 줄은 무시하고 마지막 실제 문장을 찾는다."""
    if not body:
        return True
    # Hugo shortcode, 빈 줄, 마크다운 구분선 제거 후 마지막 실제 텍스트 찾기
    cleaned = re.sub(r"\{\{[^}]*\}\}", "", body)
    cleaned = re.sub(r"^[-*_]{3,}\s*$", "", cleaned, flags=re.MULTILINE)
    cleaned = cleaned.rstrip()
    if not cleaned:
        return True
    last_char = cleaned[-1]
    return last_char not in ".?!。)"


def scan_posts():
    results = []
    md_files = list(POSTS_DIR.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "_index.md"]

    for filepath in md_files:
        try:
            content = filepath.read_text(encoding="utf-8")
        except Exception as e:
            results.append({
                "path": str(filepath),
                "rel_path": str(filepath.relative_to(POSTS_DIR)),
                "char_count": -1,
                "truncated": True,
                "error": str(e),
            })
            continue

        body = extract_body(content)
        char_count = len(body.replace("\n", "").replace(" ", ""))
        is_truncated = check_truncation(body)

        results.append({
            "path": str(filepath),
            "rel_path": str(filepath.relative_to(POSTS_DIR)),
            "char_count": char_count,
            "truncated": is_truncated,
            "short": char_count < SHORT_THRESHOLD,
            "last_30": body[-30:].replace("\n", "\\n") if body else "(empty)",
        })

    # 글자 수 오름차순 정렬
    results.sort(key=lambda x: x["char_count"])
    return results


def write_report(results):
    short_posts = [r for r in results if r.get("short")]
    truncated_posts = [r for r in results if r.get("truncated")]
    both = [r for r in results if r.get("short") or r.get("truncated")]

    lines = []
    lines.append("=" * 80)
    lines.append("블로그 포스트 전수 스캔 리포트")
    lines.append("=" * 80)
    lines.append("")
    lines.append(f"전체 포스트 수: {len(results)}")
    lines.append(f"본문 {SHORT_THRESHOLD}자 미만 (짧은 포스트): {len(short_posts)}")
    lines.append(f"문장 중간 잘림 의심 (마침표 미종결): {len(truncated_posts)}")
    lines.append(f"둘 중 하나라도 해당: {len(both)}")
    lines.append("")

    # --- 짧은 포스트 목록 ---
    lines.append("=" * 80)
    lines.append(f"[1] 본문 {SHORT_THRESHOLD}자 미만 포스트 (글자 수 오름차순)")
    lines.append("=" * 80)
    if short_posts:
        for r in short_posts:
            flag = " [잘림 의심]" if r["truncated"] else ""
            lines.append(f"  {r['char_count']:>5}자 | {r['rel_path']}{flag}")
            lines.append(f"         끝부분: ...{r.get('last_30', '')}")
            lines.append("")
    else:
        lines.append("  해당 없음")
    lines.append("")

    # --- 문장 잘림 의심 (500자 이상) ---
    truncated_long = [r for r in truncated_posts if not r.get("short")]
    lines.append("=" * 80)
    lines.append(f"[2] 문장 중간 잘림 의심 ({SHORT_THRESHOLD}자 이상, 마침표 미종결)")
    lines.append("=" * 80)
    if truncated_long:
        for r in truncated_long:
            lines.append(f"  {r['char_count']:>5}자 | {r['rel_path']}")
            lines.append(f"         끝부분: ...{r.get('last_30', '')}")
            lines.append("")
    else:
        lines.append("  해당 없음")
    lines.append("")

    # --- 전체 글자 수 분포 ---
    lines.append("=" * 80)
    lines.append("[3] 전체 포스트 글자 수 분포 (오름차순, 상위 30개)")
    lines.append("=" * 80)
    for r in results[:30]:
        flag = ""
        if r.get("short"):
            flag += " [짧음]"
        if r.get("truncated"):
            flag += " [잘림 의심]"
        lines.append(f"  {r['char_count']:>5}자 | {r['rel_path']}{flag}")
    if len(results) > 30:
        lines.append(f"  ... 외 {len(results) - 30}개")
    lines.append("")

    # --- 통계 ---
    counts = [r["char_count"] for r in results if r["char_count"] >= 0]
    if counts:
        lines.append("=" * 80)
        lines.append("[4] 통계")
        lines.append("=" * 80)
        lines.append(f"  최소: {min(counts)}자")
        lines.append(f"  최대: {max(counts)}자")
        lines.append(f"  평균: {sum(counts) // len(counts)}자")
        mid = len(counts) // 2
        median = counts[mid] if len(counts) % 2 else (counts[mid - 1] + counts[mid]) // 2
        lines.append(f"  중앙값: {median}자")

    report = "\n".join(lines)
    REPORT_PATH.write_text(report, encoding="utf-8")
    return report


if __name__ == "__main__":
    results = scan_posts()
    report = write_report(results)
    print(report)
