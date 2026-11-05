# audit-run-2 compared with audit-run-1

Run 2 used the skill at commit `89d1e55`, which includes the rule changes from the owner's review of run 1 ([../audit-run-1/REVIEW.md](../audit-run-1/REVIEW.md)). Everything else was the same as in run 1: a fresh Claude agent with no web access, working on an isolated copy of the skill, the 12 images and the unchanged `knowledge-tree.json`.

| | Run 1 | Run 2 |
|---|---|---|
| Evidence items | 221 | 231 |
| Supported | 83 | 82 |
| Findings (nodes and edges) | 15 | 16 |
| Omissions | 25 (11 core, 14 supporting) | 25 (10 core, 15 supporting) |
| Risk: high / medium / low | 1 / 12 / 27 | 0 / 13 / 28 |
| Script runs that failed | 0 | 0 |
| Cost | ~203k tokens, 14 min | ~159k tokens, 11 min |

## The 13 findings the owner reviewed

10 of 13 now match the review.

| Run 1 | Item | Owner's review | Run 2 | Match |
|---|---|---|---|---|
| F-001 | N036 贝叶斯网络 | 错 (not a conceptual error) | supported | ✓ |
| F-005 | N016 聚类 | 错 (supported by the figure on page 5) | supported | ✓ |
| F-012 | N031 回归分析 | 错 (supported by combining pages 5, 9, 10 and 11) | supported | ✓ |
| F-008 | N012 半监督学习 | 部分对 → unsupported-expansion / detail / low | F-010 detail / low | ✓ |
| F-010 | N028 自助采样 | 部分对 → detail / low | F-012 detail / low | ✓ |
| F-011 | N029 支持向量机 | 部分对 → detail / low | F-013 detail / low | ✓ |
| F-014 | N034 逻辑回归 | 部分对 → detail / low | F-015 detail / low | ✓ |
| F-004 | N002 人工智能 | 对 (ambiguous / low) | F-004 ambiguous / low | ✓ |
| F-006 | N017 降维 | 对 (ambiguous / low) | F-005 ambiguous / low | ✓ |
| F-007 | N040 计算机视觉 | 对 (ambiguous / low) | F-006 ambiguous / low | ✓ |
| F-009 | N027 集成学习 | 对 (ambiguous / low, "较弱的证据缺口") | supported | ✗ |
| F-013 | N033 正则化 | 对 (ambiguous / low) | F-009 detail / low | ✗ |
| F-015 | N039 贝叶斯优化 | 对 (ambiguous / low) | F-016 detail / low | ✗ |

All three mismatches keep the same risk or lower it. In N033 and N039 only the category changed. The source states the purpose (正则化 reduces overfitting; 贝叶斯优化 uses a Gaussian-process surrogate), but not the mechanism. The new decision order therefore reaches question 6 (one added detail) before question 7 (only named). The owner's notes on these two items describe a missing mechanism ("定义机制缺少资料支持", "定义机制未在资料展开"), which is what `detail` means. So the review may need updating rather than the rules. N027 sits on a boundary that the rules do not cover: a general definition inferred from a single instance (see skill feedback point 5).

## Changes outside the reviewed items

| Run 2 | Item | Run 1 | Run 2 |
|---|---|---|---|
| F-002 | E004 计算学习理论 —uses→ 偏差与方差分解 | supported | unsupported-expansion / medium |
| F-007 | N006 偏差与方差分解 | supported | detail / low: mechanism not in the source; the source says "泛化误差", not "预测误差" |
| F-008 | N008 过拟合 | supported | detail / low: the source gives "假设的复杂度过高" as the cause, not "过度适应训练数据的细节" |
| F-011 | N024 深度学习 | supported | detail / low: "学习数据表示" not in the source |
| F-014 | N030 核技巧 | supported | detail / low: "通过核函数计算相似性" not in the source |

E020 and E056 (unreviewed) are unsupported-expansion / medium in both runs.

The new `detail` scope is now used 9 times. In four of those (N006, N008, N024, N030), run 1 had marked the item supported. Each one names a real phrase that is absent from the source, but some may be stricter than a learner needs. These are the items to look at first to decide whether `detail` adds noise.

Omissions were not compared item by item: the two runs numbered their evidence differently (221 and 231 items).

## Points from the agent's skill feedback

The agent made 9 guesses, most because the input is a web page, not slides (full text in [skill-feedback.md](skill-feedback.md)):

1. **Overlapping screenshots:** the same sentence appears on two images. The agent extracted it once.
2. **Prose:** one evidence item per paragraph or per sentence? The agent used one per sentence.
3. **Wikipedia sidebars and navigation:** does a sidebar count as an overview of core topics?
4. **Edges that only the section structure supports,** but with a relation other than `includes` (E004).
5. **A general definition inferred from a single instance** (N027).
6. **A node label that paraphrases the source's term:** is the term "absent" for question 1?
7. **Question 6 versus 7** when the source gives only a position ("介于监督学习与无监督学习之间").
8. **Examples in running text,** not in parentheses.
9. **A paraphrased cause** (欠拟合 supported, 过拟合 flagged).

## Review sheet

Judge only the 8 items whose result differs from the review or from run 1. Use 对 / 部分对 / 错 / 不确定, as in run 1.

| Run 2 | Item | Run 2 result | Judgment | Notes |
|---|---|---|---|---|
| — | N027 集成学习 | supported | | |
| F-009 | N033 正则化 | unsupported-expansion · 细节 / 低 | | |
| F-016 | N039 贝叶斯优化 | unsupported-expansion · 细节 / 低 | | |
| F-002 | E004 计算学习理论 —uses→ 偏差与方差分解 | unsupported-expansion / 中 | | |
| F-007 | N006 偏差与方差分解 | unsupported-expansion · 细节 / 低 | | |
| F-008 | N008 过拟合 | unsupported-expansion · 细节 / 低 | | |
| F-011 | N024 深度学习 | unsupported-expansion · 细节 / 低 | | |
| F-014 | N030 核技巧 | unsupported-expansion · 细节 / 低 | | |
