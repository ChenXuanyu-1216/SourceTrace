# Audit rules

<!-- v0.1 interim rules. To be finalized on Day 6 (bidirectional review rules). -->

How to decide verdicts, categories and risk levels in stages 4 and 5.

## Verdicts

Every node and every edge gets exactly one verdict:

| Verdict | When |
|---------|------|
| `supported` | The evidence says the same thing. Paraphrase is fine if the meaning, numbers and qualifiers are unchanged. |
| `finding` | Anything else. The finding gets one category from the table below. |

A `supported` verdict also cites its evidence IDs. "Looks fine" without evidence is not a verdict.

## Categories

Pick the first category that fits, in this order:

1. **`unsupported-expansion`:** no evidence mentions the content at all. Cite the evidence that shows what the source *does* say instead, if any (e.g. the slide that lists the actual members of a group).
2. **`incorrect-relationship`:** for edges whose relationship contradicts the evidence, including reversed or swapped edges. Judge the edge on its own, even if one of its nodes also has a finding.
3. **`overgeneralization`:** the claim is supported, but a qualifier was strengthened ("通常" → "总是", "usually" → "always", "one of" → "the only", "最…"), or the scope was widened beyond what the source covers. Use this even when another page contradicts the strengthened version.
4. **`conceptual-error`:** the definition contradicts the evidence: opposite meaning, wrong number, swapped definitions, a wrong added clause.
5. **`ambiguous`:** the claim is too vague to confirm or reject, or the only relevant evidence has `low` certainty.

When a definition is partly right and partly wrong, the wrong part decides the category. Say in `reason` which part is correct.

## Default risk

| Risk | Categories |
|------|------------|
| `high` | `conceptual-error`, `incorrect-relationship` |
| `medium` | `unsupported-expansion`, `overgeneralization`, `omission` |
| `low` | `ambiguous` |

Raise or lower the default only with a reason in the finding, e.g. an omission of the lecture's central concept → `high`; a wrong number in a minor example → `medium`.

## Omissions (source → tree)

Report an omission when source content of these kinds has no matching node or edge:

- a topic named in a slide title or an agenda/overview slide,
- a defined term or a stated rule ("X is …", "X should …"),
- a row of a table, or a relationship shown in a diagram,
- a main point of a slide that the tree only covers partly (e.g. the tree has both ends of a trade-off but not the trade-off itself).

Do **not** report:

- examples in parentheses (e.g. "e.g. k-means") when the concept they illustrate is in the tree,
- administrative text: homework, reading lists, course logistics,
- content already covered by a finding on an existing node or edge (e.g. do not also report "test set may only be used once" as missing when the test-set node already has a finding that cites it, or "Supervised includes Regression" as missing when the wrong edge for Regression already has a finding that recommends it).

One omission per missing concept; group its details into that one finding.

## Edge cases

- **True but incomplete edge:** an edge whose relationship holds but tells only part of the story (e.g. linking a concept to one paradigm when the source applies it to all three) is `supported`. Mention the incompleteness in the related node's finding, if there is one.
- **Content needing two pages:** combine them. Cite both evidence IDs.
- **Evidence only in a diagram or table:** equally valid as text. Cite the `graphic` or `table` item.
- **`low` certainty evidence:** cannot reject a tree item on its own; use `ambiguous` and say which page needs checking.
- **Structure warnings** from `validate_input.py` (disconnected parts, isolated nodes, duplicate edges) go in the report's Structure section, not in the findings list. When the source shows how disconnected parts belong together (e.g. an agenda slide), say so with its evidence ID.
