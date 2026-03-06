#!/usr/bin/env python3
"""
scripts/upgrade_posts_to_saas_funnel.py

기존 Hugo 블로그 포스트 (~491개)를 M-DEENO SaaS 펀넬 구조로 일괄 업그레이드.

추가 요소:
  1. SaaS CTA 블록   (첫 번째 ## 헤딩 직후)
  2. 베타 대기자 폼  (본문 끝, 기존 CPA 숏코드 또는 Supabase 스크립트 앞)
  3. CPA 숏코드      (이미 있으면 스킵)

안전 장치:
  - backup_posts/ 에 원본 전체 백업
  - 각 요소별 마커로 중복 삽입 방지
  - frontmatter 절대 미수정

사용법:
  cd /Volumes/ssd/tech.mdeeno/mdeeno.github.io
  python3 scripts/upgrade_posts_to_saas_funnel.py
"""

import os
import re
import shutil
import datetime
from pathlib import Path
from git import Repo

# ==============================================================================
# [경로 설정]
# ==============================================================================
SCRIPT_DIR = Path(__file__).parent
BLOG_DIR   = SCRIPT_DIR.parent
POSTS_DIR  = BLOG_DIR / "content" / "posts"
BACKUP_DIR = BLOG_DIR / "backup_posts"

# ==============================================================================
# [중복 방지 마커] — 이 문자열이 본문에 있으면 해당 요소 삽입 건너뜀
# ==============================================================================
MARKER_CTA      = "mvp-cta"
MARKER_WAITLIST = "beta-waitlist"
MARKER_CPA      = "mdeeno_cpa"

# ==============================================================================
# [삽입 블록]
# ==============================================================================
SAAS_CTA_BLOCK = """
<div class="mvp-cta">
  <div class="mvp-cta__inner">
    <p class="mvp-cta__title">📊 내 아파트 재건축 리스크 무료 분석</p>
    <p class="mvp-cta__desc">
      공사비 상승과 일반분양가 변화에 따라<br>
      추가 분담금이 수천만원~수억원 차이 날 수 있습니다.
    </p>
    <a class="mvp-cta-button"
       href="https://mdeeno.com/member"
       target="_blank"
       rel="noopener noreferrer">
       무료 리스크 분석 시작 →
    </a>
  </div>
</div>

"""

BETA_WAITLIST_BLOCK = """
<div class="beta-waitlist">
  <p><strong>📩 재건축 리스크 분석 리포트 베타 신청</strong></p>
  <p>
  M-DEENO 프리미엄 리포트가
  2026년 6월 정식 출시 예정입니다.
  </p>
  <input type="email" id="beta-email" placeholder="이메일 입력">
  <button onclick="submitBetaWaitlist()">베타 신청</button>
</div>

<script>
async function submitBetaWaitlist(){
  const email=document.getElementById("beta-email").value;
  if(!email){
    alert("이메일을 입력해주세요.");
    return;
  }
  await fetch("https://mdeeno.com/api/waitlist",{
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify({email})
  });
  alert("베타 신청이 완료되었습니다.");
}
</script>

"""

CPA_SHORTCODE = '\n{{< mdeeno_cpa type="loan" >}}\n'

# ==============================================================================
# [본문 끝 감지 패턴]
# 기존 포스트는 Supabase 스크립트 또는 CPA 숏코드로 끝남
# 새 요소는 이 지점 직전에 삽입
# ==============================================================================
END_OF_BODY_PATTERNS = [
    # 기존 Supabase CDN 로드 스크립트 (구 파이프라인 잔재)
    r'<script\s+src="https://cdn\.jsdelivr\.net/npm/@supabase',
    # CPA 숏코드
    r'\{\{<\s*mdeeno_cpa\b',
    # 면책조항 변형들
    r'📢\s*\*\*면책\s*조항',
    r'<small>.*?면책',
    r'※.{0,30}본 분석은.{0,30}참고용',
    r'※.{0,30}시뮬레이션.{0,30}수치',
    r'※.{0,30}M-DEENO.{0,30}예측',
    r'※.{0,30}가상 시나리오',
]


def _find_end_of_body(text):
    """
    Supabase 스크립트 / CPA 숏코드 / 면책조항 중 가장 먼저 나타나는 위치 반환.
    없으면 -1.
    """
    earliest = -1
    for pattern in END_OF_BODY_PATTERNS:
        m = re.search(pattern, text, re.DOTALL | re.MULTILINE)
        if m:
            pos = m.start()
            if earliest == -1 or pos < earliest:
                earliest = pos
    return earliest


# ==============================================================================
# [Frontmatter 분리]
# ==============================================================================
def _split_frontmatter(text):
    """
    Hugo frontmatter(`---...---`)와 본문을 분리.
    Returns: (frontmatter: str, body: str)
    """
    if not text.startswith("---"):
        return "", text
    close = text.find("\n---", 3)
    if close == -1:
        return "", text
    end = close + 4          # '\n---' 포함
    if end < len(text) and text[end] == "\n":
        end += 1             # 닫는 --- 다음 줄바꿈 포함
    return text[:end], text[end:]


# ==============================================================================
# [단일 파일 업그레이드]
# ==============================================================================
def upgrade_post(content):
    """
    포스트 1개를 SaaS 펀넬 구조로 업그레이드.

    Returns:
        new_content (str)
        changes     (list[str]) — 삽입된 요소 이름 목록
    """
    frontmatter, body = _split_frontmatter(content)
    changes = []

    # ── Step 2: SaaS CTA (첫 번째 ## 헤딩 직후) ─────────────────────────────
    if MARKER_CTA not in body:
        m = re.search(r'^##\s+.+$', body, re.MULTILINE)
        if m:
            pos = m.end()
            body = body[:pos] + SAAS_CTA_BLOCK + body[pos:]
        else:
            # ## 헤딩 없는 경우 → 본문 첫 빈 줄 이후
            first_blank = re.search(r'\n\n', body)
            if first_blank:
                pos = first_blank.end()
                body = body[:pos] + SAAS_CTA_BLOCK + body[pos:]
            else:
                body = SAAS_CTA_BLOCK + body
        changes.append("CTA")

    # ── Step 4: CPA 숏코드 (본문 끝, 중복 불가) ─────────────────────────────
    if MARKER_CPA not in body:
        eob = _find_end_of_body(body)
        if eob != -1:
            body = body[:eob] + CPA_SHORTCODE + "\n" + body[eob:]
        else:
            body = body.rstrip() + CPA_SHORTCODE
        changes.append("CPA")

    # ── Step 3: 베타 대기자 폼 (CPA 또는 Supabase 스크립트 앞) ──────────────
    if MARKER_WAITLIST not in body:
        eob = _find_end_of_body(body)
        if eob != -1:
            body = body[:eob] + BETA_WAITLIST_BLOCK + body[eob:]
        else:
            body = body.rstrip() + "\n" + BETA_WAITLIST_BLOCK
        changes.append("Waitlist")

    return frontmatter + body, changes


# ==============================================================================
# [백업]
# ==============================================================================
def _backup(src_path):
    """원본 파일을 backup_posts/ 아래 동일 경로로 백업."""
    try:
        rel  = src_path.relative_to(POSTS_DIR)
        dest = BACKUP_DIR / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_path, dest)
    except Exception as e:
        print(f"      ⚠️  백업 실패 ({src_path.name}): {e}")


# ==============================================================================
# [메인]
# ==============================================================================
def run():
    start = datetime.datetime.now()

    print("\n" + "=" * 60)
    print("🚀 M-DEENO SaaS Funnel 마이그레이션")
    print(f"   대상: {POSTS_DIR}")
    print(f"   백업: {BACKUP_DIR}")
    print("=" * 60)

    # Step 8: 백업 디렉토리 준비
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # 파일 수집 (macOS 메타데이터 ._* 파일 제외)
    md_files = sorted(
        p for p in POSTS_DIR.rglob("*.md")
        if not p.name.startswith("._")
    )
    total = len(md_files)
    print(f"\n📂 처리 대상: {total}개 파일\n")

    modified = 0
    skipped  = 0
    errors   = 0

    for i, filepath in enumerate(md_files, 1):
        try:
            content = filepath.read_text(encoding="utf-8")

            # Step 5: 이미 세 요소 모두 있으면 완전 스킵
            if (MARKER_CTA in content and
                    MARKER_WAITLIST in content and
                    MARKER_CPA in content):
                skipped += 1
                continue

            # Step 8: 백업
            _backup(filepath)

            # 업그레이드
            new_content, changes = upgrade_post(content)

            if changes:
                filepath.write_text(new_content, encoding="utf-8")
                modified += 1
                tag = ", ".join(changes)
                print(f"  [{i:04d}/{total}] ✅  {filepath.name[:60]:<60}  [{tag}]")
            else:
                skipped += 1

        except Exception as e:
            errors += 1
            print(f"  [{i:04d}/{total}] ❌  {filepath.name} — {e}")

    elapsed = int((datetime.datetime.now() - start).total_seconds())
    print(f"\n{'─' * 60}")
    print(f"완료: 수정 {modified}개 | 스킵 {skipped}개 | 오류 {errors}개 | 소요 {elapsed}초")

    if modified == 0:
        print("변경 없음. Git 커밋 건너뜁니다.")
        return

    # Step 7: Git 커밋 & 푸시
    print(f"\n🚀 GitHub 배포 중...")
    try:
        repo = Repo(BLOG_DIR)
        repo.git.add("content/posts/")
        repo.index.commit("Upgrade posts to SaaS funnel structure")
        repo.remote(name="origin").push()
        print("✅ Push 완료!")
    except Exception as e:
        print(f"❌ Git 오류: {e}")
        print("   수동으로 git push 해주세요.")

    print("=" * 60)


if __name__ == "__main__":
    run()
