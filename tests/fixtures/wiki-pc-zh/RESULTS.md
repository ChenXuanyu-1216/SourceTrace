# wiki-pc-zh results (2026-11-07)

Two fresh Claude agents ran SourceTrace on this test set: [audit-run-1](audit-run-1/) and [audit-run-2](audit-run-2/). Each had an isolated folder with only the skill, `images/` and `knowledge-tree.json`, and no web access. The skill was at commit `1dbd02b`: the fifth rule revision, and notes on supported items in the report. This is the first time the fifth revision ran on an article that played no part in any rule, and the first real-content test where figures carry evidence.

The tree came from OpenAI Codex (GPT-6.1 Sol) in a new conversation ([TREE-SOURCE.md](TREE-SOURCE.md)). It passed validation on the first try.

The answer key is [REVIEW.md](REVIEW.md). Codex (GPT-6.1 Sol, high) reviewed both runs in a new session, separate from the one that made the tree, and the project owner accepted the review on 2026-11-07. The key is independent of the session that made the tree, but not of the model.

## Summary

| | audit-run-1 | audit-run-2 |
|---|---|---|
| Supported / item findings / omissions | 81 / 2 / 14 | 81 / 2 / 9 |
| Item findings | N023 correct; N029 partly correct | same |
| Supported items overturned by the review | 0 of 81 | 0 of 81 |
| Omission groups (10 in the review) | 9 found: 6 correct, 3 partly correct; missed the bias descriptions | 10 found: 6 correct, 4 partly correct |
| Omissions both runs missed | 1, low (the bias convention b = 0 in the learning section) | same |
| Evidence items | 88 (5 `graphic`, 1 `medium`) | 87 (4 `graphic`) |
| Script runs | each script once, all passed | each script once, all passed |
| Cost | about 143k tokens, 9 minutes | about 145k tokens, 9 minutes |

The runs gave the same verdict, category and risk on all 83 items, the first real-content test with no item disagreement. The omission counts differ only in grouping: run 1 split history, limitations and other names into several entries.

## What the results show

- **No false finding on the tree, no missed error.** Both item findings are real:
  - **N023:** the tree says the source sets "0<α<1"; the source says "0 < α ≤ 1".
  - **N029:** the tree says R is the inputs' "最大范数"; the source says "最大平均值". The source is probably wrong here, but nothing in it shows that. The review accepts judging against the source's text and warning the user, but says the finding must only say that the tree differs from the source, not that it is wrong in mathematics. The recommendation should not put the source's likely slip back into the tree.
- **Figures are used as evidence.** Both runs extracted the structure diagram on page 4 as `graphic` items and used them, with formula (1), for N007, N010, N012 and the structure edges. The review upheld all of them. The neuron figure's labels are too small to read, and both runs extracted only its caption, as the rules ask.
- **Notes on supported items work.** Run 1's note on E017 (0/1 in the definition, ±1 in the structure section) appears in its report's confirmed list.
- **Problems in the source that need reasoning are not found.** The review found four, all provable from the screenshots:
  - "E(w)是一组正数的和" fails at the boundary: f(0) = +1, so a misclassified term with wᵀpᵢ = 0 and tᵢ = −1 is 0.
  - With the 0/1 labels of the definition section, the margin condition yᵢ(w·xᵢ+b) > γ cannot hold. The source never says to switch to ±1.
  - The bound (2R/γ)² has no scale constraint: scaling w, b and γ by c keeps the condition but changes the bound.
  - "反对称的符号函数" is not antisymmetric at 0, since f(0) = +1.

  Neither run noticed them. Both reported only wording slips (a doubled 的, "叫被做", a stray colon), and both recommended adding "E(w)是一组正数的和" to N020. That breaks the fifth revision's rule against copying a source sentence that other evidence in the source contradicts, although here the contradiction takes a short derivation to see.

## Questions both agents raised

From the two `skill-feedback.md` files, and REVIEW.md section 5:

1. Overlapping screenshots: "the page where it is first complete" and "the page where it starts" conflict. This was also raised in the wiki-nb-zh re-run.
2. A slip that only outside knowledge reveals (N029): is it "evident"?
3. A wrong interval end point (N023): conceptual error or a narrower claim, and at what risk?
4. `contrasts-with` when the source never compares the two things, but their formulas differ (E017).
5. Grouping omissions: long history passages, and other names of several concepts.
6. The label test and "a class defined from a single instance" (N003).
7. A formula on a different page from the sentence that introduces it; Wikipedia citation markers and disambiguation notes.

These, the reasoning-only source problems, and the open points from wiki-nb-zh are the input for the small rule fixes (step 2 of the delivery plan).
