#!/usr/bin/env node
/**
 * generate-complex-pages.mjs
 *
 * complex-blog-export.json을 읽어 Hugo 마크다운 페이지를 생성합니다.
 *
 * 실행: node scripts/generate-complex-pages.mjs
 * 입력: ../mdeeno/mdeeno-platform/data/complex-blog-export.json
 * 출력: content/complex/{slug}.md (각 단지별)
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const BLOG_ROOT = path.join(__dirname, '..');
const DATA_PATH = path.join(
  __dirname,
  '..',
  '..',
  'mdeeno',
  'mdeeno-platform',
  'data',
  'complex-blog-export.json',
);
const OUTPUT_DIR = path.join(BLOG_ROOT, 'content', 'complex');

const CTA_URL =
  'https://mdeeno.com/member?utm_source=blog&utm_medium=complex_page&utm_campaign=seo_complex';

const TODAY = new Date().toISOString().split('T')[0];

// ── 데이터 로드 ──

if (!fs.existsSync(DATA_PATH)) {
  console.error(`[ERROR] Data file not found: ${DATA_PATH}`);
  console.error(
    'Run: node scripts/export-complex-data-for-blog.mjs in mdeeno-platform first.',
  );
  process.exit(1);
}

const complexes = JSON.parse(fs.readFileSync(DATA_PATH, 'utf-8'));
console.log(`[INFO] Loaded ${complexes.length} complexes from data file`);

// ── 출력 디렉토리 생성 ──

if (!fs.existsSync(OUTPUT_DIR)) {
  fs.mkdirSync(OUTPUT_DIR, { recursive: true });
}

// ── _index.md 생성 (섹션 목록 페이지) ──

const indexContent = `---
title: "재건축 단지별 분담금 리스크 분석"
description: "M-DEENO가 보유한 ${complexes.length}개 단지의 분담금 리스크를 시나리오별로 분석합니다. 내 단지를 찾아보세요."
date: ${TODAY}
layout: "list"
---

M-DEENO 시뮬레이션 엔진이 분석한 **${complexes.length}개 단지**의 분담금 리스크를 확인하세요.
각 단지 페이지에서 공사비 변동 시나리오별 분담금 변화를 시뮬레이션할 수 있습니다.
`;

fs.writeFileSync(path.join(OUTPUT_DIR, '_index.md'), indexContent, 'utf-8');

// ── 사업 단계 한글 → description용 ──

const STAGE_DESC = {
  정비구역지정: '정비구역 지정 단계',
  사업시행인가: '사업시행인가 단계',
  관리처분: '관리처분 단계',
  시공중: '시공 진행 중',
  미확인: '단계 미확인',
};

const RISK_DESC = {
  R1: '저위험 등급으로, 비례율이 높아 환급 가능성이 있습니다',
  R2: '보통 등급으로, 분담금이 발생하나 관리 가능한 수준입니다',
  R3: '고위험 등급으로, 공사비 변동에 따라 분담금이 크게 증가할 수 있습니다',
  R4: '초고위험 등급으로, 비례율이 낮아 분담금 부담이 매우 높습니다',
};

const RISK_BADGE = {
  R1: '안전',
  R2: '보통',
  R3: '경고',
  R4: '위험',
};

/**
 * 단지 연차 계산
 */
function getAge(buildYear) {
  if (!buildYear) return null;
  return new Date().getFullYear() - buildYear;
}

/**
 * 숫자를 한국어 형식으로 포맷
 */
function formatNumber(num) {
  if (num === null || num === undefined) return '-';
  return num.toLocaleString('ko-KR');
}

/**
 * 분담금 표시 (환급 포함)
 */
function formatExtra(extra) {
  if (extra === null || extra === undefined) return '-';
  if (extra < 0) return `환급 ${Math.abs(extra)}억`;
  return `${extra}억`;
}

/**
 * 체크포인트 생성 (단지 특성 기반)
 */
function generateCheckpoints(complex) {
  const points = [];

  // 비례율 기반
  if (complex.proportionRate < 80) {
    points.push(
      `비례율이 ${complex.proportionRate}%로 매우 낮습니다. 종전자산 대비 총사업비가 높아 분담금 부담이 클 수 있으며, 공사비 상승 시 추가 부담이 급격히 증가할 수 있습니다.`,
    );
  } else if (complex.proportionRate < 95) {
    points.push(
      `비례율 ${complex.proportionRate}%는 분담금이 발생하는 구간입니다. 공사비 변동과 분양가 확정에 따라 실제 부담액이 크게 달라질 수 있어 시나리오별 검토가 필요합니다.`,
    );
  } else if (complex.proportionRate < 105) {
    points.push(
      `비례율 ${complex.proportionRate}%는 분담금과 환급의 경계 구간입니다. 공사비·분양가 변동에 따라 결과가 달라질 수 있으므로 시나리오별 분석이 중요합니다.`,
    );
  } else {
    points.push(
      `비례율 ${complex.proportionRate}%로 환급 가능성이 있는 구간입니다. 다만 공사비 상승 시 환급 규모가 줄어들거나 분담금으로 전환될 수 있습니다.`,
    );
  }

  // 사업 단계 기반
  if (complex.stage === '정비구역지정') {
    points.push(
      '아직 정비구역 지정 단계로, 사업시행인가와 관리처분까지 상당한 시간이 소요됩니다. 공사비·분양가 확정 전이므로 현재 추정치는 참고용으로만 활용해야 합니다.',
    );
  } else if (complex.stage === '사업시행인가') {
    points.push(
      '사업시행인가 단계입니다. 관리처분계획 수립 시 감정평가와 분양가가 확정되면 실제 분담금이 결정됩니다. 총회 의결 전 시나리오를 검토하시기 바랍니다.',
    );
  } else if (complex.stage === '관리처분') {
    points.push(
      '관리처분 단계로 분담금 윤곽이 드러나는 시점입니다. 감정평가 결과와 조합원분양가를 꼼꼼히 확인하고, 이의신청 기한을 놓치지 마세요.',
    );
  }

  // 건축 연도 기반
  const age = getAge(complex.buildYear);
  if (age && age >= 40) {
    points.push(
      `건축 ${complex.buildYear}년(${age}년차)으로 노후도가 높아 안전진단 통과 가능성이 높지만, 철거·이주비 등 추가 비용 발생 가능성도 확인해야 합니다.`,
    );
  }

  return points.slice(0, 3);
}

// ── 페이지 생성 ──

let generated = 0;

for (const complex of complexes) {
  const age = getAge(complex.buildYear);
  const ageStr = age ? `${age}년차` : '';
  const buildYearStr = complex.buildYear
    ? `${complex.buildYear}년 (${ageStr})`
    : '-';

  // description: SEO 최적화 (숫자 포함으로 클릭 유인)
  const extraDesc =
    complex.confirmedExtra !== null
      ? `추정 분담금 약 ${formatExtra(complex.confirmedExtra)} 수준, `
      : '';
  const description = `${complex.name}(${complex.district}) 재건축 분담금 리스크를 시나리오별로 분석합니다. ${extraDesc}비례율 ${complex.proportionRate}%, 리스크 등급 ${complex.riskGrade}. 공사비 변동 시 분담금 변화를 확인하세요.`;

  // 체크포인트
  const checkpoints = generateCheckpoints(complex);

  // ── Front Matter (YAML) ──
  const frontMatter = {
    title: `${complex.name} 분담금 리스크 분석 | M-DEENO`,
    description,
    date: TODAY,
    lastmod: TODAY,
    slug: complex.slug,
    layout: 'complex',
    type: 'complex',
    tags: ['재건축', '분담금', complex.district, complex.riskGrade],
    categories: ['단지분석'],
    hideMeta: true,
    disableShare: false,
    ShowToc: false,
    ShowBreadCrumbs: true,
    complexData: {
      name: complex.name,
      district: complex.district,
      city: complex.city || '',
      location: complex.location || '',
      stage: complex.stage,
      buildYear: complex.buildYear,
      households: complex.households,
      proportionRate: complex.proportionRate,
      expectedCost: complex.expectedCost,
      avgAssetValue: complex.avgAssetValue,
      representativePyeong: complex.representativePyeong,
      vlRat: complex.vlRat,
      riskGrade: complex.riskGrade,
      riskLabel: complex.riskLabel,
      dataSource: complex.dataSource,
      confirmedExtra: complex.confirmedExtra,
      confirmedExtraLabel: complex.confirmedExtraLabel,
      scenarios: complex.scenarios,
    },
  };

  // YAML 직렬화 (간단한 구현)
  function yamlValue(val, indent = 0) {
    if (val === null || val === undefined) return 'null';
    if (typeof val === 'boolean') return val ? 'true' : 'false';
    if (typeof val === 'number') return String(val);
    if (typeof val === 'string') {
      // 특수문자 포함 시 따옴표
      if (
        val.includes(':') ||
        val.includes('#') ||
        val.includes('"') ||
        val.includes("'") ||
        val.includes('\n') ||
        val.includes('|') ||
        val.includes('>') ||
        val.startsWith(' ') ||
        val.endsWith(' ')
      ) {
        return `"${val.replace(/"/g, '\\"')}"`;
      }
      return `"${val}"`;
    }
    if (Array.isArray(val)) {
      return val.map((v) => `\n${'  '.repeat(indent)}- ${typeof v === 'object' ? yamlObj(v, indent + 1) : yamlValue(v)}`).join('');
    }
    if (typeof val === 'object') {
      return '\n' + yamlObj(val, indent);
    }
    return String(val);
  }

  function yamlObj(obj, indent = 1) {
    return Object.entries(obj)
      .map(([k, v]) => {
        const prefix = '  '.repeat(indent);
        if (typeof v === 'object' && v !== null && !Array.isArray(v)) {
          return `${prefix}${k}:${yamlValue(v, indent + 1)}`;
        }
        if (Array.isArray(v)) {
          return `${prefix}${k}:${yamlValue(v, indent + 1)}`;
        }
        return `${prefix}${k}: ${yamlValue(v)}`;
      })
      .join('\n');
  }

  const yamlFrontMatter = yamlObj(frontMatter);

  // ── 본문 마크다운 ──

  // 시나리오 테이블
  const scenarioRows = Object.entries(complex.scenarios)
    .map(([key, s]) => {
      const label =
        key === 'base'
          ? '기준 (0%)'
          : `+${s.costIncrease}%`;
      const extra = formatExtra(s.extra);
      const diff =
        key === 'base'
          ? '-'
          : `${s.extra >= 0 ? '+' : ''}${(s.extra - complex.scenarios.base.extra).toFixed(1)}억`;
      return `| ${label} | ${extra} | ${diff} |`;
    })
    .join('\n');

  // 확정 분담금 테이블 (있는 경우)
  let extraTable = '';
  if (complex.allExtras && complex.allExtras.length > 0) {
    const rows = complex.allExtras
      .map(
        (e) =>
          `| ${e.currentPyeong}평 | ${e.desiredPyeong}평 | ${formatExtra(e.extra)} |`,
      )
      .join('\n');
    extraTable = `
## 평형별 추정 분담금

공개 자료 기반의 평형별 추정 분담금입니다.

| 소유 평형 | 희망 평형 | 추정 분담금 |
|:---------:|:---------:|:----------:|
${rows}

> 위 수치는 조합 공개 자료 또는 언론 보도 기반이며, 실제 관리처분계획 확정 시 변동될 수 있습니다.
`;
  }

  // 체크포인트 리스트
  const checkpointsList = checkpoints
    .map((cp, i) => `${i + 1}. ${cp}`)
    .join('\n');

  // R등급 설명
  const riskExplanation = RISK_DESC[complex.riskGrade];

  const body = `
## ${complex.name}, 분담금 리스크는 어느 수준인가?

${complex.name}(${complex.district})은 비례율 <strong>${complex.proportionRate}%</strong>로 리스크 등급 <strong>${complex.riskGrade} (${complex.riskLabel})</strong>에 해당합니다.
${complex.confirmedExtra !== null ? `공개 자료 기준 대표 추정 분담금은 <strong>${formatExtra(complex.confirmedExtra)}</strong> 수준입니다 (${complex.confirmedExtraLabel}).` : '아직 확정된 분담금 데이터가 공개되지 않아 시뮬레이션 모델 기반 추정치를 제공합니다.'}

<div class="complex-cta-box">
<a href="${CTA_URL}" class="complex-cta-btn" target="_blank" rel="noopener">내 평형 기준으로 무료 리스크 진단 받기</a>
</div>

## 기본 정보

| 항목 | 값 |
|:-----|:-----|
| 위치 | ${complex.location || complex.district} |
| 건축년도 | ${buildYearStr} |
| 세대수 | ${complex.households ? formatNumber(complex.households) + '세대' : '미확인'} |
| 사업 단계 | ${complex.stage} |
| 추정 비례율 | ${complex.proportionRate}% |
| 추정 공사비 | ${formatNumber(complex.expectedCost)}만원/평 |
${complex.vlRat ? `| 용적률 | ${complex.vlRat}% |` : ''}
${complex.kaptBcompany ? `| 시공사 | ${complex.kaptBcompany} |` : ''}

## 공사비 변동 시 분담금 시나리오

> 아래 수치는 공개 데이터 기반 시뮬레이션 추정값이며, 실제와 다를 수 있습니다. 투자 판단의 근거로 사용할 수 없습니다.

공사비가 상승하면 총사업비가 증가하고, 이는 비례율 하락과 분담금 증가로 이어집니다.
아래는 ${complex.name}의 공사비 변동 시나리오별 추정 분담금입니다.

| 공사비 상승 | 추정 분담금 | 기준 대비 |
|:----------:|:----------:|:--------:|
${scenarioRows}

> **면책**: 이 수치는 M-DEENO 시뮬레이션 엔진의 추정값이며, 실제 분담금은 감정평가, 분양가, 총회 결과에 따라 달라집니다. 투자 판단의 근거로 사용하지 마시고, 반드시 조합 공식 자료를 확인하시기 바랍니다.
${extraTable}
## 리스크 등급: ${complex.riskGrade} (${complex.riskLabel})

${riskExplanation}.

M-DEENO의 리스크 등급은 비례율을 기반으로 분류됩니다:
- **R1 (저위험)**: 비례율 105% 이상 - 환급 가능성
- **R2 (보통)**: 비례율 95~105% - 분담금 발생, 관리 가능
- **R3 (고위험)**: 비례율 80~95% - 분담금 부담 주의
- **R4 (초고위험)**: 비례율 80% 미만 - 분담금 부담 매우 높음

## 이 단지 조합원이 확인해야 할 핵심 포인트

${checkpointsList}

<div class="complex-cta-box">
<a href="${CTA_URL}" class="complex-cta-btn" target="_blank" rel="noopener">내 조건으로 정밀 리스크 진단 받기 (무료)</a>
</div>

---

<p class="complex-disclaimer">
<strong>면책 조항</strong>: 본 분석은 국토교통부 실거래가, 건축물대장, 조합 공개 자료 등을 기반으로 M-DEENO 시뮬레이션 엔진이 산출한 추정값입니다.
실제 분담금은 감정평가, 관리처분계획, 총회 의결 결과에 따라 달라지며, 본 자료를 투자 판단이나 부동산 거래의 근거로 사용할 수 없습니다.
본 페이지는 정보 제공 목적이며, 정확한 분담금은 해당 조합에 직접 확인하시기 바랍니다.
</p>
`;

  // ── 파일 쓰기 ──
  const filePath = path.join(OUTPUT_DIR, `${complex.slug}.md`);
  const content = `---\n${yamlFrontMatter}\n---\n${body}`;
  fs.writeFileSync(filePath, content, 'utf-8');
  generated++;
}

console.log(`\n[DONE] ${generated} complex pages generated in ${OUTPUT_DIR}`);
console.log(`[DONE] _index.md created for section listing`);
