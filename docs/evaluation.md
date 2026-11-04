# SourceTrace v0.1 evaluation

This compares a plain AI assistant with the SourceTrace skill on the same task: check an AI-generated knowledge tree against the slides it came from. All runs used Claude (Opus 5.5) and were made between 2026-11-01 and 2026-11-03.

**In short:** both find the planted problems. SourceTrace adds what a plain model does not give: an evidence ID, page and quote behind every verdict, a verdict for every node and edge, fixed categories and risk levels, a machine-readable `audit.json`, and the same result on every run.

## Setup

### Test sets

| Test set | Slides | Tree | Planted problems | Correct controls |
|----------|--------|------|------------------|------------------|
| [ml-basics](../tests/fixtures/ml-basics/) | 4, English | 9 nodes, 9 edges | 7 on tree items + 1 omission | 11 |
| [model-eval](../tests/fixtures/model-eval/) | 8, Chinese | 19 nodes, 18 edges | 11 on tree items + 4 omissions | 26 |

model-eval is the harder set: a changed number (7:2:1 → 8:1:1), a changed qualifier (通常 → 总是), definitions swapped inside a table, a swap visible only in a diagram, and a claim that needs two slides to check. Each answer key also lists content that should **not** be reported, such as homework, examples in parentheses, and content already covered by another finding.

### Conditions

| | Baseline | SourceTrace |
|---|---|---|
| Input | Slide images and `knowledge-tree.json` | Same |
| Instructions | One plain request ("check the tree against the slides; point out problems and omissions") | The same request, with the skill folder available |
| Answer key visible | No | No |
| Runs | 2 per test set | ml-basics: 1. model-eval: 3 under the final rules, plus 1 end-to-end run with `build_report.py` |

Each run was a fresh agent restricted to its own copy of the inputs. All raw outputs are in the repository: [tests/baseline/](../tests/baseline/), [tests/smoke/](../tests/smoke/) and [tests/consistency/](../tests/consistency/).

The baselines were graded by hand against the final v0.1 answer keys. The skill runs were graded with `tools/compare_runs.py`, and the results are locked in by `tests/test_fixtures_and_runs.py`.

## Results

### Finding the problems

| | Baseline ml-basics | Skill ml-basics | Baseline model-eval | Skill model-eval |
|---|---|---|---|---|
| Planted tree problems found | 7/7, 7/7 | 7/7 | 11/11, 11/11 | 11/11 in all 4 runs |
| Expected omissions found | 1/1, 1/1 | 1/1 | 4/4, 4/4 | 4/4 in all 4 runs |
| Correct items flagged as wrong | 1, 1 (E009) | 0 | 0, 0 | 0 |
| Reported something the key says not to report | 2, 2 | 0 | 2, 2 (+ homework listed as minor) | 0 |
| Other omissions outside the key | 3, 3 | 0 | 2, 3 | 0 |

Detection is a draw: the plain model found every planted problem, including the subtle ones. The difference is **precision**. The baseline also reports:
- things the rules exclude: examples in parentheses (k-means, PCA), and content already covered by another finding (the comparison table, "测试集只能使用一次", "类别不平衡时准确率会误导");
- several extra "missing" items of its own choosing, a different set in each run.

The single flagged correct item, E009 (RL —uses→ Feedback), is a judgment call that both baseline runs made. The v0.1 rules settle it explicitly (a true but incomplete edge is supported).

### Traceability and structure

| | Baseline (4 runs) | SourceTrace |
|---|---|---|
| Evidence for each finding | Slide number in the text, sometimes with a quote; no evidence IDs | Evidence ID + page + verbatim quote, from an index that passes `validate_evidence.py` |
| Verdict for **every** node and edge | Run 1 confirmed 4/11 and 1/26 correct items; run 2 confirmed 10/11 and 24/26 | 18/18 and 37/37 in every run |
| Categories | Each run invents its own grouping. Overgeneralizations (N006, N017) end up under "errors" or "contradictions". | Six fixed categories, chosen with a decision order |
| Risk levels | None | high / medium / low with defaults; a change needs `risk_reason` |
| Machine-readable output | None | `audit.json`, checked against a schema |
| Recommended fixes that fit the tree format | Not checked. One run used relations such as `"feedback: correct answers"`, which the format does not allow. | Required to use the allowed `kind` and `relation` values |
| Disconnected tree (model-eval) | Found by both runs | Reported by the validator in every run |

### Consistency across runs (model-eval)

| | Agreement on all 37 items |
|---|---|
| Baseline, 2 runs | Not measurable: no shared structure, categories or verdict list |
| Skill before the Day 6 rules, 3 runs | verdict 37/37, category 36/37, risk 36/37 |
| Skill with the final v0.1 rules, 3 runs + end-to-end run | **verdict, category and risk 37/37 across all 4 runs** |

All four final-rule runs produced the same summary: 26 supported, 11 findings, 4 omissions; 7 high, 6 medium, 2 low. The end-to-end run's `audit.json` passed `build_report.py` on the first try. Rerunning the script reproduces its `report.md` byte for byte.

### Cost

Figures as reported by each run's agent. They are rough but comparable.

| | Tokens | Time |
|---|---|---|
| Baseline, ml-basics | ~60k | 31–43 s |
| Skill, ml-basics | ~80k | 144 s |
| Baseline, model-eval | ~66k | 51 s |
| Skill, model-eval (final rules, 3 runs) | ~86k | 143–156 s |

The skill uses about **30% more tokens and about 3× the time**. Time per stage was not measured.

## What this shows, and what it doesn't

**Shows:**
- On these two test sets, a plain model already detects the planted errors. SourceTrace's value is not better detection.
- SourceTrace's value is a result that can be **checked and repeated**: every verdict cites evidence, every item gets a verdict, the categories and risks are fixed, and four independent runs produced the same audit.
- It also keeps reports focused. The rules for what counts as an omission removed all the noise the baseline produced.

**Does not show:**
- **Real material.** Both test sets were written by the developer, and the agents that ran the skill use the same model family that helped write it. Agreement with the answer keys partly measures agreement with the rules' author. Agreement *between runs* does not depend on the keys, and is the stronger result.
- **Scale.** 4 and 8 slides. Detection may differ on 30+ slides or trees with hundreds of nodes, where a plain model is more likely to miss things.
- **Image quality.** All slides are clean renders. Scans and photos are untested.
- **Other agents.** Only Claude was tested. Codex and other Agent Skills tools are untested.
- **Sample size.** 2 baseline runs and 1–4 skill runs per test set.

## Next steps

1. **Real course slides** (the main gap): audit one or more real lectures, ideally with an answer key written by someone other than the developer.
2. **Scale:** a 30+ slide deck and a tree with 100+ nodes, to test both detection and the page-by-page workflow.
3. **Scanned or photographed slides,** to test `certainty` and the low-certainty rules.
4. **Codex** and other Agent Skills tools.

## Reproducing

```bash
pip install -r requirements.txt
python -m pytest                      # 77 tests, including the saved-run checks
python -I tools/compare_runs.py . model-eval tests/consistency/model-eval/day6/run-1 tests/consistency/model-eval/day6/run-2 tests/consistency/model-eval/day6/run-3 tests/smoke/model-eval-e2e
```
