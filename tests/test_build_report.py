"""build_report.py: checks audit.json, completes it, and generates report.md."""

import re
import shutil

import pytest

from conftest import FIXTURES, ROOT, build_report, read_json, text, write_json

E2E = ROOT / "tests" / "smoke" / "model-eval-e2e"
SMOKE_ML = ROOT / "tests" / "smoke" / "ml-basics"
COMPUTED = ("summary", "structure_warnings")


@pytest.fixture
def run(tmp_path, capsys):
    """Copy a saved run into tmp_path; return a function that runs build_report on it."""
    def prepare(source, fixture, change_audit=None, change_index=None):
        for name in ("audit.json", "evidence-index.json"):
            shutil.copy(source / name, tmp_path / name)
        if change_audit:
            audit = read_json(tmp_path / "audit.json")
            change_audit(audit)
            write_json(tmp_path / "audit.json", audit)
        if change_index:
            index = read_json(tmp_path / "evidence-index.json")
            change_index(index)
            write_json(tmp_path / "evidence-index.json", index)

        def build(*extra):
            code = build_report.main(["--tree", str(FIXTURES / fixture / "knowledge-tree.json"),
                                      "--index", str(tmp_path / "evidence-index.json"),
                                      "--audit", str(tmp_path / "audit.json"), *extra])
            out = capsys.readouterr().out
            return code, re.findall(r"^\s+ERROR (\w+)", out, re.M), re.findall(r"^\s+WARNING (\w+)", out, re.M)
        return build
    return prepare


def as_draft(audit):
    """Strip what build_report computes, leaving only what the agent writes."""
    for key in COMPUTED:
        audit.pop(key, None)
    for entry in audit["items"] + audit["omissions"]:
        entry.pop("finding_id", None)
        entry.pop("target_type", None)


def add_tiers(audit):
    """The ml-basics smoke run predates `tier`; add it the way the rules define it."""
    for om in audit["omissions"]:
        om.setdefault("tier", "core" if om["risk"] == "medium" else "supporting")


def item(audit, target):
    return next(i for i in audit["items"] if i["target"] == target)


# --- reproducing the saved end-to-end run ---------------------------------

def test_reproduces_saved_e2e_report(run, tmp_path):
    code, errors, _ = run(E2E, "model-eval")()
    assert code == 0 and errors == []
    assert text(tmp_path / "report.md") == text(E2E / "report.md")
    assert read_json(tmp_path / "audit.json") == read_json(E2E / "audit.json")


def test_draft_from_agent_gives_same_result(run, tmp_path):
    code, _, _ = run(E2E, "model-eval", change_audit=as_draft)()
    assert code == 0
    assert text(tmp_path / "report.md") == text(E2E / "report.md")
    assert read_json(tmp_path / "audit.json") == read_json(E2E / "audit.json")


def test_rerun_gives_identical_files(run, tmp_path):
    build = run(E2E, "model-eval", change_audit=as_draft)
    build()
    first = (text(tmp_path / "audit.json"), text(tmp_path / "report.md"))
    build()
    assert (text(tmp_path / "audit.json"), text(tmp_path / "report.md")) == first


def test_agent_values_for_computed_fields_are_replaced(run, tmp_path):
    def change(audit):
        audit["summary"] = {"supported": 999}
        audit["structure_warnings"] = []
        for i, entry in enumerate(e for e in audit["items"] if e["verdict"] == "finding"):
            entry["finding_id"] = f"X-{i}"
    run(E2E, "model-eval", change_audit=change)()
    assert read_json(tmp_path / "audit.json") == read_json(E2E / "audit.json")


# --- what the script computes ----------------------------------------------

def test_summary_adds_up(run, tmp_path):
    run(E2E, "model-eval", change_audit=as_draft)()
    audit = read_json(tmp_path / "audit.json")
    s = audit["summary"]
    assert s["supported"] + s["item_findings"] == s["nodes"] + s["edges"] == 37
    assert s["omissions"] == len(audit["omissions"])
    assert sum(s["by_risk"].values()) == s["item_findings"] + s["omissions"]
    assert sum(s["by_category"].values()) == s["item_findings"] + s["omissions"]


def test_finding_ids_follow_risk_order(run, tmp_path):
    run(E2E, "model-eval", change_audit=as_draft)()
    audit = read_json(tmp_path / "audit.json")
    findings = sorted((e for e in audit["items"] if e["verdict"] == "finding"), key=lambda e: e["finding_id"])
    ids = [e["finding_id"] for e in findings + audit["omissions"]]
    assert ids == [f"F-{n:03d}" for n in range(1, len(ids) + 1)]
    ranks = [build_report.RISKS.index(e["risk"]) for e in findings]
    assert ranks == sorted(ranks)


def test_disconnected_tree_is_listed_with_labels(run, tmp_path):
    run(E2E, "model-eval")()
    report = text(tmp_path / "report.md")
    assert "知识树分成 3 个互不相连的部分" in report
    assert "部分 3：N007 欠拟合, N009 高方差" in report


def test_pipes_in_quotes_are_escaped(run, tmp_path):
    run(E2E, "model-eval")()
    rows = [line for line in text(tmp_path / "report.md").splitlines() if line.startswith("| F-")]
    assert rows and all(line.count(" | ") == 6 for line in rows)


# --- language ----------------------------------------------------------------

def test_chinese_slides_give_chinese_report(run, tmp_path):
    run(E2E, "model-eval")()
    assert "## 概要" in text(tmp_path / "report.md")


def test_lang_option_overrides_detection(run, tmp_path):
    run(E2E, "model-eval")("--lang", "en")
    report = text(tmp_path / "report.md")
    assert "## Summary" in report and "## 概要" not in report


def test_english_slides_give_english_report(run, tmp_path):
    code, errors, _ = run(SMOKE_ML, "ml-basics", change_audit=lambda a: (as_draft(a), add_tiers(a)))()
    assert code == 0 and errors == []
    report = text(tmp_path / "report.md")
    assert report.startswith("# SourceTrace audit: Machine Learning")
    assert "No structural problems." in report


# --- errors: nothing is written ------------------------------------------------

@pytest.mark.parametrize("change, expected", [
    (lambda a: a["items"].remove(item(a, "N001")), "MISSING_VERDICT"),
    (lambda a: a["items"].append(dict(item(a, "N002"))), "DUPLICATE_TARGET"),
    (lambda a: a["items"].append({"target": "N099", "verdict": "supported", "evidence": ["EV-001"]}),
     "UNKNOWN_TARGET"),
    (lambda a: item(a, "N003").update(target_type="edge"), "TARGET_TYPE_MISMATCH"),
    (lambda a: item(a, "N005").update(evidence=["EV-999"]), "UNKNOWN_EVIDENCE"),
    (lambda a: item(a, "N012").update(risk="low"), "RISK_WITHOUT_REASON"),
    (lambda a: a["omissions"][0].update(risk="high"), "RISK_WITHOUT_REASON"),
    (lambda a: item(a, "N016").update(category="ambiguous"), "SUPPORTED_WITH_FINDING_FIELDS"),
    (lambda a: item(a, "N015").pop("recommendation"), "SCHEMA"),
    (lambda a: a["omissions"][0].pop("tier"), "SCHEMA"),
    (lambda a: item(a, "N002").update(evidence=[]), "SCHEMA"),
])
def test_invalid_audit_is_rejected_and_nothing_written(change, expected, run, tmp_path):
    code, errors, _ = run(E2E, "model-eval", change_audit=lambda a: (as_draft(a), change(a)))()
    assert code == 1
    assert expected in errors
    assert not (tmp_path / "report.md").exists()
    assert "summary" not in read_json(tmp_path / "audit.json")


def test_risk_change_with_reason_is_accepted(run, tmp_path):
    def change(audit):
        as_draft(audit)
        audit["omissions"][0].update(risk="high", risk_reason="central concept of the lecture")
    code, errors, _ = run(E2E, "model-eval", change_audit=change)()
    assert code == 0 and errors == []
    report = text(tmp_path / "report.md")
    assert "高（central concept of the lecture）" in report


def test_rejection_on_low_certainty_evidence_only_is_a_warning(run, tmp_path):
    def low(index):
        for e in index["evidence"]:
            if e["evidence_id"] in item(read_json(E2E / "audit.json"), "N005")["evidence"]:
                e["certainty"] = "low"
    code, errors, warnings = run(E2E, "model-eval", change_audit=as_draft, change_index=low)()
    assert code == 0 and errors == []
    assert warnings == ["LOW_CERTAINTY_REJECTION"]


# --- scope: an unsupported-expansion of one detail ----------------------------

def test_detail_scope_defaults_to_low_and_is_labelled(run, tmp_path):
    def change(audit):
        as_draft(audit)
        item(audit, "N013").update(scope="detail", risk="low")
    code, errors, _ = run(E2E, "model-eval", change_audit=change)()
    assert code == 0 and errors == []
    assert item(read_json(tmp_path / "audit.json"), "N013")["scope"] == "detail"
    assert "无依据扩展 · 细节 | 低" in text(tmp_path / "report.md")


def test_detail_scope_at_medium_needs_a_reason(run):
    def change(audit):
        as_draft(audit)
        item(audit, "N013").update(scope="detail")
    code, errors, _ = run(E2E, "model-eval", change_audit=change)()
    assert code == 1 and errors == ["RISK_WITHOUT_REASON"]


@pytest.mark.parametrize("target, expected", [
    ("N004", "SCOPE_NOT_ALLOWED"),              # a conceptual-error finding
    ("N016", "SUPPORTED_WITH_FINDING_FIELDS"),  # a supported item
])
def test_scope_only_on_unsupported_expansion_findings(target, expected, run):
    def change(audit):
        as_draft(audit)
        item(audit, target)["scope"] = "detail"
    code, errors, _ = run(E2E, "model-eval", change_audit=change)()
    assert code == 1 and expected in errors


def test_ambiguous_is_shown_as_cannot_verify(run, tmp_path):
    def change(audit):
        as_draft(audit)
        item(audit, "N013").update(category="ambiguous", risk="low")
    build = run(E2E, "model-eval", change_audit=change)
    build()
    assert "资料未定义 / 无法核验 | 低" in text(tmp_path / "report.md")
    build("--lang", "en")
    assert "cannot verify | low" in text(tmp_path / "report.md")
