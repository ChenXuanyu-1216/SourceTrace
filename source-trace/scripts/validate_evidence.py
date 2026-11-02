"""Validate an evidence index produced in stage 2 (evidence extraction).

Checks the index against schemas/evidence-index.schema.json, then the
cross-references the schema cannot express: unique evidence IDs, sources
numbered 1..n, and every evidence item pointing at a listed source and page.

Usage:
    python validate_evidence.py --index evidence-index.json
    python validate_evidence.py --index evidence-index.json --json

Exit codes: 0 valid (warnings allowed), 1 invalid index, 2 usage error.
Requires: jsonschema (pip install jsonschema).
"""

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

from validate_input import Report, json_path

SCHEMA_DIR = Path(__file__).resolve().parent.parent / "schemas"


def load_index(path, report):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        report.error("FILE_NOT_FOUND", f"Evidence index not found: {path}")
    except json.JSONDecodeError as e:
        report.error("INVALID_JSON", f"Evidence index is not valid JSON: {e}")
    except UnicodeDecodeError:
        report.error("INVALID_JSON", "Evidence index is not UTF-8 text.")
    return None


def check_schema(index, report):
    try:
        from jsonschema import Draft202012Validator
        from referencing import Registry, Resource
    except ImportError:
        sys.exit("validate_evidence.py needs the jsonschema package: pip install jsonschema")

    schemas = {}
    for name in ("evidence-index.schema.json", "evidence.schema.json"):
        with open(SCHEMA_DIR / name, encoding="utf-8") as f:
            schemas[name] = json.load(f)
    registry = Registry().with_resources(
        (s["$id"], Resource.from_contents(s)) for s in schemas.values())
    validator = Draft202012Validator(schemas["evidence-index.schema.json"], registry=registry)
    for err in sorted(validator.iter_errors(index), key=lambda e: list(e.absolute_path)):
        report.error("SCHEMA", err.message, json_path(err.absolute_path))


def check_references(index, report):
    """Checks beyond the schema. Tolerates malformed items, which check_schema reports."""
    sources = [s for s in index.get("sources", []) if isinstance(s, dict)] \
        if isinstance(index.get("sources"), list) else []
    evidence = [e for e in index.get("evidence", []) if isinstance(e, dict)] \
        if isinstance(index.get("evidence"), list) else []

    for field, code in (("source_id", "DUPLICATE_SOURCE_ID"), ("page", "DUPLICATE_PAGE")):
        for value, count in Counter(s.get(field) for s in sources if field in s).items():
            if count > 1:
                report.error(code, f"Source {field} {value} is listed {count} times.")
    pages = sorted(p for p in (s.get("page") for s in sources) if isinstance(p, int))
    if pages and pages != list(range(1, len(pages) + 1)):
        report.error("PAGE_GAP", f"Source pages must be numbered 1 to {len(pages)}; found {pages}.")

    for evidence_id, count in Counter(e.get("evidence_id") for e in evidence if "evidence_id" in e).items():
        if count > 1:
            report.error("DUPLICATE_EVIDENCE_ID", f"Evidence ID {evidence_id} is used {count} times.")

    # A duplicated source_id has no single page; DUPLICATE_SOURCE_ID already covers it.
    id_counts = Counter(s.get("source_id") for s in sources)
    page_of = {s.get("source_id"): s.get("page") for s in sources}
    cited = set()
    for i, item in enumerate(evidence):
        source_id = item.get("source_id")
        if source_id not in page_of:
            report.error("UNKNOWN_SOURCE",
                         f"{item.get('evidence_id')} cites source {source_id}, which is not in sources.",
                         f"$.evidence[{i}].source_id")
        elif id_counts[source_id] == 1 and item.get("page") != page_of[source_id]:
            report.error("PAGE_MISMATCH",
                         f"{item.get('evidence_id')} says page {item.get('page')}, "
                         f"but source {source_id} is page {page_of[source_id]}.",
                         f"$.evidence[{i}].page")
        cited.add(source_id)

    for s in sources:
        if s.get("source_id") not in cited:
            report.warning("EMPTY_SOURCE", f"No evidence was extracted from page {s.get('page')} "
                                           f"({s.get('source_id')}).")

    low = [e.get("evidence_id") for e in evidence if e.get("certainty") == "low"]
    if low:
        report.warning("LOW_CERTAINTY", f"{len(low)} item(s) have low certainty and cannot reject "
                                        f"a tree item on their own: {', '.join(map(str, low))}.")

    return len(sources), len(evidence), Counter(e.get("type") for e in evidence)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate a SourceTrace evidence index.")
    parser.add_argument("--index", required=True, help="evidence index (JSON)")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)

    report = Report()
    source_count = evidence_count = 0
    types = Counter()
    index = load_index(args.index, report)
    if index is not None:
        check_schema(index, report)
        if isinstance(index, dict):
            source_count, evidence_count, types = check_references(index, report)

    result = {
        "valid": not report.errors,
        "errors": report.errors,
        "warnings": report.warnings,
        "summary": {"sources": source_count, "evidence": evidence_count, "by_type": dict(types)},
    }

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        s = result["summary"]
        by_type = ", ".join(f"{n} {t}" for t, n in sorted(s["by_type"].items(), key=str)) or "none"
        print(f"{'VALID' if result['valid'] else 'INVALID'}: {s['sources']} sources, "
              f"{s['evidence']} evidence items ({by_type})")
        for level in ("errors", "warnings"):
            for item in result[level]:
                where = f" at {item['path']}" if item["path"] else ""
                print(f"  {level[:-1].upper()} {item['code']}{where}: {item['message']}")
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
