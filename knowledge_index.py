#!/usr/bin/env python3
"""
KitchenOS Knowledge Index — Level 2
Parses YAML frontmatter from all knowledge documents and builds an
in-memory index for impact analysis, dependency tracing, and navigation.

Documents are the source of truth. Git is the source of truth.
This index is derived — delete it and rebuild at any time.
No database. No dependencies beyond Python 3 stdlib.

Usage:
    python knowledge_index.py                    List all indexed documents
    python knowledge_index.py --impact ADR-004   What needs review if ADR-004 changes?
    python knowledge_index.py --deps ADR-005     What does ADR-005 depend on?
    python knowledge_index.py --graph            Full dependency graph
    python knowledge_index.py --tag ddd          Documents tagged 'ddd'
    python knowledge_index.py --check            Validate frontmatter refs + inline paths, links, and doc IDs
    python knowledge_index.py --dir /path        Scan a different root directory
"""

import re
import sys
import argparse
from pathlib import Path
from collections import defaultdict
from typing import Optional


# ---------------------------------------------------------------------------
# Frontmatter parser
# ---------------------------------------------------------------------------

def parse_frontmatter(filepath: Path) -> Optional[dict]:
    """
    Extract and parse YAML frontmatter from a Markdown file.
    Handles the specific format used in KitchenOS documents:
      - scalar values:  key: value
      - empty lists:    key: []
      - inline lists:   key: [item1, item2]
    Returns None if the file has no frontmatter.
    """
    try:
        content = filepath.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None

    if not content.startswith("---"):
        return None

    end = content.find("\n---", 3)
    if end == -1:
        return None

    block = content[3:end].strip()
    data: dict = {}

    for line in block.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue

        key, _, raw = line.partition(":")
        key = key.strip()
        raw = raw.strip()

        # Inline list: [item1, item2, item3]
        if raw.startswith("[") and raw.endswith("]"):
            inner = raw[1:-1].strip()
            if inner:
                data[key] = [v.strip() for v in inner.split(",") if v.strip()]
            else:
                data[key] = []
        else:
            data[key] = raw

    return data if data else None


# ---------------------------------------------------------------------------
# Graph builder
# ---------------------------------------------------------------------------

SKIP_DIRS = {"Archive", ".git", "__pycache__", "node_modules", ".venv", "Templates"}


def build_graph(root_dir: str) -> dict:
    """
    Walk the directory tree from root_dir and index all Markdown files
    that contain a YAML frontmatter block with an 'id' field.
    Returns a dict mapping document id -> frontmatter dict (with _path added).
    """
    root = Path(root_dir).resolve()
    documents: dict = {}

    for md_file in sorted(root.rglob("*.md")):
        # Skip excluded directories
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue

        fm = parse_frontmatter(md_file)
        if fm and "id" in fm:
            doc_id = fm["id"]
            fm["_path"] = str(md_file.relative_to(root))
            fm["_abs"] = str(md_file)
            documents[doc_id] = fm

    return documents


# ---------------------------------------------------------------------------
# Graph traversal
# ---------------------------------------------------------------------------

def upstream(doc_id: str, documents: dict) -> list:
    """Return all transitive dependencies (what this document depends on)."""
    visited, result, queue = set(), [], [doc_id]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        if current != doc_id and current in documents:
            result.append(current)
        for dep in documents.get(current, {}).get("depends_on", []):
            if dep and dep not in visited:
                queue.append(dep)
    return result


def downstream(doc_id: str, documents: dict) -> list:
    """
    Return all documents transitively affected if doc_id changes.
    Combines referenced_by (explicit) and reverse depends_on (implicit).
    """
    # Build reverse graph from both referenced_by and depends_on
    reverse: dict = defaultdict(set)
    for d_id, doc in documents.items():
        for ref in doc.get("referenced_by", []):
            if ref:
                reverse[ref].add(d_id)
        for dep in doc.get("depends_on", []):
            if dep:
                reverse[dep].add(d_id)

    visited, result, queue = set(), [], [doc_id]
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        visited.add(current)
        if current != doc_id:
            result.append(current)
        for d in reverse.get(current, set()):
            if d not in visited:
                queue.append(d)
    return result


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

SEP = "─" * 62


def doc_line(doc_id: str, documents: dict) -> str:
    if doc_id not in documents:
        return f"{doc_id} (not indexed)"
    doc = documents[doc_id]
    return f"{doc_id}: {doc.get('title', '(no title)')}  [{doc.get('_path', '')}]"


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(documents: dict) -> None:
    print(f"\n{SEP}")
    print(f"  KitchenOS Knowledge Index — {len(documents)} document(s) indexed")
    print(f"{SEP}")

    by_type: dict = defaultdict(list)
    for doc_id, doc in documents.items():
        by_type[doc.get("type", "unknown")].append((doc_id, doc))

    for doc_type in sorted(by_type):
        print(f"\n  {doc_type.upper()}")
        for doc_id, doc in sorted(by_type[doc_type]):
            status = doc.get("status", "—")
            title = doc.get("title", doc_id)
            path = doc.get("_path", "")
            tags = ", ".join(doc.get("tags", []))
            print(f"    [{status:10}] {doc_id:<12} {title}")
            print(f"               path : {path}")
            if tags:
                print(f"               tags : {tags}")
    print()


def cmd_impact(doc_id: str, documents: dict) -> None:
    if doc_id not in documents:
        print(f"\n  '{doc_id}' not found. Run without arguments to list all documents.\n")
        return

    doc = documents[doc_id]
    affected = downstream(doc_id, documents)

    print(f"\n{SEP}")
    print(f"  Impact Analysis: {doc_id} — {doc.get('title', '')}")
    print(f"{SEP}")
    print(f"\n  If '{doc_id}' changes, review:")

    if not affected:
        print("    No downstream documents indexed yet.")
    else:
        for a_id in affected:
            print(f"\n    → {doc_line(a_id, documents)}")
            a_doc = documents.get(a_id, {})
            a_tags = ", ".join(a_doc.get("tags", []))
            if a_tags:
                print(f"       tags: {a_tags}")
    print()


def cmd_deps(doc_id: str, documents: dict) -> None:
    if doc_id not in documents:
        print(f"\n  '{doc_id}' not found.\n")
        return

    doc = documents[doc_id]
    direct = [d for d in doc.get("depends_on", []) if d]
    all_deps = upstream(doc_id, documents)
    transitive = [d for d in all_deps if d not in direct]

    print(f"\n{SEP}")
    print(f"  Dependencies: {doc_id} — {doc.get('title', '')}")
    print(f"{SEP}")

    print(f"\n  Direct ({len(direct)}):")
    if not direct:
        print("    None")
    else:
        for dep in direct:
            print(f"    ← {doc_line(dep, documents)}")

    if transitive:
        print(f"\n  Transitive ({len(transitive)}):")
        for dep in transitive:
            print(f"    ← {doc_line(dep, documents)}")
    print()


def cmd_graph(documents: dict) -> None:
    print(f"\n{SEP}")
    print(f"  Full Dependency Graph")
    print(f"{SEP}\n")

    for doc_id in sorted(documents):
        doc = documents[doc_id]
        deps = [d for d in doc.get("depends_on", []) if d]
        refs = [r for r in doc.get("referenced_by", []) if r]
        print(f"  {doc_id}: {doc.get('title', '')}")
        print(f"    type   : {doc.get('type', '—')}")
        print(f"    status : {doc.get('status', '—')}")
        if deps:
            print(f"    depends_on    : {', '.join(deps)}")
        if refs:
            print(f"    referenced_by : {', '.join(refs)}")
        print()


def cmd_tag(tag: str, documents: dict) -> None:
    print(f"\n{SEP}")
    print(f"  Documents tagged: '{tag}'")
    print(f"{SEP}")

    found = [
        (doc_id, doc)
        for doc_id, doc in documents.items()
        if tag in doc.get("tags", [])
    ]

    if not found:
        print(f"\n  No documents found with tag '{tag}'.")
        all_tags = sorted({t for doc in documents.values() for t in doc.get("tags", [])})
        if all_tags:
            print(f"  Available tags: {', '.join(all_tags)}")
    else:
        for doc_id, doc in sorted(found):
            print(f"\n  {doc_id}: {doc.get('title', '')}")
            print(f"    {doc.get('_path', '')}")
    print()


# --- Inline reference validation -------------------------------------------
#
# Frontmatter IDs are not the only way documents reference each other.
# Prose contains backtick paths (`Company/Operating_Principles.md`),
# markdown links, and document-ID mentions (ADR-009). Stale inline paths
# are invisible to the frontmatter check but actively mislead readers —
# especially AI agents that follow paths literally.

INLINE_SKIP_DIRS = {"0000_Archive", "Archive", ".git", "__pycache__",
                    "node_modules", ".venv"}

BACKTICK_RE = re.compile(r"`([^`\n]+)`")
MDLINK_RE = re.compile(r"\[[^\]]*\]\(([^)\s#]+)\)")
DOC_ID_RE = re.compile(r"\b(?:ADR|PDR|UXDR|GDR|DOC|GOV|AGENT|COMPANY)-\d{3}\b")
PATH_CHARS_RE = re.compile(r"^[A-Za-z0-9_\-./]+$")
PLACEHOLDER_MARKERS = ("XXX", "path/to", "Example", "example")


def looks_like_path(candidate: str) -> bool:
    """Heuristic: does a backtick/link string look like a repo path?"""
    if not PATH_CHARS_RE.match(candidate):
        return False
    if any(m in candidate for m in PLACEHOLDER_MARKERS):
        return False
    return candidate.endswith("/") or candidate.endswith((".md", ".py"))


# Lines containing these markers reference planned-but-not-yet-created
# artifacts on purpose. Missing targets on such lines are warnings, not errors.
PLANNED_LINE_MARKERS = ("planned", "future", "do not create", "add when", "add as")


def check_inline_refs(root: Path, documents: dict) -> tuple:
    """
    Scan every Markdown file (excluding archives) for inline references:
      - backtick paths and markdown link targets → must exist on disk
        (resolved against repo root, then against the file's own directory)
      - document IDs (ADR-009, GDR-001, ...) → must exist in the index
    Returns (errors, warnings). Missing directories, and missing files on
    lines explicitly marked as planned/future, are warnings — the repo
    intentionally references artifacts that do not exist yet.
    """
    known_ids = set(documents)
    errors: list = []
    warnings: list = []

    for md_file in sorted(root.rglob("*.md")):
        if any(part in INLINE_SKIP_DIRS for part in md_file.parts):
            continue
        try:
            text = md_file.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rel = md_file.relative_to(root)

        for lineno, line in enumerate(text.splitlines(), start=1):
            planned = any(m in line.lower() for m in PLANNED_LINE_MARKERS)
            candidates = set(BACKTICK_RE.findall(line)) | set(MDLINK_RE.findall(line))

            for cand in sorted(candidates):
                if not looks_like_path(cand):
                    continue
                if cand.endswith("/"):
                    if not ((root / cand).is_dir() or (md_file.parent / cand).is_dir()):
                        warnings.append(f"  {rel}:{lineno}: directory `{cand}` not found (planned?)")
                elif not ((root / cand).is_file() or (md_file.parent / cand).is_file()):
                    if planned:
                        warnings.append(f"  {rel}:{lineno}: file `{cand}` not found (planned?)")
                    else:
                        errors.append(f"  {rel}:{lineno}: `{cand}` — file not found")

            for doc_id in sorted(set(DOC_ID_RE.findall(line))):
                if doc_id not in known_ids:
                    errors.append(f"  {rel}:{lineno}: document ID '{doc_id}' — not indexed")

    return errors, warnings


def cmd_check(documents: dict, root_dir: str) -> None:
    print(f"\n{SEP}")
    print(f"  Reference Validation")
    print(f"{SEP}\n")

    issues: list = []

    for doc_id, doc in documents.items():
        for dep in doc.get("depends_on", []):
            if dep and dep not in documents:
                issues.append(f"  {doc_id}: depends_on '{dep}' — not indexed")
        for ref in doc.get("referenced_by", []):
            if ref and ref not in documents:
                issues.append(f"  {doc_id}: referenced_by '{ref}' — not indexed")

    inline_errors, inline_warnings = check_inline_refs(Path(root_dir).resolve(), documents)
    issues.extend(inline_errors)

    if not issues:
        print(f"  ✓ Frontmatter: all {len(documents)} indexed documents' cross-references are valid.")
        print(f"  ✓ Inline: all paths, links, and document IDs resolve.\n")
    else:
        print(f"  {len(issues)} issue(s) found:\n")
        for issue in issues:
            print(issue)
        print()

    if inline_warnings:
        print(f"  {len(inline_warnings)} warning(s) — referenced directories that do not exist yet:\n")
        for warning in inline_warnings:
            print(warning)
        print()

    if issues:
        sys.exit(1)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(
        description="KitchenOS Knowledge Index — impact analysis and navigation tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python knowledge_index.py                    List all indexed documents
  python knowledge_index.py --impact ADR-004   Impact analysis for ADR-004
  python knowledge_index.py --deps ADR-005     Dependencies of ADR-005
  python knowledge_index.py --graph            Full dependency graph
  python knowledge_index.py --tag ddd          Documents tagged 'ddd'
  python knowledge_index.py --check            Validate all references
        """,
    )
    parser.add_argument("--impact", metavar="ID",
                        help="Impact analysis: what needs review if this document changes?")
    parser.add_argument("--deps", metavar="ID",
                        help="Dependency analysis: what does this document depend on?")
    parser.add_argument("--graph", action="store_true",
                        help="Print the full dependency graph")
    parser.add_argument("--tag", metavar="TAG",
                        help="List documents by tag")
    parser.add_argument("--check", action="store_true",
                        help="Validate that all referenced document IDs exist")
    parser.add_argument("--dir", default=".",
                        help="Root directory to scan (default: current directory)")
    args = parser.parse_args()

    documents = build_graph(args.dir)

    if not documents:
        print(
            "\n  No documents indexed.\n"
            "  Run from the Product Design directory or pass --dir /path/to/docs\n"
            "  Documents require YAML frontmatter with an 'id' field to be indexed.\n"
        )
        sys.exit(1)

    if args.impact:
        cmd_impact(args.impact, documents)
    elif args.deps:
        cmd_deps(args.deps, documents)
    elif args.graph:
        cmd_graph(documents)
    elif args.tag:
        cmd_tag(args.tag, documents)
    elif args.check:
        cmd_check(documents, args.dir)
    else:
        cmd_list(documents)


if __name__ == "__main__":
    main()
