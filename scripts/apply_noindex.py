#!/usr/bin/env python3
"""
보존 목록에 없는 포스트에 robotsNoIndex: true를 추가하는 스크립트.

사용법:
  python3 scripts/apply_noindex.py --keep-list scripts/keep_posts.txt --dry-run
  python3 scripts/apply_noindex.py --keep-list scripts/keep_posts.txt

keep_posts.txt 형식 (한 줄에 하나, 카테고리/파일명):
  reconstruction/2026-03-26-부산-삼익비치-분담금-6억8천-조합원이-알아야-할-것.md
  reconstruction/2026-05-27-압구정-5구역-재건축-분담금-시나리오와-생존-전략.md
"""
import argparse
import os
import re

POSTS_DIR = os.path.join(os.path.dirname(__file__), '..', 'content', 'posts')

def load_keep_list(path):
    with open(path, 'r') as f:
        return set(line.strip() for line in f if line.strip() and not line.startswith('#'))

def add_noindex(filepath, dry_run=False):
    with open(filepath, 'r') as f:
        content = f.read()

    if 'robotsNoIndex' in content:
        return False  # already has it

    # Insert robotsNoIndex: true after the first '---' line in front matter
    match = re.match(r'^(---\n)', content)
    if not match:
        return False

    new_content = '---\nrobotsNoIndex: true\n' + content[4:]  # skip first '---\n'

    if dry_run:
        return True

    with open(filepath, 'w') as f:
        f.write(new_content)
    return True

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--keep-list', required=True, help='보존할 포스트 목록 파일')
    parser.add_argument('--dry-run', action='store_true', help='실제 수정 없이 카운트만')
    args = parser.parse_args()

    keep = load_keep_list(args.keep_list)

    total = 0
    noindex_count = 0
    keep_count = 0
    already_count = 0

    for cat in os.listdir(POSTS_DIR):
        cat_dir = os.path.join(POSTS_DIR, cat)
        if not os.path.isdir(cat_dir):
            continue
        for fname in sorted(os.listdir(cat_dir)):
            if not fname.endswith('.md') or fname.startswith('_'):
                continue
            total += 1
            rel = f'{cat}/{fname}'
            if rel in keep:
                keep_count += 1
                continue

            filepath = os.path.join(cat_dir, fname)
            if add_noindex(filepath, dry_run=args.dry_run):
                noindex_count += 1
            else:
                already_count += 1

    action = '(dry-run)' if args.dry_run else '적용 완료'
    print(f'{action}: 전체 {total}개 | 보존 {keep_count}개 | noindex {noindex_count}개 | 이미 처리 {already_count}개')

if __name__ == '__main__':
    main()
