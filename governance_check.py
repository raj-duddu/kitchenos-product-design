#!/usr/bin/env python3
"""
Amanaska Governance Check — generic enforcement engine.

This script contains NO policy. Every rule parameter is read at runtime
from the frontmatter of the documents that own the rules:

  - 00_Knowledge_Map.md                              (documentation-system rules)
      enforced_governed_dirs         which folders are governed
      enforced_required_frontmatter  keys every governed document must declare
      enforced_document_statuses     legal status values for ordinary documents

  - Company/Governance/Architecture_Governance.md    (decision-record rules)
      enforced_decision_types        which document types are decision records
      enforced_section_types         which of those must carry required sections
      enforced_required_sections     mandatory sections (## headings)
      enforced_decision_statuses     legal status values for decision records
      enforced_principles_field      frontmatter field citing Operating Principles
      enforced_no_delete_dirs        directories whose records are never deleted
      enforced_history_section       section logging state transitions
      enforced_status_header         header line that must mirror frontmatter status

To change a rule: change the governing document (prose AND its enforced_*
frontmatter, same commit). This script never needs to change for a rule
change — that is the point.

Usage:
    python governance_check.py                       Lint whole repo
    python governance_check.py --strict-files A B    Error-level Operating-
                                                     Principles check for
                                                     the listed files
    python governance_check.py --dir /path           Scan a different root

Exit code 1 on errors (including missing enforcement config).
No dependencies beyond stdlib.
"""

import sys
import argparse
from pathlib import Path

from knowledge_index import parse_frontmatter

# Where the rules live (locations, not policy — the Knowledge Map's
# Source of Truth table names these as the owning documents).
KNOWLEDGE_MAP = "00_Knowledge_Map.md"
GOVERNANCE_DOC = "Company/Governance/Architecture_Governance.md"

# Structural mechanics only — not policy.
SKIP_DIRS = {"0000_Archive", "Archive", ".git", "__pycache__",
             "node_modules", ".venv", "Templates"}

SEP = "─" * 62


def load_enforcement(root: Path) -> dict:
    """Read all rule parameters from the documents that own them."""
    sources = {
        KNOWLEDGE_MAP: ["enforced_governed_dirs",
                        "enforced_required_frontmatter",
                        "enforced_document_statuses"],
        GOVERNANCE_DOC: ["enforced_decision_types",
                         "enforced_section_types",
                         "enforced_required_sections",
                         "enforced_decision_statuses",
                         "enforced_principles_field",
                         "enforced_no_delete_dirs",
                         "enforced_history_section",
                         "enforced_status_header"],
    }
    config: dict = {}
    missing: list = []

    for doc, keys in sources.items():
        fm = parse_frontmatter(root / doc) or {}
        for key in keys:
            value = fm.get(key)
            if not value:
                missing.append(f"  {doc}: missing '{key}' in frontmatter")
            config[key] = value

    if missing:
        print(f"\n{SEP}\n  Governance Check — CONFIGURATION ERROR\n{SEP}\n")
        print("  Enforcement parameters could not be loaded:\n")
        for m in missing:
            print(m)
        print("\n  Rules live in the governing documents' frontmatter. "
              "Restore them there.\n")
        sys.exit(1)

    return config


def check_deletions(cfg: dict, deleted_files: list) -> list:
    """Deleted paths under enforced_no_delete_dirs are governance violations."""
    protected = cfg["enforced_no_delete_dirs"]
    errors = []
    for f in deleted_files:
        parts = Path(f).parts
        if any(p in parts for p in protected):
            errors.append(
                f"  {f}: decision records are never deleted — mark them "
                f"Superseded or Deprecated instead ({GOVERNANCE_DOC})")
    return errors


def check(root: Path, cfg: dict, strict_files: set) -> tuple:
    errors: list = []
    warnings: list = []
    seen_ids: dict = {}

    governed_dirs = set(cfg["enforced_governed_dirs"])
    required_keys = cfg["enforced_required_frontmatter"]
    doc_statuses = set(cfg["enforced_document_statuses"])
    decision_types = {t.lower() for t in cfg["enforced_decision_types"]}
    section_types = {t.lower() for t in cfg["enforced_section_types"]}
    required_sections = [f"## {s}" for s in cfg["enforced_required_sections"]]
    decision_statuses = set(cfg["enforced_decision_statuses"])
    principles_field = cfg["enforced_principles_field"]

    for md_file in sorted(root.rglob("*.md")):
        if any(part in SKIP_DIRS for part in md_file.parts):
            continue
        rel = md_file.relative_to(root)
        if not rel.parts or rel.parts[0] not in governed_dirs:
            continue

        fm = parse_frontmatter(md_file)
        if fm is None:
            errors.append(f"  {rel}: missing YAML frontmatter")
            continue

        # Frontmatter completeness and unique id
        for key in required_keys:
            if key not in fm or not fm[key]:
                errors.append(f"  {rel}: frontmatter missing '{key}'")

        doc_id = fm.get("id", "")
        if doc_id:
            if doc_id in seen_ids:
                errors.append(
                    f"  {rel}: duplicate id '{doc_id}' (also in {seen_ids[doc_id]})")
            seen_ids[doc_id] = rel

        # ID/filename consistency for prefixed records (ADR-001_*.md etc.)
        stem_prefix = md_file.stem.split("_")[0]
        if "-" in stem_prefix and doc_id and stem_prefix != doc_id:
            errors.append(
                f"  {rel}: filename says '{stem_prefix}' but frontmatter id is '{doc_id}'")

        doc_type = str(fm.get("type", "")).lower()
        is_decision = doc_type in decision_types

        # Status vocabulary — decision records have their own lifecycle
        status = fm.get("status", "")
        allowed = decision_statuses if is_decision else doc_statuses
        if status and status not in allowed:
            errors.append(
                f"  {rel}: status '{status}' not one of {sorted(allowed)} "
                f"({'decision-record lifecycle' if is_decision else 'document statuses'})")

        if not is_decision:
            continue

        text = md_file.read_text(encoding="utf-8")

        # Required sections in decision records
        if doc_type in section_types:
            for section in required_sections:
                if section not in text:
                    errors.append(f"  {rel}: missing required section '{section}'")

        # History section — state transitions recorded in the record itself
        history_heading = f"## {cfg['enforced_history_section']}"
        if history_heading not in text:
            msg = (f"  {rel}: missing '{history_heading}' section — every state "
                   f"change is logged in the record ({GOVERNANCE_DOC}, "
                   f"Recording State Changes)")
            if str(rel) in strict_files or str(md_file) in strict_files:
                errors.append(msg)
            else:
                warnings.append(msg + "  [warning: pre-existing record]")

        # Status header must mirror frontmatter — single authority, checked projection
        marker = f"**{cfg['enforced_status_header']}:**"
        idx = text.find(marker)
        if idx == -1:
            msg = (f"  {rel}: missing '{marker}' header line — human-readable "
                   f"status display is required ({GOVERNANCE_DOC}, Recording State Changes)")
            if str(rel) in strict_files or str(md_file) in strict_files:
                errors.append(msg)
            else:
                warnings.append(msg + "  [warning: pre-existing record]")
        else:
            line_end = text.find("\n", idx)
            shown = text[idx + len(marker):line_end if line_end != -1 else None].strip()
            if status and not shown.lower().startswith(status.lower()):
                errors.append(
                    f"  {rel}: header shows '{shown}' but frontmatter status is "
                    f"'{status}' — frontmatter is the authority; fix the header")

        # Operating Principles citation
        principles = fm.get(principles_field)
        cited = bool(principles) if isinstance(principles, list) else bool(
            principles and str(principles).strip())
        if not cited:
            msg = (f"  {rel}: no '{principles_field}:' frontmatter field — "
                   f"every decision record must cite at least one Operating "
                   f"Principle ({GOVERNANCE_DOC})")
            if str(rel) in strict_files or str(md_file) in strict_files:
                errors.append(msg)
            else:
                warnings.append(msg + "  [warning: pre-existing record]")

    return errors, warnings


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Lint knowledge documents against the rules defined in "
                    "the governing documents' frontmatter")
    parser.add_argument("--strict-files", nargs="*", default=[],
                        help="Files (repo-relative) held to error-level "
                             "Operating-Principles citation")
    parser.add_argument("--deleted-files", nargs="*", default=[],
                        help="Files deleted in this change — checked against "
                             "enforced_no_delete_dirs")
    parser.add_argument("--dir", default=".",
                        help="Root directory to scan (default: current directory)")
    args = parser.parse_args()

    root = Path(args.dir).resolve()
    cfg = load_enforcement(root)
    strict = {f.strip() for f in args.strict_files if f.strip()}
    deleted = [f.strip() for f in args.deleted_files if f.strip()]

    errors, warnings = check(root, cfg, strict)
    errors.extend(check_deletions(cfg, deleted))

    print(f"\n{SEP}")
    print("  Governance Check")
    print(f"{SEP}\n")
    print(f"  Rules loaded from: {KNOWLEDGE_MAP}, {GOVERNANCE_DOC}\n")

    if errors:
        print(f"  {len(errors)} error(s):\n")
        for e in errors:
            print(e)
        print()
    if warnings:
        print(f"  {len(warnings)} warning(s):\n")
        for w in warnings:
            print(w)
        print()
    if not errors and not warnings:
        print("  ✓ All governed documents comply.\n")
    elif not errors:
        print("  ✓ No errors.\n")

    if errors:
        sys.exit(1)


if __name__ == "__main__":
    main()
