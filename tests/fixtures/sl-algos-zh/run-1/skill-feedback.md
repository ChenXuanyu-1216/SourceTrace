# Skill feedback: sl-run-1 (32 slides, 78 nodes, 91 edges)

## 1. Script runs

| Script | Runs | Result |
|---|---|---|
| `validate_input.py --json` | 1 | valid, no errors, no warnings |
| `validate_evidence.py` | 1 | VALID: 32 sources, 162 evidence items (14 graphic, 24 table, 124 text) |
| `build_report.py` | 1 | WRITTEN on the first run: supported 141, findings 28, omissions 12 |

No script run failed. The one failure was in my own helper, not a skill script. A Python one-liner I used to print the tree hit `UnicodeEncodeError: 'gbk' codec can't encode character '−'` because the Windows console uses GBK. I reran it with `PYTHONIOENCODING=utf-8`. The skill scripts were not affected. A note in SKILL.md about this could help agents on Chinese-locale Windows.

## 2. Unclear or missing guidance

1. **A sub-topic slide that never names its parent method (E044 SVM uses 核函数).** The rule says: "Two terms that only appear in the same section or paragraph support no relationship." The only structural rules are the agenda rule and the paragraph rule. Slide 16 「核方法」 comes right after the SVM slide. It is not its own agenda item, so it is clearly part of the SVM topic, but it never says "SVM". Following the rule literally, I reported E044 as `unsupported-expansion` (medium). I recommended marking it as an outside-source link, not deleting it. This will look pedantic to a user, because the deck plainly teaches kernels as part of SVM. A rule for "a slide without its own agenda entry, placed inside a method's slides, belongs to that method" would settle it.
   I had the same doubt about E043 (软间隔 uses 惩罚参数 C). There I judged the content linked the two terms, because C's bullet says 「允许更多误分类」, which restates the soft margin's 「允许部分样本违反间隔约束」. So I marked it `supported` by combining EV-071 and EV-072. Another run could reasonably decide E043 and E044 the other way.
2. **A general class described by its only instance, on a slide titled with the class (N048 神经网络).** The single-instance rule applies "when the source never defines a general class and only explains one member of it". Slide 22 is titled 「神经网络」, but its text describes 「多层感知机」. It is unclear whether the title counts as defining the class. I chose `unsupported-expansion` / `detail` (low).
3. **Label spelled out vs. ambiguous (N078 随机搜索).** The source only says 「超参数较多时，也可以使用随机搜索代替网格搜索」. I treated 「在超参数空间中随机采样若干组超参数进行评估」 as spelling out the label in that context, and marked it `supported`. The alternative was `ambiguous` under question 7 ("the source only names the term"). The two rules overlap here.
4. **Formulas the tree leaves out.** For example, ŷ = w·x + b for 线性回归, and the Tanh expression. The omission tiers mention "a notation or symbol legend", but not a formula missing from an otherwise compatible definition. Following "A node with a compatible definition already covers the source's definition", I did not report these.
5. **Whether an omission is reported depends on which evidence a finding cites.** The rule "do not report … when the … node already has a finding that cites it" means my choice of citations decides whether an omission appears. EV-158 (「没有一种算法在所有问题上都是最优的」) bears on the N032 overgeneralization, and it is also the lecture's own takeaway. I did not cite it in N032 and reported it as a core omission. Citing it in N032 instead would have removed the omission. A rule for which way to lean would help.
6. **Correct relationship not in the relation enum (E068 ReLU causes 梯度消失).** The source says ReLU 「可缓解梯度消失」. The instruction "if the source shows the correct relationship, recommend replacing it" has no matching relation, since there is no "mitigates". I recommended `related-to`, or deleting the edge, and noted that the direction already appears in N052's definition.
7. **When to split a bullet.** The rule is "split a bullet only if it states two unrelated facts". I split summary bullets that pair two different algorithms, e.g. 「kNN 不构建显式模型；朴素贝叶斯依赖条件独立假设」. That fits the rule. I also split 「高偏差通常对应欠拟合，高方差通常对应过拟合」 and slide 26 bullet 2 (feature scaling matters for kNN/SVM; not needed for 决策树), because separate edges (E070/E071, E026/E040) each needed their own evidence item. These clauses are related, so this departs slightly from the rule. The edge-evidence rationale in the extraction guide supports it, but the guide does not say so for text.
8. **Qualifier test leaving a slightly stronger remainder (N019).** After deleting 「总能」, the remainder 「也能取得很好的效果」 is still a bit stronger than the source's 「通常仍能取得不错的效果」 (很好 vs 不错, and it drops 「在文本分类等任务中」). I treated this as close enough and reported `overgeneralization`. The rule does not say how close the remainder must be.

Everything else (stages, file locations, paths, schema fields, risk defaults) was clear.

## 3. Effect of the input size

- **Keeping track of evidence.** 162 items is too many to number by hand reliably. I wrote a pipe-delimited draft (`page|type|certainty|location|content`), adding to it every 4 slides right after reading them. A small script then assigned EV IDs in order and wrote both `evidence-index.json` and a numbered plain-text list. I worked from that list for all of stage 4, so I did not have to re-read slides to find IDs. These working files are in `sl-run-1/work/`, outside the output folder.
- **Keeping track of tree items.** I printed the 78 nodes and 91 edges once, with labels resolved on the edges. I wrote the verdicts in four batch files (N001–N039, N040–N078, E001–E047, E048–E091), checked each batch's count against the tree, and merged them into `audit.json` with a script. That made the "exactly one entry per node and edge" check easy.
- **Re-reading slides.** I read each slide once during extraction. I re-opened only slides 15 and 26, to re-check the exact wording for findings that hinge on one word (C 越大/越小, 标准化/归一化), as `audit-rules.md` asks. The other single-word findings (0,1 range; 奇数; 有放回; 信息增益率; 大多数) were already quoted verbatim in the index from the first read.
- **Context.** Reading 32 images in batches of 4, and writing to files after each batch, kept the work manageable. The main cost was the omission pass: I had to walk the 162-item list against 169 verdicts and check whether a finding already covered each item. A per-evidence "cited by" listing from a script would have made that pass faster and less error-prone.
