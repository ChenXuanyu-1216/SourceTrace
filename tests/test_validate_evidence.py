"""validate_evidence.py: the evidence index built in stage 2."""

from pathlib import Path

import pytest

from conftest import FIXTURES, ROOT, codes, read_json, run_json, validate_evidence, write_json

EXAMPLE = FIXTURES / "ml-basics" / "evidence-index.example.json"
SAVED_INDEXES = sorted(p.relative_to(ROOT).as_posix() for p in (ROOT / "tests").glob("**/evidence-index.json"))


def check(index, capsys):
    return run_json(validate_evidence.main, ["--index", str(index)], capsys)


def index_with(tmp_path, change):
    index = read_json(EXAMPLE)
    change(index)
    return write_json(tmp_path / "index.json", index)


def test_example_index_is_valid(capsys):
    code, result = check(EXAMPLE, capsys)
    assert code == 0 and result["errors"] == [] and result["warnings"] == []
    assert result["summary"] == {"sources": 4, "evidence": 21, "by_type": {"text": 15, "graphic": 3, "table": 3}}


@pytest.mark.parametrize("path", SAVED_INDEXES)
def test_every_saved_run_index_is_valid(path, capsys):
    code, result = check(ROOT / path, capsys)
    assert code == 0, result["errors"]


@pytest.mark.parametrize("change, expected", [
    (lambda d: d["evidence"][5].update(type="photo"), "SCHEMA"),
    (lambda d: d["evidence"][5].pop("location"), "SCHEMA"),
    (lambda d: d["evidence"][5].update(evidence_id="E6"), "SCHEMA"),
    (lambda d: d["evidence"][1].update(evidence_id="EV-001"), "DUPLICATE_EVIDENCE_ID"),
    (lambda d: d["evidence"][2].update(source_id="slide-09"), "UNKNOWN_SOURCE"),
    (lambda d: d["evidence"][3].update(page=2), "PAGE_MISMATCH"),
    (lambda d: d["sources"][3].update(page=6), "PAGE_GAP"),
    (lambda d: d["sources"][3].update(page=3), "DUPLICATE_PAGE"),
    (lambda d: d["sources"].append({"source_id": "slide-01", "page": 5, "path": "x.png"}), "DUPLICATE_SOURCE_ID"),
])
def test_index_errors(change, expected, tmp_path, capsys):
    code, result = check(index_with(tmp_path, change), capsys)
    assert code == 1
    assert expected in codes(result["errors"])


def test_single_page_mismatch_gives_exactly_one_error(tmp_path, capsys):
    _, result = check(index_with(tmp_path, lambda d: d["evidence"][3].update(page=2)), capsys)
    assert codes(result["errors"]) == ["PAGE_MISMATCH"]


def test_duplicate_source_does_not_cascade_into_page_mismatches(tmp_path, capsys):
    def change(d):
        d["sources"].append({"source_id": "slide-01", "page": 5, "path": "x.png"})
    _, result = check(index_with(tmp_path, change), capsys)
    assert "PAGE_MISMATCH" not in codes(result["errors"])


def test_empty_source_and_low_certainty_are_warnings(tmp_path, capsys):
    def change(d):
        d["evidence"] = [e for e in d["evidence"] if e["source_id"] != "slide-03"]
        d["evidence"][0]["certainty"] = "low"
    code, result = check(index_with(tmp_path, change), capsys)
    assert code == 0
    assert sorted(codes(result["warnings"])) == ["EMPTY_SOURCE", "LOW_CERTAINTY"]
    assert "EV-001" in result["warnings"][-1]["message"]


def test_invalid_json(tmp_path, capsys):
    bad = Path(tmp_path / "index.json")
    bad.write_text("[1, 2", encoding="utf-8")
    code, result = check(bad, capsys)
    assert code == 1 and codes(result["errors"]) == ["INVALID_JSON"]
