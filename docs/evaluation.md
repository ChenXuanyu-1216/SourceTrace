# SourceTrace evaluation

Three parts:

- **[Synthetic slides (v0.1)](#setup):** a plain AI assistant compared with the SourceTrace skill on two test sets with planted errors. Runs made between 2026-11-01 and 2026-11-03.
- **[Real content (v0.2)](#real-content-v02):** SourceTrace on two Wikipedia articles, with knowledge trees from another AI tool, graded by the project owner. Runs made on 2026-11-04 and 2026-11-05.
- **[Since v0.2.0](#since-v020):** a scale test, degraded images, two more Wikipedia articles, and the first runs by OpenAI Codex. Runs made between 2026-11-05 and 2026-11-10.

Up to v0.2.0, all runs used Claude (Opus 5.5). Since then, two runs used OpenAI Codex and the rest Claude.

**In short:** on synthetic slides, both the plain model and SourceTrace find the planted problems. SourceTrace adds what a plain model does not give: an evidence ID, page and quote behind every verdict, a verdict for every node and edge, fixed categories and risk levels, a machine-readable `audit.json`, and the same result on every run. On real content, the first run had too many false or mislabelled findings. After two rule revisions based on the owner's reviews, 85 of 88 judged items on a new article were right, 1 was partly right and 2 were wrong. Since v0.2.0, a 169-item tree and degraded images caused no loss, and on two more articles the item verdicts matched the answer keys. The main remaining gap is problems in the source that take a short derivation to see.

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

## Since v0.2.0

Three more rule revisions (the fourth to the sixth) and two sets of rule fixes followed v0.2.0, each driven by the test before it. Every test below has a `RESULTS.md` (or `COMPARISON.md`) with the details.

### Setup

| Test set | Tests | Source | Pages | Tree | Answer key |
|----------|-------|--------|-------|------|------------|
| [sl-algos-zh](../tests/fixtures/sl-algos-zh/) | scale | synthetic lecture | 32 | 78 nodes, 91 edges, from the developer; 27 planted item problems, 8 planted omissions | planted, revised by the owner after the runs |
| [model-eval-scan](../tests/fixtures/model-eval-scan/), [-photo](../tests/fixtures/model-eval-photo/), [-occluded](../tests/fixtures/model-eval-occluded/) | image quality | the model-eval slides, degraded by `tools/degrade_images.py` | 8 | 19 nodes, 18 edges (model-eval) | the model-eval key, revised by the owner after the runs |
| [wiki-nb-zh](../tests/fixtures/wiki-nb-zh/) | a fresh article | Chinese Wikipedia, 朴素贝叶斯分类器 (CC BY-SA 4.0) | 10 | 35 nodes, 52 edges, from ChatGPT (GPT-6.1 Sol) | a ChatGPT review in the conversation that made the tree, accepted by the owner |
| [wiki-pc-zh](../tests/fixtures/wiki-pc-zh/) | a fresh article with figures as evidence | Chinese Wikipedia, 感知器 (CC BY-SA 4.0) | 6 | 35 nodes, 48 edges, from Codex (GPT-6.1 Sol) | a Codex (GPT-6.1 Sol, high) review in a separate session, accepted by the owner |

Runs were set up as before: a fresh agent with its own copy of the skill and the inputs, and no web access. The two Codex runs were started by the owner in a clean folder outside the repository.

### Results

| Test | Rules | Agent, runs | Result | Cost per run |
|------|-------|-------------|--------|--------------|
| [sl-algos-zh](../tests/fixtures/sl-algos-zh/RESULTS.md) | third revision (v0.2.0) | Claude, 2 | Against the revised key: 28/28 item findings, 8/8 omissions, no correct item flagged. Same verdict, category and risk on all 169 items. | ~162–174k tokens, 7–8 min |
| [model-eval-scan, -photo](../tests/fixtures/model-eval-occluded/RESULTS.md) | fourth revision | Claude, 2 each | 11/11 item findings, 4/4 omissions, all evidence read with `high` certainty | ~92–93k tokens, 3 min |
| [model-eval-occluded](../tests/fixtures/model-eval-occluded/RESULTS.md) | fourth revision | Claude, 2 | 11/11 and 4/4 against the revised key. Hidden text was marked `low` and never filled in. | ~96–98k tokens, 4 min |
| [wiki-ml-zh, Codex](../tests/fixtures/wiki-ml-zh/codex-run-1/COMPARISON.md) | third revision (v0.2.0) | Codex (model not recorded), 1 | 15 of the 18 items the owner judged, the same score as Claude run 2 on different items. 44 omissions where Claude reported 25, mostly one per name in a list; not judged. | ~15 min |
| [wiki-nb-zh, runs 1–2](../tests/fixtures/wiki-nb-zh/RESULTS.md) | fourth revision and fixes | Claude, 2 | No conceptual or relationship error, and none missed. The runs agree on 85 of 87 items; run 2 has two wrong source notes and misses one low omission. | ~132–145k tokens, 8–9 min |
| [wiki-nb-zh, runs 3–4](../tests/fixtures/wiki-nb-zh/RESULTS.md#re-run-with-the-fifth-revision-2026-11-07) | fifth revision | Claude, 2 | 87/87 items and 11/11 omission groups. Some of the revision's examples come from this article. | ~145–166k tokens, 11–13 min |
| [wiki-pc-zh, runs 1–2](../tests/fixtures/wiki-pc-zh/RESULTS.md) | fifth revision | Claude, 2 | Both real tree errors found (N029's fix only partly right), none of the 81 supported items overturned, same verdicts on all 83 items. 9 and 10 of 10 omission groups. Missed all 4 source problems that take a derivation, and the b = 0 omission. | ~143–145k tokens, 9 min |
| [wiki-pc-zh, Codex](../tests/fixtures/wiki-pc-zh/codex-run-1/COMPARISON.md) | sixth revision | Codex (GPT-6.1 Sol, high), 1 | Same verdicts as the Claude runs on all 83 items, with N029's fix now as the review asks. 2 of 4 source problems found, and the b = 0 omission. Two omissions in the wrong tier (core instead of supporting). | ~16.5 min |

Every script run in these tests passed. Where an agent ran a script twice, it was to apply its own edits, not to fix an error. The Codex run on wiki-pc-zh was graded by Claude against the review; of its omissions, the owner judged only the two tier differences.

### What the revisions changed

| Revision | Prompted by | Main changes |
|----------|-------------|--------------|
| Fourth (`fb2bbc2`) | sl-algos-zh | The label test comes before `ambiguous`; a slide title does not define a class; slide order supports no relationship; a finding covers only its own content |
| Fixes (`9b74d78`) | image test | `related-to` rule narrowed; partly unreadable evidence split into a readable and a `low` item; working files in `work/` |
| Fifth (`80616a0`, `1dbd02b`) | wiki-nb-zh | Judge the concept, not the label's word; web pages and screenshots; formulas; problems in the source itself; background omissions; recommendations checked like findings; notes on supported items shown in the report |
| Sixth (`ae1084e`) | wiki-pc-zh, wiki-nb-zh re-runs | Check a source claim against the source's own formulas; possible slips; one tie-break for overlapping screenshots; one omission entry per node or topic; wrong range end points; `contrasts-with` from two conventions |
| Rule line after the Codex run | wiki-pc-zh Codex run | A method named only in a history passage is background |

## What this shows, and what it doesn't

**Shows:**
- On these two test sets, a plain model already detects the planted errors. SourceTrace's value is not better detection.
- SourceTrace's value is a result that can be **checked and repeated**: every verdict cites evidence, every item gets a verdict, the categories and risks are fixed, and four independent runs produced the same audit.
- It also keeps reports focused. The rules for what counts as an omission removed all the noise the baseline produced.

- On real content, the owner's reviews found real rule problems. The first revision, re-run on the same article, fixed most of the cases it targeted: 12 of the 13 reviewed findings then matched the review. The second article, which played no part in the first two revisions, had no high-risk false finding and no supported item that the owner rejected.
- Since v0.2.0: a 169-item tree and moderately degraded images did not reduce accuracy or agreement, and hidden text was never guessed. On two fresh articles the runs agreed on almost every item and matched the keys. Codex followed the skill without help, twice.

**Does not show:**
- **The latest rules on new material.** The sixth revision ran once, by Codex, on wiki-pc-zh, the article several of its examples come from. The rule line after that run has not been run. No article that played no part in the sixth revision has been tested.
- **Independent grading.** One owner judged or accepted every key. The keys of wiki-nb-zh and wiki-pc-zh are AI reviews: the first from the conversation that made the tree, the second from the same model that made the tree and ran the Codex audit. The omissions of the wiki-ml-zh runs were not judged. On the synthetic sets, the developer wrote both the rules and the answer keys, and the agents that ran the skill use the same model family that helped write it. Agreement *between runs* does not depend on the keys, and is the stronger result.
- **Problems in the source that need reasoning.** With the sixth revision, zero-boundary checks are found. A problem that needs combining sections (0/1 labels against a margin condition) or a scaling argument was still missed.
- **Scale on real decks.** The large test is one synthetic 32-slide deck with 169 items. Real content goes up to 12 pages and 98 items.
- **Real image quality.** The degraded images are scripted versions of one clean 8-slide deck with typed text. Real photos, handwriting and heavy blur are untested.
- **Other agents and languages.** Codex ran twice, on two different rule versions, so its results can't be separated from the rule changes. No other Agent Skills tool was tested. All real content is Chinese; English was tested only on the 4-slide synthetic set.
- **Sample size.** 2 baseline runs and 1–4 skill runs per synthetic test set; 1–2 runs per real-content test set and rule version. No baseline was run on real content.

## Next steps

Test data must be openly licensed, written by the project owner, or synthetic. No third-party course material is used.

1. **Release v0.3.0.**
2. **A fresh article for the sixth revision:** one that played no part in any rule, ideally in English or another field, with an answer key from a model other than the tree's.
3. **Independent grading:** a reviewer other than the owner, or keys from a different model than the agent's.
4. **Real images:** photos or scans of openly licensed or owner-written slides.
5. **Task modes:** a strict source-tracing mode and a review mode that allows short, marked explanations from outside the source.

## Reproducing

```bash
pip install -r requirements.txt
python -m pytest                      # 120 tests, including the saved-run checks
python -I tools/compare_runs.py . model-eval tests/consistency/model-eval/day6/run-1 tests/consistency/model-eval/day6/run-2 tests/consistency/model-eval/day6/run-3 tests/smoke/model-eval-e2e
```
