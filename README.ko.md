# SourceTrace

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | **한국어** | [Italiano](README.it.md) | [العربية](README.ar.md)

> 이 문서는 [README.md](README.md)를 AI가 번역한 것입니다. 내용이 다르면 영어판을 기준으로 합니다.

AI가 생성한 지식 트리를 그 바탕이 된 슬라이드와 대조해 감사하는 Agent Skill입니다.

AI 도구는 강의 슬라이드를 몇 초 만에 지식 트리로 바꿔 주지만, 정의가 틀리거나 관계가 지어낸 것이거나 중요한 내용이 빠질 수 있습니다. SourceTrace는 모든 노드와 엣지를 원본 이미지와 대조하고, 판정마다 근거를 제시합니다. **왜** 문제인지, 슬라이드의 **어디**에 있는지(페이지와 인용), 그리고 **무엇**에 근거하는지(증거 ID)입니다.

Claude Code나 Codex처럼 Agent Skills를 지원하는 도구에서 동작하며, 중국어 또는 영어로 된 슬라이드와 웹 페이지 스크린샷을 처리합니다.

## 결과물

슬라이드 이미지(PNG/JPG)와 지식 트리(JSON)를 주면, 트리 옆의 `sourcetrace-output/` 폴더에 파일 세 개를 씁니다.

| 파일 | 내용 |
|------|---------|
| `report.md` | 감사 보고서: 요약, 문제, 출처 메모(접힘), 누락, 구조 문제, 확인된 항목 |
| `audit.json` | 같은 결과의 기계 판독용 버전: 모든 노드와 엣지에 대한 판정 |
| `evidence-index.json` | 슬라이드에서 추출한 모든 내용. 항목마다 ID, 페이지, 원문 그대로의 인용이 붙습니다 |

중국어 슬라이드 8페이지에서 실행했을 때의 지적 두 건입니다. 보고서는 중국어로 작성되었습니다. 글은 줄였고 수정 제안 열은 뺐습니다([전체 보고서](tests/smoke/model-eval-e2e/report.md)).

| 编号 | 对象 | 类别 | 风险 | 问题 | 证据 |
|---|---|---|---|---|---|
| F-002 | N005 数据集划分比例 | 概念错误 | 高 | 比例数字错误：树中写"8 : 1 : 1"，课件写"7 : 2 : 1"。 | EV-013 第 2 页 "本课程推荐的划分比例：训练集 : 验证集 : 测试集 = 7 : 2 : 1。" |
| F-004 | E010 过拟合 —related-to→ 高偏差 | 关系错误 | 高 | 关系对调：第 4 页图示为"过拟合 → 高方差"，树中却把过拟合连到高偏差。 | EV-020 第 4 页 "Diagram: 过拟合 → 高方差（对训练数据过于敏感）" |

각 문제는 여섯 범주(개념 오류, 잘못된 관계, 근거 없는 확장, 과잉 일반화, 검증 불가, 누락) 중 하나와 위험 수준을 받으며, 모든 지적에는 수정 제안이 붙습니다. 덧붙은 세부 사항 하나를 빼면 자료가 뒷받침하는 정의는 오류로 보지 않습니다. 낮은 위험의 *출처 메모*로, 따로 접힌 섹션에 표시됩니다.

## 빠른 시작

1. 유일한 의존 패키지를 설치합니다.

   ```bash
   pip install jsonschema
   ```

2. `source-trace/` 폴더를 사용하는 도구의 skills 폴더에 복사합니다.

   | 도구 | Skills 폴더 |
   |------|---------------|
   | Claude Code(개인) | `~/.claude/skills/source-trace/` |
   | Claude Code(프로젝트 하나) | `<project>/.claude/skills/source-trace/` |
   | Codex | `~/.codex/skills/source-trace/`(사용 중인 Codex 버전의 문서를 확인하세요) |

3. 슬라이드 이미지와 트리를 주고 자신의 말로 요청합니다.

   > 这是我的课件截图（slides/ 文件夹）和 AI 生成的知识树 tree.json，帮我对照课件检查一下。

   > Check knowledge-tree.json against my lecture slides in images/.

트리는 [`knowledge-tree.schema.json`](source-trace/schemas/knowledge-tree.schema.json)을 따라야 합니다(노드는 `id`, `label`, `definition`, `kind`, 엣지는 `id`, `source`, `target`, `relation`). 다른 형식이라면 스킬이 먼저 변환하고 어떻게 대응시켰는지 알려 줍니다. PPT나 PDF 슬라이드는 먼저 이미지로 내보내야 합니다.

## 개인정보

SourceTrace는 AI 에이전트 안에서 실행되므로, 에이전트가 슬라이드 이미지와 지식 트리를 읽습니다. 이 내용은 에이전트가 사용하는 AI 모델로 전송되며, 해당 제공자의 약관이 적용됩니다. 스킬 자체의 스크립트는 로컬에서 실행되며 어디로도 데이터를 보내지 않습니다.

- **AI 제공자와 공유해도 되는 슬라이드만 감사하세요.** 강의 슬라이드는 보통 강사의 것이므로 허락이 필요할 수 있습니다.
- **결과물은 슬라이드 자체처럼 다루세요.** `evidence-index.json`과 `report.md`에는 슬라이드의 원문 인용이 들어 있습니다.
- **다른 사람의 슬라이드나 감사 결과를 허락 없이 커밋하거나 공개하지 마세요.**

## 얼마나 잘 동작하나

**합성 슬라이드.** 오류를 심어 둔 두 테스트 세트(영어 슬라이드 4페이지, 중국어 슬라이드 8페이지)에서 일반 AI 어시스턴트와 SourceTrace 모두 심어 둔 오류를 전부 찾았습니다. SourceTrace는 일반 모델에 없는 것을 더합니다.

- 모든 판정 뒤에 있는 증거 ID, 페이지, 인용
- 모든 노드와 엣지에 대한 판정
- 고정된 범주와 위험 수준
- 기계 판독용 `audit.json`
- 엉뚱한 "누락" 항목이 없음
- 중국어 테스트 세트에서 네 번 실행한 결과가 모두 같음

대신 토큰은 약 30% 더 쓰고 시간은 약 3배 걸립니다.

**실제 콘텐츠.** 중국어 위키백과 문서(CC BY-SA 4.0)를 사용했고, 지식 트리는 다른 AI 도구로 생성했으므로 오류가 실제입니다. 처음 두 문서의 트리는 OpenAI Codex가 만들었으며, 프로젝트 소유자가 보고서마다 검토했고 검토할 때마다 규칙을 개정했습니다.

| 실행 | 검토한 항목 | 맞음 | 일부 맞음 | 틀림 |
|-----|--------------|---------|----------------|-------|
| 机器学习(기계 학습), 1회차(v0.1.0 규칙) | 13 | 6 | 4 | 3 |
| 机器学习(기계 학습), 2회차(1차 개정) | 18 | 14 | 1 | 3 |
| 决策树学习(결정 트리 학습), 1회차(2차 개정) | 지적 11건 + 확인된 항목 77개 | 85 | 1 | 2 |

v0.3.0의 내용(자세한 내용은 [CHANGELOG.md](CHANGELOG.md)):

- **문서 두 개를 더** 5차 규칙 개정으로 테스트했습니다. 朴素贝叶斯分类器(나이브 베이즈 분류기, 트리는 ChatGPT 제작): 두 번의 재실행이 87개 항목 모두에서 정답과 일치했습니다. 感知器(퍼셉트론, 트리는 Codex 제작): 두 실행 모두 트리에 있는 실제 오류 두 개를 찾았고 올바른 항목을 문제로 판정하지 않았지만, 자료 자체에 있는, 짧은 유도를 거쳐야 보이는 문제 네 개를 놓쳤습니다. 이 두 문서의 정답은 소유자가 승인한 AI 검토입니다. 朴素贝叶斯分类器의 정답은 트리를 만든 바로 그 대화에서 나왔습니다.
- **규모 테스트**(합성 슬라이드 32페이지, 169개 항목의 트리), **품질을 낮춘 이미지**(스캔, 사진, 일부를 가린 버전), 그리고 **Codex의 두 번의 실행**.

6차 규칙 개정은 Codex가 感知器(퍼셉트론)에서 한 번 실행했습니다. 항목 판정은 같았고, 짧은 유도가 필요한 자료 문제 네 개 중 두 개를 찾았습니다. 이 개정과 무관한 문서에서는 아직 테스트하지 않았으며, 모든 검토는 한 사람이 하거나 승인했습니다. 자세한 내용과 주의점: [docs/evaluation.md](docs/evaluation.md)와 각 테스트 세트의 `RESULTS.md`.

## 동작 방식

SourceTrace는 여섯 단계로 실행됩니다: 자료 수집 → 증거 추출 → 지식 매핑 → 양방향 감사 → 충돌 탐지 → 감사 보고서. 판단이 필요한 부분은 에이전트가 맡습니다: 슬라이드를 읽고, 주장과 증거를 맞추고, 판정을 고릅니다. 확인하거나 계산할 수 있는 일은 모두 스크립트 세 개가 합니다.

| 스크립트 | 단계 | 하는 일 |
|--------|-------|------|
| `validate_input.py` | 1 | 트리와 이미지를 확인하고, 페이지에 번호를 매기고, 트리가 끊어진 것 같은 구조 문제를 경고합니다 |
| `validate_evidence.py` | 2 | 증거 색인을 확인합니다: ID의 고유성, 페이지와 출처의 일치 |
| `build_report.py` | 6 | 에이전트의 `audit.json`을 트리와 증거에 비추어 확인하고, 요약과 지적 ID를 더해 `report.md`를 생성합니다 |

판정, 범주, 위험, 누락에 관한 규칙은 [`references/audit-rules.md`](source-trace/references/audit-rules.md)에 있습니다. 그 바탕이 된 설계 결정은 [docs/requirements.md](docs/requirements.md)에 있습니다.

스크립트를 직접 실행할 수도 있습니다.

```bash
python source-trace/scripts/validate_input.py --tree tests/fixtures/ml-basics/knowledge-tree.json --images tests/fixtures/ml-basics/images
python source-trace/scripts/validate_evidence.py --index tests/fixtures/ml-basics/evidence-index.example.json
python source-trace/scripts/build_report.py --tree <tree.json> --index <output>/evidence-index.json --audit <output>/audit.json
```

두 검증 스크립트는 `--json`을 주면 기계 판독용으로 출력합니다. `validate_input.py`가 쓰는 이미지 경로는 출력 폴더(트리 옆의 `sourcetrace-output/`, 또는 `--out`으로 지정한 폴더)에 대한 상대 경로입니다. 세 스크립트 모두 성공하면 0, 입력이 잘못되면 1, 사용법이 잘못되면 2로 종료합니다.

## 개발

```bash
pip install -r requirements.txt
python -m pytest
```

테스트는 119개이고 약 2초 걸립니다. 세 스크립트(유효한 입력, 모든 오류와 경고 코드, 출력의 재현성, 중국어와 영어 보고서)를 다루고, 저장된 스킬 실행 결과가 여전히 정답을 만족하는지도 확인합니다. 스킬 자체는 에이전트가 필요하므로 실행하지 않습니다. 새 실행을 채점할 때는 `tools/compare_runs.py`를 사용하세요.

```
source-trace/          스킬 본체(설치하는 것이 이 폴더)
├── SKILL.md           지침과 트리거 설명
├── schemas/           JSON Schema: 지식 트리, 증거 항목, 증거 색인, 감사 결과
├── references/        추출 규칙과 감사 규칙, 필요할 때 불러옴
└── scripts/           위의 스크립트 세 개
docs/                  요구 사항과 평가
tests/fixtures/        테스트 세트: 정답이 있는 합성 슬라이드, 위키백과 스크린샷(CC BY-SA)과 감사 실행 및 검토
tests/baseline/        비교용 일반 AI 실행
tests/smoke/           스킬의 종단 간 실행
tests/consistency/     스킬의 반복 실행
tests/test_*.py        pytest 테스트
tools/                 make_fixture_slides.py, compare_runs.py, degrade_images.py
```

## 현황과 다음 단계

v0.3.0입니다. [CHANGELOG.md](CHANGELOG.md)를 보세요.

테스트 데이터 원칙: SourceTrace는 공개 라이선스 자료, 프로젝트 소유자가 직접 쓴 자료, 또는 합성 자료로만 테스트합니다. 제3자의 강의 자료와 개인 데이터는 쓰지 않습니다.

다음 단계:

1. **6차 개정을 위한 새 문서:** 어떤 규칙에도 쓰이지 않은 문서. 가능하면 영어나 다른 분야이고, 정답은 트리를 만든 모델과 다른 모델이 작성합니다.
2. **독립적인 검토:** 소유자가 아닌 검토자, 또는 에이전트와 다른 모델이 만든 정답.
3. **실제 이미지:** 공개 라이선스이거나 소유자가 직접 만든 슬라이드의 사진 또는 스캔.
4. **작업 모드:** 엄격한 출처 추적 모드와, 자료 밖의 짧은 설명을 표시해서 허용하는 검토 모드.

## 라이선스

[MIT](LICENSE)
