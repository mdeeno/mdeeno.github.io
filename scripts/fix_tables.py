#!/usr/bin/env python3
"""
Fix broken markdown tables in blog posts.

Patterns handled:
  A) Header row → broken separator (|, blank lines, |---|) → data rows
  B) Header row → | : lines with blank lines → data rows

Strategy: find header rows (lines with 2+ pipes), then look ahead for broken
separator patterns and replace with a proper |---|---|...| separator row.
"""

import re
import sys
from pathlib import Path

POSTS_DIR = Path(__file__).resolve().parent.parent / "content" / "posts"

# Match a proper table header: | col1 | col2 | ... |
HEADER_RE = re.compile(r'^\|.*\|.*\|')
# Match a proper separator: |---|---|
SEPARATOR_RE = re.compile(r'^\|[\s:-]+\|')
# Match a data row: | val1 | val2 | ... |
DATA_RE = re.compile(r'^\|.*\|.*\|')
# Match broken separator fragments
BROKEN_RE = re.compile(r'^\|\s*:?\s*$|^\|---\|?\s*$|^\s*$')


def count_cols(line: str) -> int:
    """Count number of columns in a table row."""
    return line.count('|') - 1  # subtract 1 for trailing pipe


def fix_file(path: Path) -> bool:
    lines = path.read_text(encoding='utf-8').splitlines(keepends=True)
    new_lines = []
    i = 0
    fixed = False

    while i < len(lines):
        line = lines[i].rstrip('\n')

        # Check if this looks like a table header
        if HEADER_RE.match(line):
            cols = count_cols(line)
            if cols < 2:
                new_lines.append(lines[i])
                i += 1
                continue

            # Look ahead: is the next non-empty content a proper separator?
            j = i + 1
            broken_lines = []
            while j < len(lines):
                next_line = lines[j].rstrip('\n')
                if SEPARATOR_RE.match(next_line) and next_line.count('|') >= cols:
                    # Already has proper separator, skip
                    break
                if DATA_RE.match(next_line) and next_line.count('|') >= cols:
                    # Hit a data row without separator → need to insert one
                    separator = '| ' + ' | '.join(['---'] * cols) + ' |\n'
                    new_lines.append(lines[i])  # header
                    new_lines.append(separator)  # fixed separator
                    # Skip the broken lines between header and data
                    i = j
                    fixed = True
                    break
                if BROKEN_RE.match(next_line):
                    broken_lines.append(j)
                    j += 1
                    continue
                # Some other content, not a table continuation
                break
            else:
                # Reached end of file
                new_lines.append(lines[i])
                i += 1
                continue

            if not fixed or new_lines[-1] != lines[i]:
                new_lines.append(lines[i])
                i += 1
            else:
                continue
        else:
            new_lines.append(lines[i])
            i += 1

    if fixed:
        path.write_text(''.join(new_lines), encoding='utf-8')
    return fixed


def main():
    md_files = list(POSTS_DIR.rglob("*.md"))
    fixed_count = 0
    for f in md_files:
        if fix_file(f):
            fixed_count += 1
            print(f"  FIXED: {f.relative_to(POSTS_DIR)}")
    print(f"\nTotal: {len(md_files)} files scanned, {fixed_count} fixed")


if __name__ == "__main__":
    main()
