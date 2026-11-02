---
name: source-trace
description: Trace claims back to their original sources and verify them across text, PDFs, web pages, images, audio, and video. Use this skill whenever the user wants to fact-check a statement, find where a quote, figure, statistic, or image came from, check whether a summary or report faithfully reflects its sources, or audit citations, even if they don't say "verify" or "trace" explicitly (e.g. "is this true?", "where did this number come from?", "does this paper actually say that?").
---

# SourceTrace

<!-- DRAFT: scaffold only. Refine the workflow once the scope is settled. -->

SourceTrace turns a piece of content into a set of checkable claims, follows each claim back to the evidence it rests on, and reports how well that evidence supports it. The point is to make the chain from claim to source visible, so the reader can judge it for themselves instead of trusting a bare verdict.

## Workflow

1. **Extract claims.** Break the input into atomic, checkable claims (one fact per claim). Keep the exact wording and where it appeared, because paraphrasing at this stage hides drift later.
2. **Identify modality.** Note what each claim refers to: text, a table or a diagram. See `references/evidence-extraction.md` for how to record each.
3. **Trace.** Find the earliest or most authoritative source for each claim. Prefer primary sources over coverage of them, and record the precise location (page, timestamp, URL, figure number).
4. **Verify.** Compare the claim with the source and assign a verdict:
   - `supported`: the source says this.
   - `partially-supported`: the source says something close, but the claim overstates, omits a qualifier, or changes a number.
   - `contradicted`: the source says otherwise.
   - `unverifiable`: no source could be found or accessed.
5. **Report.** Use the template below.

## Report format

```markdown
# SourceTrace report

## Summary
<one paragraph: how many claims, how many in each verdict, the most important problems>

## Claims
| # | Claim | Verdict | Source (exact location) | Notes |
|---|-------|---------|-------------------------|-------|
```

Quote the source sparingly and only as much as needed to show the match or mismatch.
