# Skill feedback (SourceTrace run on input/, naive Bayes)

## 1. Script runs

| Script | Runs | Result |
|---|---|---|
| `validate_input.py --json` | 1 | valid, no errors, no warnings (35 nodes, 52 edges, 10 images) |
| `validate_evidence.py` | 1 | VALID, 146 items; one `LOW_CERTAINTY` warning for EV-114 (the cut-off part of the evidence formula on page 7), which is intended |
| `build_report.py` | 1 | succeeded on the first run: 84 supported, 3 findings (all `detail`), 10 omissions |

No run failed, so nothing had to be changed in response to script errors. I generated `evidence-index.json` and `audit.json` with two small helper scripts in `work/` (items keyed by name, so evidence IDs were assigned automatically in page order and the audit could refer to them without hand-typing IDs).

## 2. Unclear or missing instructions

1. **Node label is a term of art the source never uses, while the definition is fully supported.** audit-rules.md question 1: "Is the node's term (or, for an edge, either end node's term) absent from the source? → `unsupported-expansion` (scope `whole`)." Question 6 covers "one specific added detail" of a *definition*. N031 词袋表示 and N024 概率平滑修正 describe exactly what the source describes (单词集 / 词频 / position independence; 对概率估计进行修正 to avoid 0), but the names 词袋 and 平滑 never appear. Read literally, question 1 makes both `whole` / medium, which seems too harsh for a node whose content is all in the source. I read "term" as the concept and treated the unsupported name as a `detail` (low), recommending to mark the name as 资料外术语 or use the source's wording. For descriptive labels made of source words (N018 均匀类别先验 ≈ "各类等概率", N023 零频率问题 ≈ "基于频率的估计下该概率将为0。这将是一个问题", N002 监督分类 ≈ 监督式学习 + 分类) I gave `supported`. A sentence on where the line between "new term of art" and "descriptive label" lies would help.
2. **Overlapping screenshots.** The source is one web page captured as ten scrolled screenshots that overlap (the bottom of each page reappears at the top of the next, and one sentence is split across pages 1 and 2). evidence-extraction.md assumes one slide per image and says nothing about repeated content. I extracted each passage once, on the first page where it is fully visible, so IDs are not duplicated.
3. **Web-page source, not slides.** The location vocabulary (`Title`, `Bullet 2`, `Table row`, `Diagram`) does not fit paragraphs and section headings; I used `Section X, paragraph N, part M` / `sentence N`. "Skip page numbers, logos and decoration" does not say what to do with site chrome. I skipped the site header, the Telegram notice and the revision banner (no knowledge), kept the sidebar navbox entries as text items (they are knowledge-adjacent) but did not count them as omissions, and kept citation markers such as "[1]:488" in the quotes because the rule says to quote verbatim.
4. **Math formulas.** There is no transcription format for formulas (only text, table rows and diagrams). I wrote them as linear Unicode text inside `text` items together with the sentence that introduces them.
5. **Inconsistencies inside the source itself.** The skill treats the images as the single source of truth but does not say what to do when the source contradicts itself or contains an obvious slip: "两个相互独立的类别 S和¬S" next to "要么是垃圾邮件，要么就不是"; "只需要估计各个变量的方法" (likely 方差); and "朴素贝叶斯方法都用到离散化方法，而不是概率分布估计的方法" right after the Gaussian method is presented. I judged the tree against the clear statements (e.g. N033 互斥且穷尽 supported by "要么…要么就不是" and p(S|D)+p(¬S|D)=1), quoted the source as printed, and did not report source errors as findings. A rule for this case would help.
6. **History and applications in omissions.** The tier table has no row for history (1950 年代起研究), applications (自动医疗诊断) or literature notes (2004/2006 papers). I put them under supporting detail as properties of a concept in the tree; one could also argue they are "not knowledge".
7. **Edges to a task the source never names as such** (E001 监督分类 uses 朴素贝叶斯分类器, E035, E041 文本分类 is-a 监督分类). The source never says "监督分类"; it says NB gets good results "在监督式学习的样本集中" and estimates p(wi|C) from class-C texts. I judged these `supported` by combining pages, but this was a judgment call that two runs could make differently.

## 3. Image difficulties

- The images are small (800×600) with small text, subscripts and exponents. I made 2× crops of the dense passages (page 2 body, page 4 parameter-count paragraph, page 5 Gaussian formula, page 7 evidence formula) in `work/` and checked the wording and numbers against them before quoting.
- On page 7 the evidence formula is cut off by the right edge after "p(weight|f". I split it into a readable `high` item (EV-113) and a `low` item with ［无法辨认］ (EV-114). No tree item depended on the hidden part (N010 is supported by other text), so no finding rests on low-certainty evidence.
- The pages overlap (see 2.2). Some passages appear twice; I cite the first full occurrence.
