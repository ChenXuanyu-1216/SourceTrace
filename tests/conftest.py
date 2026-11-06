"""Shared helpers for the SourceTrace test suite.

The skill's scripts are plain files, not a package, so their folder is put on
sys.path here. Each test copies what it needs into tmp_path before changing
anything, so the committed fixtures are never modified.
"""

import json
import shutil
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS = ROOT / "source-trace" / "scripts"
FIXTURES = ROOT / "tests" / "fixtures"
sys.path.insert(0, str(SCRIPTS))

import build_report  # noqa: E402
import validate_evidence  # noqa: E402
import validate_input  # noqa: E402

FIXTURE_NAMES = ["ml-basics", "model-eval", "sl-algos-zh", "model-eval-scan", "model-eval-photo", "model-eval-occluded"]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, data):
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return Path(path)


def text(path):
    """File text with line endings normalized (git may check files out with CRLF)."""
    return Path(path).read_text(encoding="utf-8").replace("\r\n", "\n")


def codes(items):
    return [i["code"] for i in items]


def run_json(main, argv, capsys):
    """Run a validator's main() with --json; return (exit code, parsed result)."""
    code = main(argv + ["--json"])
    return code, json.loads(capsys.readouterr().out)


@pytest.fixture
def fixture_copy(tmp_path):
    """Copy a fixture folder into tmp_path and return the copy's path."""
    def copy(name):
        dst = tmp_path / name
        shutil.copytree(FIXTURES / name, dst)
        return dst
    return copy
