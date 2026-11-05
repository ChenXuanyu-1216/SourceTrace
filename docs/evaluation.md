# SourceTrace evaluation

Two parts:

- **[Synthetic slides (v0.1)](#setup):** a plain AI assistant compared with the SourceTrace skill on two test sets with planted errors. Runs made between 2026-11-01 and 2026-11-03.
- **[Real content (v0.2)](#real-content-v02):** SourceTrace on two Wikipedia articles, with knowledge trees from another AI tool, graded by the project owner. Runs made on 2026-11-04 and 2026-11-05.

All runs used Claude (Opus 5.5).

**In short:** on synthetic slides, both the plain model and SourceTrace find the planted problems. SourceTrace adds what a plain model does not give: an evidence ID, page and quote behind every verdict, a verdict for every node and edge, fixed categories and risk levels, a machine-readable `audit.json`, and the same result on every run. On real content, the first run had too many false or mislabelled findings. After two rule revisions based on the owner's reviews, 85 of 88 judged items on a new article were right, 1 was partly right and 2 were wrong.

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

## Real content (v0.2)

### Setup

| Test set | Source | Pages | Tree |
|----------|--------|-------|------|
| [wiki-ml-zh](../tests/fixtures/wiki-ml-zh/) | Chinese Wikipedia, 机器学习 (CC BY-SA 4.0) | 12 | 40 nodes, 58 edges |
| [wiki-dt-zh](../tests/fixtures/wiki-dt-zh/) | Chinese Wikipedia, 决策树学习 (CC BY-SA 4.0) | 6 | 35 nodes, 46 edges |

- **Trees:** generated by OpenAI Codex from the screenshots with a fixed prompt, and saved unedited. Their mistakes are real, not planted.
- **Runs:** each run was a fresh Claude agent with no web access, working on its own copy of the skill and the inputs.
- **Answer key:** the project owner judged each finding as correct, partly correct (right problem, wrong category or risk) or wrong, and listed what the audit missed. The reviews are saved next to each run.

### Results

| Run | Rules | Supported / findings / omissions | Owner's judgments | Cost |
|-----|-------|----------------------------------|-------------------|------|
| wiki-ml-zh run 1 | v0.1.0 | 83 / 15 / 25 | 13 findings: 6 correct, 4 partly, 3 wrong | ~203k tokens, 14 min |
| wiki-ml-zh run 2 | first revision | 82 / 16 / 25 | 18 items: 14 correct, 1 partly, 3 wrong | ~159k tokens, 11 min |
| wiki-dt-zh run 1 | second revision | 77 / 4 / 7 | 11 findings: 8 correct, 1 partly, 2 wrong. All 77 supported items upheld; 2 low-risk omissions missed | ~139k tokens, 9 min |

In every run, all three scripts passed on the first try.

### What the reviews changed

| Review | Main problems found | Rule change |
|--------|---------------------|-------------|
| wiki-ml-zh run 1 | A high-risk "conceptual error" that was not one (条件依赖 vs 条件独立性); evidence in a figure and across pages ignored; one added detail labelled "ambiguous" | Gather all evidence first; contradiction test; new `scope: detail` (low risk); `ambiguous` narrowed |
| wiki-ml-zh run 2 | The explanation of a term reported as an added detail; a class defined from one example accepted; an edge supported by its paragraph rejected | Boundaries of `detail`; paragraph rule for `uses`; recommendations add no claims |
| wiki-dt-zh run 1 | Narrower or more cautious claims reported as details; limitations sections skimmed | Narrowing the source implies is supported; a different word for a different property is a detail; omissions only for parts a node lacks |

The two wrong findings on wiki-dt-zh are both low-risk source notes, and the third revision addresses them. No run after the first revision produced a high-risk finding that the owner rejected.

### Report changes from the reviews

- `detail` findings appear as folded source notes, apart from the problems.
- The summary counts problems, source notes and omissions separately.
- Evidence quotes are shown in full.

## What this shows, and what it doesn't

**Shows:**
- On these two test sets, a plain model already detects the planted errors. SourceTrace's value is not better detection.
- SourceTrace's value is a result that can be **checked and repeated**: every verdict cites evidence, every item gets a verdict, the categories and risks are fixed, and four independent runs produced the same audit.
- It also keeps reports focused. The rules for what counts as an omission removed all the noise the baseline produced.

- On real content, the owner's reviews found real rule problems. The first revision, re-run on the same article, fixed most of the cases it targeted: 12 of the 13 reviewed findings then matched the review. The second article, which played no part in the first two revisions, had no high-risk false finding and no supported item that the owner rejected.

**Does not show:**
- **The latest rules in action.** Only the first revision was re-run on the article that prompted it. The second was used once, on wiki-dt-zh; the third has not been run.
- **Independent grading at scale.** One reviewer, and one tree generator (Codex). The omissions of the wiki-ml-zh runs (25 per run) were not judged. On the synthetic sets, the developer wrote both the rules and the answer keys, and the agents that ran the skill use the same model family that helped write it. Agreement *between runs* does not depend on the keys, and is the stronger synthetic result.
- **Scale.** At most 12 pages and 98 tree items. Detection may differ on 30+ slides or trees with hundreds of nodes.
- **Image quality.** All inputs are clean renders or screenshots. Scans and photos are untested.
- **Other agents.** Only Claude was tested. Codex and other Agent Skills tools are untested.
- **Sample size.** 2 baseline runs and 1–4 skill runs per synthetic test set; 1–2 runs per real-content test set. No baseline was run on real content.

## Next steps

Test data must be openly licensed, written by the project owner, or synthetic. No third-party course material is used.

1. **Codex** and other Agent Skills tools: run SourceTrace in Codex on the `wiki-ml-zh` inputs.
2. **Scale:** a synthetic deck of 30+ slides and a tree with 100+ nodes, to test both detection and the page-by-page workflow.
3. **Image quality:** scan- and photo-like versions of the test slides (blur, noise, rotation, compression) generated by a script, to test `certainty` and the low-certainty rules.
4. **A new real-content test set** to check the third rule revision, ideally with a tree from a tool other than Codex.

## Reproducing

```bash
pip install -r requirements.txt
python -m pytest                      # 91 tests, including the saved-run checks
python -I tools/compare_runs.py . model-eval tests/consistency/model-eval/day6/run-1 tests/consistency/model-eval/day6/run-2 tests/consistency/model-eval/day6/run-3 tests/smoke/model-eval-e2e
```
