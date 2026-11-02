"""Finalize audit.json and generate report.md (stage 6).

The agent writes the judgments (`items` and `omissions`) into audit.json. This
script checks them against the knowledge tree and the evidence index, then
fills in what can be computed: `summary`, `structure_warnings` and a
`finding_id` for every finding, numbered in report order. It rewrites
audit.json and writes report.md next to it. Running it again gives the same
result, so it is safe to rerun after fixing errors.

Usage:
    python build_report.py --tree knowledge-tree.json --index evidence-index.json --audit audit.json
    python build_report.py ... --lang zh      (report language: auto, zh or en; default auto)

Exit codes: 0 written (warnings allowed), 1 invalid audit (nothing written), 2 usage error.
Requires: jsonschema (pip install jsonschema).
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

from validate_input import Report, check_structure, connected_parts, json_path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "audit.schema.json"
RISKS = ("high", "medium", "low")
DEFAULT_RISK = {
    "conceptual-error": "high",
    "incorrect-relationship": "high",
    "unsupported-expansion": "medium",
    "overgeneralization": "medium",
    "ambiguous": "low",
}
DEFAULT_OMISSION_RISK = {"core": "medium", "supporting": "low"}
QUOTE_CHARS = 60

LABELS = {
    "en": {
        "title": "SourceTrace audit", "summary": "Summary", "findings": "Findings", "omissions": "Omissions",
        "structure": "Structure", "confirmed": "Confirmed items", "no_structure": "No structural problems.",
        "none": "None.", "top": "Most important problems:",
        "cols": ["ID", "Target", "Category", "Risk", "Problem", "Evidence", "Recommendation"],
        "counts": "{supported} of {total} tree items ({nodes} nodes, {edges} edges) are supported. "
                  "Findings on tree items: {findings}. Omissions: {omissions}. "
                  "By risk: {high} high, {medium} medium, {low} low.",
        "risk": {"high": "high", "medium": "medium", "low": "low"},
        "category": {c: c for c in list(DEFAULT_RISK) + ["omission"]},
        "tier": {"core": "core", "supporting": "supporting detail"},
        "page": "p.",
        "sep": ": ",
        "parts": "The tree falls apart into {n} parts that are not linked to each other:",
        "part": "Part {n}",
    },
    "zh": {
        "title": "SourceTrace 审核报告", "summary": "概要", "findings": "问题清单", "omissions": "遗漏内容",
        "structure": "结构问题", "confirmed": "已确认内容", "no_structure": "未发现结构问题。",
        "none": "无。", "top": "最重要的问题：",
        "cols": ["编号", "对象", "类别", "风险", "问题", "证据", "修改建议"],
        "counts": "知识树共 {total} 项（{nodes} 个节点、{edges} 条边），其中 {supported} 项有证据支持；"
                  "发现 {findings} 个问题，另有 {omissions} 处遗漏。按风险：高 {high}，中 {medium}，低 {low}。",
        "risk": {"high": "高", "medium": "中", "low": "低"},
        "category": {
            "conceptual-error": "概念错误", "incorrect-relationship": "关系错误",
            "unsupported-expansion": "无依据扩展", "overgeneralization": "过度概括",
            "ambiguous": "含糊不清", "omission": "遗漏",
        },
        "tier": {"core": "核心内容", "supporting": "补充细节"},
        "page": "第 {} 页",
        "sep": "：",
        "parts": "知识树分成 {n} 个互不相连的部分：",
        "part": "部分 {n}",
    },
}


def load(path, what, report):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        report.error("FILE_NOT_FOUND", f"{what} not found: {path}")
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        report.error("INVALID_JSON", f"{what} is not valid UTF-8 JSON: {e}")
    return None


def check_schema(audit, report):
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        sys.exit("build_report.py needs the jsonschema package: pip install jsonschema")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    for err in sorted(Draft202012Validator(schema).iter_errors(audit), key=lambda e: list(e.absolute_path)):
        report.error("SCHEMA", err.message, json_path(err.absolute_path))


def check_audit(audit, tree, evidence, report):
    """Cross-checks between the audit, the tree and the evidence index."""
    types = {n["id"]: "node" for n in tree["nodes"]} | {e["id"]: "edge" for e in tree["edges"]}

    counts = Counter(i["target"] for i in audit["items"])
    for target, n in counts.items():
        if target not in types:
            report.error("UNKNOWN_TARGET", f"{target} is not a node or edge of the tree.")
        elif n > 1:
            report.error("DUPLICATE_TARGET", f"{target} has {n} verdicts; give it exactly one.")
    missing = [t for t in types if t not in counts]
    if missing:
        report.error("MISSING_VERDICT", f"No verdict for: {', '.join(missing)}. Every node and edge needs one.")

    for i, item in enumerate(audit["items"]):
        path = f"$.items[{i}]"
        expected = types.get(item["target"])
        if expected and item.get("target_type", expected) != expected:
            report.error("TARGET_TYPE_MISMATCH",
                         f"{item['target']} is a {expected}, but target_type says {item['target_type']}.", path)
        if item["verdict"] == "supported":
            extra = [k for k in ("category", "risk", "risk_reason", "recommendation") if k in item]
            if extra:
                report.error("SUPPORTED_WITH_FINDING_FIELDS",
                             f"{item['target']} is supported but has {', '.join(extra)}. Remove them, "
                             "or make the verdict a finding.", path)
        else:
            check_risk(item, DEFAULT_RISK[item["category"]], item["category"], path, report)
            low = [e for e in item["evidence"] if evidence.get(e, {}).get("certainty") == "low"]
            if item["category"] != "ambiguous" and low and len(low) == len(item["evidence"]):
                report.warning("LOW_CERTAINTY_REJECTION",
                               f"{item['target']} is rejected on low-certainty evidence only ({', '.join(low)}); "
                               "the rules say to use ambiguous.", path)

    for i, om in enumerate(audit["omissions"]):
        check_risk(om, DEFAULT_OMISSION_RISK[om["tier"]], f"a {om['tier']} omission", f"$.omissions[{i}]", report)

    for where, entries in (("items", audit["items"]), ("omissions", audit["omissions"])):
        for i, entry in enumerate(entries):
            unknown = [e for e in entry["evidence"] if e not in evidence]
            if unknown:
                report.error("UNKNOWN_EVIDENCE", f"Evidence not in the index: {', '.join(unknown)}.",
                             f"$.{where}[{i}].evidence")


def check_risk(entry, default, what, path, report):
    if entry["risk"] != default and "risk_reason" not in entry:
        report.error("RISK_WITHOUT_REASON",
                     f"Risk is {entry['risk']}, but the default for {what} is {default}. "
                     "Add risk_reason, or use the default.", path)


def finalize(audit, tree, evidence, structure):
    """Add the computed fields. Returns the findings in report order."""
    order = {t: i for i, t in enumerate([n["id"] for n in tree["nodes"]] + [e["id"] for e in tree["edges"]])}

    def sort_key(entry):
        pages = [evidence[e]["page"] for e in entry["evidence"]]
        return RISKS.index(entry["risk"]), min(pages), order.get(entry.get("target"), len(order))

    items = sorted(audit["items"], key=lambda i: order[i["target"]])
    findings = sorted((i for i in items if i["verdict"] == "finding"), key=sort_key)
    omissions = sorted(audit["omissions"], key=sort_key)
    for n, entry in enumerate(findings + omissions, start=1):
        entry["finding_id"] = f"F-{n:03d}"
    types = {n["id"]: "node" for n in tree["nodes"]}
    for item in items:
        item["target_type"] = types.get(item["target"], "edge")

    risk_counts = Counter(e["risk"] for e in findings + omissions)
    audit.clear()
    audit.update({
        "schema_version": "0.1",
        "summary": {
            "nodes": len(tree["nodes"]),
            "edges": len(tree["edges"]),
            "supported": len(items) - len(findings),
            "item_findings": len(findings),
            "omissions": len(omissions),
            "by_risk": {r: risk_counts.get(r, 0) for r in RISKS},
            "by_category": dict(Counter(e["category"] for e in findings + omissions)),
        },
        "structure_warnings": [{"code": w["code"], "message": w["message"]} for w in structure],
        "items": [reorder(i) for i in items],
        "omissions": [reorder(o) for o in omissions],
    })
    return findings, omissions


def reorder(entry):
    keys = ["finding_id", "target", "target_type", "verdict", "category", "tier", "risk", "risk_reason",
            "evidence", "reason", "recommendation"]
    return {k: entry[k] for k in keys if k in entry}


def detect_language(evidence):
    text = "".join(e["content"] for e in evidence.values())
    cjk = len(re.findall(r"[\u4e00-\u9fff]", text))
    latin = len(re.findall(r"[A-Za-z]", text))
    return "zh" if cjk > 0.3 * (cjk + latin) else "en"


def cell(text):
    return str(text).replace("|", "\\|").replace("\r", " ").replace("\n", " ")


def render(audit, findings, omissions, tree, evidence, lang):
    L = LABELS[lang]
    labels = {n["id"]: n["label"] for n in tree["nodes"]}
    edges = {e["id"]: e for e in tree["edges"]}

    def target(entry):
        t = entry.get("target")
        if t is None:
            return "—"
        if t in edges:
            e = edges[t]
            return f"{t} {labels.get(e['source'], e['source'])} —{e['relation']}→ {labels.get(e['target'], e['target'])}"
        return f"{t} {labels.get(t, '')}"

    def page(n):
        return L["page"].format(n) if "{}" in L["page"] else f"{L['page']}{n}"

    def quotes(ids):
        parts = []
        for e in ids:
            content = evidence[e]["content"]
            short = content if len(content) <= QUOTE_CHARS else content[:QUOTE_CHARS] + "…"
            parts.append(f"{e} {page(evidence[e]['page'])} “{short}”")
        return "<br>".join(cell(p) for p in parts)

    def risk(entry):
        r = L["risk"][entry["risk"]]
        return f"{r}（{entry['risk_reason']}）" if lang == "zh" and "risk_reason" in entry else \
            f"{r} ({entry['risk_reason']})" if "risk_reason" in entry else r

    def category(entry):
        c = L["category"][entry["category"]]
        if "tier" in entry:
            c += f" · {L['tier'][entry['tier']]}"
        return c

    def table(entries):
        if not entries:
            return [L["none"]]
        rows = ["| " + " | ".join(L["cols"]) + " |", "|" + "---|" * len(L["cols"])]
        for e in entries:
            rows.append("| " + " | ".join([e["finding_id"], cell(target(e)), category(e), risk(e), cell(e["reason"]),
                                           quotes(e["evidence"]), cell(e["recommendation"])]) + " |")
        return rows

    s = audit["summary"]
    lines = [f"# {L['title']}{L['sep']}{tree['title']}", "", f"## {L['summary']}", "",
             L["counts"].format(total=s["nodes"] + s["edges"], findings=s["item_findings"], **s, **s["by_risk"])]
    top = (findings + omissions)[:3]
    if top:
        lines += ["", L["top"], ""]
        lines += [f"{n}. {e['finding_id']} {target(e)}{L['sep']}{e['reason']}" for n, e in enumerate(top, start=1)]

    lines += ["", f"## {L['findings']}", ""] + table(findings)
    lines += ["", f"## {L['omissions']}", ""] + table(omissions)
    lines += ["", f"## {L['structure']}", ""]
    for w in audit["structure_warnings"]:
        if w["code"] == "DISCONNECTED_TREE":
            parts = connected_parts(tree["edges"], set(labels))
            lines.append(f"- {w['code']}{L['sep']}{L['parts'].format(n=len(parts))}")
            lines += [f"  - {L['part'].format(n=n)}{L['sep']}" + ", ".join(f"{x} {labels[x]}" for x in part)
                      for n, part in enumerate(parts, start=1)]
        else:
            lines.append(f"- {w['code']}{L['sep']}{w['message']}")
    if not audit["structure_warnings"]:
        lines.append(L["no_structure"])

    confirmed = [i for i in audit["items"] if i["verdict"] == "supported"]
    lines += ["", f"## {L['confirmed']}", ""]
    lines += [f"- {target(i)} ({', '.join(i['evidence'])})" for i in confirmed] or [L["none"]]
    return "\n".join(lines) + "\n"


def main(argv=None):
    parser = argparse.ArgumentParser(description="Finalize audit.json and generate report.md.")
    parser.add_argument("--tree", required=True, help="the knowledge tree that was audited")
    parser.add_argument("--index", required=True, help="evidence-index.json")
    parser.add_argument("--audit", required=True, help="audit.json written by the agent; rewritten in place")
    parser.add_argument("--lang", choices=["auto", "zh", "en"], default="auto", help="report language")
    args = parser.parse_args(argv)
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    report = Report()
    tree = load(args.tree, "Knowledge tree", report)
    index = load(args.index, "Evidence index", report)
    audit = load(args.audit, "Audit", report)
    if audit is not None:
        check_schema(audit, report)
    if not report.errors:
        evidence = {e["evidence_id"]: e for e in index["evidence"]}
        check_audit(audit, tree, evidence, report)

    for level in ("errors", "warnings"):
        for item in getattr(report, level):
            where = f" at {item['path']}" if item["path"] else ""
            print(f"  {level[:-1].upper()} {item['code']}{where}: {item['message']}")
    if report.errors:
        print(f"INVALID: {len(report.errors)} error(s); nothing was written. Fix audit.json and run again.")
        return 1

    structure = Report()
    check_structure(tree, structure)
    findings, omissions = finalize(audit, tree, evidence, structure.warnings)
    lang = detect_language(evidence) if args.lang == "auto" else args.lang

    audit_path = Path(args.audit)
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    report_path = audit_path.with_name("report.md")
    report_path.write_text(render(audit, findings, omissions, tree, evidence, lang), encoding="utf-8")
    s = audit["summary"]
    print(f"WRITTEN: {audit_path} and {report_path} ({lang}). Supported: {s['supported']}, "
          f"findings: {s['item_findings']}, omissions: {s['omissions']}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
