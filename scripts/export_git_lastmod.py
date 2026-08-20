#!/usr/bin/env python3
"""Hugo가 Unicode 경로에서도 실제 Git 수정일을 사용하도록 data 파일을 만든다."""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path


COMMIT_PREFIX = "@@MDEENO_COMMIT_DATE="


def git_output(blog_dir: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(blog_dir), "-c", "core.quotepath=false", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def collect_lastmod(blog_dir: Path) -> dict[str, str]:
    tracked = {
        Path(line).as_posix()
        for line in git_output(blog_dir, "ls-files", "content").splitlines()
        if line and (blog_dir / line).is_file()
    }
    history = git_output(
        blog_dir,
        "log",
        "--no-renames",
        f"--format={COMMIT_PREFIX}%cI",
        "--name-only",
        "--",
        "content",
    )
    lastmod: dict[str, str] = {}
    commit_date = ""
    for raw_line in history.splitlines():
        line = raw_line.strip()
        if line.startswith(COMMIT_PREFIX):
            commit_date = line.removeprefix(COMMIT_PREFIX)
            continue
        if not commit_date or not line.startswith("content/") or line not in tracked:
            continue
        relative = line.removeprefix("content/")
        lastmod.setdefault(relative, commit_date)

    missing = sorted(path for path in tracked if path.removeprefix("content/") not in lastmod)
    if missing:
        preview = ", ".join(missing[:3])
        raise RuntimeError(
            f"Git 수정일을 찾지 못한 content 파일 {len(missing)}개: {preview}"
        )
    return dict(sorted(lastmod.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Hugo용 Git lastmod data 생성")
    parser.add_argument("--blog-dir", type=Path, default=Path.cwd())
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("data/git_lastmod.json"),
    )
    args = parser.parse_args()
    blog_dir = args.blog_dir.resolve()
    output = args.output if args.output.is_absolute() else blog_dir / args.output
    values = collect_lastmod(blog_dir)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(values, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"[git-lastmod] {len(values)}개 경로 → {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
