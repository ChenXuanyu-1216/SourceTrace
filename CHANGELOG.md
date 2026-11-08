# Changelog

## Unreleased

- **First run by OpenAI Codex** (`tests/fixtures/wiki-ml-zh/codex-run-1`), with the v0.2.0 skill on the wiki-ml-zh inputs:
  - Codex followed the skill without help: all three scripts passed, and it read the images with its own image tool.
  - It matched 15 of the 18 items the owner has judged, the same score as Claude run 2 but on different items.
  - It reported 44 omissions where the Claude runs reported 25, mostly by listing each named model in the article's model list separately. The rules don't settle that granularity yet.
- **Scale test** (`tests/fixtures/sl-algos-zh`): a synthetic 32-slide Chinese lecture with a 169-item tree (78 nodes, 91 edges), 27 planted item problems and 8 planted omissions.
  - Two fresh Claude runs each found 27 of 28 item findings and all 8 omissions, flagged one correct item, and agreed on every item. Each took about 170k tokens and 8 minutes, in the range of the 98-item wiki-ml-zh runs.
  - Both runs found a mistake in the deck: the kernel slide never names SVM, so an edge meant to be correct has no support. The key now lists it as an unplanted finding.
  - The owner then revised the key: N078 is correct, N048 is a source note, Laplace smoothing stays a supporting omission, and four unplanned omissions are acceptable. Against the revised key, both runs match 28 of 28 item findings and flag no correct items ([RESULTS.md](tests/fixtures/sl-algos-zh/RESULTS.md#owners-decisions)).
- **Audit rules, fourth revision,** from the scale test: the owner's decisions on N078 and N048, and the questions both agents raised in their feedback. No run has used it yet.
  - **Question 7** applies the label test first: a definition that only spells out the name is supported, not `ambiguous`.
  - **A slide title does not define a class** described only through one member.
  - **Slide order supports no relationship;** only the agenda rule lets structure state one.
  - **Omissions:** a finding covers only the content it is about, and a topic whose members are all in the tree is covered.
  - **Evidence:** a bullet is split when its parts can be cited separately.
  - **Recommendations:** when no relation value fits (e.g. "mitigates"), delete the edge and state the relationship in a definition. `is-a` from a method to a task reads as "is a method for".
  - **SKILL.md** notes `PYTHONIOENCODING=utf-8` for the agent's own Python commands on Windows.
- **Rule fixes from the image-quality runs:**
  - "Do not fall back on `related-to`" applies only when no relation value fits; when only an end node is wrong, keep the relation and correct the node.
  - Partly unreadable evidence is split into a readable item and a `low` item with the placeholder ［无法辨认］, and hidden text is never filled in.
  - Working files go in a `work/` folder inside the output folder.
- **Image-quality test:** `tools/degrade_images.py` makes seeded scan, photo and occluded versions of a test set's slides (`tests/fixtures/model-eval-scan`, `-photo`, `-occluded`). Two fresh Claude runs on each, the first runs with the fourth rule revision:
  - Scan and photo versions changed nothing: all findings and omissions found, all evidence read with high certainty, and full agreement.
  - On the occluded version, both runs marked hidden evidence `low`, did not guess the hidden ratio (N005 "cannot verify"), and did not fill in the hidden definition. They kept N015 as a conceptual error from the readable recall row; the owner accepted that as well as "cannot verify" ([RESULTS.md](tests/fixtures/model-eval-occluded/RESULTS.md)).
  - Three runs reported one new low-risk omission (L2 "使权重整体变小"), probably an effect of the fourth rule revision. The owner accepted it as an optional omission in all model-eval keys.
  - `compare_runs.py` reports evidence certainty and skips the risk check when a run gives an accepted alternative category.
- **Fresh-article test** (`tests/fixtures/wiki-nb-zh`): 10 screenshots of the Chinese Wikipedia article 朴素贝叶斯分类器 (CC BY-SA 4.0), with a 35-node, 52-edge tree from ChatGPT (GPT-6.1 Sol), the first real-content tree not made by Codex. Two fresh Claude runs with the fourth rule revision and the fixes after it ([RESULTS.md](tests/fixtures/wiki-nb-zh/RESULTS.md)):
  - Neither run reported a conceptual or relationship error, and the review found none they missed. Both found the one core omission (the discretization method for continuous values).
  - The runs agreed on 85 of 87 items. Run 2 reported two labels with terms not in the source (词袋, 平滑) as source notes; the review counts them as supported, as run 1 did. Run 2 also missed one low-risk omission.
  - All omissions were real, but several recommended fixes need narrowing, e.g. not copying a source sentence that its own formula contradicts.
  - The answer key is an AI-assisted review (ChatGPT, in the conversation that made the tree) that the owner accepted, so it is not independent of the tree's generator.
- **Fresh-article test for the fifth revision** (`tests/fixtures/wiki-pc-zh`): 6 screenshots of the Chinese Wikipedia article 感知器 (CC BY-SA 4.0), the first real-content set with figures as evidence, and a 35-node, 48-edge tree from Codex (GPT-6.1 Sol) in a new conversation. Two fresh Claude runs ([RESULTS.md](tests/fixtures/wiki-pc-zh/RESULTS.md)):
  - Same verdict, category and risk on all 83 items, the first real-content test with no item disagreement. Both runs found the two real tree errors (N023, a wrong interval end point; N029, a definition of R that differs from the source), and the review overturned none of the 81 supported items.
  - Both used the structure diagram as `graphic` evidence. A note on a supported item appeared in the report.
  - Both missed one low-risk omission, and four problems in the source that take a short derivation to see (e.g. "E(w)是一组正数的和" fails at the boundary). Both even recommended copying that sentence into the tree.
  - The answer key is a review by Codex in a separate session, accepted by the owner: independent of the tree's session, not of its model.
- **Audit rules, fifth revision,** from the owner's decisions on wiki-nb-zh and the questions both agents raised. Two re-runs on wiki-nb-zh (`audit-run-3`, `audit-run-4`) match the answer key on all 87 items and find all 11 omission groups; they also showed that a source problem on a supported item had no visible place in the report, so `build_report.py` now shows a supported item's optional `reason` as a note (说明 / Note) in the confirmed list ([RESULTS.md](tests/fixtures/wiki-nb-zh/RESULTS.md#re-run-with-the-fifth-revision-2026-11-07)). Some examples come from wiki-nb-zh, so a re-run on that article can only show that the rules are followed; a fresh article is needed to show they generalize.
  - **Question 1 is about the concept, not the word:** a label from outside the source is supported when the source describes what it names (词袋表示, 概率平滑修正). Only a claim the name adds is checked, as a `detail`.
  - **Web pages and documents** (evidence-extraction.md): overlapping screenshots, split paragraphs, site chrome, and navigation boxes, which can back up the article's text but never stand alone or create an omission.
  - **Formulas** are transcribed as linear Unicode text, exactly as printed.
  - **Problems in the source itself** are quoted as printed, judged by the more specific evidence, explained in the item's `reason` and listed in the final message, with no new category or schema change.
  - **Omissions:** a rule or caveat about a concept that has a node is supporting; history, applications, other names and comparisons are supporting background; a missing claim appears in only one entry; a supported node does not cover a limitation it leaves out.
  - **Recommendations** are checked like findings: they keep the source's conditions and do not copy a source sentence that other evidence contradicts.
  - **SKILL.md** suggests `python -X utf8` on Windows, since `python -I` and `-E` ignore `PYTHONIOENCODING`.
- **Audit rules, sixth revision,** from the open questions of the wiki-pc-zh runs and the wiki-nb-zh re-runs. Small changes, with no new category or schema field. No run has used it yet.
  - **Check a source claim before relying on it:** before a recommendation quotes a general claim of the source, test it against the source's own formulas at the boundary cases and other conventions (e.g. "E(w)是一组正数的和" fails because f(0)=+1). A claim that fails is a source problem, handled as before in `reason` and the final message.
  - **A slip only outside knowledge reveals** (N029 "最大平均值") is judged against the printed text; the recommendation marks the tree's version as an outside explanation to check, and the final message calls it a possible slip.
  - **Overlapping screenshots:** a statement goes on the first page that shows all of it; "the page where it starts" applies only when no single image does.
  - **Omissions:** one entry per node or topic. A node's missing details form one entry; background is one entry per kind in each section, so a long history section is one entry and the other names of several concepts are one. A convention a formula relies on (b = 0) is a supporting detail.
  - **A wrong end point of a range** that the tree gives as the source's condition (0<α<1 vs 0 < α ≤ 1) is a `conceptual-error`, not a narrower claim, at risk `medium` when the rest of the definition is right. A claim attributed to the source ("资料给出的") must match the source.
  - **`contrasts-with`** is supported by two formulas or conventions for the same thing, even if the source never compares them (E017).
  - **The label test comes before the single-instance rule:** a class definition that only says what the name means is supported (N003 线性分类器).
  - **Smaller points:** `=`/展开为 vs `∝`; web-page heading levels neither state nor rule out a relationship; a formula on a different page from its intro sentence; citation markers [n] are left out of quotes; disambiguation notes and reference lists are site chrome.
- **`tools/make_fixture_slides.py`** builds decks from data files in `tools/decks/`, with bullets, tables, flow and tree diagrams, and stops if a slide overflows.
- **`tools/compare_runs.py`** also checks `scope` (`detail` or `whole`) against the key, and counts omissions that match an acceptable extra in the key as accepted. Its item count is now labelled `expected items`.

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
