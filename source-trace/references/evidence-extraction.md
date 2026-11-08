# Evidence extraction rules

Stage 2 turns the source images into `evidence-index.json` (schema: `schemas/evidence-index.schema.json`). Every finding in the audit cites evidence by ID, so the index has to be complete and fine-grained enough that each claim in the tree can be matched to one or a few items.

## Start from the validator

Run `scripts/validate_input.py --json` first and copy its `summary.images` list into `sources` unchanged, including each `path` exactly as reported (relative to the output folder, with forward slashes, so the index can be moved together with its images). It fixes each image's `source_id` and `page`, so pages are numbered the same way every time.

## One item per checkable statement

| Content | One item per | `type` | `content` | `location` |
|---------|--------------|--------|-----------|------------|
| Slide title | title | `text` | the title, verbatim | `Title` |
| Bullet or sentence | bullet; split a bullet when its parts can be cited separately (see below) | `text` | verbatim | `Bullet 2`, `Bullet 2, sub-bullet 1` |
| Table | data row | `table` | `Header: value \| Header: value \| …` | `Table row 2 (Supervised)` |
| Diagram | relationship it shows (box → box, arrow, grouping) | `graphic` | `Diagram: A → B`, plus any label on the arrow | `Diagram, top row` |

Why this granularity: nodes are checked against single statements, and edges against the relationships a slide shows. A table row or diagram arrow is often the *only* evidence for an edge, so it needs its own ID.

**Splitting a bullet:** split it into one item per clause when the clauses state facts about different concepts, or when different tree items would cite them. Examples: "kNN 不构建显式模型；朴素贝叶斯依赖条件独立假设" (two concepts); "高偏差通常对应欠拟合，高方差通常对应过拟合" (two edges). Each item keeps its clause verbatim, with its qualifiers, and the same `location` plus a part number (`Bullet 3, part 2`). Do not split a definition from its own explanation ("Sigmoid 函数 … 映射到 (0, 1) 区间，输出可解释为…的概率").

**Formulas:** write a formula as linear Unicode text, exactly as printed, in a `text` item together with the sentence that introduces it. Keep subscripts and superscripts (`μ_c`, `σ_c²` or `σ_c^2`, `e^(−z)`), conditions (`p(F_i|C)`), index ranges (`∏_{i=1}^{n}`) and the source's symbols, even ones that look wrong: `=` and `∝` are different claims. A formula cut off by the edge of the image follows the rule for partly unreadable items below.

## Web pages and documents

When the images are screenshots of a web page or a document rather than slides:

- **Units:** use section headings, paragraphs (split into sentences or clauses by the rule above), formulas, table rows and figures. `location` names them, e.g. `Section 参数估计, paragraph 2, sentence 3`.
- **Overlapping screenshots:** consecutive images often repeat a few lines. Extract each statement once, on the first page that shows all of it, and do not skip the lines that appear only at the bottom of one image. Only when no single image shows all of it is it one item on the page where it starts, with `continues on page N` in `location`. If you split such a sentence into parts anyway (see "Splitting a bullet"), each part goes on the first page that shows that part.
- **A formula on a different page from the sentence that introduces it:** one item on the page with the formula, quoting the sentence too; if the sentence is not repeated there, `location` says where it is.
- **Citation markers** such as [1] or [注 2] are not part of the statement: leave them out of `content`.
- **Site chrome:** skip menus, banners, edit links, revision notices, disambiguation notes at the top ("关于与…标题相近…"), the reference list and the footer. A navigation box (e.g. a sidebar listing related topics) may be extracted as `text`, with `location` saying `Navigation box`; the audit decides how much it counts.

## Quote, don't paraphrase

Copy text in its original language and wording, including punctuation and qualifiers such as "通常" or "usually". Keep evident slips and typos as printed; the audit rules say how to handle them. Small wording changes are exactly what the audit has to catch; paraphrasing here would hide them. For tables and diagrams, transcribe in the fixed formats above instead of describing them in prose.

## What to extract

- Everything that states knowledge, including examples in parentheses.
- Also extract non-knowledge text such as homework or reading notes. The audit decides what is significant, not the extraction.
- Skip page numbers, logos and decoration.

## IDs and order

Number items `EV-001`, `EV-002`, … across the whole deck: by page, then top to bottom, left to right. IDs are never reused within one index.

## Certainty

| Value | Use when |
|-------|----------|
| `high` | The text is clearly legible, or the diagram relationship is unambiguous. |
| `medium` | Part of the text is hard to read, or the diagram could be read more than one way. Say which reading you chose in `location`. |
| `low` | You had to guess. The audit must not reject a tree item on `low` evidence alone. |

**Partly unreadable items** (glare, a fold, a cut-off edge): enlarge the area first. If part of a bullet or table row is still unreadable, split it into a readable item and an unreadable one. The readable item keeps its own certainty. The unreadable item gets `low`, with ［无法辨认］ in `content` in place of the hidden text, and `location` says what hides it. Example: "本课程推荐的划分比例：训练集 : 验证集 : 测试集 =" (`high`), then "［无法辨认］" (`low`, "Bullet 4, part 2: the ratio after = is covered by glare"). For a table row, keep the readable cells and put ［无法辨认］ in the hidden ones; the row's certainty is `low` if a hidden cell is the one a claim depends on. Never fill in hidden text from your own knowledge, even when you are sure what it says.

## Example

From a 4-slide machine-learning deck (slide 1 has a title, two bullets and a diagram; slide 4 has a table):

```json
{ "evidence_id": "EV-002", "source_id": "slide-01", "page": 1, "type": "text",
  "content": "Machine learning lets computers learn patterns from data instead of following hand-written rules.",
  "location": "Bullet 1", "certainty": "high" }
{ "evidence_id": "EV-004", "source_id": "slide-01", "page": 1, "type": "graphic",
  "content": "Diagram: Machine Learning → Supervised",
  "location": "Diagram, line from top box to left box", "certainty": "high" }
{ "evidence_id": "EV-019", "source_id": "slide-04", "page": 4, "type": "table",
  "content": "Paradigm: Supervised | Training data: Labeled | Feedback: Correct answers",
  "location": "Table row 1 (Supervised)", "certainty": "high" }
```
