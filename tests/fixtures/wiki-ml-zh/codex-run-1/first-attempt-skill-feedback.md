# Skill feedback

## 1. Script runs

| Script | Runs | Result |
|---|---|---|
| `validate_input.py` | 1 | Failed: `valid: false`, two `FILE_NOT_FOUND` errors. |
| `validate_evidence.py` | 0 | Not run: source ingestion failed. |
| `build_report.py` | 0 | Not run: no valid input, evidence index or audit judgments. |

Command, run from `source-trace/`:

```text
python scripts/validate_input.py --tree ../input/knowledge-tree.json --images ../input/images --json
```

Reported errors:

```text
Knowledge tree not found: ../input/knowledge-tree.json
Image not found: ..\input\images
```

No input files were changed, substituted or fabricated. The validator reported zero nodes, zero edges and no images; the requested 12-page / 40-node / 58-edge input could not be verified. This feedback file is stored in the requested default output location, `input/sourcetrace-output/`. No `report.md`, `audit.json` or `evidence-index.json` was generated.

## 2. Instruction clarity and decisions

Read `source-trace/SKILL.md`, `source-trace/references/evidence-extraction.md` and `source-trace/references/audit-rules.md`, all within the workspace. No web browsing or files outside the workspace were used.

The applicable instruction was explicit: “Errors (`\"valid\": false`): stop, show the user the errors in plain words, and ask them to fix the input. Do not audit an invalid tree.” Accordingly, auditing stopped at stage 1; no different fixture was assumed to be the intended input.

No ambiguity prevented the ingestion check. Later extraction and judgment rules were read but not exercised, so this run cannot assess their practical clarity on the requested dataset. The feedback file records an incomplete run, not a completed audit.

## 3. Image reading

No images were opened. The input validator could not find the requested image folder, so there were no image paths available for visual reading. This is a missing-input issue, not an assessment that any page is illegible. No OCR or image-reading tool was used.
