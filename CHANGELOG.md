# Changelog

## v0.3.0 (2026-11-10)

Three more rule revisions, each driven by a new test: a 169-item scale test, degraded images, and two more Chinese Wikipedia articles with trees from ChatGPT and Codex. OpenAI Codex ran the skill for the first time, twice. Every script run in the saved runs passed.

### Results

| Test | Rules | Agent | Result |
|------|-------|-------|--------|
| sl-algos-zh (32 slides, 169 items) | v0.2.0 | Claude, 2 runs | 28/28 item findings and 8/8 omissions against the revised key; same verdict on all 169 items |
| model-eval scan, photo, occluded | fourth revision | Claude, 2 runs each | 11/11 and 4/4 on every version; hidden text marked `low` and never guessed |
| wiki-ml-zh | v0.2.0 | Codex, 1 run | 15 of the 18 items the owner judged; 44 omissions where Claude reported 25 (not judged) |
| wiki-nb-zh (朴素贝叶斯分类器) | fourth, then fifth revision | Claude, 2 + 2 runs | no conceptual or relationship error, none missed; the fifth-revision re-runs match the key on 87/87 items |
| wiki-pc-zh (感知器) | fifth revision | Claude, 2 runs | same verdict on all 83 items, both tree errors found; 0 of 4 source problems that take a derivation |
| wiki-pc-zh | sixth revision | Codex (GPT-6.1 Sol, high), 1 run | same verdicts on all 83 items; 2 of 4 source problems found, and the b = 0 omission both Claude runs missed |

The answer keys of wiki-nb-zh and wiki-pc-zh are AI reviews accepted by the owner. Details and caveats: [docs/evaluation.md](docs/evaluation.md#since-v020).

### Audit rules

- **Fourth revision,** from the scale test:
  - **Question 7** applies the label test first: a definition that only spells out the name is supported, not `ambiguous`.
  - **A slide title does not define a class** described only through one member.
  - **Slide order supports no relationship;** only the agenda rule lets structure state one.
  - **Omissions:** a finding covers only the content it is about, and a topic whose members are all in the tree is covered.
  - **Evidence:** a bullet is split when its parts can be cited separately.
  - **Recommendations:** when no relation value fits (e.g. "mitigates"), delete the edge and state the relationship in a definition. `is-a` from a method to a task reads as "is a method for".
- **Fixes after the image-quality test:**
  - "Do not fall back on `related-to`" applies only when no relation value fits; when only an end node is wrong, keep the relation and correct the node.
  - Partly unreadable evidence is split into a readable item and a `low` item with the placeholder ［无法辨认］, and hidden text is never filled in.
  - Working files go in a `work/` folder inside the output folder.
- **Fifth revision,** from wiki-nb-zh:
  - **Question 1 is about the concept, not the word:** a label from outside the source is supported when the source describes what it names (词袋表示, 概率平滑修正). Only a claim the name adds is checked, as a `detail`.
  - **Web pages and documents** (evidence-extraction.md): overlapping screenshots, split paragraphs, site chrome, and navigation boxes, which can back up the article's text but never stand alone or create an omission.
  - **Formulas** are transcribed as linear Unicode text, exactly as printed.
  - **Problems in the source itself** are quoted as printed, judged by the more specific evidence, explained in the item's `reason` and listed in the final message, with no new category or schema change.
  - **Omissions:** a rule or caveat about a concept that has a node is supporting; history, applications, other names and comparisons are supporting background; a missing claim appears in only one entry; a supported node does not cover a limitation it leaves out.
  - **Recommendations** are checked like findings: they keep the source's conditions and do not copy a source sentence that other evidence contradicts.
- **Sixth revision,** from wiki-pc-zh and the wiki-nb-zh re-runs:
  - **Check a source claim before relying on it:** before a recommendation quotes a general claim of the source, test it against the source's own formulas at the boundary cases and other conventions (e.g. "E(w)是一组正数的和" fails because f(0)=+1).
  - **A slip only outside knowledge reveals** (N029 "最大平均值") is judged against the printed text; the recommendation marks the tree's version as an outside explanation to check, and the final message calls it a possible slip.
  - **Overlapping screenshots:** a statement goes on the first page that shows all of it; "the page where it starts" applies only when no single image does.
  - **Omissions:** one entry per node or topic. A node's missing details form one entry; background is one entry per kind in each section. A convention a formula relies on (b = 0) is a supporting detail.
  - **A wrong end point of a range** that the tree gives as the source's condition (0<α<1 vs 0 < α ≤ 1) is a `conceptual-error`, at risk `medium` when the rest of the definition is right. A claim attributed to the source ("资料给出的") must match the source.
  - **`contrasts-with`** is supported by two formulas or conventions for the same thing, even if the source never compares them.
  - **The label test comes before the single-instance rule:** a class definition that only says what the name means is supported (线性分类器).
  - **Smaller points:** `=`/展开为 vs `∝`; web-page heading levels neither state nor rule out a relationship; a formula on a different page from its intro sentence; citation markers [n] are left out of quotes; disambiguation notes and reference lists are site chrome.
- **After the Codex run:** a method that the source names only in a history passage is a background omission, not core.
- **SKILL.md** suggests `python -X utf8` for the agent's own Python commands on Windows, since `python -I` and `-E` ignore `PYTHONIOENCODING`.

### Report, scripts and tools

- **Notes on supported items:** `build_report.py` shows a supported item's optional `reason` as a note (说明 / Note) in the confirmed list. It holds only a problem in the source that the verdict had to resolve.
- **`tools/degrade_images.py`** makes seeded scan, photo and occluded versions of a test set's slides.
- **`tools/make_fixture_slides.py`** builds decks from data files in `tools/decks/`, with bullets, tables, flow and tree diagrams, and stops if a slide overflows.
- **`tools/compare_runs.py`** reports evidence certainty, checks `scope` against the key, counts omissions that match an acceptable extra as accepted, and skips the risk check when a run gives an accepted alternative category. Its item count is labelled `expected items`.

### Test sets and runs

- **`tests/fixtures/sl-algos-zh`:** a synthetic 32-slide Chinese lecture with a 169-item tree, 27 planted item problems and 8 planted omissions. The runs found a real gap in the deck (the kernel slide never names SVM), and the owner revised the key ([RESULTS.md](tests/fixtures/sl-algos-zh/RESULTS.md)).
- **`tests/fixtures/model-eval-scan`, `-photo`, `-occluded`:** degraded versions of model-eval ([RESULTS.md](tests/fixtures/model-eval-occluded/RESULTS.md)).
- **`tests/fixtures/wiki-nb-zh`:** 10 screenshots of 朴素贝叶斯分类器 (CC BY-SA 4.0), with a tree from ChatGPT, the first real-content tree not made by Codex. Four Claude runs ([RESULTS.md](tests/fixtures/wiki-nb-zh/RESULTS.md)).
- **`tests/fixtures/wiki-pc-zh`:** 6 screenshots of 感知器 (CC BY-SA 4.0), the first real-content set with figures as evidence, with a tree from Codex. Two Claude runs and one Codex run ([RESULTS.md](tests/fixtures/wiki-pc-zh/RESULTS.md)). The Codex run's prompt and final message are saved, a first.
- **`tests/fixtures/wiki-ml-zh/codex-run-1`:** the first Codex run, with a comparison against the owner's judgments ([COMPARISON.md](tests/fixtures/wiki-ml-zh/codex-run-1/COMPARISON.md)).
- 120 tests, up from 91.

### Documentation

- **README in five more languages:** 简体中文, 日本語, 한국어, Italiano and العربية (right to left), translated by AI from the English README, which stays the reference.
- **[docs/evaluation.md](docs/evaluation.md)** has a "Since v0.2.0" section, and its list of what the results do not show is up to date.

### Known limitations

- **The sixth revision ran once,** by Codex, on wiki-pc-zh, the article several of its examples come from. No article that played no part in it has been tested. The rule line added after that run has not been run.
- **Answer keys:** the keys of wiki-nb-zh and wiki-pc-zh are AI reviews accepted by the owner, the second by the same model that made the tree and ran the Codex audit. One person judged or accepted every key.
- **Source problems that need reasoning** across sections, or a scaling argument, are still missed.
- **Not judged:** the omissions of the wiki-ml-zh runs (44 in the Codex run), and one extra omission in wiki-nb-zh run 4 (F-012).
- **Coverage:** all real content is Chinese; real photos, handwriting and real decks of 30+ slides are untested. Codex ran on two different rule versions, so its results can't be separated from the rule changes.
- Only PNG/JPG input; node `kind` is not audited; pytest 9.2.0 crashes on Python 3.10.0, so tests pin pytest 8.x.

### Next steps

1. **A fresh article for the sixth revision:** one that played no part in any rule, ideally in English or another field, with an answer key from a model other than the tree's.
2. **Independent grading:** a reviewer other than the owner, or keys from a different model than the agent's.
3. **Real images:** photos or scans of openly licensed or owner-written slides.
4. **Task modes:** a strict source-tracing mode and a review mode that allows short, marked explanations from outside the source.

## v0.2.0 (2026-11-05)

Tested on real content for the first time, and revised three times based on the project owner's reviews. Two openly licensed Wikipedia articles were added as test sets. The knowledge trees were generated by OpenAI Codex, so their mistakes are real, not planted.

### Results on real content

| Run | Rules | Items judged by the owner | Correct | Partly correct | Wrong |
|-----|-------|---------------------------|---------|----------------|-------|
| wiki-ml-zh, run 1 | v0.1.0 | 13 findings | 6 | 4 | 3 (one high-risk) |
| wiki-ml-zh, run 2 | first revision | 18 items (findings and changed verdicts) | 14 | 1 | 3 |
| wiki-dt-zh, run 1 | second revision | 11 findings, 77 supported items | 8 findings, 77 supported items | 1 | 2 |

After the first revision, no run produced a high-risk false finding. On wiki-dt-zh the audit also missed 2 low-risk omissions. Details: [docs/evaluation.md](docs/evaluation.md#real-content-v02).

### Audit rules

- **Gather all evidence first:** text, tables and figures on every page, combined across pages, before deciding anything.
- **Contradiction test:** a conceptual error must contradict the source in meaning. Opposite-looking words are not enough (a Bayesian network represents both dependencies and conditional independencies).
- **New `scope: detail`** for an `unsupported-expansion` limited to one added detail of an otherwise supported definition, low risk by default. Its boundaries:
  - **An explanation of the term is not a detail:** a part of a definition is a separate claim only if it could be false while the rest is true.
  - **A class defined from a single instance is a detail** (集成学习 from random forest).
  - **A different word for a different property is a detail** (多路划分 vs the source's 多层分裂); a different word for the same thing is not (预测误差 vs 泛化误差), and only the unsupported fragment is the finding.
  - **A narrower or more cautious claim that the source implies is supported,** the mirror image of the qualifier test ("在分类时", "某些", 通常, 缓解).
- **`ambiguous` narrowed** to "never defined or unreadable", and shown as "资料未定义 / 无法核验" / "cannot verify".
- **Edges:** a paragraph about a field that introduces a method for the field's purpose supports `uses`, under three stated conditions.
- **Omissions:** a node with a compatible definition covers the source's definition; only missing parts such as a symbol legend count. Limitations sections are read sentence by sentence.
- **Recommendations** keep the definition's learning value (mark the unverified part as 资料外释义 instead of shrinking the definition) and add no claims of their own.

### Report and scripts

- **Source notes:** `detail` findings are listed in a folded "来源提示" / "Source notes" section after the other findings, because they mark a gap in the source, not an error.
- **Summary:** counts problems, source notes and omissions (core and supporting) separately. The top-three list leaves out source notes and low-risk items, and names omissions as "遗漏（核心内容）".
- **Evidence quotes are shown in full;** a 60-character cut had hidden the key word of a finding.
- **Portable image paths:** `validate_input.py` writes each image path relative to the output folder, with forward slashes (new `--out` option). A saved run next to its `images/` folder now resolves.
- **Checks:** `build_report.py` rejects `scope` on categories other than `unsupported-expansion`, and applies the low default risk to `detail` findings.

### Test data and privacy

- **Privacy section in the README:** the agent sends slide images and the tree to its AI provider. Only audit slides you may share, and treat the outputs like the slides.
- **Test data policy:** tests use only openly licensed, owner-written or synthetic material, never third-party course slides. The source's terms must also allow use with AI tools; OpenStax was ruled out for that reason.
- **`tests/fixtures/wiki-ml-zh`:** 12 screenshots of the Chinese Wikipedia article 机器学习 (revision 94516905).
- **`tests/fixtures/wiki-dt-zh`:** 6 screenshots of 决策树学习 (revision 93550494), with formulas and a worked calculation with exact numbers. The article titled 决策树 was not used because it carries a suspected copy-paste template.
- Both are under CC BY-SA 4.0 in their own folders, with attribution, the prompt used for the tree, the unedited Codex tree, every audit run, the agent's skill feedback and the owner's reviews.
- 91 tests, up from 77.

### Known limitations

- **The third rule revision has not been run yet.** It was made after the wiki-dt-zh review, and no fresh audit has used it.
- **The rules were tuned on the articles they were reviewed on.** wiki-dt-zh checked the first two revisions on a new article; the next new test set will check the third.
- **Partial reviews:** the owner has not judged the omissions of the wiki-ml-zh runs (25 per run).
- **One tree generator and one reviewer:** all real-content trees come from OpenAI Codex (model version not recorded), and all reviews are by the project owner.
- Only Claude has run the skill. Codex and other Agent Skills tools are untested.
- Small inputs: at most 12 pages and 98 tree items, all clean screenshots.
- Only PNG/JPG input; node `kind` is not audited; pytest 9.2.0 crashes on Python 3.10.0, so tests pin pytest 8.x.

### Next steps

1. **Codex:** run SourceTrace in Codex on the `wiki-ml-zh` inputs.
2. **Scale:** a synthetic deck of 30+ slides and a tree with 100+ nodes.
3. **Image quality:** scan- and photo-like versions of the test slides, generated by a script.
4. **Task modes:** a strict source-tracing mode and a review mode that allows short, marked explanations from outside the source.

## v0.1.0 (2026-11-03)

First release. SourceTrace audits an AI-generated knowledge tree against the slide images it was built from, and backs every verdict with evidence.

### Features

- **Six-stage workflow** for Agent Skills tools (Claude Code, Codex): source ingestion, evidence extraction, knowledge mapping, bidirectional audit, conflict detection, audit report.
- **Input:** slide images (PNG/JPG) and a knowledge tree in JSON, in Chinese or English.
- **Evidence index:** every slide title, bullet, table row and diagram relationship becomes an evidence item with an ID, page and verbatim quote.
- **A verdict for every node and edge**, each citing evidence. Nodes and edges are audited separately.
- **Six categories** chosen with a fixed decision order: conceptual error, incorrect relationship, unsupported expansion, overgeneralization, ambiguous, omission.
- **Risk levels** with defaults per category. Any change from the default needs a stated reason.
- **Omissions in two tiers:** core content at medium risk, supporting details at low risk. Examples, homework and content already covered by another finding are never reported.
- **Three scripts** for everything that can be checked or computed: `validate_input.py`, `validate_evidence.py` and `build_report.py`. The last one generates `report.md` from `audit.json` in Chinese or English.
- **Outputs:** `report.md`, `audit.json` and `evidence-index.json`, each with a JSON Schema.

### Evaluation

Two synthetic test sets: 4 English slides, and 8 Chinese slides with subtle errors. The full comparison is in [docs/evaluation.md](docs/evaluation.md).

- **Detection:** a plain AI assistant and SourceTrace both found every planted problem.
- **Precision:** SourceTrace flagged no correct items and reported nothing the rules exclude. The plain assistant did both in every run.
- **Traceability and structure:** SourceTrace gave a verdict for all 37 items in every run, each with evidence IDs, fixed categories, risk levels and `audit.json`.
- **Consistency:** four independent runs on the Chinese set agreed on the verdict, category and risk of all 37 items.
- **Cost:** about 30% more tokens and 3× the time of a plain request.
- **Tests:** a 77-test pytest suite covers the scripts and locks in the saved runs.

### Known limitations

- Tested only on two synthetic test sets written by the developer, with Claude.
- Only small decks (4 and 8 slides) and clean images.
- Only PNG/JPG input; PPT and PDF must be exported to images first.
- Node `kind` is not audited.
- `evidence-index.json` stores image paths as reported by the validator, which are relative and not portable between machines.
- Tested with pytest 8.x: pytest 9.2.0 crashes at startup on Python 3.10.0.

### Next steps

1. Openly licensed real content (the Chinese Wikipedia article 机器学习, CC BY-SA 4.0, in its own folder under that license), with the tree generated by a different AI tool and the report reviewed by the project owner as an independent answer key.
2. A synthetic deck of 30+ slides and a tree with 100+ nodes.
3. Scan- and photo-like versions of the test slides, generated by a script.
4. Codex and other Agent Skills tools.
