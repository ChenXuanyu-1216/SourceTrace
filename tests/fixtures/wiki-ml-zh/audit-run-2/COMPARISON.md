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

The new `detail` scope is now used 10 times. In four of those (N006, N008, N024, N030), run 1 had marked the item supported. Each one names a real phrase that is absent from the source, but some may be stricter than a learner needs. These are the items to look at first to decide whether `detail` adds noise.

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
| — | N027 集成学习 | supported | 错 | [Certain] 第 9 页只明确解释随机森林这一实例如何组合多树预测，第 6 页另列 AdaBoost；没有新增证据足以把实例说明直接等同于类别的一般定义。维持 run 1 对“存在较弱资料缺口”的判断，不应仅因新决策顺序未覆盖就默认 supported。[Likely] 按新分类宜为 unsupported-expansion · 细节 / 低：组合预测和改善准确性有实例依据，把它推广为整个类别的定义则需标明是概括；旧 ambiguous 标签不必固守。不是判该定义在学术上错误。 |
| F-009 | N033 正则化 | unsupported-expansion · 细节 / 低 | 对 | [Certain] 第 10 页支持减轻过拟合及岭回归例子；结合第 4 页模型复杂度的说明，可支持控制复杂度的概括，但未说明“约束模型参数或增加惩罚项”。新 Q6 比旧 Q6 更准确地区分了部分支持与完全未定义；这是分类规则变更后的合理修正，应更新旧审查的类别预期。保留低风险及原定义，只标记机制的资料来源缺口；不应强制补写“减轻偏差”。 |
| F-016 | N039 贝叶斯优化 | unsupported-expansion · 细节 / 低 | 对 | [Certain] 第 12 页明确高斯过程可在贝叶斯优化中作为代理模型，但没有说明“利用不确定性来选择评估点”。用途和代理模型已有支持、选择机制未出现，符合新 Q6 的 detail / low；旧审查已指出同一缺口，类别应随新规则调整。[Likely] 这类提示比单纯要求字面一致更有价值，因为它定位了独立的优化机制；只需标注来源范围，不必改写为必须使用高斯过程。 |
| F-002 | E004 计算学习理论 —uses→ 偏差与方差分解 | unsupported-expansion / 中 | 错 | [Certain] 第 4 页不是仅把两个术语列在同一节：同一论述段先界定计算学习理论对算法及性能的分析，再说明概率性能界限，最后明确偏差与方差分解“是一种用于量化泛化误差的方法”。[Likely] 研究领域 uses 该段介绍的误差分析方法，是这段功能关系的合理概括，没有因关系词未逐字出现而删边的必要。此结论依赖段内的方法用途，不意味着任意同节术语都支持 uses；建议保留原边，N006 related-to N004 可另加，不能作为必须替换的理由。 |
| F-007 | N006 偏差与方差分解 | unsupported-expansion · 细节 / 低 | 部分对 | [Certain] 第 4 页仅说量化泛化误差，没有解释“系统性偏离”及“对训练数据的敏感程度”；这两项不只是把“分解”换个说法，作为机制的 detail / low 来源提示有价值。但“预测误差”并未断言排除泛化误差，不能因术语更宽就一并当成无依据机制；应只对机制报 detail / low，把“泛化误差”作为可选的精确措辞建议。报告示例又写成“把误差分为……两部分”，引入原节点没有的穷尽性表述，应删去“两部分”，保留原来的“区分……来分析”。 |
| F-008 | N008 过拟合 | unsupported-expansion · 细节 / 低 | 错 | [Certain] 第 4 页结合训练数据、训练误差、模型复杂度与未见样本表现讨论过拟合，原定义也没有否认复杂度过高这一原因。[Likely] “过度适应训练数据的细节”在这里是对过拟合现象的直观释义，未增加具体算法、数值条件或排他原因；把它另列为机制扩展，超出了合理改写应承受的审查粒度。建议 supported，可选补充复杂度背景；不必给这一术语释义加资料外警告。此项主要增加复习干扰。 |
| F-011 | N024 深度学习 | unsupported-expansion · 细节 / 低 | 对 | [Certain] 第 7～8 页支持神经网络通过学习完成任务、多层结构及逐层信号变换，但没有说明“学习数据表示”；逐层变换本身也不等于明确讲授表示学习。按严格资料溯源，新 Q6 的 detail / low 成立。[Likely] 对补充了哪一项学习目标的追踪有有限价值，但复习时优先级低，应保留定义并作可展开的来源提示；不要强制换成资料中模拟光和声音的目标描述。 |
| F-014 | N030 核技巧 | unsupported-expansion · 细节 / 低 | 对 | [Certain] 第 10 页支持隐式映射到高维特征空间以处理非线性关系，却没有解释“通过核函数……计算……相似性”。第 12 页虽出现“核函数”，其语境是高斯过程的协方差函数，不能直接充当核技巧中相似性计算的证据。新增的是具体计算机制，detail / low 合适；在四个新增条目中，这类可定位机制的来源提示较有价值。保留定义并标记该片段即可，未在资料出现不等于已证明知识错误。 |

[Certain] 本轮仅填写上述 8 行：对 4 项、部分对 1 项、错 3 项。“对”认可严格资料溯源下的分类和低风险，不表示知识树的相关定义在学术上错误；本轮未使用外部材料补充截图证据，也未评估其余发现和遗漏。

[Likely] `detail` 有实际价值，但应增加两道边界：先排除术语的直观释义及段内已支持的功能关系，再逐片段定位独立机制、条件或性质。对复习任务，把低风险来源提示折叠展示，不应与需要纠正的知识错误同等突出。四个新增节点中，N006 的机制片段、N024、N030 可保留来源提示，N008 应撤回；N006 关于“预测误差”的提醒只宜作为措辞建议。此结果不能外推为整个类别已验证有效，还需要其他测试集检查其误报率与修改价值。
