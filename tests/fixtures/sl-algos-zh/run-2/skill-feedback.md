# Skill feedback: SourceTrace run on sl-algos (32 slides, 78 nodes, 91 edges)

## 1. Script runs

| Script | Runs | Result |
|---|---|---|
| `validate_input.py --json` | 1 | Valid, no errors, no warnings. |
| `validate_evidence.py` | 1 | Valid on the first run (32 sources, 170 items: 127 text, 24 table, 19 graphic). |
| `build_report.py` | 2 | Both runs succeeded. The second was not a fix for an error: I shortened one omission's recommendation (I had suggested an edge `N001 related-to <new node>` for "没有一种算法在所有问题上都是最优的", and on review that edge was my own invention, so I removed it) and rebuilt. |

No run failed, so there were no errors to fix.

I also used small helper files of my own in `sl-run-2/work/` (not part of the skill): `ev.tsv` (one line per evidence item, appended slide by slide), `build_index.py` (turns it into `evidence-index.json`), and `audit_nodes.py`, `audit_edges.py`, `omissions.py`, `combine.py` (write `audit.json`).

## 2. Unclear places, and what I did

1. **Splitting bullets.** `evidence-extraction.md`: "split a bullet only if it states two unrelated facts". Several bullets state two *related* facts that the tree splits between different nodes, e.g. slide 31 "kNN 不构建显式模型；朴素贝叶斯依赖条件独立假设", slide 26 "特征缩放对 kNN、SVM … 尤其重要；决策树 … 不需要特征缩放", slide 7 "Sigmoid … 映射到 (0, 1) 区间，输出可解释为样本属于正类的概率", slide 24 "高偏差通常对应欠拟合，高方差通常对应过拟合". "Unrelated" is a vague test. I split wherever the two halves would be cited by different nodes or edges, so each ID points at one claim. A rule like "split when the two halves could be cited separately" would be easier to apply.

2. **A slide titled with a class that describes only one member.** Slide 22 is titled "神经网络" but its text says "多层感知机由输入层、一个或多个隐藏层和输出层组成，层与层之间全连接". N048 神经网络 copies this as a general definition. The rule "A class defined from a single instance: when the source never defines a general class and only explains one member of it" fits, but it is unclear whether a slide title makes that member *the* definition of the class. I applied the rule and made it an `unsupported-expansion` with scope `detail`, low risk (F-027). Another run could reasonably call it `supported`.

3. **Relationships suggested only by where a slide sits.** Slide 16 "核方法" comes right after slide 15 SVM but never mentions SVM. The paragraph rule needs "the same paragraph", and "Two terms that only appear in the same section or paragraph support no relationship". So E044 支持向量机 uses 核函数 became `unsupported-expansion` (whole, medium, F-017), even though the deck's ordering suggests that is what it means. The rules say nothing about a sub-topic slide inside an algorithm's section. If that should count, it needs its own rule. If it should not, a sentence saying so would stop runs from disagreeing.

4. **Spelled-out label vs. "only names the term".** 随机搜索 (N078: "在超参数空间中随机采样若干组超参数进行评估") and GELU (N054: "基于高斯分布累积分布函数的平滑激活函数") are both only named in the source. I called N078 `supported`, because its definition just spells out "random search" over hyperparameters and slide 29 says it replaces grid search. I called N054 `ambiguous`, because "高斯 CDF、平滑" can be false while the name stays true. The "could this part be false while the rest is true?" test settled it, but that test sits in the Verdicts section, while question 7 (ambiguous) does not refer back to it. A cross-reference from question 7 would help.

5. **`is-a` from a method to a task node.** E011 线性回归 is-a 回归 and E012 逻辑回归 is-a 分类 link a method to a task. Since `kind` is not audited, I judged them only on the claims: the source says "最基本的回归方法" and "用于二分类的方法". I marked both `supported`. The rules do not say whether `is-a` between a method and a task should be read as "is a method for".

6. **Absolute claims that the source contradicts outright.** N065 "所有机器学习算法在训练前都必须进行特征缩放" is contradicted twice, on slide 26 and on slide 30 ("常见误区"). Question 4 says it is still `overgeneralization` ("This holds even when another page contradicts the absolute version"), and I followed that with default medium risk. I thought about raising the risk because the deck itself lists this as a common mistake. But the rules give no example of a reason that justifies raising it, so I kept the default.

7. **Whether an omission is "already covered" depends on what I chose to cite.** The rule is "do not report … when the … node already has a finding that cites it". EV-166 ("没有一种算法在所有问题上都是最优的") could support the SVM overgeneralization (N032). If I cite it there, the general lesson disappears from omissions. If I don't, it is reported. I left it out of N032 and reported it as a core omission, because it is a deck-level conclusion, not a fact about SVM. A rule saying a finding covers only the content it is *about* would remove the circularity.

8. **Agenda topics with no grouping node.** Slide 1 lists "评估指标、模型选择" as topics. The tree has their members (MSE, 精确率, 交叉验证, 网格搜索 …) but no node for either topic. The core tier says "A topic in a slide title or an agenda/overview slide". I did not report these, because the content is covered. The rules don't say whether a missing *grouping* node counts as an omission.

9. **Relations the schema cannot express.** ReLU "可缓解梯度消失" (E068 says `causes`) and "集成学习/神经网络 可用于分类与回归" have no matching relation. For E068 I recommended deleting the edge, as SKILL.md says. For the omission I suggested `related-to` edges as the closest allowed value, or a sentence in the definition.

## 3. Input size

- **Context.** All 32 slide images go into context. I viewed them four at a time and transcribed each batch straight into `ev.tsv` before opening the next, so I never had to re-open a slide to recall its text. The exact-word findings (0,1 vs −1,1; 奇数 vs 偶数; 有放回; 信息增益率; 偏差; 标准化/归一化; 可缓解; 大多数; 通常) were all transcribed from the image as I read it, and the `reason` fields quote that transcription.
- **Keeping track of items.** 170 evidence items and 169 tree items are too many to hold in mind. I printed a one-line-per-item list (`work/ev-list.txt`: ID, page, content) and used it as the lookup table for stage 4. I wrote the verdicts as three separate files (78 nodes, 91 edges, 11 omissions). Each file was printed with a count, so that a missing or duplicate verdict would show before `build_report.py` ran.
- **Omission pass.** The source → tree pass was the step most at risk of slips at this size. I went through the evidence list once more, top to bottom, and noted for every item whether it was covered by a node, an edge or a finding, was not knowledge, or was a gap.
- The skill's advice to work page by page and write to files as I went was enough. Nothing failed because of size.
