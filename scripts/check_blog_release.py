#!/usr/bin/env python3
"""블로그 공개 직전 품질과 7일 발행 간격을 함께 검증한다.

Pages 배포와 posting-engine의 발행 직전 단계가 이 파일을 같이 호출한다.
외부 패키지 없이 실행되어 public Pages 저장소에서도 비밀값 없이 동작한다.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import subprocess
import sys
from pathlib import Path


MIN_INDEXABLE_POSTS = 20
MIN_BODY_CHARS = 2_000
PUBLICATION_COOLDOWN_DAYS = 7
# 2026-09-07 사용자의 첫 위클리 즉시 공개 지시: 이 날짜의 첫 1건만 허용한다.
WEEKLY_LAUNCH_DATE = dt.date(2026, 9, 7)
WEEKLY_LAUNCH_BRIEF_ID = "weekly-2026-w37"
KST = dt.timezone(dt.timedelta(hours=9))
ZERO_SHA = "0" * 40
REQUIRED_FRONTMATTER = ("title", "date", "description", "tags")
DISCLAIMER_MARKERS = (
    "시뮬레이션",
    "참고용",
    "투자 자문이 아",
    "법률 자문이 아",
    "감정평가",
    "관리처분계획",
    "M-DEENO 계산",
    "면책",
)
ESTIMATE_MARKERS = ("추정", "가정", "시나리오", "범위")
VERIFY_MARKERS = ("실제", "확인", "관리처분", "감정평가", "조합", "공식")
PUBLIC_REVIEW_DISCLOSURE_PATTERNS = (
    r"자동\s*편집\s*검토",
    r"편집\s*검수\s*완료",
    r"AI의\s*도움을\s*받아\s*작성",
)
SOURCE_BACKED_FORBIDDEN_PATTERNS = (
    r"분담금\s*폭탄",
    r"세금\s*폭탄",
    r"밤잠",
    r"소름",
    r"충격",
    r"무조건",
    r"정확한\s*(?:분담금|금액)",
    r"분담금은\s*\d[\d,.]*\s*(?:억|만\s*원|원)",
    r"가장\s*확실한",
    r"정확히\s*진단",
    r"완벽한\s*분양\s*성공",
)
GENERAL_FORBIDDEN_PHRASES = (
    "분담금 계산기",
    "정확한 " + "분담금",
    "무료로 분석해",
    "무료 분석",
)
ALLOWED_SOURCE_HOST_PATTERN = r"(?:www\.)?(?:law\.go\.kr|molit\.go\.kr|reb\.or\.kr|seoul\.go\.kr)"
STATUTORY_BURDEN_TERM_RE = re.compile(
    r"(?:재건축|개발|학교용지|광역교통시설|기반시설)부담금"
)
LEGAL_BURDEN_QUOTE_RE = re.compile(
    r"법령상\s*[\"'“‘]개략적(?:인)?\s+부담금(?:\s+내역)?[\"'”’]"
)
# 과거 글은 법정 부담금을 문맥상 줄여 쓰기도 하므로 명백한 혼용만 차단한다.
# 새 공식 원천 글에는 아래의 엄격한 has_ambiguous_burden_term 검사를 유지한다.
MISLABELED_COST_RE = re.compile(
    r"(?:추가|실질|실|특별|초기|조합원(?:당|의)?)\s*부담금|부담금\s*폭탄"
)


def extract_frontmatter(text: str) -> str | None:
    match = re.match(r"^---\r?\n(.*?)\r?\n---[^\n]*\n", text, flags=re.DOTALL)
    return match.group(1) if match else None


def frontmatter_scalar(frontmatter: str, key: str) -> str:
    match = re.search(
        rf"^{re.escape(key)}:\s*(.*?)\s*$",
        frontmatter,
        flags=re.MULTILINE,
    )
    if not match:
        return ""
    return match.group(1).strip().strip('"\'')


def frontmatter_date(value: object) -> dt.date | None:
    match = re.match(r"(\d{4}-\d{2}-\d{2})", str(value or ""))
    return dt.date.fromisoformat(match.group(1)) if match else None


def is_public_post(text: str) -> bool:
    frontmatter = extract_frontmatter(text)
    if frontmatter is None:
        return False
    return (
        frontmatter_scalar(frontmatter, "draft").lower() != "true"
        and frontmatter_scalar(frontmatter, "robotsNoIndex").lower() != "true"
    )


def visible_body_char_count(body: str) -> int:
    text = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", body)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
    text = re.sub(r"^[#>\-*\s]+", "", text, flags=re.MULTILINE)
    return len(text.strip())


def has_disclaimer(body: str) -> bool:
    if any(marker in body for marker in DISCLAIMER_MARKERS):
        return True
    return any(marker in body for marker in ESTIMATE_MARKERS) and any(
        marker in body for marker in VERIFY_MARKERS
    )


def has_ambiguous_burden_term(text: str) -> bool:
    remaining = STATUTORY_BURDEN_TERM_RE.sub("", text)
    remaining = LEGAL_BURDEN_QUOTE_RE.sub("", remaining)
    return "부담금" in remaining


def check_public_terminology(blog_dir: Path) -> list[str]:
    """noindex도 독자가 열 수 있다. 과거 글·단지 소개까지 배포마다 검사한다."""
    failures: list[str] = []
    checked = 0
    for path in sorted(blog_dir.joinpath("content").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(text)
        if frontmatter is None or re.search(r"^\s*draft:\s*true\s*$", frontmatter, re.MULTILINE):
            continue
        checked += 1
        # 링크 주소·HTML 속성·주석은 보존하고 독자가 보는 문구만 검사한다.
        visible = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)
        visible = re.sub(r"\]\([^)]+\)", "]", visible)
        visible = re.sub(r"<[^>]+>", "", visible)
        visible = re.sub(r"[*_`]", "", visible)
        visible = STATUTORY_BURDEN_TERM_RE.sub("", visible)
        visible = LEGAL_BURDEN_QUOTE_RE.sub("", visible)
        matches = sorted(set(MISLABELED_COST_RE.findall(visible)))
        if matches:
            failures.append(f"{path.relative_to(blog_dir)}: 용어 혼용 — {', '.join(matches)}")
    print(f"[blog-release] 전체 공개 문서 용어 검사 {checked}개, 실패 {len(failures)}개")
    return failures


def check_post(path: Path) -> tuple[list[str], list[str]]:
    text = path.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(text)
    if frontmatter is None:
        return ["frontmatter 파싱 실패"], []
    body = text[text.find("\n---", 3) + 4 :]
    errors: list[str] = []
    warnings: list[str] = []

    for key in REQUIRED_FRONTMATTER:
        if not frontmatter_scalar(frontmatter, key):
            errors.append(f"frontmatter 필수 필드 누락: {key}")
    chars = visible_body_char_count(body)
    if chars < MIN_BODY_CHARS:
        errors.append(f"본문 {chars}자 < {MIN_BODY_CHARS}자")
    if len(re.findall(r"^##\s+", body, flags=re.MULTILINE)) < 3:
        errors.append("H2 섹션 3개 미만")
    if not re.search(r"<div class=['\"](?:blog-cta-box|lab-card)", body):
        errors.append("CTA 0개")
    if not has_disclaimer(body):
        errors.append("면책·실제 자료 확인 문구 없음")
    description = frontmatter_scalar(frontmatter, "description")
    if description and not 60 <= len(description) <= 200:
        warnings.append(f"description 길이 {len(description)}자")
    lowered = text.lower()
    for phrase in GENERAL_FORBIDDEN_PHRASES:
        if phrase in lowered:
            errors.append(f"금지 표현: {phrase}")

    if frontmatter_scalar(frontmatter, "sourceBacked").lower() != "true":
        return errors, warnings

    status = frontmatter_scalar(frontmatter, "reviewStatus")
    if status == "approved":
        if frontmatter_scalar(frontmatter, "draft").lower() == "true":
            errors.append("승인 글은 draft: true일 수 없음")
        if frontmatter_scalar(frontmatter, "robotsNoIndex").lower() == "true":
            errors.append("승인 글은 robotsNoIndex: true일 수 없음")
        for pattern in PUBLIC_REVIEW_DISCLOSURE_PATTERNS:
            if re.search(pattern, body, flags=re.IGNORECASE):
                errors.append(f"공개 본문에 내부 검토 과정 노출: {pattern}")
    for key in ("contentBriefId", "primaryKeyword", "searchIntent", "funnelGoal"):
        if not frontmatter_scalar(frontmatter, key):
            errors.append(f"공식 원천 글 frontmatter 누락: {key}")
    for label, prefix in (
        ("필라 글", "/posts/"),
        ("계산기", "/calculators/"),
        ("단지 페이지", "/complex/"),
    ):
        if prefix not in body:
            errors.append(f"공식 원천 글 {label} 내부 링크 누락: {prefix}")
    source_count = len(
        re.findall(rf"^\s+-\s+https://{ALLOWED_SOURCE_HOST_PATTERN}/\S+\s*$", text, re.MULTILINE)
    )
    if source_count < 2:
        errors.append(f"허용 공식 원천 {source_count}개 < 2개")
    brief_id = frontmatter_scalar(frontmatter, "contentBriefId")
    expected_utm = (
        "utm_source=blog&utm_medium=blog_cta&utm_campaign=source_backed"
        f"&utm_content={brief_id}"
    )
    if brief_id and expected_utm not in body:
        errors.append("공식 원천 글 CTA에 주제 식별 UTM 누락")
    first_h2 = re.search(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    if first_h2 is None or first_h2.group(1).strip() != "핵심 답변":
        errors.append("공식 원천 글 첫 H2는 '핵심 답변'이어야 함")
    for pattern in SOURCE_BACKED_FORBIDDEN_PATTERNS:
        if re.search(pattern, f"{frontmatter_scalar(frontmatter, 'title')}\n{body}", re.IGNORECASE):
            errors.append(f"공식 원천 글 금지 표현: {pattern}")
    terminology_text = "\n".join(
        frontmatter_scalar(frontmatter, key)
        for key in ("title", "description", "tags", "primaryKeyword")
    ) + f"\n{body}"
    if has_ambiguous_burden_term(terminology_text):
        errors.append("용어 혼동: 일반 조합원 비용은 '분담금', 법정 부과금만 '부담금'")
    return errors, warnings


def git_output(blog_dir: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(blog_dir), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def resolve_base_ref(blog_dir: Path, base_ref: str | None) -> str | None:
    value = (base_ref or "").strip()
    if not value:
        return None
    if value == ZERO_SHA:
        raise RuntimeError("초기 push의 비교 기준 SHA가 없어 공개 발행 여부를 검증할 수 없습니다")
    result = subprocess.run(
        ["git", "-C", str(blog_dir), "cat-file", "-e", f"{value}^{{commit}}"],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(f"비교 기준 커밋을 찾을 수 없습니다: {value}")
    return value


def text_at_ref(blog_dir: Path, ref: str, relative_path: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(blog_dir), "show", f"{ref}:{relative_path.as_posix()}"],
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else None


def changed_post_paths(blog_dir: Path, base_ref: str) -> list[Path]:
    output = git_output(
        blog_dir,
        "diff",
        "--name-only",
        "-z",
        "--diff-filter=ACMR",
        base_ref,
        "HEAD",
        "--",
        "content/posts",
    )
    return [Path(name) for name in output.split("\0") if name.endswith(".md")]


def newly_public_posts(blog_dir: Path, base_ref: str) -> list[Path]:
    published: list[Path] = []
    for relative_path in changed_post_paths(blog_dir, base_ref):
        current_path = blog_dir / relative_path
        if not current_path.is_file():
            continue
        current_text = current_path.read_text(encoding="utf-8")
        if not is_public_post(current_text):
            continue
        previous_text = text_at_ref(blog_dir, base_ref, relative_path)
        if previous_text is None or not is_public_post(previous_text):
            published.append(current_path)
    return published


def latest_source_backed_publication(
    blog_dir: Path,
    *,
    exclude_path: Path | None = None,
) -> tuple[dt.date, Path] | None:
    latest: tuple[dt.date, Path] | None = None
    excluded = exclude_path.resolve() if exclude_path else None
    for path in blog_dir.joinpath("content", "posts").rglob("*.md"):
        if path.name == "_index.md" or (excluded is not None and path.resolve() == excluded):
            continue
        text = path.read_text(encoding="utf-8")
        frontmatter = extract_frontmatter(text)
        if frontmatter is None:
            continue
        if frontmatter_scalar(frontmatter, "sourceBacked").lower() != "true":
            continue
        if frontmatter_scalar(frontmatter, "reviewStatus") != "approved" or not is_public_post(text):
            continue
        published = frontmatter_date(frontmatter_scalar(frontmatter, "date"))
        if published is not None and (latest is None or published > latest[0]):
            latest = (published, path)
    return latest


def publication_cooldown_error(
    blog_dir: Path,
    candidate_date: dt.date,
    *,
    exclude_path: Path,
) -> str | None:
    latest = latest_source_backed_publication(blog_dir, exclude_path=exclude_path)
    if latest is None:
        return None
    latest_date, latest_path = latest
    if (candidate_date - latest_date).days < PUBLICATION_COOLDOWN_DAYS:
        next_date = latest_date + dt.timedelta(days=PUBLICATION_COOLDOWN_DAYS)
        return (
            f"최근 공식 원천 글 {latest_path.name}이 {latest_date.isoformat()}에 공개되어 "
            f"{next_date.isoformat()} 전에는 새 글을 공개할 수 없습니다"
        )
    return None


def check_indexable_baseline(blog_dir: Path) -> list[str]:
    posts = [
        path
        for path in sorted(blog_dir.joinpath("content", "posts").rglob("*.md"))
        if path.name != "_index.md" and is_public_post(path.read_text(encoding="utf-8"))
    ]
    failures: list[str] = []
    if len(posts) < MIN_INDEXABLE_POSTS:
        failures.append(f"검색 노출 글 {len(posts)}개 < 최소 {MIN_INDEXABLE_POSTS}개")
    warning_count = 0
    for path in posts:
        errors, warnings = check_post(path)
        warning_count += len(warnings)
        relative = path.relative_to(blog_dir)
        failures.extend(f"{relative}: {error}" for error in errors)
        failures.extend(f"{relative}: 경고를 공개 전에 해소하세요 — {warning}" for warning in warnings)
    print(
        f"[blog-release] indexable {len(posts)}개, "
        f"실패 {len(failures)}개, 경고 {warning_count}개"
    )
    return failures


def check_subscribe_form_metrics(blog_dir: Path) -> list[str]:
    path = blog_dir / "layouts" / "partials" / "subscribe-form.html"
    text = path.read_text(encoding="utf-8")
    failures: list[str] = []
    if "blog_subscribe_request_accepted" not in text:
        failures.append("구독 폼 요청 접수 이벤트 누락")
    if "blog_subscribe_confirmation_sent" in text:
        failures.append("구독 폼이 generic 202를 실제 확인메일 발송으로 오집계")
    if "구독 가능한 주소라면 확인 이메일을 보내드립니다" not in text:
        failures.append("구독 폼의 generic 202 조건부 발송 문구 누락")
    return failures


def check_new_publication(blog_dir: Path, candidates: list[Path]) -> list[str]:
    if not candidates:
        print("[blog-release] 새 공개 글 0개 — cadence 변경 없음")
        return []
    if len(candidates) > 1:
        names = ", ".join(path.name for path in candidates)
        return [f"한 번에 공개된 글 {len(candidates)}개 > 1개: {names}"]
    candidate = candidates[0]
    text = candidate.read_text(encoding="utf-8")
    frontmatter = extract_frontmatter(text)
    if frontmatter is None:
        return [f"{candidate.name}: frontmatter 파싱 실패"]
    failures: list[str] = []
    if frontmatter_scalar(frontmatter, "sourceBacked").lower() != "true":
        failures.append(f"{candidate.name}: 새 공개 글은 sourceBacked: true여야 합니다")
    if frontmatter_scalar(frontmatter, "reviewStatus") != "approved":
        failures.append(f"{candidate.name}: 새 공개 글은 reviewStatus: approved여야 합니다")
    candidate_date = frontmatter_date(frontmatter_scalar(frontmatter, "date"))
    if candidate_date is None:
        failures.append(f"{candidate.name}: 유효한 공개 date가 없습니다")
    else:
        authorized_launch = (
            candidate_date == WEEKLY_LAUNCH_DATE
            and dt.datetime.now(KST).date() == WEEKLY_LAUNCH_DATE
            and frontmatter_scalar(frontmatter, "contentBriefId") == WEEKLY_LAUNCH_BRIEF_ID
            and frontmatter_scalar(frontmatter, "weeklyBriefing").lower() == "true"
        )
        if authorized_launch:
            for path in blog_dir.joinpath("content", "posts").rglob("*.md"):
                if path.resolve() == candidate.resolve():
                    continue
                previous_text = path.read_text(encoding="utf-8")
                previous = extract_frontmatter(previous_text)
                if previous is not None and is_public_post(previous_text) and (
                    frontmatter_scalar(previous, "weeklyBriefing").lower() == "true"
                    or frontmatter_scalar(previous, "contentBriefId").startswith("weekly-")
                ):
                    authorized_launch = False
                    break
        cadence_error = publication_cooldown_error(
            blog_dir,
            candidate_date,
            exclude_path=candidate,
        )
        if cadence_error and not authorized_launch:
            failures.append(cadence_error)
        elif cadence_error and not failures:
            print("[blog-release] 사용자 지시로 2026-09-07 첫 위클리 1건 공개 허용")
    if not failures:
        print(f"[blog-release] 새 공개 글 1개 발행 정책 통과: {candidate.name}")
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description="Pages 공개 콘텐츠 출고 게이트")
    parser.add_argument("--blog-dir", type=Path, default=Path.cwd())
    parser.add_argument("--base-ref")
    args = parser.parse_args()
    blog_dir = args.blog_dir.resolve()
    if not blog_dir.joinpath("content", "posts").is_dir():
        print(f"[blog-release] Hugo 블로그 경로가 아닙니다: {blog_dir}", file=sys.stderr)
        return 2
    try:
        base_ref = resolve_base_ref(blog_dir, args.base_ref)
        failures = check_indexable_baseline(blog_dir)
        failures.extend(check_public_terminology(blog_dir))
        failures.extend(check_subscribe_form_metrics(blog_dir))
        if base_ref is not None:
            failures.extend(check_new_publication(blog_dir, newly_public_posts(blog_dir, base_ref)))
        else:
            print("[blog-release] 수동 재배포 — 현재 indexable 품질만 검사")
    except (OSError, RuntimeError, subprocess.SubprocessError) as error:
        print(f"[blog-release] 게이트 실행 실패: {error}", file=sys.stderr)
        return 2
    if failures:
        for failure in failures:
            print(f"[FAIL] {failure}", file=sys.stderr)
        return 1
    print("[blog-release] PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
