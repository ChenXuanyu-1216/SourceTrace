"""Validate SourceTrace inputs before an audit.

Checks the knowledge tree against schemas/knowledge-tree.schema.json, then runs
the structural checks JSON Schema cannot express (unique IDs, edge references,
self-loops). Checks that the source images exist and really are PNG/JPG, and
assigns each image its page number.

Usage:
    python validate_input.py --tree knowledge-tree.json --images images/
    python validate_input.py --tree knowledge-tree.json --images a.png b.jpg --json

Exit codes: 0 valid (warnings allowed), 1 invalid input, 2 usage error.
Requires: jsonschema (pip install jsonschema).
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "knowledge-tree.schema.json"
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, code, message, path=None):
        self.errors.append({"code": code, "message": message, "path": path})

    def warning(self, code, message, path=None):
        self.warnings.append({"code": code, "message": message, "path": path})


def load_json(path, report):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        report.error("FILE_NOT_FOUND", f"Knowledge tree not found: {path}")
    except json.JSONDecodeError as e:
        report.error("INVALID_JSON", f"Knowledge tree is not valid JSON: {e}")
    except UnicodeDecodeError:
        report.error("INVALID_JSON", "Knowledge tree is not UTF-8 text.")
    return None


def check_schema(tree, report):
    try:
        from jsonschema import Draft202012Validator
    except ImportError:
        sys.exit("validate_input.py needs the jsonschema package: pip install jsonschema")

    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema = json.load(f)
    validator = Draft202012Validator(schema)
    for err in sorted(validator.iter_errors(tree), key=lambda e: list(e.absolute_path)):
        report.error("SCHEMA", err.message, json_path(err.absolute_path))


def json_path(parts):
    path = "$"
    for part in parts:
        path += f"[{part}]" if isinstance(part, int) else f".{part}"
    return path


def check_structure(tree, report):
    """Checks beyond the schema. Tolerates malformed items, which check_schema reports."""
    nodes = [n for n in tree.get("nodes", []) if isinstance(n, dict)] if isinstance(tree.get("nodes"), list) else []
    edges = [e for e in tree.get("edges", []) if isinstance(e, dict)] if isinstance(tree.get("edges"), list) else []

    for code, items, kind in (("DUPLICATE_NODE_ID", nodes, "node"), ("DUPLICATE_EDGE_ID", edges, "edge")):
        for item_id, count in Counter(i.get("id") for i in items if "id" in i).items():
            if count > 1:
                report.error(code, f"{kind.capitalize()} ID {item_id} is used {count} times.")

    node_ids = {n.get("id") for n in nodes}
    seen_edges = {}
    linked = set()
    for i, edge in enumerate(edges):
        path = f"$.edges[{i}]"
        src, dst = edge.get("source"), edge.get("target")
        for end in ("source", "target"):
            if end in edge and edge[end] not in node_ids:
                report.error("DANGLING_EDGE", f"Edge {edge.get('id')} {end} {edge[end]} is not a node.", path)
        if src is not None and src == dst:
            report.error("SELF_LOOP", f"Edge {edge.get('id')} connects node {src} to itself.", path)
        linked.update((src, dst))

        key = (src, dst, edge.get("relation"))
        if key in seen_edges:
            report.warning("DUPLICATE_EDGE",
                           f"Edge {edge.get('id')} repeats edge {seen_edges[key]} ({src} {key[2]} {dst}).", path)
        else:
            seen_edges[key] = edge.get("id")

    if len(nodes) > 1:
        for i, node in enumerate(nodes):
            if node.get("id") not in linked:
                report.warning("ISOLATED_NODE", f"Node {node.get('id')} has no edges.", f"$.nodes[{i}]")

    return len(nodes), len(edges)


def natural_key(path):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", path.name)]


def collect_images(paths, report):
    """Expand directories, check every image, and number them as pages in order."""
    files = []
    for raw in paths:
        p = Path(raw)
        if p.is_dir():
            found = sorted((f for f in p.iterdir() if f.is_file() and f.suffix.lower() in IMAGE_SUFFIXES),
                           key=natural_key)
            if not found:
                report.error("NO_IMAGES", f"No PNG/JPG images in directory: {p}")
            files.extend(found)
        elif p.is_file():
            files.append(p)
        else:
            report.error("FILE_NOT_FOUND", f"Image not found: {p}")

    images = []
    for f in files:
        suffix = f.suffix.lower()
        if suffix not in IMAGE_SUFFIXES:
            report.error("UNSUPPORTED_IMAGE", f"Only PNG/JPG images are supported: {f}")
            continue
        with open(f, "rb") as fh:
            head = fh.read(8)
        expected = PNG_MAGIC if suffix == ".png" else JPEG_MAGIC
        if not head.startswith(expected):
            report.error("NOT_AN_IMAGE", f"File content is not a real {suffix[1:].upper()} image: {f}")
            continue
        images.append({"page": len(images) + 1, "source_id": f.stem, "path": str(f)})

    for source_id, count in Counter(i["source_id"] for i in images).items():
        if count > 1:
            report.error("DUPLICATE_SOURCE_ID",
                         f"{count} images share the name {source_id}; rename them so each source_id is unique.")
    return images


def main(argv=None):
    parser = argparse.ArgumentParser(description="Validate SourceTrace inputs.")
    parser.add_argument("--tree", required=True, help="AI-generated knowledge tree (JSON)")
    parser.add_argument("--images", required=True, nargs="+", help="source images (PNG/JPG) or directories of them")
    parser.add_argument("--json", action="store_true", help="print the result as JSON")
    args = parser.parse_args(argv)

    report = Report()
    node_count = edge_count = 0
    tree = load_json(args.tree, report)
    if tree is not None:
        check_schema(tree, report)
        if isinstance(tree, dict):
            node_count, edge_count = check_structure(tree, report)
    images = collect_images(args.images, report)

    result = {
        "valid": not report.errors,
        "errors": report.errors,
        "warnings": report.warnings,
        "summary": {"nodes": node_count, "edges": edge_count, "images": images},
    }

    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_text(result)
    return 0 if result["valid"] else 1


def print_text(result):
    s = result["summary"]
    print(f"{'VALID' if result['valid'] else 'INVALID'}: {s['nodes']} nodes, {s['edges']} edges, "
          f"{len(s['images'])} images")
    for level in ("errors", "warnings"):
        for item in result[level]:
            where = f" at {item['path']}" if item["path"] else ""
            print(f"  {level[:-1].upper()} {item['code']}{where}: {item['message']}")
    for img in s["images"]:
        print(f"  page {img['page']}: {img['source_id']} ({img['path']})")


if __name__ == "__main__":
    sys.exit(main())
