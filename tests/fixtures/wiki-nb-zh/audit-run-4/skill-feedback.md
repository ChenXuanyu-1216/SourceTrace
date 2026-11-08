# Skill feedback: SourceTrace run on the naive Bayes screenshots (10 pages, 35 nodes, 52 edges)

## 1. Script runs

| Script | Runs | Result |
|--------|------|--------|
| `validate_input.py --json` | 1 | Valid. No errors or warnings. |
| `validate_evidence.py` | 2 | Both runs valid, each with one warning: `LOW_CERTAINTY` for EV-105 (the part of the `evidence = …` formula on page 7 that is cut off by the right edge of the image). This warning was expected. |
| `build_report.py` | 2 | Both runs succeeded on the first try (86 supported, 1 source note, 12 omissions). |

No run failed. I ran the second `validate_evidence.py` and `build_report.py` because I changed the index, not because of an error. After the first build, I noticed I had placed some overlapping statements inconsistently. A statement that starts at the bottom of one screenshot and appears in full on the next went to the first page in some cases (EV-012, EV-029, EV-039, EV-125, EV-132) and to the second page in another (EV-110). I moved those five to the page where the statement is first complete. The evidence IDs did not change, only `page`, `source_id` and `location`. Then I revalidated and rebuilt. I also ran two helper scripts of my own (`work/make_index.py` and `work/make_audit.py`), which write the JSON files.

## 2. Unclear or missing instructions

1. **Two overlap rules can conflict.** `evidence-extraction.md` says: "Extract each statement once, on the page where it is first complete" and also "A sentence split across two images is one item on the page where it starts; say `continues on page N` in `location`." With overlapping screenshots, a sentence often starts at the bottom of image N and then appears again in full at the top of image N+1. The first rule puts it on N+1 and the second on N. I first applied the rules inconsistently (see section 1), then settled on this: use "first complete" whenever one image shows the whole statement, and use "where it starts" only when no single image shows all of it. It would help to state that order of precedence in the file.

2. **`reason` on supported items is not shown.** `audit-rules.md` ("Problems in the source itself") says: "When the problem bears on an item's verdict or recommendation, say in that item's `reason` which statements conflict and which one you used." Several of these items are `supported` (N019 vs. "朴素贝叶斯方法都用到离散化方法", N033 vs. "相互独立", N034 vs. "可以表达为似然比", N029's `e^{−09}` notation, N025's "各个变量的方法"). SKILL.md describes `reason` as "why it is a problem", which does not fit a supported item. The schema accepts `reason` there and `build_report.py` does not reject it, but the report never shows a supported item's `reason`. I wrote the reasons anyway (they are in `audit.json`) and listed the source problems in the final message.

3. **Worked-example data versus "a table row" as core.** The omission tiers list "a table row" as core. The not-knowledge tier covers only "Examples in parentheses when the concept they illustrate is in the tree". The gender example has 8 training-data rows, 2 mean/variance rows and about 10 intermediate likelihood values. They are not in parentheses, and the tree has the example (N027 to N029) but not the numbers. I treated them as covered by the example nodes and did not report them. Reporting each data row as a core omission would have flooded the report. A rule for data tables inside a worked example would remove the guess.

4. **How much weight a navigation box gets when combined with text.** The rule says navigation boxes "can be cited together with the article's own text, but never support a node or edge on their own." For E041 (文本分类 is-a 监督分类), the article says that text classification is a classification problem (EV-006) and that naive Bayes gives good classification results "在监督式学习的样本集中" (EV-020). The word "监督" for classification itself appears only in the sidebar ("监督学习（分类 · 回归）"). I judged the edge `supported` from the article text, with the sidebar as extra support, and explained this in the item's `reason`. Another run could reasonably call it `unsupported-expansion`.

5. **`includes` across sibling sections.** E030 is 参数估计 includes 概率平滑修正. In the article, 样本修正 is a sibling section of 参数估计, not a subsection. The slide-order rule says position supports no relationship, but it does not cover the reverse case: the content links the two (it corrects "基于频率的估计", and parameters are estimated "通过训练集的相关频率"), while the heading structure separates them. I judged the edge by its content (`supported`) and noted that in `reason`.

6. **= versus ∝.** The extraction rules say that `=` and `∝` are different claims. The audit rules do not say how to judge a tree that says "展开为" (equality) when the source writes the chain-rule expansion with ∝ throughout, even though the expansion is an equality. Both statements can be true, so it fails the contradiction test, and the source's "写成条件概率的形式" reads as a rewrite. I marked N012 `supported`.

Apart from these points, the instructions were clear. The worked examples in `audit-rules.md` (互斥且穷尽, the N026 limitation omission, 概率平滑修正, the 离散化 core omission and 词袋表示) matched this source almost exactly and settled several decisions.

## 3. Image difficulties

- **Low resolution:** each image is 800×600. Subscripts and the exponent of the Gaussian density on page 5 were very small. I enlarged crops 2× and 5× (saved in `work/`) and read the exponent as −(v−μ_c)²/(2σ_c²). EV-061 is marked `medium`, with the reading stated in `location`.
- **Overlapping screenshots:** every page repeats a few lines of the one before, and several formulas are cut at the bottom of one image and complete on the next. Each statement was extracted once (see section 2, point 1).
- **Cut-off formula:** on page 7, the `evidence = …` formula runs off the right edge after "p(weight|f", and page 8 does not show it again. I split it into a readable `high` item (EV-104) and a `low` item ［无法辨认］ (EV-105). No verdict depends on the hidden part.
- **Site chrome:** the Wikipedia header, a banner, the revision notice ("这是…的当前版本…") and the edit links were skipped. The "机器学习与数据挖掘" sidebar was extracted once as a navigation-box item (EV-002).
- **Exponent notation in the source:** values are typeset as `6.1984e^{−09}` and look like powers of e. I checked them against the e-notation in the table (3.5033e-02) and by recomputing p(height|male) ≈ 1.5789 and both numerators. They mean ×10⁻ᵏ.
