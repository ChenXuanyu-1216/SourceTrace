"""validate_input.py: the knowledge tree and the source images."""

import shutil

import pytest

from conftest import FIXTURE_NAMES, FIXTURES, codes, read_json, run_json, validate_input, write_json

ML = FIXTURES / "ml-basics"


def check(tree, images, capsys):
    return run_json(validate_input.main, ["--tree", str(tree), "--images", *map(str, images)], capsys)


def tree_with(tmp_path, change):
    tree = read_json(ML / "knowledge-tree.json")
    change(tree)
    return write_json(tmp_path / "tree.json", tree)


@pytest.mark.parametrize("name", FIXTURE_NAMES)
def test_fixtures_are_valid(name, capsys):
    code, result = check(FIXTURES / name / "knowledge-tree.json", [FIXTURES / name / "images"], capsys)
    assert code == 0
    assert result["valid"] and result["errors"] == []
    pages = [i["page"] for i in result["summary"]["images"]]
    assert pages == list(range(1, len(pages) + 1))


def test_model_eval_tree_is_disconnected(capsys):
    _, result = check(FIXTURES / "model-eval" / "knowledge-tree.json", [FIXTURES / "model-eval" / "images"], capsys)
    assert codes(result["warnings"]) == ["DISCONNECTED_TREE"]
    assert "3 parts" in result["warnings"][0]["message"]


def test_ml_basics_has_no_warnings(capsys):
    _, result = check(ML / "knowledge-tree.json", [ML / "images"], capsys)
    assert result["warnings"] == []


def test_pages_follow_natural_file_order(tmp_path, capsys):
    for name in ("slide-10.png", "slide-2.png", "slide-1.png"):
        shutil.copy(ML / "images" / "slide-01.png", tmp_path / name)
    _, result = check(ML / "knowledge-tree.json", [tmp_path], capsys)
    assert [i["source_id"] for i in result["summary"]["images"]] == ["slide-1", "slide-2", "slide-10"]


@pytest.mark.parametrize("change, expected", [
    (lambda t: t["nodes"][0].update(kind="idea"), "SCHEMA"),
    (lambda t: t["edges"][0].update(relation="contains"), "SCHEMA"),
    (lambda t: t.update(schema_version="0.2"), "SCHEMA"),
    (lambda t: t["nodes"][1].update(id="N001"), "DUPLICATE_NODE_ID"),
    (lambda t: t["edges"][1].update(id="E001"), "DUPLICATE_EDGE_ID"),
    (lambda t: t["edges"][0].update(target="N999"), "DANGLING_EDGE"),
    (lambda t: t["edges"][0].update(target=t["edges"][0]["source"]), "SELF_LOOP"),
])
def test_tree_errors(change, expected, tmp_path, capsys):
    code, result = check(tree_with(tmp_path, change), [ML / "images"], capsys)
    assert code == 1
    assert expected in codes(result["errors"])


def test_duplicate_edge_and_isolated_node_are_warnings(tmp_path, capsys):
    def change(t):
        t["edges"].append(dict(t["edges"][0], id="E099"))
        t["nodes"].append({"id": "N099", "label": "Lonely", "definition": "x", "kind": "concept"})
    code, result = check(tree_with(tmp_path, change), [ML / "images"], capsys)
    assert code == 0
    assert set(codes(result["warnings"])) == {"DUPLICATE_EDGE", "ISOLATED_NODE"}


def test_isolated_node_is_not_also_reported_as_disconnected(tmp_path, capsys):
    def change(t):
        t["nodes"].append({"id": "N099", "label": "Lonely", "definition": "x", "kind": "concept"})
    _, result = check(tree_with(tmp_path, change), [ML / "images"], capsys)
    assert "DISCONNECTED_TREE" not in codes(result["warnings"])


def test_invalid_json(tmp_path, capsys):
    bad = tmp_path / "tree.json"
    bad.write_text('{"nodes": [', encoding="utf-8")
    code, result = check(bad, [ML / "images"], capsys)
    assert code == 1 and codes(result["errors"]) == ["INVALID_JSON"]


@pytest.mark.parametrize("make, expected", [
    (lambda d: d / "missing.png", "FILE_NOT_FOUND"),
    (lambda d: (d / "fake.png").write_text("not an image") and d / "fake.png", "NOT_AN_IMAGE"),
    (lambda d: (d / "notes.txt").write_text("hi") and d / "notes.txt", "UNSUPPORTED_IMAGE"),
    (lambda d: (d / "empty").mkdir() or d / "empty", "NO_IMAGES"),
])
def test_image_errors(make, expected, tmp_path, capsys):
    code, result = check(ML / "knowledge-tree.json", [make(tmp_path)], capsys)
    assert code == 1
    assert expected in codes(result["errors"])


def test_duplicate_image_names(tmp_path, capsys):
    (tmp_path / "a").mkdir()
    (tmp_path / "b").mkdir()
    shutil.copy(ML / "images" / "slide-01.png", tmp_path / "a" / "x.png")
    shutil.copy(ML / "images" / "slide-01.png", tmp_path / "b" / "x.png")
    code, result = check(ML / "knowledge-tree.json", [tmp_path / "a" / "x.png", tmp_path / "b" / "x.png"], capsys)
    assert code == 1
    assert codes(result["errors"]) == ["DUPLICATE_SOURCE_ID"]


def test_missing_argument_is_a_usage_error():
    with pytest.raises(SystemExit) as exc:
        validate_input.main(["--tree", "x.json"])
    assert exc.value.code == 2


# --- image paths: relative to the output folder, so a saved run stays portable ---

def test_image_paths_resolve_from_the_default_output_folder(capsys):
    _, result = check(ML / "knowledge-tree.json", [ML / "images"], capsys)
    out = ML / "sourcetrace-output"
    for img in result["summary"]["images"]:
        assert "\\" not in img["path"] and not img["path"].startswith("/")
        assert (out / img["path"]).resolve() == (ML / "images" / f"{img['source_id']}.png").resolve()


def test_out_option_sets_the_folder_paths_are_relative_to(tmp_path, capsys):
    out = tmp_path / "results"
    _, result = run_json(validate_input.main, ["--tree", str(ML / "knowledge-tree.json"),
                                               "--images", str(ML / "images"), "--out", str(out)], capsys)
    first = result["summary"]["images"][0]
    assert (out / first["path"]).resolve() == (ML / "images" / f"{first['source_id']}.png").resolve()
