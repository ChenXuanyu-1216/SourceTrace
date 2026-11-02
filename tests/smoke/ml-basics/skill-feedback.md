# Skill feedback (smoke run on ml-basics-style input)

Overall the workflow was clear and the scripts ran without problems. The places below are where I had to guess or interpret.

1. **`path` in `sources`.** evidence-extraction.md: "copy its `summary.images` list into `sources`". The validator returns paths relative to the directory it was run from (`..\\input\\images\\slide-01.png`, because SKILL.md says to run scripts from the skill folder). Copied verbatim, the path is relative to the skill folder, not to the evidence index, and uses Windows backslashes. I copied it verbatim. It is unclear whether `path` should be relative to the index file, absolute, or as-given.

2. **What `findings` in `summary` counts.** The `audit.json` example shows `"findings": 8` but does not say whether omissions are included. I included them (7 item findings + 1 omission), which also makes `supported + findings` != nodes + edges. `by_risk` likewise includes the omission. A one-line definition would remove the guess.

3. **`ID` column in the report table.** SKILL.md: "table sorted by risk, then page: ID | Category | Risk | ...". Findings have no ID of their own in `audit.json`, so I used the target node/edge ID. If a finding ID (e.g. F-001) was meant, it is not defined anywhere.

4. **"sorted by risk, then page".** A finding can cite several pages (E004 cites p.2 and p.3; N002 cites p.2 and p.4). I sorted by the lowest page cited. Not specified.

5. **Undefined term in the source (N009 Feedback).** The source only uses "Feedback" as a table column header. The category order in audit-rules.md did not clearly fit: it is not `unsupported-expansion` ("no evidence mentions the content at all" — the word is mentioned, the definition is not), not contradicted, and the evidence is `high` certainty. I chose `ambiguous` ("too vague to confirm or reject"), but a definition that is plausible but not stated in the source is a recurring case and deserves an explicit rule (is an unstated definition of a mentioned term `unsupported-expansion` or `ambiguous`?).

6. **Interaction between the "true but incomplete edge" rule and the omission rules.** audit-rules.md says for an incomplete edge to "Mention the incompleteness in the related node's finding, if there is one", and the omission rules say not to report content "already covered by a finding on an existing node". I put the missing feedback-for-all-paradigms comparison (table rows EV-019/EV-020) into the N009 finding and therefore did not report a separate omission for the comparison table. This felt right but required combining three rules; if N009 had been `supported`, it is unclear whether the comparison would then become an omission.

7. **Missing edge vs. wrong edge (Regression).** Regression is attached to the wrong parent (E004). The correct relationship (Supervised includes Regression) is missing from the tree, which is also "a relationship shown in a diagram"/stated rule. I did not report it as a separate omission, using the rule "content already covered by a finding on an existing node" by analogy (it is covered by an edge finding, the rule only says "node"). Saying "node or edge" would make this explicit.

8. **N006 category: overgeneralization vs. conceptual-error.** "every unsupervised learning task is a clustering task" could be read as a "wrong added clause" (`conceptual-error`) or a widened scope (`overgeneralization`). The "pick the first category that fits" order plus "Use this even when another page contradicts the strengthened version" resolved it to `overgeneralization`. This worked, but the "wrong added clause" example under conceptual-error overlaps.

9. **`kind` mismatch not covered.** The slides call Classification, Regression and Clustering "tasks", while the tree gives them `kind: concept` (the schema has a `task` kind). The rules do not say whether a wrong `kind` is a finding. I treated the nodes as `supported` on their label and definition and did not report it.

10. **Reference example file missing.** evidence-extraction.md says "The full example is `tests/fixtures/ml-basics/evidence-index.example.json`", but no `tests/` folder is shipped with the skill. The inline snippet was enough, so it did not block me.

11. **Interim audit rules.** audit-rules.md contains the comment "v0.1 interim rules. To be finalized on Day 6". I followed them as written.

## Environment note (not a skill problem)

Writing `report.md` was refused by the agent harness ("Subagents should return findings as text, not write report files"), apparently because of the file name. I did not work around the block; the report content was returned in my final message instead. `evidence-index.json`, `audit.json` and this file were written normally. If the skill is run by subagents, this harness rule can stop stage 6 from producing `report.md`.
