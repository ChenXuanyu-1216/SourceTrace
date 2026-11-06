"""Compare SourceTrace runs on one fixture: validity, agreement between runs, and grading.

Usage: python -I tools/compare_runs.py <repo> <fixture> <run-dir> [<run-dir> ...]
Each run-dir holds audit.json and evidence-index.json, directly or in input/sourcetrace-output/.
Output is UTF-8; on Windows, redirect it to a file if the console shows garbled Chinese.
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

repo, fixture, run_dirs = Path(sys.argv[1]), sys.argv[2], [Path(p) for p in sys.argv[3:]]
fx = repo / "tests" / "fixtures" / fixture
tree = json.load(open(fx / "knowledge-tree.json", encoding="utf-8"))
key = json.load(open(fx / "expected-findings.json", encoding="utf-8"))
ids = [n["id"] for n in tree["nodes"]] + [e["id"] for e in tree["edges"]]

runs = {}
for d in run_dirs:
    out = d if (d / "audit.json").exists() else d / "input" / "sourcetrace-output"
    name = d.name
    r = subprocess.run([sys.executable, str(repo / "source-trace/scripts/validate_evidence.py"),
                        "--index", str(out / "evidence-index.json")],
                       capture_output=True, text=True, encoding="utf-8")
    audit = json.load(open(out / "audit.json", encoding="utf-8"))
    index = json.load(open(out / "evidence-index.json", encoding="utf-8"))
    content = {e["evidence_id"]: e["content"] for e in index["evidence"]}
    runs[name] = {"valid": r.stdout.splitlines()[0], "audit": audit, "content": content,
                  "items": {i["target"]: i for i in audit["items"]}}

print("== Validity")
for name, run in runs.items():
    a, items = run["audit"], run["items"]
    s = a.get("summary", {})
    unknown = sorted({e for i in a["items"] + a.get("omissions", []) for e in i.get("evidence", [])}
                     - set(run["content"]))
    no_ev = [i["target"] for i in a["items"] if not i.get("evidence")]
    total_ok = s.get("supported", 0) + s.get("item_findings", 0) == len(ids)
    print(f"{name}: {run['valid']} | verdicts {len(items)}/{len(ids)} | missing {[x for x in ids if x not in items]}"
          f" | unknown evidence {unknown} | items without evidence {no_ev} | summary adds up: {total_ok} {s}")

print("\n== Agreement per item (verdict / category / risk)")
agree = Counter()
for tid in ids:
    vals = [(r["items"].get(tid, {}).get("verdict"), r["items"].get(tid, {}).get("category"),
             r["items"].get(tid, {}).get("risk")) for r in runs.values()]
    v = len({x[0] for x in vals}) == 1
    c = v and len({x[1] for x in vals}) == 1
    k = c and len({x[2] for x in vals}) == 1
    agree["verdict"] += v; agree["category"] += c; agree["risk"] += k
    if not k:
        print(f"  {tid}: " + " | ".join(f"{n}={x[0]}/{x[1]}/{x[2]}" for n, x in zip(runs, vals)))
n = len(ids)
print(f"  verdict agree {agree['verdict']}/{n}, category agree {agree['category']}/{n}, risk agree {agree['risk']}/{n}")

print("\n== Grading against the answer key")
for name, run in runs.items():
    items = run["items"]
    found = []
    for f in key["expected_findings"]:
        if f["target"] is None:
            continue
        got = items.get(f["target"], {})
        ok = got.get("verdict") == "finding" and got.get("category") in [f["category"]] + f.get("also_accept", [])
        found.append(ok)
        if not ok:
            print(f"  {name} MISS {f['target']}: expected {f['category']}, got {got.get('verdict')}/{got.get('category')}")
        elif f.get("scope") and got.get("scope", "whole") != f["scope"]:
            print(f"  {name} SCOPE {f['target']}: expected {f['scope']}, got {got.get('scope', 'whole')}")
        elif got.get("risk") != f.get("risk", got.get("risk")) and not got.get("risk_reason"):
            print(f"  {name} RISK {f['target']}: expected {f['risk']}, got {got.get('risk')} without risk_reason")
    fp = [c for c in key["correct_items"] if items.get(c, {}).get("verdict") != "supported"]

    # Omissions are matched by a substring of the cited evidence or the reason.
    oms = run["audit"].get("omissions", [])
    om_text = [" ".join(run["content"].get(e, "") for e in o.get("evidence", [])) + " " + o.get("reason", "") for o in oms]
    used = set()
    om_found = []
    for f in key["expected_findings"]:
        if f["target"] is not None:
            continue
        hits = [i for i, text in enumerate(om_text) if f["match"] in text]
        used.update(hits)
        risks = {oms[i].get("risk") for i in hits}
        ok = bool(hits)
        om_found.append(ok)
        if not ok:
            print(f"  {name} MISS omission '{f['match']}' ({f['risk']})")
        elif f["risk"] not in risks and not any(oms[i].get("risk_reason") for i in hits):
            print(f"  {name} RISK omission '{f['match']}': expected {f['risk']}, got {sorted(risks)} without risk_reason")
    noise = [s["match"] for s in key.get("should_not_report", []) if any(s["match"] in text for text in om_text)]
    extra = [i for i in range(len(oms)) if i not in used]
    print(f"  {name}: planted items {sum(found)}/{len(found)} | omissions {sum(om_found)}/{len(om_found)} "
          f"| false positives {fp} | should-not-report hit {noise} | unmatched omissions {len(extra)}")
    for i in extra:
        print(f"      unmatched [{oms[i].get('risk')}] {om_text[i][:90]}")
