#!/usr/bin/env python3
"""
seo_title_update.py
기존 포스트의 title/description을 CTR 최적화 기준으로 일괄 업데이트.

- 본문, URL, 발행일 변경 없음
- frontmatter의 title / description 만 교체
- 처리 결과를 seo_update_log.json에 저장 (재시작 시 이어서 처리)

사용법:
    python3 scripts/seo_title_update.py
    python3 scripts/seo_title_update.py --dry-run   # 실제 파일 미수정
    python3 scripts/seo_title_update.py --folder reconstruction  # 폴더 한정
"""

import os, re, json, time, sys, argparse
from pathlib import Path
import google.generativeai as genai
from dotenv import load_dotenv

# ── 경로 설정 ──────────────────────────────────────────────────────────────────
BASE_DIR   = Path(__file__).resolve().parent.parent
POSTS_DIR  = BASE_DIR / "content" / "posts"
LOG_FILE   = Path(__file__).resolve().parent / "seo_update_log.json"
ENV_FILE   = BASE_DIR.parent / "posting-engine" / ".env"

load_dotenv(ENV_FILE)
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    # 폴백: mdeeno-platform .env.local 시도
    load_dotenv(BASE_DIR.parent / "mdeeno" / "mdeeno-platform" / ".env.local")
    api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel("gemini-flash-latest")

# ── 설정 ───────────────────────────────────────────────────────────────────────
BATCH_SIZE     = 8    # 한 번에 Gemini에 보낼 포스트 수
DELAY_SECONDS  = 3    # 배치 간 딜레이 (rate limit 방어)

# ── 로그 로드/저장 ──────────────────────────────────────────────────────────────
def load_log():
    if LOG_FILE.exists():
        with open(LOG_FILE) as f:
            return json.load(f)
    return {"done": [], "failed": []}

def save_log(log):
    with open(LOG_FILE, "w") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

# ── 마크다운 프론트매터 파싱 ────────────────────────────────────────────────────
FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)

def parse_frontmatter(text):
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None, text
    fm = m.group(1)
    body = text[m.end():]
    return fm, body

def get_field(fm, key):
    """프론트매터에서 특정 필드값 추출."""
    pattern = rf'^{key}:\s*"?(.*?)"?\s*$'
    m = re.search(pattern, fm, re.MULTILINE)
    return m.group(1).strip() if m else ""

def replace_field(fm, key, new_value):
    """프론트매터에서 특정 필드값만 교체."""
    new_value_clean = new_value.strip().replace('"', "'")
    pattern = rf'^({key}:\s*)(".*?"|.*?)(\s*)$'
    replacement = rf'\g<1>"{new_value_clean}"\g<3>'
    new_fm, count = re.subn(pattern, replacement, fm, flags=re.MULTILINE)
    if count == 0:
        # 필드가 없으면 추가
        new_fm = fm + f'\n{key}: "{new_value_clean}"'
    return new_fm

# ── Gemini 배치 호출 ───────────────────────────────────────────────────────────
PROMPT_TEMPLATE = """
당신은 한국 부동산/재건축 SEO 전문가입니다.
아래 블로그 포스트들의 title과 description을 CTR 최적화 기준으로 개선하세요.

[개선 기준]
Title:
- 30자 이내 (초과하면 검색결과에서 잘림)
- 핵심 키워드를 앞쪽에 배치
- 숫자("3가지", "2배") 또는 질문형("~이란?", "~방법") 사용
- 클릭욕구 유발: "실제 사례", "계산 예시", "체크리스트" 등
- "완벽 정리", "총정리", "A to Z" 금지

Description:
- 80~120자
- 핵심 키워드 자연스럽게 포함
- 구체적 수치나 혜택 명시
- 행동 유도 문구로 마무리: "지금 확인하세요", "무료로 계산해보세요"
- title과 내용 그대로 반복 금지

[입력] (JSON 배열)
{input_json}

[출력] 반드시 아래 JSON 배열 형식만 출력하세요 (다른 텍스트 없이):
[
  {{"id": 0, "title": "개선된 제목", "description": "개선된 설명"}},
  ...
]
"""

def call_gemini_batch(batch):
    """batch: [{"id": int, "title": str, "description": str, "tags": str}]"""
    prompt = PROMPT_TEMPLATE.format(input_json=json.dumps(batch, ensure_ascii=False, indent=2))
    try:
        resp = model.generate_content(prompt)
        raw = resp.text.strip()
        # JSON만 추출 (```json ``` 블록 대응)
        json_match = re.search(r'\[.*\]', raw, re.DOTALL)
        if not json_match:
            return None
        return json.loads(json_match.group())
    except Exception as e:
        print(f"  ⚠️ Gemini 오류: {e}")
        return None

# ── 파일 목록 수집 ──────────────────────────────────────────────────────────────
def collect_files(folder_filter=None):
    files = []
    for folder in sorted(POSTS_DIR.iterdir()):
        if not folder.is_dir():
            continue
        if folder_filter and folder.name != folder_filter:
            continue
        for md in sorted(folder.glob("*.md")):
            files.append(md)
    return files

# ── 메인 ───────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true", help="파일 미수정 (테스트)")
    parser.add_argument("--folder", default=None, help="특정 폴더만 처리 (예: reconstruction)")
    args = parser.parse_args()

    log = load_log()
    done_set = set(log["done"])

    all_files = collect_files(args.folder)
    pending = [f for f in all_files if str(f) not in done_set]

    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}총 {len(all_files)}개 중 {len(pending)}개 처리 예정\n")

    updated = 0
    failed  = 0

    for i in range(0, len(pending), BATCH_SIZE):
        batch_files = pending[i:i + BATCH_SIZE]
        batch_input = []
        file_data   = []

        for j, md_path in enumerate(batch_files):
            text = md_path.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(text)
            if fm is None:
                continue
            title = get_field(fm, "title")
            desc  = get_field(fm, "description")
            tags  = get_field(fm, "tags")
            batch_input.append({"id": j, "title": title, "description": desc, "tags": tags})
            file_data.append({"path": md_path, "fm": fm, "body": body, "text": text})

        if not batch_input:
            continue

        print(f"배치 {i//BATCH_SIZE + 1}: {len(batch_input)}개 처리 중...")
        results = call_gemini_batch(batch_input)

        if not results:
            print("  ❌ Gemini 응답 실패, 건너뜀")
            for d in file_data:
                log["failed"].append(str(d["path"]))
            failed += len(file_data)
            save_log(log)
            time.sleep(DELAY_SECONDS)
            continue

        for r in results:
            idx = r.get("id", 0)
            if idx >= len(file_data):
                continue
            d = file_data[idx]
            new_title = r.get("title", "").strip()
            new_desc  = r.get("description", "").strip()

            if not new_title or not new_desc:
                continue

            # 길이 초과 시 경고만 (Gemini가 30자 넘기는 경우 대비)
            if len(new_title) > 35:
                print(f"  ⚠️ 제목 길이 초과({len(new_title)}자): {new_title[:30]}...")

            if not args.dry_run:
                new_fm = replace_field(d["fm"], "title", new_title)
                new_fm = replace_field(new_fm, "description", new_desc)
                new_text = f"---\n{new_fm}\n---\n{d['body']}"
                d["path"].write_text(new_text, encoding="utf-8")

            log["done"].append(str(d["path"]))
            updated += 1
            print(f"  ✓ {d['path'].name[:50]}")
            print(f"    제목: {new_title}")
            print(f"    설명: {new_desc[:60]}...")

        save_log(log)
        time.sleep(DELAY_SECONDS)

    print(f"\n{'[DRY-RUN] ' if args.dry_run else ''}완료: {updated}개 수정, {failed}개 실패")
    print(f"로그: {LOG_FILE}")

if __name__ == "__main__":
    main()
