# SourceTrace audit: Machine Learning

<!-- Smoke test, 2026-11-02. The agent harness blocked the sub-agent from writing report.md, so it returned this text and it was saved here unchanged. -->

## Summary

11 of 18 tree items are supported (5 nodes, 6 edges). There are 8 findings: 7 on tree items and 1 omission. By risk: 3 high, 4 medium, 1 low.

Most important problems:

1. N002 says supervised learning uses data that "does not require labels". The slides say it uses labeled data (EV-008, p.2).
2. E004 puts Regression under Unsupervised Learning. The slides list it as a supervised task (EV-011, p.2).
3. E007 says Supervised Learning includes Unsupervised Learning. They are sibling paradigms (EV-004/005, p.1).

## Findings

| ID | Category | Risk | Problem | Evidence | Recommendation |
|----|----------|------|---------|----------|----------------|
| N002 | conceptual-error | high | Definition says the opposite of the source | EV-008 p.2 "uses labeled data for training"; EV-019 p.4 | Change the definition to: training on labeled data, where each input comes with the correct output |
| E004 | incorrect-relationship | high | Regression is a supervised task | EV-011 p.2; EV-015/016 p.3 | Replace with N002 includes N005 |
| E007 | incorrect-relationship | high | The two are sibling paradigms, so neither includes the other | EV-004/005 p.1; EV-019/020 p.4 | Remove, or replace with N002 contrasts-with N003 |
| N008 | unsupported-expansion | medium | Deep learning does not appear in the slides | EV-003 p.1 "three main learning paradigms"; EV-004–006 | Remove |
| E008 | unsupported-expansion | medium | Same as N008 | EV-003–006 p.1 | Remove together with N008 |
| N006 | overgeneralization | medium | "every unsupervised learning task is a clustering task", but clustering is only one of two typical tasks | EV-015, EV-014, EV-016 p.3 | Change to: one typical unsupervised task |
| N009 | ambiguous | low | "Feedback" is only a table column header and is never defined; the table gives feedback for all three paradigms | EV-019–021 p.4 | Define it as correct answers / none / rewards |

## Omissions

| ID | Category | Risk | Problem | Evidence | Recommendation |
|----|----------|------|---------|----------|----------------|
| — | omission | medium | Dimensionality reduction is missing | EV-016 p.3 "compress features while keeping the structure of the data (e.g. PCA)" | Add a task node and the edge N003 includes it |

## Structure

No structural problems.

## Confirmed items

N001 (EV-002), N003 (EV-013, EV-020), N004 (EV-010), N005 (EV-011), N007 (EV-018, EV-021), E001 (EV-004), E002 (EV-005), E003 (EV-009, EV-010), E005 (EV-014, EV-015), E006 (EV-006), E009 (EV-021, EV-018).
