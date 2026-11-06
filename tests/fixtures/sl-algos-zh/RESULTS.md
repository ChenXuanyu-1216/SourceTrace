# Scale test results (2026-11-06)

Two fresh Claude agents ran SourceTrace v0.2.0 on this test set, each in an isolated folder with only the skill, `images/` and `knowledge-tree.json`, and no web access. Their outputs are saved unedited in [run-1/](run-1/) and [run-2/](run-2/), each with the agent's `skill-feedback.md`.

## Summary

| | Run 1 | Run 2 |
|---|---|---|
| Scripts | all passed on the first run | all passed on the first run (`build_report.py` re-run once after editing a recommendation) |
| Evidence items | 162 | 170 |
| Verdicts | 169 / 169 | 169 / 169 |
| Supported / problems / source notes | 141 / 24 / 4 | 141 / 24 / 4 |
| Omissions | 12 (8 core, 4 supporting) | 11 (8 core, 3 supporting) |
| Planted item problems found | 27 / 28 | 27 / 28 |
| Planted omissions found | 8 / 8 | 8 / 8 |
| Correct items flagged | 1 (N048) | 1 (N048) |
| Should-not-report items reported | 0 | 0 |
| Cost | about 174k tokens, 8 minutes | about 162k tokens, 7 minutes |

- **Agreement:** the two runs gave the same verdict, category and risk on all 169 items.
- **Size:** neither run reported trouble with the size. Both read the slides in batches of four, wrote evidence to a draft file after each batch, and used small scripts of their own to number evidence and merge verdicts. Problems on the last two slides (N017, N032) and the cross-slide errors were all found.
- **Cost:** about the same as the 12-page wiki-ml-zh runs (159k–203k tokens, 11–14 minutes), with 72% more items.

## A mistake in the answer key, found by both runs

E044 支持向量机 uses 核函数 was meant to be correct. But slide 16 (核方法) never mentions SVM, and slide 15 never mentions kernels. Under the rules, two terms on neighbouring slides support no relationship, so both runs reported it as `unsupported-expansion`. The deck is at fault, not the runs: the key now lists E044 as an expected finding marked `"planted": false`. This is why the key has 28 item findings instead of the 27 planted ones.

## For the owner to judge

These are the places where both runs differ from the key. In each, the runs' reading is defensible, so I have not changed the key.

1. **N078 随机搜索 (key: `ambiguous`; runs: supported).** The deck only says "超参数较多时，也可以使用随机搜索代替网格搜索". Both runs read the tree's definition, "在超参数空间中随机采样若干组超参数进行评估", as spelling out the name, not as a claim. They marked GELU (N054), which the deck also only names, as `ambiguous`, because "基于高斯分布累积分布函数" could be false while the name stays true.
2. **N048 神经网络 (key: correct; runs: source note).** Slide 22 is titled 神经网络, but its text describes 多层感知机. Both runs applied the single-instance rule (a class defined from one member is a detail). The key treated the slide title as defining the class.
3. **Laplace smoothing (key: supporting, low; runs: core, medium).** It is a note under the naive Bayes table on slide 12.
4. **Omissions the key did not expect** (all real gaps in the tree that I did not plan):
   - Slide 3: the grouping of algorithms by task, e.g. 集成学习 and 神经网络 under 分类与回归均可. Both runs, medium.
   - Slide 21: the 样本权重 row of the Bagging/Boosting table. Both runs, medium.
   - Slide 14: "决策树容易过拟合". Both runs, low.
   - Slide 23: Sigmoid "两端饱和". Run 1 only, low.

## Rule gaps the agents reported

Both `skill-feedback.md` files raise the same points:

- **Sub-topic slides:** whether a slide placed inside a method's section, like 核方法 after SVM, can support an edge to that method (E044).
- **Single-instance rule:** whether a slide title counts as defining the class (N048).
- **Spelled-out name vs. `ambiguous`:** question 7 does not refer to the "could this part be false" test that settled N078 and N054.
- **Splitting bullets:** "split only if two unrelated facts" is vague. Both runs split related clauses when different edges needed to cite them.
- **Omissions covered by a finding:** whether an omission is reported depends on what a finding chooses to cite (the closing line on slide 31).
- **Relations:** there is no relation for "mitigates" (ReLU 可缓解梯度消失, E068). Neither the relations nor the rules say how to read `is-a` from a method to a task (线性回归 is-a 回归).

Run 1 also suggested a script that lists, for each evidence item, the findings and verdicts that cite it, to make the omission pass faster. It also suggested a note on running scripts on a Chinese-locale Windows console (`PYTHONIOENCODING=utf-8`).
