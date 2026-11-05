# Skill feedback: SourceTrace run on wiki-audit-2 (12 pages, 40 nodes, 58 edges)

## 1. Script runs

| Script | Runs | Result |
|--------|------|--------|
| `validate_input.py --json` | 1 | Valid on the first run. No errors, no warnings. |
| `validate_evidence.py` | 1 | Valid on the first run (12 sources, 231 items: 12 graphic, 219 text). |
| `build_report.py` | 1 | Written on the first run (82 supported, 16 findings, 25 omissions). |

No script run failed, so I made no fixes in response to script errors.

Notes:
- I wrote evidence pages 1–4 directly into `evidence-index.json`. For pages 5–12, I wrote one tab-separated file per batch of pages and appended it with a small helper script of my own (`scratchpad/work/add_evidence.py`, outside the skill). It numbered the IDs in sequence. The skill does not provide a tool for this, and it does not need to. One bash heredoc failed because of shell quoting before any skill script ran. That was my tooling, not the skill's.
- I set `PYTHONIOENCODING=utf-8` before running `build_report.py`, because the Windows console mangles Chinese output (the `python -c` listing of evidence IDs showed mojibake without it). I don't know whether the script needs this, since I never ran it without the setting.

## 2. Unclear or missing instructions

1. **Overlapping screenshots.** These images are scrolled captures of one web page, and consecutive pages repeat several lines (for example, the end of page 3 appears again at the top of page 4, and the model list continues from page 6 onto page 7). `evidence-extraction.md` says "Number items … by page, then top to bottom" and "IDs are never reused", but it does not say what to do when the same sentence appears on two images. I extracted each sentence once: on the page where it first appears complete. In `location` I noted where it repeats or is cut off (for example, "repeated at the top of page 8"). A one-line rule would make this consistent between runs.

2. **Prose paragraphs, not bullets.** The granularity table covers "Bullet or sentence: bullet; split a bullet only if it states two unrelated facts". Wikipedia paragraphs contain 3–7 sentences, and each one states a separate fact. It was unclear whether the unit should be the paragraph or the sentence. I used one item per sentence, so nodes can cite a single statement. The supervised-learning bullet on page 5 has six sentences, and I split it into five items. The table could say "prose: one item per sentence".

3. **Non-slide material: section headings, sidebars and page chrome.** The rules are written for slides ("Slide title", "agenda/overview slide").
   - I treated section headings (定义, 理论, 分类 …) as `Title`.
   - I extracted the Wikipedia revision notice and maintenance banners, following "Also extract non-knowledge text such as homework", even though they are close to "decoration".
   - The tier table says "A topic in a slide title or an agenda/overview slide" is core. I had to guess whether the "机器学习与数据挖掘" navigation sidebar counts as an overview. I counted its rows 结构预测 and 异常检测 as core omissions, because they stand at the same level as 聚类分析 and 降维. I treated 范式, 问题, 与人类学习, 模型诊断与优化, 数学基础, 大会与出版物 and 相关条目 as navigation headings, not knowledge, and did not report them. A sentence on navigation boxes and sidebars would remove this guess.

4. **Edges supported only by section structure, but with a relation other than `includes`.** The agenda rule says a topic list "supports `includes` from the lecture's subject to each listed topic" and "says nothing about how the listed topics relate to each other". E003 (计算学习理论 includes 泛化) fits that rule, and I marked it supported. E004 (计算学习理论 **uses** 偏差与方差分解) is backed by the same section structure but uses a different relation. Question 3 then gives `unsupported-expansion`, which is what I reported. It was not obvious whether a section structure that supports `includes` should also count for `uses`. An example in the edge cases would help.

5. **A term defined only through its single instance.** The source never defines 集成学习. It says only "RFR 是一种集成学习方法（ensemble learning method），它通过构建多个决策树并对其预测结果进行平均，从而提高预测的准确性". N027 defines ensemble learning in general as "组合多个模型的预测以改善整体表现的方法". The decision order has no question for "general definition inferred from one instance". Q4 does not apply, because there is no absolute word. Q7 does not fit either, because the definition is partly checkable. I marked it `supported`, reading the "它通过…" clause as explaining what makes RFR an ensemble method. Another run could reasonably choose `ambiguous`.

6. **Node labels that paraphrase the source term.** Q1 asks whether "the node's term" is absent. 网络层次结构 never appears literally; the source says "人工神经元会被组织成不同的层（layers）". I treated the label as a paraphrase of a term that is present and marked the node supported. The rules don't say whether Q1 means the literal word or the concept.

7. **Q6 versus Q7 when the source gives only a position, not a definition.** For 半监督学习, the source says only "介于监督学习与无监督学习之间". The tree's "结合有标签数据与无标签数据" is a specific reading of that position. I chose Q6 (`detail`), because the source does say something about the term, so Q7's "only names the term" did not fit. The boundary between "names the term" and "says one vague thing about it" is not covered.

8. **Lists of examples that are not in parentheses.** The "Not knowledge" tier covers "Examples in parentheses when the concept they illustrate is in the tree". The source also has examples in running text: "常见的无监督学习算法有生成对抗网络（GAN）、聚类", the ANN application list, and the Titanic and Rain/Sprinkler figures. I treated GAN and the two figures as non-knowledge examples. I folded the ANN application list into a supporting omission. The rule could say whether only the parentheses matter, or the role of the content.

9. **Paraphrase of a cause.** For 欠拟合, "模型过于简单" corresponds to the source's "假设的复杂度低于真实函数的复杂度", and I marked it supported. For 过拟合, the tree gives a different mechanism ("过度适应训练数据的细节") instead of "复杂度过高", and I made that a `detail` finding. I think this is consistent under Q6, but it is a judgment call the rules do not illustrate.

Everything else was clear. That includes the risk defaults, the rule to keep the definition useful for learning (which I applied to every `detail` and `ambiguous` recommendation), the Bayesian-network 条件独立性 versus 条件依赖 example (N036 matched it exactly), the bootstrap 有放回 and SVM 较大间隔 examples (N028 and N029 matched them exactly), and the regression-analysis two-page example (N031).
