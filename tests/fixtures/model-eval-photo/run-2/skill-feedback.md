# Skill feedback: SourceTrace run on 模型评估与泛化 (8 photographed slides)

## 1. Script runs

| Script | Runs | Result |
|--------|------|--------|
| `scripts/validate_input.py --json` | 1 | Valid. One warning, `DISCONNECTED_TREE` (3 parts), passed through to the report's structure section. |
| `scripts/validate_evidence.py` | 1 | Valid on the first run: 8 sources, 39 items (33 text, 4 table, 2 graphic). |
| `scripts/build_report.py` | 1 | Succeeded on the first run: 26 supported, 11 findings, 5 omissions. |

No run failed, so nothing had to be changed.

## 2. Unclear or conflicting instructions

1. **Replacing a swapped `related-to` edge.** SKILL.md says: "Do not fall back on `related-to`, which loses the direction." E010 (过拟合 related-to 高偏差) and E011 (欠拟合 related-to 高方差) only have the wrong target. The slide arrow (欠拟合 → 高偏差, 过拟合 → 高方差) has no label, and no allowed relation says "corresponds to" (`causes` would be wrong: high bias causes underfitting, not the other way round). I recommended keeping the tree's own `related-to` and changing only the target. I read the rule as being about choosing a new relation, not about keeping the one the tree already has, but it does not say so. The alternative it offers ("delete the edge and state the relationship in a node's definition") would have thrown away a relationship the slide states plainly.

2. **One evidence item with two separate points, one of them in a finding.** EV-025 is "L2 正则化：惩罚权重平方和，使权重整体变小，但一般不产生稀疏解。" The N012 finding is about 稀疏解 and cites EV-025. audit-rules.md says both "check that the content is not already covered by a finding … that cites it" and "A finding covers only the content it is about … a separate point stays an omission". Going only by citations, "使权重整体变小" would count as covered. Going by content, it is a separate point. I followed the second rule and reported it as a supporting omission (F-014). The extraction rules did not have me split the bullet, because only one tree item cites it. A note saying "cited" means the clause and not the whole item would settle this.

3. **"Uses the test set" versus "uses the validation set" for k-fold (E016).** No slide literally says "k-fold does not use the test set". I took it as a contradiction (question 2, `incorrect-relationship`) and not as unstated (question 3). Page 6 says the folds come from "训练数据" and are used "做验证". Pages 2 and 8 say the test set is used "仅在最后" and "只能…使用一次", which rules out reusing it in k rounds. That is the "combine pages" reading. A stricter reader could call it `unsupported-expansion`. The rules don't say how strong an implied contradiction has to be.

4. **Recommended replacement after deleting E016.** The source does not say "k 折交叉验证 uses 验证集": it says the fold is used "做验证" and that the method suits cases where "单独划分验证集代价较高". So I recommended deleting the edge with no replacement, as SKILL.md asks ("Do not invent a replacement the source does not state").

Everything else (output location, path format, decision order, the agenda rule for E001/E006/E018, the qualifier test for 准确率 and 过拟合, the omission tiers) was clear and fit this deck directly.

## 3. Image issues

- The slides are photos of a projected or displayed screen. They have a keystone/perspective skew (each slide is a tilted trapezoid), a dark border, vignetting, a warm yellow cast, and slightly soft text, especially toward the right and bottom edges.
- Despite this, all text stayed legible at the given resolution. I marked every item `high` certainty and needed no `low`/`medium` items.
- As the rules ask, I looked again at every finding that depends on an exact word or number before writing it: "7 : 2 : 1" (p.2), "不可用于调参" (p.2), "通常" (p.3), the direction and pairing of both arrows (p.4), "一般不产生稀疏解" (p.5), the 精确率/召回率 rows (p.7) and "只能…使用一次" (p.8).
- Small transcription choices: I kept the minus sign in "k−1" as shown. I separated the TP/FP/FN/TN legend on p.7 with spaces, because the slide uses wide gaps and not punctuation.
