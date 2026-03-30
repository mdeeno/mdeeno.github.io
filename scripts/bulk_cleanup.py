#!/usr/bin/env python3
"""
M-DEENO 블로그 포스트 일괄 정리 스크립트
작업:
  2. _auto 중복 파일 삭제
  3. description == title 수정
  4. frontmatter 형식 통일
  5. 깨진 Markdown 구문 수정
  6. CTA UTM 통일
"""

import os
import re
import sys
import glob
from pathlib import Path

BLOG_ROOT = Path(__file__).resolve().parent.parent
POSTS_DIR = BLOG_ROOT / "content" / "posts"

# Category mapping by directory
CATEGORY_MAP = {
    "reconstruction": "재건축/재개발",
    "market": "시장 분석",
    "strategy": "투자 전략",
    "analysis": "세금/정책",
    "niche": "부동산 꿀팁",
}

UTM_PARAMS = "utm_source=blog&utm_medium=post_cta&utm_campaign=auto_post"

DRY_RUN = "--dry-run" in sys.argv


def parse_frontmatter(content):
    """Parse YAML frontmatter from markdown content. Returns (frontmatter_str, body)."""
    if not content.startswith("---"):
        return None, content
    end = content.find("---", 3)
    if end == -1:
        return None, content
    fm_str = content[3:end].strip()
    body = content[end + 3:].lstrip("\n")
    return fm_str, body


def rebuild_frontmatter(fm_str, body):
    """Rebuild full content from frontmatter string and body."""
    return f"---\n{fm_str}\n---\n\n{body}"


def extract_fm_value(fm_str, key):
    """Extract a value from frontmatter string."""
    # Handle multi-line list format
    pattern = rf'^{key}:\s*(.*)$'
    match = re.search(pattern, fm_str, re.MULTILINE)
    if match:
        val = match.group(1).strip()
        if val:
            # Remove quotes
            if (val.startswith('"') and val.endswith('"')) or \
               (val.startswith("'") and val.endswith("'")):
                return val[1:-1]
            return val
        # Could be multi-line list
        lines = fm_str.split('\n')
        for i, line in enumerate(lines):
            if line.strip().startswith(f'{key}:'):
                items = []
                for j in range(i + 1, len(lines)):
                    stripped = lines[j].strip()
                    if stripped.startswith('- '):
                        items.append(stripped[2:].strip().strip('"').strip("'"))
                    else:
                        break
                if items:
                    return items
    return None


def set_fm_value(fm_str, key, value, quote_style='"'):
    """Set a value in frontmatter string."""
    if isinstance(value, list):
        list_str = ", ".join(f'{quote_style}{v}{quote_style}' for v in value)
        new_val = f"[{list_str}]"
    else:
        # Escape quotes in value
        escaped = value.replace('"', '\\"')
        new_val = f'{quote_style}{escaped}{quote_style}'

    # Try to replace existing key (inline value)
    pattern = rf'^({key}:\s*)(.+)$'
    match = re.search(pattern, fm_str, re.MULTILINE)
    if match:
        fm_str = fm_str[:match.start()] + f"{key}: {new_val}" + fm_str[match.end():]
        return fm_str

    # Try to replace multi-line list format
    lines = fm_str.split('\n')
    new_lines = []
    skip_list = False
    replaced = False
    for i, line in enumerate(lines):
        if skip_list:
            if line.strip().startswith('- '):
                continue
            else:
                skip_list = False
        if line.strip().startswith(f'{key}:'):
            # Check if next line is list
            if i + 1 < len(lines) and lines[i + 1].strip().startswith('- '):
                skip_list = True
                new_lines.append(f"{key}: {new_val}")
                replaced = True
                continue
            else:
                new_lines.append(f"{key}: {new_val}")
                replaced = True
                continue
        new_lines.append(line)

    if replaced:
        return '\n'.join(new_lines)

    # Key doesn't exist, add it
    return fm_str + f"\n{key}: {new_val}"


def normalize_quotes_in_fm(fm_str):
    """Normalize frontmatter to use double quotes consistently."""
    lines = fm_str.split('\n')
    new_lines = []
    for line in lines:
        # Skip empty lines
        if not line.strip():
            new_lines.append(line)
            continue

        # Handle key: value pairs
        match = re.match(r'^(\w[\w-]*):\s*(.*)', line)
        if match:
            key = match.group(1)
            val = match.group(2).strip()

            # Skip date, draft, image, slug, aliases lines — don't re-quote
            if key in ('date', 'draft', 'image', 'slug'):
                # For image/slug, ensure double quotes
                if val and val.startswith("'") and val.endswith("'"):
                    val = '"' + val[1:-1] + '"'
                elif val and not val.startswith('"') and key in ('image', 'slug'):
                    val = f'"{val}"'
                new_lines.append(f"{key}: {val}")
                continue

            if key == 'aliases':
                new_lines.append(line)
                continue

            # Handle inline list: ['a', 'b'] or ["a", "b"]
            if val.startswith('['):
                # Normalize list items to double quotes
                items = re.findall(r"""['"]([^'"]*?)['"]""", val)
                if items:
                    list_str = ', '.join(f'"{item}"' for item in items)
                    new_lines.append(f"{key}: [{list_str}]")
                else:
                    new_lines.append(line)
                continue

            # Handle single-quoted string value
            if val.startswith("'") and val.endswith("'"):
                inner = val[1:-1]
                # Escape any double quotes inside
                inner = inner.replace('"', '\\"')
                new_lines.append(f'{key}: "{inner}"')
                continue

            # Handle unquoted string value (for title, description etc.)
            if key in ('title', 'description') and val and not val.startswith('"'):
                inner = val.replace('"', '\\"')
                new_lines.append(f'{key}: "{inner}"')
                continue

            new_lines.append(line)
        elif line.strip().startswith('- '):
            # List item — keep as is (will be converted to inline later if categories/tags)
            new_lines.append(line)
        else:
            new_lines.append(line)

    return '\n'.join(new_lines)


def fix_categories(fm_str, directory):
    """Fix categories to match directory structure."""
    expected_cat = CATEGORY_MAP.get(directory)
    if not expected_cat:
        return fm_str

    # Replace categories with correct value
    return set_fm_value(fm_str, "categories", [expected_cat])


def convert_multiline_lists_to_inline(fm_str):
    """Convert multi-line YAML lists to inline format for categories and tags."""
    lines = fm_str.split('\n')
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(r'^(categories|tags):\s*$', line.strip())
        if match:
            key = match.group(1)
            items = []
            j = i + 1
            while j < len(lines):
                stripped = lines[j].strip()
                # Standard YAML list: - item
                if stripped.startswith('- '):
                    item = stripped[2:].strip().strip('"').strip("'")
                    items.append(item)
                    j += 1
                # Broken format: indented 'item', or "item", possibly with trailing comma or ]
                elif re.match(r"""^['"].*['"],?\s*$""", stripped) or stripped == ']':
                    if stripped == ']':
                        j += 1
                        break
                    item = stripped.rstrip(',').rstrip(']').strip().strip('"').strip("'")
                    if item:
                        items.append(item)
                    j += 1
                else:
                    break
            if items:
                list_str = ', '.join(f'"{item}"' for item in items)
                new_lines.append(f'{key}: [{list_str}]')
                i = j
                continue
        new_lines.append(line)
        i += 1
    return '\n'.join(new_lines)


def extract_description_from_body(body, max_len=155):
    """Extract first 2-3 sentences from body for description."""
    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', body)
    # Remove markdown formatting
    clean = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', clean)
    clean = re.sub(r'[*_#>`]', '', clean)
    clean = re.sub(r'!\[[^\]]*\]\([^)]*\)', '', clean)

    # Split into sentences
    lines = clean.strip().split('\n')
    text = ' '.join(line.strip() for line in lines if line.strip() and not line.strip().startswith('|'))

    # Get first 2-3 sentences
    sentences = re.split(r'(?<=[.!?다니요])\s+', text)
    desc = ''
    for sent in sentences:
        sent = sent.strip()
        if not sent:
            continue
        if len(desc) + len(sent) + 1 > max_len:
            if desc:
                break
            desc = sent[:max_len - 3] + '...'
            break
        desc = (desc + ' ' + sent).strip() if desc else sent

    if not desc or len(desc) < 30:
        # Fallback: just take first chunk of text
        desc = text[:max_len - 3].rsplit(' ', 1)[0] + '...' if len(text) > max_len else text

    return desc.strip()


def fix_broken_blockquotes(content):
    """Fix > **> pattern to > **."""
    return re.sub(r'> \*\*>', '> **', content)


def fix_unclosed_brackets(content):
    """Fix common unclosed bracket patterns."""
    # Fix standalone [ on a line (incomplete link)
    lines = content.split('\n')
    new_lines = []
    for i, line in enumerate(lines):
        stripped = line.strip()
        # Line that is just [
        if stripped == '[':
            # Check if next line has the rest of the link
            if i + 1 < len(lines) and ']' in lines[i + 1]:
                # Merge with next line
                new_lines.append(line + lines[i + 1].strip())
                # Mark next line to skip
                lines[i + 1] = '___SKIP___'
                continue
            else:
                # Remove orphan bracket
                continue
        if stripped == '___SKIP___':
            continue
        new_lines.append(line)
    return '\n'.join(new_lines)


def fix_broken_html(content):
    """Fix common broken HTML patterns."""
    # Fix unclosed <br> tags that might be <br/>
    content = re.sub(r'<br(?!\s*/?\s*>)', '<br />', content)
    return content


def fix_utm_links(content):
    """Add UTM parameters to mdeeno.com/member links that don't have them."""
    def replace_link(match):
        url = match.group(0)
        if 'utm_source' in url:
            return url
        if '?' in url:
            return url + '&' + UTM_PARAMS
        else:
            return url + '?' + UTM_PARAMS

    # Match href="https://mdeeno.com/member..." patterns
    content = re.sub(
        r'https://mdeeno\.com/member(?=["\s>?])',
        lambda m: m.group(0) + '?' + UTM_PARAMS if 'utm_source' not in m.group(0) else m.group(0),
        content
    )
    # Also handle cases where /member has query params but no UTM
    content = re.sub(
        r'(https://mdeeno\.com/member\?)(?!.*utm_source)',
        lambda m: m.group(0) + UTM_PARAMS + '&',
        content
    )
    return content


def find_auto_duplicates():
    """Find _auto files that have non-auto counterparts."""
    auto_files = []
    duplicates = []
    orphans = []

    for root, dirs, files in os.walk(POSTS_DIR):
        for f in files:
            if '_auto' in f and f.endswith('.md'):
                auto_path = os.path.join(root, f)
                # Generate expected non-auto filename
                non_auto_name = f.replace('_auto.md', '.md').replace('_auto', '')
                non_auto_path = os.path.join(root, non_auto_name)

                auto_files.append(auto_path)

                if os.path.exists(non_auto_path):
                    duplicates.append((auto_path, non_auto_path))
                else:
                    orphans.append(auto_path)

    return auto_files, duplicates, orphans


def process_file(filepath, stats, delete_list):
    """Process a single markdown file."""
    rel_path = os.path.relpath(filepath, BLOG_ROOT)

    with open(filepath, 'r', encoding='utf-8') as f:
        original = f.read()

    content = original

    # Parse frontmatter
    fm_str, body = parse_frontmatter(content)
    if fm_str is None:
        return

    # Determine directory
    parts = Path(filepath).relative_to(POSTS_DIR).parts
    directory = parts[0] if len(parts) > 1 else None

    # === Task 4: Normalize frontmatter ===

    # Convert multi-line lists to inline first
    fm_str = convert_multiline_lists_to_inline(fm_str)

    # Normalize quotes
    fm_str = normalize_quotes_in_fm(fm_str)

    # Fix categories based on directory
    if directory:
        fm_str = fix_categories(fm_str, directory)

    # === Task 3: Fix description == title ===
    title = extract_fm_value(fm_str, 'title')
    description = extract_fm_value(fm_str, 'description')

    if title and description:
        # Normalize for comparison (strip quotes, whitespace)
        title_clean = title.strip().strip('"').strip("'")
        desc_clean = description.strip().strip('"').strip("'")

        if title_clean == desc_clean:
            new_desc = extract_description_from_body(body)
            if new_desc and len(new_desc) >= 30:
                fm_str = set_fm_value(fm_str, 'description', new_desc)
                stats['desc_fixed'] += 1

    # Rebuild content
    content = rebuild_frontmatter(fm_str, body)

    # === Task 5: Fix broken markdown ===
    old_content = content
    content = fix_broken_blockquotes(content)
    if content != old_content:
        stats['blockquote_fixed'] += 1

    old_content = content
    content = fix_unclosed_brackets(content)
    if content != old_content:
        stats['bracket_fixed'] += 1

    # === Task 6: Fix UTM links ===
    old_content = content
    content = fix_utm_links(content)
    if content != old_content:
        stats['utm_fixed'] += 1

    # Write if changed
    if content != original:
        stats['files_modified'] += 1
        if not DRY_RUN:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)


def main():
    mode = "DRY-RUN" if DRY_RUN else "LIVE"
    print(f"=== M-DEENO 블로그 일괄 정리 ({mode}) ===\n")

    stats = {
        'files_total': 0,
        'files_modified': 0,
        'auto_deleted': 0,
        'auto_orphan_deleted': 0,
        'desc_fixed': 0,
        'blockquote_fixed': 0,
        'bracket_fixed': 0,
        'utm_fixed': 0,
    }

    # === Task 2: Find and delete _auto duplicates ===
    print("--- Task 2: _auto 중복 파일 ---")
    auto_files, duplicates, orphans = find_auto_duplicates()
    print(f"  전체 _auto 파일: {len(auto_files)}개")
    print(f"  중복 (비_auto 존재): {len(duplicates)}개")
    print(f"  단독 _auto (비_auto 없음): {len(orphans)}개")

    if duplicates:
        print(f"\n  삭제 대상 (중복 _auto): {len(duplicates)}개")
        for auto_path, non_auto_path in duplicates[:5]:
            print(f"    - {os.path.basename(auto_path)}")
        if len(duplicates) > 5:
            print(f"    ... 외 {len(duplicates) - 5}개")

        if not DRY_RUN:
            for auto_path, _ in duplicates:
                os.remove(auto_path)
                stats['auto_deleted'] += 1
        else:
            stats['auto_deleted'] = len(duplicates)

    # Orphan _auto files: these have no non-auto counterpart, keep them but rename
    # Actually per spec: only delete if non-auto counterpart exists. Keep orphans.
    print(f"\n  유지되는 _auto (단독): {len(orphans)}개\n")

    # === Tasks 3-6: Process all remaining files ===
    print("--- Tasks 3-6: frontmatter/markdown/UTM 수정 ---")

    all_posts = []
    for root, dirs, files in os.walk(POSTS_DIR):
        for f in files:
            if f.endswith('.md') and f != '_index.md':
                filepath = os.path.join(root, f)
                # Skip files we just deleted
                if not DRY_RUN and not os.path.exists(filepath):
                    continue
                # In dry-run, skip duplicates that would be deleted
                if DRY_RUN and any(filepath == d[0] for d in duplicates):
                    continue
                all_posts.append(filepath)

    stats['files_total'] = len(all_posts)

    for filepath in all_posts:
        process_file(filepath, stats, [])

    print(f"\n=== 결과 요약 ({mode}) ===")
    print(f"  전체 포스트 수: {stats['files_total']}")
    print(f"  _auto 중복 삭제: {stats['auto_deleted']}개")
    print(f"  description 수정: {stats['desc_fixed']}개")
    print(f"  blockquote 수정: {stats['blockquote_fixed']}개")
    print(f"  bracket 수정: {stats['bracket_fixed']}개")
    print(f"  UTM 추가: {stats['utm_fixed']}개")
    print(f"  총 수정 파일: {stats['files_modified']}개")

    if DRY_RUN:
        print("\n⚠ DRY-RUN 모드입니다. 실제 변경은 없습니다.")
        print("실행하려면: python3 scripts/bulk_cleanup.py")


if __name__ == "__main__":
    main()
