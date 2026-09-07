#!/usr/bin/env python3
"""Hugo 출력만 새 블로그의 즉시 이동 문서로 바꾼다. 원본 content는 수정하지 않는다.

기본은 dry-run. --apply 전에 새 플랫폼의 모든 목적 URL을 검증한다.
https://developers.google.com/search/docs/crawling-indexing/301-redirects
"""
import argparse
import html
import json
import re
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import quote, unquote, urlsplit

OLD_HOSTS = {"tech.mdeeno.com", "mdeeno.github.io"}
NEW_ORIGIN = "https://mdeeno.com"
BLOG_PATH = "/blog"
# src/lib/funnel-events.js sanitizeAttributionValue와 같은 공개 유입 값 계약.
PRESERVE_ATTRIBUTION_SCRIPT = r"""<script>
(function () {
  if (!location.search && !location.hash) return;
  var target = new URL(document.querySelector('link[rel="canonical"]').href);
  if (target.origin !== 'https://mdeeno.com' || !/^\/blog(?:\/|$)/.test(target.pathname)) return;
  var params = new URLSearchParams(location.search);
  ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content'].forEach(function (key) {
    var value = (params.get(key) || '').trim().toLowerCase();
    if (/^[a-z0-9][a-z0-9._-]{0,79}$/.test(value)
        && !/^(?:\+?82|0)?1\d[-_.]?\d{3,4}[-_.]?\d{4}$/.test(value)
        && !/^\d{6}[-_.]?[1-4]\d{6}$/.test(value)) target.searchParams.set(key, value);
  });
  target.hash = location.hash;
  location.replace(target.href);
})();
</script>"""


class Canonical(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.url = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        values = dict(attrs)
        if tag == "link" and values.get("rel") == "canonical":
            self.url = values.get("href")


def new_path(url):
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.username or parts.password or parts.port:
        raise ValueError(f"허용하지 않은 canonical URL: {url}")
    if parts.hostname in OLD_HOSTS:
        path = unquote(parts.path)
    elif parts.hostname == "mdeeno.com" and (parts.path == BLOG_PATH or parts.path.startswith(BLOG_PATH + "/")):
        path = unquote(parts.path[len(BLOG_PATH):])
    else:
        raise ValueError(f"허용하지 않은 canonical 호스트/경로: {url}")
    if parts.query or parts.fragment or "\\" in path or any(ord(char) < 32 for char in path) or any(part in {".", ".."} for part in path.split("/")):
        raise ValueError(f"순수 경로가 아닌 canonical: {url}")
    return BLOG_PATH + path.rstrip("/")


def destination(url):
    path = new_path(url)
    return NEW_ORIGIN + quote(path, safe="/-._~")


def bridge_html(target):
    safe = html.escape(target, quote=True)
    return (
        '<!doctype html><html lang="ko"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width, initial-scale=1">'
        '<meta name="referrer" content="no-referrer">'
        f'<link rel="canonical" href="{safe}">'
        + PRESERVE_ATTRIBUTION_SCRIPT +
        f'<meta http-equiv="refresh" content="0; url={safe}">'
        '<title>M-DEENO 블로그로 이동합니다</title>'
        '</head><body><p>블로그 주소가 변경되었습니다. '
        f'<a href="{safe}">같은 글을 새 블로그에서 읽기</a></p></body></html>\n'
    )


def plan_bridge(public_dir):
    plans = []
    for path in sorted(public_dir.rglob("*.html")):
        relative = path.relative_to(public_dir).as_posix()
        if relative == "404.html":
            # GitHub Pages는 존재하지 않는 모든 URL에 이 문서를 사용한다. 홈으로 자동 이동하지 않는다.
            text = ('<!doctype html><html lang="ko"><head><meta charset="utf-8">'
                    '<meta name="robots" content="noindex"><title>페이지를 찾을 수 없습니다</title>'
                    '</head><body><h1>페이지를 찾을 수 없습니다</h1>'
                    '<p><a href="https://mdeeno.com/blog">새 블로그에서 글 찾기</a></p></body></html>\n')
            plans.append((path, text, None))
            continue
        canonical = Canonical(path.read_text(encoding="utf-8")).url
        if relative == "offline.html":
            canonical = "https://tech.mdeeno.com/"
        if not canonical:
            raise ValueError(f"canonical이 없는 HTML: {relative}")
        target = destination(canonical)
        plans.append((path, bridge_html(target), target))
    if not plans:
        raise ValueError("Hugo HTML 출력이 0개입니다")
    return plans


def rewrite_feed_links(text):
    # RSS 본문과 XML 구조를 보존하며 기존 블로그 절대 링크만 바꾼다.
    pattern = r'https://(?:tech\.mdeeno\.com|mdeeno\.github\.io)(?:/[^\s<>"\']*)?'

    def replace(match):
        url = match.group(0)
        parts = urlsplit(html.unescape(url))
        if parts.path.endswith((".png", ".webp", ".jpg", ".svg", ".ico")):
            # 과거 피드 이미지는 남아 있는 원본 정적 자산을 계속 사용한다.
            return url
        if parts.path.endswith("index.xml"):
            return NEW_ORIGIN + BLOG_PATH + "/index.xml"
        clean = parts._replace(query="", fragment="").geturl()
        return destination(clean)

    return re.sub(pattern, replace, text)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-dir", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    public_dir = args.public_dir.resolve()
    if not (public_dir / "index.html").is_file() or (public_dir / "content").exists():
        raise ValueError("원본 저장소가 아닌 Hugo 빌드 출력 경로를 지정하세요")
    plans = plan_bridge(public_dir)
    xml_plans = [(path, rewrite_feed_links(path.read_text(encoding="utf-8")))
                 for path in sorted(public_dir.rglob("*.xml"))]
    if args.apply:
        for path, text, _ in plans:
            path.write_text(text, encoding="utf-8")
        for path, text in xml_plans:
            path.write_text(text, encoding="utf-8")
    report = {"applied": args.apply, "html": len(plans), "redirects": sum(target is not None for _, _, target in plans),
              "xml": len(xml_plans), "targets": [{"file": str(path.relative_to(public_dir)), "url": target} for path, _, target in plans]}
    if args.report:
        args.report.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in report.items() if key != "targets"}, ensure_ascii=False))


if __name__ == "__main__":
    main()
