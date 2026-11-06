# Skill feedback (img-scan-1 run)

## 1. Script runs

| Script | Runs | Failed runs |
|--------|------|-------------|
| `validate_input.py` | 1 | 0 (valid; one warning `DISCONNECTED_TREE`, passed through to the report) |
| `validate_evidence.py` | 1 | 0 (40 items: 34 text, 4 table, 2 graphic) |
| `build_report.py` | 1 | 0 |

I also ran `build_report.py --help` once to confirm the argument names; that is not a real run.

## 2. Unclear or missing instructions

Mostly clear. Places where I had to make a call:

- **Replacing a wrong `related-to` edge.** SKILL.md says: "If no allowed relation expresses the correct relationship ... recommend deleting the edge and stating the relationship in a node's definition. Do not fall back on `related-to`, which loses the direction." E010 (过拟合 related-to 高偏差) and E011 (欠拟合 related-to 高方差) point at the wrong target. The slide 4 diagram shows unlabelled arrows 过拟合 → 高方差 and 欠拟合 → 高偏差. No more specific relation is stated (`causes` would be my own claim). I recommended replacing them with `related-to` to the correct target. The tree already used `related-to`, so no direction is lost. The rule reads as if it is about edges whose relation had a direction to begin with ("ReLU 可缓解梯度消失"), but it does not say so. A sentence on "the source shows an unlabelled association and the tree already uses related-to" would remove the guess.
- **Does a slide title plus its bullets support `includes`?** The agenda rule covers "lecture subject includes listed topic". It does not say whether a slide titled 数据集划分 that lists 训练集/验证集/测试集 (plus "划分比例：训练集 : 验证集 : 测试集") supports 数据集划分 includes 训练集. The same question applies to the 分类评价指标 table rows (E007–E009). I treated both as supported: the slide's text states the split into those three sets, and the table lists the metrics under that title. Two runs could disagree here.
- **Edge E016 (k 折交叉验证 uses 测试集): contradiction (Q2) or unstated (Q3)?** The source says k-fold splits the *training* data, and that the test set "不可用于调参". I read that as ruling out the link, so I chose `incorrect-relationship`. A stricter reading could call it merely unstated (`unsupported-expansion`).
- **Omission vs. finding coverage for L2 "使权重整体变小".** That clause is not in N012. The N012 finding cites the whole bullet (EV-026), and its recommended wording restores the clause, so I did not report a separate omission. The rule "A finding covers only the content it is about" leaves room to report it separately as a supporting detail.

## 3. Image difficulties

All 8 JPGs look like scans or photos of printed slides: grey speckle noise over the whole page, slightly tilted title bars (slides 4 and 8), and a low-contrast background. None of it hid any text. Every character, including the numbers that decide findings (7 : 2 : 1, "一般不产生稀疏解", "通常"), was legible at the given resolution. I read each image once at full resolution and did not zoom in or re-open any of them. So all evidence is `high` certainty. The only non-text evidence is the two diagram arrows on slide 4, and their direction was unambiguous.
