#!/usr/bin/env python3
"""
블로그 포스트 품질 이슈 스캐너
스캔 항목:
1. front matter에 title/date/description 누락 또는 빈 값
2. "Prop-Logic™" 본문 노출
3. 깨진 내부 링크 (/posts/... 링크의 실제 파일 존재 여부)
4. 닫히지 않은 HTML 태그 (열린/닫힌 태그 수 불일치)
"""

import os
import re
import glob
from collections import defaultdict
from pathlib import Path

POSTS_DIR = "/Users/suhun/Projects/mdeeno/mdeeno.github.io/content/posts"
REPORT_PATH = "/Users/suhun/Projects/mdeeno/mdeeno.github.io/quality_issues_report.txt"

# 모든 md 파일 수집
all_md_files = glob.glob(os.path.join(POSTS_DIR, "**", "*.md"), recursive=True)
# _index.md 제외
all_md_files = [f for f in all_md_files if not f.endswith("_index.md")]

# 포스트 slug 목록 생성 (내부 링크 검증용)
# /posts/category/slug/ 형태의 링크를 검증하기 위해 상대 경로 매핑
existing_slugs = set()
for f in all_md_files:
    rel = os.path.relpath(f, POSTS_DIR)
    # category/filename.md -> category/filename (확장자 제거)
    slug = os.path.splitext(rel)[0]
    existing_slugs.add(slug)
    # 파일명만으로도 매칭 시도
    basename = os.path.splitext(os.path.basename(f))[0]
    existing_slugs.add(basename)

# 카테고리 디렉토리 목록
existing_dirs = set()
for f in all_md_files:
    rel = os.path.relpath(f, POSTS_DIR)
    parts = rel.split(os.sep)
    if len(parts) > 1:
        existing_dirs.add(parts[0])

# 결과 저장
issues_frontmatter = []
issues_proplogic = []
issues_broken_links = []
issues_unclosed_tags = []

# 검사할 HTML 태그 목록
CHECK_TAGS = ["div", "span", "section", "article", "header", "footer",
              "nav", "main", "aside", "table", "thead", "tbody", "tr",
              "td", "th", "ul", "ol", "li", "p", "blockquote", "details",
              "summary", "figure", "figcaption", "a", "strong", "em",
              "b", "i", "u", "h1", "h2", "h3", "h4", "h5", "h6"]


def parse_frontmatter(content):
    """YAML front matter 파싱 (간단 버전)"""
    if not content.startswith("---"):
        return None
    end = content.find("---", 3)
    if end == -1:
        return None
    fm_text = content[3:end]
    result = {}
    for line in fm_text.split("\n"):
        line = line.strip()
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip().strip('"').strip("'")
            result[key] = val
    return result


def check_frontmatter(filepath, content):
    """front matter에서 title, date, description 누락/빈 값 확인"""
    fm = parse_frontmatter(content)
    if fm is None:
        issues_frontmatter.append((filepath, "front matter 자체가 없음"))
        return
    missing = []
    for field in ["title", "date", "description"]:
        if field not in fm or not fm[field]:
            missing.append(field)
    if missing:
        issues_frontmatter.append((filepath, f"누락/빈 값: {', '.join(missing)}"))


def check_proplogic(filepath, content):
    """Prop-Logic™ 노출 확인 (front matter 제외, 본문만)"""
    # front matter 이후 본문 추출
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            body = content[end + 3:]
        else:
            body = content
    else:
        body = content

    # 대소문자 무시, 다양한 변형 포함
    patterns = [r"Prop-Logic™", r"Prop-Logic", r"PropLogic", r"prop-logic"]
    for pat in patterns:
        matches = re.findall(pat, body, re.IGNORECASE)
        if matches:
            issues_proplogic.append((filepath, f"'{matches[0]}' 발견 ({len(matches)}회)"))
            break


def check_internal_links(filepath, content):
    """내부 링크 (/posts/...) 검증"""
    # 마크다운 링크와 HTML href 모두 검사
    link_patterns = [
        r'\[.*?\]\((/posts/[^)]+)\)',        # [text](/posts/...)
        r'href=["\'](/posts/[^"\']+)["\']',  # href="/posts/..."
    ]
    for pat in link_patterns:
        links = re.findall(pat, content)
        for link in links:
            # 앵커 제거
            link_clean = link.split("#")[0].rstrip("/")
            # /posts/ 이후 경로 추출
            post_path = link_clean.replace("/posts/", "", 1)

            # 실제 파일 존재 확인
            # 1) 정확한 경로로 md 파일 찾기
            candidate_paths = [
                os.path.join(POSTS_DIR, post_path + ".md"),
                os.path.join(POSTS_DIR, post_path, "index.md"),
                os.path.join(POSTS_DIR, post_path, "_index.md"),
            ]

            # 2) slug 기반 매칭
            found = False
            for cp in candidate_paths:
                if os.path.exists(cp):
                    found = True
                    break

            if not found:
                # slug 부분 매칭 시도
                if post_path in existing_slugs:
                    found = True

            if not found:
                # glob으로 부분 매칭
                glob_results = glob.glob(
                    os.path.join(POSTS_DIR, "**", f"*{os.path.basename(post_path)}*"),
                    recursive=True,
                )
                if glob_results:
                    found = True

            if not found:
                issues_broken_links.append((filepath, link))


def check_unclosed_tags(filepath, content):
    """닫히지 않은 HTML 태그 간단 체크"""
    # front matter 이후 본문만
    if content.startswith("---"):
        end = content.find("---", 3)
        if end != -1:
            body = content[end + 3:]
        else:
            body = content
    else:
        body = content

    tag_mismatches = []
    for tag in CHECK_TAGS:
        # 열린 태그 (<tag ...> 또는 <tag>), self-closing 제외
        open_pattern = rf"<{tag}(?:\s[^>]*)?>(?!.*/>)"
        close_pattern = rf"</{tag}\s*>"
        self_closing = rf"<{tag}[^>]*/>"

        open_count = len(re.findall(open_pattern, body, re.IGNORECASE))
        close_count = len(re.findall(close_pattern, body, re.IGNORECASE))
        sc_count = len(re.findall(self_closing, body, re.IGNORECASE))

        # self-closing은 열린 태그에서 제외
        effective_open = open_count - sc_count
        if effective_open < 0:
            effective_open = 0

        diff = effective_open - close_count
        if diff != 0:
            tag_mismatches.append(f"<{tag}>: 열림 {effective_open}, 닫힘 {close_count} (차이: {diff:+d})")

    if tag_mismatches:
        issues_unclosed_tags.append((filepath, tag_mismatches))


# 전체 스캔 실행
print(f"총 {len(all_md_files)}개 포스트 스캔 시작...")

for i, filepath in enumerate(all_md_files):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        issues_frontmatter.append((filepath, f"파일 읽기 실패: {e}"))
        continue

    check_frontmatter(filepath, content)
    check_proplogic(filepath, content)
    check_internal_links(filepath, content)
    check_unclosed_tags(filepath, content)

    if (i + 1) % 100 == 0:
        print(f"  {i + 1}/{len(all_md_files)} 완료...")

print(f"스캔 완료. 리포트 생성 중...")

# 상대 경로 변환 헬퍼
def rel(path):
    return os.path.relpath(path, POSTS_DIR)

# 리포트 생성
with open(REPORT_PATH, "w", encoding="utf-8") as f:
    f.write("=" * 80 + "\n")
    f.write("  블로그 포스트 품질 이슈 리포트\n")
    f.write(f"  스캔 대상: {len(all_md_files)}개 포스트\n")
    f.write(f"  경로: {POSTS_DIR}\n")
    f.write("=" * 80 + "\n\n")

    # 1. Front matter 이슈
    f.write("-" * 80 + "\n")
    f.write(f"[1] Front Matter 누락/빈 값 ({len(issues_frontmatter)}건)\n")
    f.write("-" * 80 + "\n")
    if issues_frontmatter:
        for path, issue in issues_frontmatter:
            f.write(f"  - {rel(path)}\n    → {issue}\n")
    else:
        f.write("  (이슈 없음)\n")
    f.write("\n")

    # 2. Prop-Logic 노출
    f.write("-" * 80 + "\n")
    f.write(f"[2] Prop-Logic™ 본문 노출 ({len(issues_proplogic)}건)\n")
    f.write("    → 'M-DEENO 분석 엔진'으로 교체 필요\n")
    f.write("-" * 80 + "\n")
    if issues_proplogic:
        for path, issue in issues_proplogic:
            f.write(f"  - {rel(path)}\n    → {issue}\n")
    else:
        f.write("  (이슈 없음)\n")
    f.write("\n")

    # 3. 깨진 내부 링크
    f.write("-" * 80 + "\n")
    f.write(f"[3] 깨진 내부 링크 ({len(issues_broken_links)}건)\n")
    f.write("-" * 80 + "\n")
    if issues_broken_links:
        for path, link in issues_broken_links:
            f.write(f"  - {rel(path)}\n    → 깨진 링크: {link}\n")
    else:
        f.write("  (이슈 없음)\n")
    f.write("\n")

    # 4. 닫히지 않은 HTML 태그
    f.write("-" * 80 + "\n")
    f.write(f"[4] HTML 태그 불일치 ({len(issues_unclosed_tags)}건)\n")
    f.write("-" * 80 + "\n")
    if issues_unclosed_tags:
        for path, mismatches in issues_unclosed_tags:
            f.write(f"  - {rel(path)}\n")
            for m in mismatches:
                f.write(f"    → {m}\n")
    else:
        f.write("  (이슈 없음)\n")
    f.write("\n")

    # 요약
    f.write("=" * 80 + "\n")
    f.write("  요약\n")
    f.write("=" * 80 + "\n")
    total = len(issues_frontmatter) + len(issues_proplogic) + len(issues_broken_links) + len(issues_unclosed_tags)
    f.write(f"  총 이슈: {total}건\n")
    f.write(f"    [1] Front Matter 이슈: {len(issues_frontmatter)}건\n")
    f.write(f"    [2] Prop-Logic™ 노출: {len(issues_proplogic)}건\n")
    f.write(f"    [3] 깨진 내부 링크: {len(issues_broken_links)}건\n")
    f.write(f"    [4] HTML 태그 불일치: {len(issues_unclosed_tags)}건\n")

print(f"리포트 저장 완료: {REPORT_PATH}")
print(f"\n=== 요약 ===")
print(f"[1] Front Matter 이슈: {len(issues_frontmatter)}건")
print(f"[2] Prop-Logic™ 노출: {len(issues_proplogic)}건")
print(f"[3] 깨진 내부 링크: {len(issues_broken_links)}건")
print(f"[4] HTML 태그 불일치: {len(issues_unclosed_tags)}건")
print(f"총 이슈: {len(issues_frontmatter) + len(issues_proplogic) + len(issues_broken_links) + len(issues_unclosed_tags)}건")
