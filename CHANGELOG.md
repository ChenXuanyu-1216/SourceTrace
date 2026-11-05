# Changelog

## Unreleased

- **Privacy section in the README:** the agent sends slide images and the tree to its AI provider; only audit slides you may share, and treat the outputs like the slides.
- **Test data policy:** tests use only openly licensed, owner-written or synthetic material, never third-party course slides. The source's terms must also allow use with AI tools: OpenStax was ruled out for that reason. The next steps below were revised to match.
- **New test set `tests/fixtures/wiki-ml-zh`:** 12 screenshots of the Chinese Wikipedia article 机器学习 (revision 94516905), under CC BY-SA 4.0 in its own folder, with attribution and a prompt for generating the knowledge tree with another AI tool.
- **Codex-generated knowledge tree and first real-content audit** for `wiki-ml-zh` (`audit-run-1`), with the project owner's review of 13 findings: 6 correct, 4 partly correct, 3 wrong.
- **Audit rules revised after that review:**
  - **Gather all evidence first:** text, tables and figures on every page, combined across pages.
  - **Contradiction test:** a conceptual error must contradict the source in meaning, not just use opposite-looking words. This fixes the false high-risk Bayesian-network finding.
  - **New `scope: detail`** for an `unsupported-expansion` limited to one added detail of an otherwise supported definition, with low risk by default. `build_report.py` and the audit schema check it.
  - **`ambiguous` narrowed** to "never defined or unreadable", and shown as "资料未定义 / 无法核验" / "cannot verify".
  - **Recommendations keep the definition's learning value:** mark the unverified part instead of shrinking the definition.
- **Second audit on `wiki-ml-zh` (`audit-run-2`)** with the revised rules: 10 of the 13 reviewed findings now match the owner's review, including all 3 false positives (no high-risk finding remains). Of the 3 mismatches, one (集成学习, now supported) is a case the rules don't cover. The other two change category but keep the same low risk. Four items that run 1 supported are now low-risk `detail` findings and are waiting for review.
- **Owner's review of the 8 items that changed in run 2:** 4 correct, 1 partly correct, 3 wrong. Across the 18 run-2 items judged so far: 14 correct, 1 partly correct, 3 wrong.
- **Rules revised after that review:**
  - **An explanation of the term is not a detail:** a part of a definition is a separate claim only if it could be false while the rest is true (过拟合 "过度适应训练数据" is supported).
  - **A class defined from a single instance** is a `detail` finding (集成学习 from random forest).
  - **Only the unsupported fragment is the finding;** a non-contradicting word difference becomes optional wording in the recommendation.
  - **A method introduced in a paragraph about a field supports `uses`,** only under three stated conditions.
  - **Recommendations add no claims of their own.**
- **Second real-content test set `tests/fixtures/wiki-dt-zh`:** 6 screenshots of the Chinese Wikipedia article 决策树学习 (revision 93550494), under CC BY-SA 4.0 in its own folder, to check that the revised rules were not tuned to one article. It adds formulas and a worked calculation with exact numbers. The article titled 决策树 was not used, because it carries a suspected copy-paste template. The knowledge tree comes from OpenAI Codex, saved unedited. The first audit (`audit-run-1`) supports 77 of 81 items, gives 4 low-risk source notes and 7 omissions.
- **Owner's review of that audit:** of 11 findings, 8 correct, 1 partly correct and 2 wrong; 2 low-risk omissions missed; all 77 supported items upheld.
- **Rules revised after that review:**
  - **A narrower or more cautious claim that the source implies is supported,** the mirror image of the qualifier test (装袋法 "在分类时", "某些决策树方法", 通常, 缓解).
  - **A different word for a different property is a detail** (多路划分 vs 多层分裂); a different word for the same thing is not.
  - **A node with a compatible definition covers the source's definition;** only missing parts such as a symbol legend are omissions.
  - **Limitations sections are read sentence by sentence,** with a 缺点 example in the supporting-detail tier.
- **Report fixes:**
  - Evidence quotes are shown in full; a 60-character cut had hidden the key word of a finding.
  - The summary counts problems, source notes and omissions (core and supporting) separately.
  - The top-three list names omissions ("遗漏（核心内容）") instead of showing "—", and leaves out low-risk items.
- **Portable image paths:** `validate_input.py` writes each image path relative to the output folder, with forward slashes (new `--out` option for a non-default folder). A saved run next to its `images/` folder now resolves. This removes a known limitation of v0.1.0.
- **Source notes in the report:** `detail` findings are now listed in a folded "来源提示" / "Source notes" section after the other findings, numbered after them, and left out of the top three. `audit.json` and its summary are unchanged.

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
