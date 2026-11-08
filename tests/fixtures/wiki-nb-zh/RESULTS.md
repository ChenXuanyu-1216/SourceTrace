# wiki-nb-zh results (2026-11-06)

Two fresh Claude agents ran SourceTrace on this test set: [audit-run-1](audit-run-1/) and [audit-run-2](audit-run-2/). Each had an isolated folder with only the skill, `images/` and `knowledge-tree.json`, and no web access. The skill was at commit `9b74d78`: the fourth rule revision and the fixes after the image-quality test. This is the first time those rules ran on an article that played no part in any rule.

The tree came from ChatGPT (GPT-6.1 Sol), not Codex, so it is also the first real-content tree from a second generator ([TREE-SOURCE.md](TREE-SOURCE.md)).

The answer key is [REVIEW.md](REVIEW.md). ChatGPT reviewed both runs in the same conversation that generated the tree, and the project owner accepted the review on 2026-11-06. The key is therefore owner-confirmed, but not independent of the tree's generator.

## Summary

| | audit-run-1 | audit-run-2 |
|---|---|---|
| Supported / item findings / omissions | 86 / 1 / 11 | 84 / 3 / 10 |
| Conceptual or relationship errors reported | 0 | 0 |
| Source notes (`detail`, low) | 1, correct (N022) | 3: N022 correct; N024 and N031 wrong |
| Omissions | 11 groups, all real: 5 correct, 6 partly correct | 10, all real; missed the limitations in 讨论 (low) |
| Errors in the tree the audit missed | none found by the review | none found by the review |
| Evidence items (certainty low) | 135 (1) | 146 (1) |
| Script runs | each script once, all passed | each script once, all passed |
| Cost | about 145k tokens, 9 minutes | about 132k tokens, 8 minutes |

The runs agree on 85 of 87 items. Both disagreements are the same rule question (below).

"Partly correct" here means the omission is real but the recommended fix needs narrowing, for example keeping the source's conditions ("适当预处理", "2006 年所引研究"), or not copying a source sentence that its own formula contradicts.

## What the results show

- **No high-risk false finding, no missed error.** The tree is mostly correct. Neither run reported a conceptual or relationship error, and the review found none they missed. All 86 items run 1 marked supported were upheld.
- **The main gap is found by both runs.** Both report the discretization method for continuous values (page 5) as the only core omission, at medium risk, and the review agrees.
- **Labels with outside terms split the runs.** N024 概率平滑修正 and N031 词袋表示 have fully supported definitions, but "平滑" and "词袋" are not in the source. Run 1 treated them as paraphrases; run 2 reported low-risk source notes. Read literally, question 1 ("term absent") would make both medium findings, and neither run did that. The review decided for run 1: judge the concept, not the label's exact wording.
- **Recommendations need the same care as findings.** Several omission fixes would copy the source too closely, including run 1's F-012, which repeats "概率比可以表达为似然比" although the source's formula keeps the prior ratio.
- **Web pages are not slides.** Both agents had to invent handling for overlapping screenshots, paragraphs split across pages, site menus and the navigation sidebar. Both runs cited the sidebar as evidence for N002, and run 1 also for E035 and E041.

## Questions both agents raised

From the two `skill-feedback.md` files:

1. Question 1's "term absent": the wording or the concept?
2. Web-page screenshots: overlaps, split paragraphs, site chrome and navigation boxes.
3. No format for writing out formulas.
4. What to do when the source contradicts itself or has a typo (S and ¬S called "相互独立"; "朴素贝叶斯方法都用到离散化方法" right after the Gaussian method; "估计各个变量的方法").
5. Omission tiers: no tier for history, applications and literature comparisons; the core "stated rule" and the supporting "property or caveat" overlap.
6. Windows: `python -I` ignores `PYTHONIOENCODING` (run 1).

These, and the review's own suggestions (REVIEW.md, section 6), are the input for the fifth rule revision.

## Re-run with the fifth revision (2026-11-07)

Two more fresh Claude runs, [audit-run-3](audit-run-3/) and [audit-run-4](audit-run-4/), set up the same way, with the skill at commit `80616a0`. Some examples in the fifth revision come from this article, so these runs show that the new rules are followed, not that they generalize.

| | audit-run-3 | audit-run-4 | Answer key |
|---|---|---|---|
| Supported / item findings / omissions | 86 / 1 / 13 | 86 / 1 / 12 | 86 / 1 (N022) / 11 groups |
| Item verdicts matching the key | 87/87 | 87/87 | |
| Key omission groups found | 11/11 | 11/11 | |
| Omissions outside the key | 0 | 1 (F-012, not judged) | |
| Source problems listed in the final message | 5, plus the cut-off formula | 6 | |
| Script runs | `build_report.py` twice, the others once; all passed | `validate_evidence.py` and `build_report.py` twice; all passed | |
| Cost | about 145k tokens, 11 minutes | about 166k tokens, 13 minutes | |

- **Both runs match the key on every item,** and agree with each other on all 87. N024 and N031 are now supported in both, and N022 is the only source note.
- **Every omission group in the key is found by both runs,** including the 讨论 limitations that run 2 missed. The counts differ (13 vs 12) only because the runs split the key's groups differently: run 3 lists training time, the curse of dimensionality and the parameter count as three entries, and the aliases apart from the 不一定用到贝叶斯方法 point.
- **One new omission, not yet judged:** run 4's F-012, the derivation of Bayes' theorem from the definition of conditional probability in the text-classification section (p(D|C) = p(D∩C)/p(C)). Run 4's F-007 also adds "类标签取自有限集合" to the key's "a family of algorithms" group.
- **Background omissions are labelled** 背景 in both runs (history, applications, other names, comparisons).
- **Recommendations no longer copy** "概率比可以表达为似然比". Run 3 rebuilt the report once to fix a recommendation that had merged two separate source points into one claim.
- **The navigation box is never cited on its own:** run 3 cites it for N002 and run 4 for E041, each together with the article's text.
- **Both runs listed the source's own problems** in the final message: the "相互独立" classes, "都用到离散化方法", "估计各个变量的方法", the 似然比 sentence, and "概率" vs "概率密度". Run 4 also noted the `e^{−09}` notation and the `∝` in the chain-rule expansion.

### Gaps the re-run found

1. **A source problem on a supported item has nowhere to go.** The rule says to explain it in the item's `reason`. Run 4 wrote a `reason` on seven supported items (N019, N025, N029, N033, N034, E030, E041); the schema allows it, but the report never shows it. Run 3 thought supported items cannot have a `reason` and used only the final message. The fifth revision introduced this gap. **Fixed after the re-run:** `build_report.py` now shows a supported item's `reason` as a note (说明) in the confirmed list, and the rules say a supported item's `reason` holds only such a note. The saved reports of these runs predate the fix.
2. **Overlapping screenshots:** "the page where it is first complete" and "the page where it starts" conflict when a sentence starts at the very bottom of one image and is repeated in full on the next.
3. **Several missing properties of one existing node:** one entry or one per property? This is why the omission counts differ.
4. **`∝` in the source where the tree says "展开为":** both runs judged N012 supported from the source's wording ("写成"), without a rule.
5. **Section nesting on a web page** (E030, 样本修正 next to 参数估计): both runs judged it from the content, not the position.
6. **Cost:** both runs took longer than the first two (11 and 13 minutes, against 8 and 9).
