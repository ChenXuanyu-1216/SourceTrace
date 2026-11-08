# Skill feedback (SourceTrace, run on input/knowledge-tree.json + 6 page images)

## 1. Script runs

| Script | Runs | Result |
|--------|------|--------|
| `scripts/validate_input.py --json` | 1 | valid, no errors, no warnings (35 nodes, 48 edges, 6 images) |
| `scripts/validate_evidence.py` | 1 | VALID: 6 sources, 88 evidence items (5 graphic, 83 text) |
| `scripts/build_report.py` | 1 | written: 81 supported, 2 findings, 14 omissions (zh) |

No run failed, so nothing had to be changed in response to script errors.

## 2. Unclear, contradictory or missing instructions

1. **Overlapping screenshots: "first complete" vs "where it starts".** evidence-extraction.md says both "Extract each statement once, on the page where it is first complete" and "A sentence split across two images is one item on the page where it starts; say `continues on page N`". Several sentences here start on the cut-off last line of one image and are only complete on the next (EV-012, EV-045, EV-046, EV-069, EV-085, EV-086). The two rules point to different pages. I followed the more specific one (page where it starts) and wrote "continues on page N (read there)" in `location`.
2. **A split sentence whose second part is only on the next image.** The Novikoff sentence starts on the last line of page 5 but its second clause (the bound and R) is only on page 6. The rules do not say which page a *part* of a split sentence goes on. I put part 1 on page 5 and part 2 (EV-087) on page 6, where its text actually is.
3. **Is "R为输入向量的最大平均值" a source slip?** audit-rules.md gives examples of "an evident slip", but all of them are detectable from other content in the same source. Nothing in these pages contradicts "最大平均值", so I did not treat it as a source problem and judged the tree's "最大范数" against it. Then I had to choose between question 5 and question 6: "A different word for a different property is a detail ... Contradiction is not needed: if the two cannot both be true, question 5 applies instead." It was not obvious whether "cannot both be true" applies to two competing *definitions* of one symbol. I read it as yes (R cannot be defined as both) → `conceptual-error`. I mention in the user message that the wording is unusual, without asserting the correct value.
4. **Narrower claim vs. wrong range (N023, "0<α<1" where the source says "0 < α ≤ 1").** The rule "A narrower or more cautious claim that the source implies is `supported`" could be read as covering a stricter range. I decided it does not, because the tree states a *requirement* ("资料将其设为满足0<α<1") that excludes a value the source allows, so the source does not imply it. An explicit example of a range/inequality would help.
5. **Lowering the risk of a conceptual error.** The only example for a lower risk is "a wrong number in a minor example → medium". I extended it to an inequality endpoint (N023) and a symbol legend inside a supporting fact (N029) and gave `risk_reason`. That was a judgment call; the rules do not say whether a symbol legend counts as "minor".
6. **`contrasts-with` between two formulas (E017).** The source shows a 0/1 output in 定义 and a ±1 sign function in 结构 but never says they differ. The edge rules cover "stated", "agenda" and "paragraph" structures, not a contrast that is visible only by comparing two formulas. I judged it `supported` (the difference is in the evidence itself) and added a short source-problem note, because the two unreconciled conventions are an inconsistency in the source.
7. **Omission granularity for a long history section.** "One omission per missing concept" is hard to apply to a narrative history paragraph (events, people, books). I grouped by episode: precursors (1943/1949), Rosenblatt's own work, the 1969 book and its aftermath, the 1998 kernel-method work, plus Novikoff as the theorem's attribution. Another run might group differently, which changes the omission count.
8. **Aliases of two concepts.** "other names" is a background supporting detail, but it is unclear whether aliases of two different nodes (激励函数/传递函数 for 激活函数; 权量/权值 for 权重) should be one entry or two. I made two (one per concept).
9. **Wikipedia citation markers and hatnotes.** The rules do not say whether to keep reference markers such as "[1]" in verbatim quotes; I kept them. The disambiguation hatnote ("关于与'感知器'标题相近…") and the revision banner are not listed explicitly under site chrome (only "revision notices" is); I skipped both as site chrome.

Everything else (verdict order, label test, omission tiers, audit.json format, script usage) was clear.

## 3. Image difficulties

- The images are small (800×600). Formulas with subscripts and superscripts (formula (1), (2), (3), the update rule, the margin condition, (2R/γ)²) and the inequality "0 < α ≤ 1" were hard to read at native size. I made 2× enlarged crops in `work/` and re-read every formula and every word or number a finding depends on (α ≤ 1, "最大平均值") before writing them.
- The screenshots overlap and the last line of most images is cut horizontally. I read each such line on the next image, where it is complete, and recorded it once (see point 1 and 2 above).
- The neuron illustration on page 1 has illegible labels; I extracted only its caption. The output label "t" in the page 4 diagram is partly cut by the figure border, so that diagram item has `medium` certainty and the reading is confirmed by the text ("t为标量输出").
