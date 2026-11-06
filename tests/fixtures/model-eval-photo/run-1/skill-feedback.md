# Skill feedback (img-photo-1 run)

## 1. Script runs

| Script | Runs | Result |
|--------|------|--------|
| `validate_input.py --json` | 1 | Valid; one warning `DISCONNECTED_TREE` (3 parts). |
| `validate_evidence.py` | 1 | VALID: 8 sources, 39 evidence items (2 graphic, 4 table, 33 text). |
| `build_report.py` | 1 | Written (zh). Supported 26, findings 11, omissions 5. |

No run failed, so nothing had to be changed.

## 2. Unclear or guessed points

- **Replacement relation for the swapped bias/variance edges (E010, E011).** SKILL.md says: "If no allowed relation expresses the correct relationship ... recommend deleting the edge and stating the relationship in a node's definition. Do not fall back on `related-to`, which loses the direction." It also says: "if the source shows the correct relationship, recommend replacing it and give the new `source`, `relation` and `target`." The slide's arrows (过拟合 → 高方差, 欠拟合 → 高偏差) carry no label, so the source states a correspondence but not `causes` or any other specific relation. I recommended replacing the edges with the corrected target and kept the tree's own `related-to`, because an unlabeled arrow gives no ground for a more specific relation, and the "do not fall back" sentence seemed aimed at relationships that do have a specific meaning (like "mitigates"). A rule for unlabeled diagram arrows would remove the guess.
- **Is a property in the same bullet as a contradiction covered by that finding?** EV-025 ("L2 正则化：惩罚权重平方和，使权重整体变小，但一般不产生稀疏解") is the evidence for the N012 conceptual error (sparsity), and also contains "使权重整体变小", which the tree lacks. audit-rules.md says "A finding covers only the content it is about ... Content that is a separate point stays an omission". I followed that: N012's recommendation only fixes the sparsity clause, and "使权重整体变小" is a separate supporting omission. For N017, by contrast, I treated the remedy part of EV-037 ("应结合精确率和召回率一起判断") as covered by the accuracy overgeneralization finding, because it is the same sentence that refutes "最可靠" and the recommendation quotes it. The boundary between these two cases was a judgment call.
- **E016 (k 折交叉验证 uses 测试集): contradiction or merely unstated?** Question 2 vs 3 in the decision order. The slide says CV splits the *training* data; it never says "CV does not use the test set". I judged it a contradiction (incorrect-relationship) by combining page 6 with pages 2 and 8 ("不可用于调参", "只能在最终评估时使用一次"). A stricter reader might call it unsupported-expansion. An example for "contradicted only by combining a usage rule on another page" would help.
- **Agenda rule with a compound lecture title.** The agenda rule supports `includes` "from the lecture's subject". The title is "模型评估与泛化：课程概览" while the tree's node is 模型评估. I treated 模型评估 as the lecture's subject (E001, E006, E018 supported). This seemed clearly intended but is not spelled out.
- Everything else (evidence granularity, qualifier test, risk defaults, omission tiers) was clear; several tree errors matched the reference examples almost word for word (8:1:1 vs 7:2:1, 不产生 vs 产生 稀疏解, precision given recall's definition, 总是由训练数据过少导致, 最可靠的指标, test set used once).

## 3. Image conditions

All eight images are photographs of a projected or displayed slide: the slide is shot at a slight angle (keystone/perspective distortion), surrounded by a dark border, with uneven lighting (a vignette and a bright patch in the lower right) and some softness. All text, the page-4 diagram and the page-7 table were still fully legible, so every evidence item is `high` certainty. I re-checked the exact numbers and negations the findings hinge on (7 : 2 : 1, "一般不产生稀疏解", "通常", "不可用于调参", the precision/recall row meanings, and the arrow directions on page 4) against the images before writing the findings. The only minor transcription choice was the minus sign in "k−1" on page 6, which I copied as a Unicode minus.
