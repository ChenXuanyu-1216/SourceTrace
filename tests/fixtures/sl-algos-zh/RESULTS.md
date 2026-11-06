# Scale test results (2026-11-06)

Two fresh Claude agents ran SourceTrace v0.2.0 on this test set, each in an isolated folder with only the skill, `images/` and `knowledge-tree.json`, and no web access. Their outputs are saved unedited in [run-1/](run-1/) and [run-2/](run-2/), each with the agent's `skill-feedback.md`.

Both runs covered all 169 items and matched 27 of the 28 expected item findings in the key used for grading, plus all 8 planted omissions. They also shared the same miss and the same finding on an item that key marked correct. Agreement between the runs therefore does not establish that their judgments are correct.

The owner then reviewed the disagreements and revised the key (see [Owner's decisions](#owners-decisions)). Against the revised key, both runs match 28 of 28 expected item findings and flag no correct items. That revision accepts the runs' reading in two places, so the revised score is not an independent measure either.

## Summary (key before the owner's decisions)

| | Run 1 | Run 2 |
|---|---|---|
| Skill scripts (agent-reported) | each succeeded once | input and evidence validators succeeded once; report builder succeeded twice, before and after a recommendation edit |
| Evidence items | 162 | 170 |
| Verdicts | 169 / 169 | 169 / 169 |
| Supported / whole-item findings / detail source notes | 141 / 24 / 4 | 141 / 24 / 4 |
| Omissions | 12 (8 core, 4 supporting) | 11 (8 core, 3 supporting) |
| Expected item findings matched (current key) | 27 / 28 | 27 / 28 |
| Planted item problems matched | 26 / 27 | 26 / 27 |
| Unplanted E044 matched | yes | yes |
| Planted omissions found | 8 / 8 | 8 / 8 |
| Items marked correct by the key but flagged | 1 (N048) | 1 (N048) |
| Should-not-report omission candidates matched | 0 / 10 | 0 / 10 |
| Omissions unmatched by the key | 4 | 3 |
| Reported cost | about 174k tokens, 8 minutes | about 162k tokens, 7 minutes |

- **Agreement:** the two runs gave the same verdict, category and risk on all 169 items.
- **Size:** neither agent reported a failure caused by input size. Both described reading slides in batches of four, saving evidence to draft files, and using their own helper scripts to number evidence and assemble verdicts. The saved audits cover every tree item, including findings supported by the last two slides (N017, N032). Two runs on one synthetic fixture do not establish reliable scaling to other decks.
- **Cost:** the reported token counts fall within the range of the earlier Claude wiki-ml-zh runs (159k–203k tokens), while reported elapsed times are shorter (7–8 versus 11–14 minutes). This fixture has 72% more tree items, but differs in content and format, so this is not a controlled efficiency comparison.

To reproduce the comparison from the repository root:

```bash
python -I tools/compare_runs.py . sl-algos-zh tests/fixtures/sl-algos-zh/run-1 tests/fixtures/sl-algos-zh/run-2
```

The comparison validates both evidence indexes, finds no missing item verdicts or unknown evidence references, and confirms the 169/169 agreement on verdict, category and risk. It reports N078 as missed, N048 as a false positive against the key, and a Laplace-smoothing risk mismatch in both runs. Its item count (labelled `planted items 27/28` at the time, now `expected items`) includes the unplanted E044. Omissions are matched by substrings in cited evidence or reasons; 8/8 means all key omissions matched, not that all omission judgments or severities were accepted. Script success during the original audits and cost figures are historical reports, not measurements made by this comparison.

## Answer-key correction after the runs

E044 支持向量机 uses 核函数 was originally meant to be correct. Slide 16 (核方法) never mentions SVM, and slide 15 never mentions kernels. Both runs treated the placement of these slides as insufficient evidence for the relationship and reported `unsupported-expansion`. The key was updated to include E044 with `"planted": false`, increasing the expected item findings from 27 to 28.

This is an evidence gap under that reading of the rules, rather than a claim that the SVM–kernel relationship is factually wrong. Both agents asked for clearer guidance on whether a sub-topic slide can inherit its parent method from deck structure. The reported score uses the corrected key, which incorporates a finding from these runs.

## Disagreements reviewed by the owner

These were the disagreements between both runs and the key. The agents' reasons are summarized here; matching judgments from two runs are not independent confirmation of those reasons. The owner's decisions follow in the next section.

1. **N078 随机搜索 (key: `ambiguous`; runs: supported).** The deck only says "超参数较多时，也可以使用随机搜索代替网格搜索". Both runs read the tree's definition, "在超参数空间中随机采样若干组超参数进行评估", as spelling out the name, not as a claim. They marked GELU (N054), which the deck also only names, as `ambiguous`, because "基于高斯分布累积分布函数" could be false while the name stays true.
2. **N048 神经网络 (key: correct; runs: source note).** Slide 22 is titled 神经网络, but its text describes 多层感知机. Both runs applied the single-instance rule (a class defined from one member is a detail). The key treated the slide title as defining the class.
3. **Laplace smoothing (key: supporting, low; runs: core, medium).** It is a note under the naive Bayes table on slide 12. Both audits omit a `risk_reason`, so the comparison flags the severity difference. The owner needs to decide the tier and risk, as well as whether an explanation is required for departing from the key.
4. **Additional omission candidates absent from the key.** These match source content, but their reportability and severity still need review under the coverage rules:
   - Slide 3: the grouping of algorithms by task, e.g. 集成学习 and 神经网络 under 分类与回归均可. Both runs, medium.
   - Slide 21: the 样本权重 row of the Bagging/Boosting table. Both runs, medium.
   - Slide 14: "决策树容易过拟合". Both runs, low.
   - Slide 23: Sigmoid "两端饱和". Run 1 only, low.

## Owner's decisions

Decided by the project owner on 2026-11-06, after this review:

1. **N078 随机搜索 is correct.** "在超参数空间中随机采样若干组超参数进行评估" could not be false while "随机搜索" is true, so it only explains the name. The key had it wrong. It moves to `correct_items`, with a note in `tricky_correct_items`. GELU (N054) stays `ambiguous`.
2. **N048 神经网络 is a source note** (`unsupported-expansion`, scope `detail`, low). "层与层之间全连接" describes 多层感知机, not neural networks in general. It is added to the key with `"planted": false`.
3. **Laplace smoothing stays supporting, low risk.** It is a one-line note under a table, and neither run gave a reason for raising it. Both runs keep a risk mismatch on this omission.
4. **All four extra omissions are acceptable** in either run's tier. They are real gaps in the tree that were not planted. They are listed in `acceptable_extra_findings` with a `match` string, and `compare_runs.py` now counts them as accepted instead of unmatched.

The revised key has 28 expected item findings: 26 planted problems (N078 is no longer one), plus E044 and N048, both unplanted. It has 141 correct items.

Regrading the saved runs against the revised key:

| | Run 1 | Run 2 |
|---|---|---|
| Expected item findings matched | 28 / 28 | 28 / 28 |
| Planted omissions found | 8 / 8 | 8 / 8 |
| Correct items flagged | 0 | 0 |
| Should-not-report omission candidates matched | 0 / 10 | 0 / 10 |
| Accepted extra omissions / unmatched omissions | 4 / 0 | 3 / 0 |
| Omission risk mismatches | 1 (Laplace smoothing) | 1 (Laplace smoothing) |

Future runs should be graded against this revised key.

## Rule gaps the agents reported

The following concerns appear in both [run-1/skill-feedback.md](run-1/skill-feedback.md) and [run-2/skill-feedback.md](run-2/skill-feedback.md). They are agent feedback, not adopted rule changes:

- **Sub-topic slides:** whether a slide placed inside a method's section, like 核方法 after SVM, can support an edge to that method (E044).
- **Single-instance rule:** whether a slide title counts as defining the class (N048).
- **Spelled-out name vs. `ambiguous`:** how question 7 interacts with the "could this part be false" test. Run 2 explicitly requested a cross-reference; both used the distinction to accept N078 while flagging N054.
- **Splitting bullets:** "split only if two unrelated facts" is vague. Both runs split related clauses when different edges needed to cite them.
- **Omissions covered by a finding:** whether an omission is reported depends on what a finding chooses to cite (the closing line on slide 31).
- **Relations:** the allowed relations cannot directly express "mitigates" (ReLU 可缓解梯度消失, E068). Run 1 suggested `related-to` or deletion; run 2 recommended deletion.

Run-specific concerns also matter:

- **Run 1:** whether a missing formula is an omission when a compatible definition is already present; how close the remaining wording must be to the source after removing an absolute qualifier (N019).
- **Run 2:** how to interpret `is-a` from a method to a task (E011, E012); when to raise risk for an absolute claim explicitly contradicted by the source (N065); whether a missing agenda grouping node is an omission when its members are covered.

Run 1 also suggested a per-evidence list of citing findings and verdicts to help with the omission pass, and a Windows console encoding note (`PYTHONIOENCODING=utf-8`). Its own helper encountered a `UnicodeEncodeError`; it reported no failures in the skill scripts.

The owner's decisions above settle the key. The rule gaps are still open: they could become a rule revision, which should be recorded before scoring future runs so their results stay comparable.
