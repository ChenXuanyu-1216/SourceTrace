"""Integrity of the answer keys and the saved skill runs that the evaluation relies on.

These tests do not run the skill (that needs an agent). They check that the
committed results still meet the answer keys under the current rules, so a
change to a key or a rule that breaks them is caught.
"""

import pytest

from conftest import FIXTURE_NAMES, FIXTURES, ROOT, read_json

# Runs made with the final v0.1 rules. The earlier consistency runs in
# tests/consistency/model-eval/run-* predate them and are kept only as history.
CURRENT_RUNS = {
    "smoke/ml-basics": "ml-basics",
    "consistency/model-eval/day6/run-1": "model-eval",
    "consistency/model-eval/day6/run-2": "model-eval",
    "consistency/model-eval/day6/run-3": "model-eval",
    "smoke/model-eval-e2e": "model-eval",
}


def tree_ids(fixture):
    tree = read_json(FIXTURES / fixture / "knowledge-tree.json")
    return [n["id"] for n in tree["nodes"]] + [e["id"] for e in tree["edges"]]


def key(fixture):
    return read_json(FIXTURES / fixture / "expected-findings.json")


@pytest.mark.parametrize("fixture", FIXTURE_NAMES)
def test_answer_key_covers_every_item_exactly_once(fixture):
    k = key(fixture)
    planted = [f["target"] for f in k["expected_findings"] if f["target"]]
    correct = k["correct_items"]
    assert sorted(planted + correct) == sorted(tree_ids(fixture))


@pytest.mark.parametrize("fixture", FIXTURE_NAMES)
def test_answer_key_entries_are_complete(fixture):
    for f in key(fixture)["expected_findings"]:
        assert f["risk"] in ("high", "medium", "low")
        if f["target"] is None:
            assert f["category"] == "omission" and f["tier"] in ("core", "supporting") and f["match"]
    for s in key(fixture)["should_not_report"]:
        assert s["match"]


@pytest.mark.parametrize("run, fixture", CURRENT_RUNS.items())
def test_saved_run_meets_answer_key(run, fixture):
    folder = ROOT / "tests" / run
    audit = read_json(folder / "audit.json")
    content = {e["evidence_id"]: e["content"] for e in read_json(folder / "evidence-index.json")["evidence"]}
    items = {i["target"]: i for i in audit["items"]}
    k = key(fixture)

    assert sorted(items) == sorted(tree_ids(fixture))
    for f in k["expected_findings"]:
        if f["target"]:
            got = items[f["target"]]
            assert (got["verdict"], got["category"], got["risk"]) == ("finding", f["category"], f["risk"]), f["target"]
    for target in k["correct_items"]:
        assert items[target]["verdict"] == "supported", target

    texts = [" ".join(content[e] for e in o["evidence"]) + " " + o["reason"] for o in audit["omissions"]]
    for f in k["expected_findings"]:
        if f["target"] is None:
            hits = [o for o, t in zip(audit["omissions"], texts) if f["match"] in t]
            assert hits, f"missing omission: {f['match']}"
            assert f["risk"] in {o["risk"] for o in hits}, f"wrong risk for omission: {f['match']}"
    for s in k["should_not_report"]:
        assert not any(s["match"] in t for t in texts), f"reported: {s['match']}"


def test_current_model_eval_runs_agree_on_every_item():
    runs = [r for r, f in CURRENT_RUNS.items() if f == "model-eval"]
    verdicts = []
    for run in runs:
        audit = read_json(ROOT / "tests" / run / "audit.json")
        verdicts.append({i["target"]: (i["verdict"], i.get("category"), i.get("risk")) for i in audit["items"]})
    assert all(v == verdicts[0] for v in verdicts[1:])
