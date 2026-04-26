#!/usr/bin/env python3
"""
블로그 전체 품질 일괄 수정 스크립트

1. Prop-Logic™ → M-DEENO 분석 엔진
2. 깨진 이미지(404 외부 URL) 참조 제거
3. 깨진 내부 링크 수정/제거
4. HTML 태그 불일치 수정 (고아 닫힘 태그 제거)
5. 짧은/잘린 포스트 처리 (draft 또는 마무리)
"""

import os
import re
import glob
import yaml

POSTS_DIR = "/Users/suhun/Projects/mdeeno/mdeeno.github.io/content/posts"

# 카운터
stats = {
    "prop_logic": 0,
    "broken_img": 0,
    "broken_link": 0,
    "html_fix": 0,
    "draft_set": 0,
    "truncated_trim": 0,
    "files_modified": 0,
}


def get_all_post_slugs():
    """모든 포스트의 URL slug를 수집 (내부 링크 검증용)"""
    slugs = set()
    for md_file in glob.glob(os.path.join(POSTS_DIR, "**/*.md"), recursive=True):
        rel = os.path.relpath(md_file, POSTS_DIR)
        # Hugo slug: /posts/category/filename-without-ext/
        slug_parts = rel.rsplit(".", 1)[0]  # .md 제거
        slug = f"/posts/{slug_parts}/"
        slugs.add(slug)
    return slugs


def parse_frontmatter(content):
    """front matter와 본문 분리"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            return parts[1], "---" + parts[1] + "---" + parts[2], parts[2]
    return "", content, content


def get_body_text(body):
    """HTML 태그, shortcode 제외한 순수 텍스트 글자 수"""
    text = re.sub(r'\{\{<.*?>\}\}', '', body)  # Hugo shortcodes
    text = re.sub(r'\{\{%.*?%\}\}', '', text)
    text = re.sub(r'<[^>]+>', '', text)  # HTML tags
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)  # markdown images
    text = re.sub(r'\[([^\]]*)\]\([^\)]*\)', r'\1', text)  # markdown links → text only
    text = re.sub(r'[#*_`>|~\-]', '', text)  # markdown formatting
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def is_sentence_complete(text):
    """마지막 문장이 정상 종료인지"""
    text = text.rstrip()
    if not text:
        return True
    return text[-1] in '.?!。？！'


def fix_prop_logic(content):
    """Prop-Logic™ → M-DEENO 분석 엔진"""
    count = content.count("Prop-Logic™")
    if count > 0:
        content = content.replace("Prop-Logic™", "M-DEENO 분석 엔진")
        stats["prop_logic"] += count
    # Prop-Logic (without ™) 도 처리
    count2 = len(re.findall(r'Prop-Logic(?!™)', content))
    if count2 > 0:
        content = re.sub(r'Prop-Logic(?!™)', 'M-DEENO 분석 엔진', content)
        stats["prop_logic"] += count2
    return content


def fix_broken_images(content):
    """깨진 이미지 참조 제거"""
    # 패턴: ![alt](https://raw.githubusercontent.com/mdeeno/mdeeno.github.io/main/static/images/chart-*.png)
    pattern = r'!\[[^\]]*\]\(https://raw\.githubusercontent\.com/mdeeno/mdeeno\.github\.io/main/static/images/chart-[^)]+\)\n?'
    matches = re.findall(pattern, content)
    if matches:
        content = re.sub(pattern, '', content)
        stats["broken_img"] += len(matches)

    # <img src="...chart-..."> 패턴도 처리
    img_pattern = r'<img[^>]*src=["\']https://raw\.githubusercontent\.com/mdeeno/mdeeno\.github\.io/main/static/images/chart-[^"\']+["\'][^>]*/?\s*>\n?'
    matches2 = re.findall(img_pattern, content)
    if matches2:
        content = re.sub(img_pattern, '', content)
        stats["broken_img"] += len(matches2)

    return content


def fix_broken_internal_links(content, valid_slugs):
    """깨진 내부 링크를 텍스트로 변환"""
    # 패턴: [text](/posts/category/slug/)
    def replace_link(match):
        full = match.group(0)
        text = match.group(1)
        path = match.group(2)
        # /posts/로 시작하는 내부 링크만 검증
        if path.startswith("/posts/"):
            # slug 정규화
            normalized = path.rstrip("/") + "/"
            if normalized not in valid_slugs:
                stats["broken_link"] += 1
                return text  # 링크 제거, 텍스트만 남김
        return full

    content = re.sub(r'\[([^\]]+)\]\((/posts/[^\)]+)\)', replace_link, content)
    return content


def fix_html_tags(content):
    """고아 닫힘 태그 정리 — 열린 태그보다 닫힌 태그가 많은 경우 여분 제거"""
    # div 태그 불일치 수정
    for tag in ['div', 'span', 'p']:
        open_count = len(re.findall(f'<{tag}[\\s>]', content))
        close_count = len(re.findall(f'</{tag}>', content))

        if close_count > open_count:
            excess = close_count - open_count
            # 뒤에서부터 여분의 닫힘 태그 제거
            for _ in range(excess):
                # 가장 마지막 닫힘 태그 제거
                idx = content.rfind(f'</{tag}>')
                if idx >= 0:
                    content = content[:idx] + content[idx + len(f'</{tag}>'):]
                    stats["html_fix"] += 1

    return content


def handle_short_truncated(content, filepath):
    """짧은/잘린 포스트 처리"""
    fm_str, full, body = parse_frontmatter(content)
    body_text = get_body_text(body)
    char_count = len(body_text)
    complete = is_sentence_complete(body_text)

    # 본문 1000자 미만 → draft: true
    if char_count < 1000:
        content = set_draft(content)
        stats["draft_set"] += 1
        return content

    # 1000~2000자
    if char_count < 2000:
        if not complete:
            # 문장 중간 잘림 → draft: true
            content = set_draft(content)
            stats["draft_set"] += 1
            return content
        # 문장 정상 종료 → 유지
        return content

    # 2000자 이상
    if not complete:
        # 마지막 미완성 문장만 제거하여 자연스럽게 마무리
        content = trim_incomplete_sentence(content)
        stats["truncated_trim"] += 1
        return content

    return content


def set_draft(content):
    """front matter에 draft: true 설정"""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            fm = parts[1]
            if "draft:" in fm:
                fm = re.sub(r'draft:\s*\w+', 'draft: true', fm)
            else:
                fm = fm.rstrip() + "\ndraft: true\n"
            return "---" + fm + "---" + parts[2]
    return content


def trim_incomplete_sentence(content):
    """마지막 미완성 문장 제거"""
    if not content.startswith("---"):
        return content

    parts = content.split("---", 2)
    if len(parts) < 3:
        return content

    body = parts[2]

    # 본문에서 마지막 실제 텍스트 라인을 찾아 마침표로 끝나지 않으면 제거
    lines = body.split('\n')
    # 뒤에서부터 실제 텍스트 라인 찾기 (빈 줄, shortcode, HTML만 있는 줄 스킵)
    last_text_idx = -1
    for i in range(len(lines) - 1, -1, -1):
        line = lines[i].strip()
        if not line:
            continue
        if line.startswith('{{') or line.startswith('<') or line.startswith('>') or line.startswith('---'):
            continue
        # 실제 텍스트 라인
        if line and not is_sentence_complete(line):
            # 이 줄을 제거
            lines[i] = ''
            last_text_idx = i
            break
        else:
            break  # 마지막 텍스트 라인이 정상 종료 → 수정 불필요

    if last_text_idx >= 0:
        body = '\n'.join(lines)

    return "---" + parts[1] + "---" + body


def main():
    valid_slugs = get_all_post_slugs()
    md_files = glob.glob(os.path.join(POSTS_DIR, "**/*.md"), recursive=True)

    for filepath in sorted(md_files):
        with open(filepath, "r", encoding="utf-8") as f:
            original = f.read()

        content = original

        # 1. Prop-Logic™ 치환
        content = fix_prop_logic(content)

        # 2. 깨진 이미지 제거
        content = fix_broken_images(content)

        # 3. 깨진 내부 링크
        content = fix_broken_internal_links(content, valid_slugs)

        # 4. HTML 태그 불일치
        content = fix_html_tags(content)

        # 5. 짧은/잘린 포스트
        content = handle_short_truncated(content, filepath)

        # 연속 빈 줄 정리
        content = re.sub(r'\n{4,}', '\n\n\n', content)

        if content != original:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            stats["files_modified"] += 1

    print("=" * 60)
    print("블로그 품질 일괄 수정 완료")
    print("=" * 60)
    print(f"  Prop-Logic™ 치환: {stats['prop_logic']}건")
    print(f"  깨진 이미지 제거: {stats['broken_img']}건")
    print(f"  깨진 내부 링크 수정: {stats['broken_link']}건")
    print(f"  HTML 태그 수정: {stats['html_fix']}건")
    print(f"  draft 처리 (짧은/잘린): {stats['draft_set']}건")
    print(f"  잘린 문장 마무리: {stats['truncated_trim']}건")
    print(f"  수정된 파일: {stats['files_modified']}개")


if __name__ == "__main__":
    main()
