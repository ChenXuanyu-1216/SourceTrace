# SourceTrace skill feedback (wiki-ml-zh run, 12 pages, 40 nodes, 58 edges)

## 1. Script runs

| Script | Runs | Result |
|--------|------|--------|
| `validate_input.py --json` | 1 | valid, no errors, no warnings |
| `validate_evidence.py` | 1 | VALID: 12 sources, 221 evidence items (27 graphic, 194 text) |
| `build_report.py` | 1 | written: Supported 83, findings 15, omissions 25 |

No run failed, so I made no fixes in response to script errors.

Before running the scripts, I made a few corrections myself:
- In the evidence list I had at first put "例如：" in front of the two example bullets on page 11. I removed it because the bullets themselves do not contain that text, and recorded "under '例如：'" in `location` instead.
- One omission recommendation suggested `N026 related-to N035`. The source never links random forest regression to multivariate linear regression, so I removed that part before `build_report.py` ran.

Helpers: I generated `evidence-index.json` from a small Python list with a script, so that EV numbering stayed sequential across 221 items. To quote small text exactly, I made 2x enlarged crops of each page. Both lived in a temporary folder inside `wiki-audit/` and were deleted at the end.

## 2. Unclear or missing instructions

1. **A node definition that adds an uncheckable detail to an otherwise supported definition.** The decision order sends nodes to `unsupported-expansion` only when "the node's term … [is] absent from the source" (Q1). It sends them to `ambiguous` only when "the source never defines it, or … the only relevant evidence has `low` certainty" (Q6). Several nodes fit neither case. Their term is in the source and the source gives a partial definition, but the tree adds a specific claim the source never makes:
   - N028 自助采样: "有放回地"
   - N029 支持向量机: "较大间隔的决策边界"
   - N034 逻辑回归: "线性组合映射为类别概率"
   - N031 回归分析: the source's "输入变量与其相关特征" becomes "目标变量与输入变量"

   No question covers this case, and the category table's description of `unsupported-expansion` ("Content not found in the source, even if true in general") fits better than its decision-order rule allows. I used `ambiguous`, which is the closest match to "too vague or uncertain to confirm or reject", and said in each reason which part is supported. A rule for "term present, extra detail absent" would remove this guess.

2. **"Spells out its own label".** The rule says "A definition that only restates or spells out its own label adds no claim to check". I used it for N006 偏差与方差分解: the tree's "系统性偏离 / 对训练数据的敏感程度" spells out 偏差 / 方差, and the rest matches "用于量化泛化误差的方法". So I marked N006 `supported`. Where "spelling out" ends and "adding a claim" begins is a judgment call (compare item 1).

3. **The source is web-page screenshots, not slides.** The rules assume slides: titles, agenda slides and bullets. Three gaps came up:
   - *Navigation sidebars.* Is the "机器学习与数据挖掘" navbox an "agenda/overview slide"? I treated it as an overview. Its uncovered topics (结构预测, 异常检测, …) became one core omission, with risk lowered to `low` and a `risk_reason`. I treated the "人工智能系列内容" navbox as non-knowledge, because it only lists generic AI headings. Both were guesses.
   - *Section headings with a "主条目：" line.* I applied the agenda rule to these: for example, the 理论 section with "主条目：计算学习理论" supports E002 机器学习 includes 计算学习理论. The rules do not say whether article sections count as an agenda.
   - *Overlapping screenshots.* Consecutive pages repeat a few lines, because the screenshots were taken while scrolling. The rules do not say which page to cite for duplicated text. I extracted each statement once, on the page where it is fully legible, and skipped the cut-off copies.

4. **Ordering with a right-hand column.** The rule is "by page, then top to bottom, left to right". With a sidebar or figure running down the right side, strict top-to-bottom ordering would interleave sidebar rows with paragraph sentences. I numbered the main column first and the right column second on each page.

5. **Granularity for prose.** The table says "Bullet or sentence … one item per bullet". For long paragraphs I made one item per sentence, which gave 221 items. That was workable, but one item per paragraph would also have been defensible. A sentence of guidance for prose-heavy sources would help.

6. **Core vs supporting tiers overlap.** "A stated rule ('X is …')" is core, and "a property or caveat of a concept that is in the tree" is supporting. Almost every sentence about a concept already in the tree is both. My rule was:
   - *core* when the content introduces a new defined term or rule (PAC, 正面/负面结果, 分类树/回归树, 动态贝叶斯网络/影响图) or is the main point of a section;
   - *supporting* when it is an extra property of an existing node.

7. **"One omission per missing concept" vs. a long list.** The "具体的机器学习模型有" list names about 20 models in four groups. I reported it as one omission, "model taxonomy", rather than about 20 separate ones. The rule does not say how to handle a list of many missing members.

8. **"Already covered by a finding".** The rule says not to report an omission when "the … node already has a finding that cites it". I read this as covering only `finding` items, not `supported` items that cite the same evidence. On that reading:
   - GAN (EV-085) was not reported separately, because the E020 finding cites it and its recommendation mentions it;
   - 超参数优化 was not reported separately, because the E056 recommendation covers it;
   - the alias 核函数 in EV-214 was still reported, because only supported items (N038, E054) cite that evidence.

9. **Section with no content.** The screenshots end at "软件 / 包含各种机器学习算法的软件套装包括：" with no list visible. I did not report it as an omission, because it has no knowledge content to cover. The "missing pages" guidance applies only when the tree covers material that is not in the images, so I did not raise it either.

Everything else was clear. That includes the stage order, the evidence ID and certainty rules, the qualifier test (no node had an absolute qualifier), the risk defaults and `risk_reason`, the recommendation constraints, and the final-message instructions.
