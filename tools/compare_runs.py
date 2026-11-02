"""Compare SourceTrace runs on one fixture: validity, agreement between runs, and grading.

Usage: python -I tools/compare_runs.py <repo> <fixture> <run-dir> [<run-dir> ...]
Each run-dir holds audit.json and evidence-index.json, directly or in input/sourcetrace-output/.
Set PYTHONIOENCODING=utf-8 on Windows consoles to print Chinese correctly.
"""
import json
import subprocess
import sys
from collections import Counter
from pathlib import Path

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
    fp = [c for c in key["correct_items"] if items.get(c, {}).get("verdict") != "supported"]
    oms = run["audit"].get("omissions", [])
    om_text = [" ".join(run["content"].get(e, "") for e in o.get("evidence", [])) + " " + o.get("reason", "") for o in oms]
    f1 = any("F1" in t for t in om_text)
    homework = any("课后作业" in t or "Iris" in t for t in om_text)
    print(f"  {name}: planted items {sum(found)}/{len(found)} | F1 omission {f1} | false positives {fp} "
          f"| homework reported {homework} | omissions {len(oms)}")
    for o, t in zip(oms, om_text):
        print(f"      omission [{o.get('risk')}] {t[:90]}")
