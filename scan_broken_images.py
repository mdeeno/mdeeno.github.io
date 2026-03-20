#!/usr/bin/env python3
"""
블로그 포스트의 깨진 이미지 전수 스캔 스크립트
- content/posts/ 아래 모든 .md 파일 순회
- 마크다운 이미지 ![alt](path) 및 HTML <img src="path"> 추출
- 로컬 파일 존재 여부 확인
- 외부 URL은 HTTP HEAD 요청으로 확인
"""

import os
import re
import glob
import urllib.request
import urllib.error
from pathlib import Path
from datetime import datetime

BLOG_ROOT = Path("/Users/suhun/Desktop/document/mdeeno.github.io")
POSTS_DIR = BLOG_ROOT / "content" / "posts"
STATIC_DIR = BLOG_ROOT / "static"
ASSETS_DIR = BLOG_ROOT / "assets"
REPORT_PATH = BLOG_ROOT / "broken_images_report.txt"

# 이미지 참조 추출 패턴
MD_IMAGE_RE = re.compile(r'!\[([^\]]*)\]\(([^)]+)\)')
HTML_IMG_RE = re.compile(r'<img\s+[^>]*src=["\']([^"\']+)["\']', re.IGNORECASE)


def extract_image_refs(filepath: Path) -> list[dict]:
    """md 파일에서 이미지 참조를 추출한다."""
    refs = []
    try:
        content = filepath.read_text(encoding="utf-8")
    except Exception as e:
        return [{"path": f"[READ ERROR: {e}]", "type": "error", "line": 0}]

    for i, line in enumerate(content.splitlines(), 1):
        for match in MD_IMAGE_RE.finditer(line):
            refs.append({"path": match.group(2).strip(), "type": "markdown", "line": i})
        for match in HTML_IMG_RE.finditer(line):
            refs.append({"path": match.group(1).strip(), "type": "html_img", "line": i})
    return refs


def resolve_image_path(img_path: str, post_file: Path) -> tuple[str, str]:
    """
    이미지 경로를 분류하고 절대 경로로 변환한다.
    Returns: (절대경로 또는 URL, 분류)
    """
    if img_path.startswith(("http://", "https://", "//")):
        return img_path, "external"

    if img_path.startswith("/"):
        # Hugo 루트 기준: static/ 또는 assets/
        candidate_static = STATIC_DIR / img_path.lstrip("/")
        candidate_assets = ASSETS_DIR / img_path.lstrip("/")
        if candidate_static.exists():
            return str(candidate_static), "local_static"
        if candidate_assets.exists():
            return str(candidate_assets), "local_assets"
        return str(candidate_static), "local_static"  # 기본은 static 기준
    else:
        # 상대경로: 포스트 파일 위치 기준
        resolved = (post_file.parent / img_path).resolve()
        return str(resolved), "local_relative"


def check_external_url(url: str, timeout: int = 10) -> tuple[bool, str]:
    """외부 URL의 존재 여부를 HEAD 요청으로 확인한다."""
    if url.startswith("//"):
        url = "https:" + url
    try:
        req = urllib.request.Request(url, method="HEAD")
        req.add_header("User-Agent", "Mozilla/5.0 (broken-image-scanner)")
        resp = urllib.request.urlopen(req, timeout=timeout)
        return resp.status < 400, f"HTTP {resp.status}"
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except Exception as e:
        return False, str(e)


def main():
    md_files = sorted(POSTS_DIR.rglob("*.md"))
    print(f"스캔 대상 파일: {len(md_files)}개")

    total_images = 0
    broken_local = []
    broken_external = []
    ok_local = 0
    ok_external = 0
    external_urls = []

    for md_file in md_files:
        refs = extract_image_refs(md_file)
        if not refs:
            continue

        rel_md = md_file.relative_to(BLOG_ROOT)

        for ref in refs:
            total_images += 1
            img_path = ref["path"]
            resolved, category = resolve_image_path(img_path, md_file)

            if category == "external":
                exists, detail = check_external_url(resolved)
                if exists:
                    ok_external += 1
                else:
                    broken_external.append({
                        "file": str(rel_md),
                        "line": ref["line"],
                        "url": img_path,
                        "reason": detail,
                    })
                external_urls.append({
                    "file": str(rel_md),
                    "line": ref["line"],
                    "url": img_path,
                    "exists": exists,
                    "detail": detail,
                })
            else:
                if Path(resolved).exists():
                    ok_local += 1
                else:
                    broken_local.append({
                        "file": str(rel_md),
                        "line": ref["line"],
                        "img_path": img_path,
                        "resolved": resolved,
                    })

    # 리포트 작성
    lines = []
    lines.append("=" * 80)
    lines.append("깨진 이미지 전수 스캔 리포트")
    lines.append(f"스캔 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    lines.append(f"스캔 대상: {len(md_files)}개 .md 파일")
    lines.append("=" * 80)
    lines.append("")

    lines.append("## 요약")
    lines.append(f"  총 이미지 참조: {total_images}개")
    lines.append(f"  로컬 이미지 정상: {ok_local}개")
    lines.append(f"  로컬 이미지 깨짐: {len(broken_local)}개")
    lines.append(f"  외부 URL 정상: {ok_external}개")
    lines.append(f"  외부 URL 깨짐: {len(broken_external)}개")
    lines.append("")

    if broken_local:
        lines.append("-" * 80)
        lines.append(f"## 깨진 로컬 이미지 ({len(broken_local)}건)")
        lines.append("-" * 80)
        for item in broken_local:
            lines.append(f"  파일: {item['file']}:{item['line']}")
            lines.append(f"  참조: {item['img_path']}")
            lines.append(f"  경로: {item['resolved']}")
            lines.append("")

    if broken_external:
        lines.append("-" * 80)
        lines.append(f"## 깨진 외부 URL ({len(broken_external)}건)")
        lines.append("-" * 80)
        for item in broken_external:
            lines.append(f"  파일: {item['file']}:{item['line']}")
            lines.append(f"  URL:  {item['url']}")
            lines.append(f"  사유: {item['reason']}")
            lines.append("")

    if external_urls:
        lines.append("-" * 80)
        lines.append(f"## 전체 외부 URL 목록 ({len(external_urls)}건)")
        lines.append("-" * 80)
        for item in external_urls:
            status = "OK" if item["exists"] else "BROKEN"
            lines.append(f"  [{status}] {item['file']}:{item['line']}")
            lines.append(f"         {item['url']}")
            if not item["exists"]:
                lines.append(f"         사유: {item['detail']}")
            lines.append("")

    report = "\n".join(lines)
    REPORT_PATH.write_text(report, encoding="utf-8")
    print(report)
    print(f"\n리포트 저장됨: {REPORT_PATH}")


if __name__ == "__main__":
    main()
