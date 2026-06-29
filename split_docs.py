#!/usr/bin/env python3
"""
Split KitchenOS_Older_Product_Vision_Rewritten.md into four documents.

Destination mapping:
  10_Product_Vision.md          <- lines 1-1144, 2211-2435, 2801-end
  40_Technical_Architecture.md  <- lines 1145-2210, 2436-2454
  50_Engineering_Handbook.md    <- lines 2455-2800
  20_Domain_Model.md            <- synthesised separately (not this script)
"""

from pathlib import Path

SOURCE = "KitchenOS_Older_Product_Vision_Rewritten.md"

PRODUCT_VISION_FRONTMATTER = """\
---
id: DOC-010
title: KitchenOS Product Vision
type: product-vision
status: active
owner: product
depends_on: []
referenced_by: [DOC-020, DOC-040, DOC-050]
tags: [product-vision, ux, features, mvp, marketplace, household, personas, onboarding, growth]
date: 2026
---

# KitchenOS: Product Vision

> This document is the authoritative source for what KitchenOS is, why it exists, how it looks to users, and the phased plan to build it. Technical implementation decisions live in `40_Technical_Architecture.md`. Engineering practices live in `50_Engineering_Handbook.md`. Architectural decisions live in `60_ADRs/`.

---

"""

TECHNICAL_ARCHITECTURE_FRONTMATTER = """\
---
id: DOC-040
title: KitchenOS Technical Architecture
type: architecture
status: active
owner: architecture
depends_on: [DOC-020, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006]
referenced_by: [DOC-050]
tags: [architecture, backend, ai, event-sourcing, offline, technology-stack, ddd, household-decision-engine, building-blocks]
date: 2026
---

# KitchenOS: Technical Architecture

> This document is the authoritative source for how KitchenOS is built: the AI architecture, backend design, event sourcing model, offline strategy, technology stack, architecture principles, and building blocks. Product decisions live in `10_Product_Vision.md`. Domain entity definitions live in `20_Domain_Model.md`. Specific technology choices are recorded in `60_ADRs/`.

---

"""

ENGINEERING_HANDBOOK_FRONTMATTER = """\
---
id: DOC-050
title: KitchenOS Engineering Handbook
type: engineering-handbook
status: active
owner: engineering
depends_on: [DOC-040, ADR-001, ADR-002, ADR-003, ADR-004, ADR-005, ADR-006]
referenced_by: []
tags: [engineering, testing, ci-cd, tdd, bdd, ddd, quality, testcontainers, flutter-test, jest]
date: 2026
---

# KitchenOS: Engineering Handbook

> This document is the authoritative source for how the KitchenOS engineering team works: MVP tech stack, testing philosophy, coverage targets, CI/CD pipeline, and engineering principles. Architecture decisions live in `40_Technical_Architecture.md` and `60_ADRs/`.

---

"""


def extract(lines: list, start: int, end: int) -> str:
    """Extract lines (1-indexed, inclusive)."""
    return "".join(lines[start - 1 : end])


def main():
    source = Path(SOURCE)
    if not source.exists():
        print(f"ERROR: {SOURCE} not found. Run from the Product Design directory.")
        return

    lines = source.read_text(encoding="utf-8").splitlines(keepends=True)
    total = len(lines)
    print(f"Source: {SOURCE} ({total} lines)")

    # -----------------------------------------------------------------------
    # 10_Product_Vision.md
    # Sections 1-23  (lines 1-1144)
    # Sections 38-40 (lines 2211-2435)
    # Sections 43-62 (lines 2801-end)
    # -----------------------------------------------------------------------
    pv = (
        PRODUCT_VISION_FRONTMATTER
        + extract(lines, 1, 1144)
        + "\n\n---\n\n"
        + extract(lines, 2211, 2435)
        + "\n\n---\n\n"
        + extract(lines, 2801, total)
    )
    Path("10_Product_Vision.md").write_text(pv, encoding="utf-8")
    pv_lines = len(pv.splitlines())
    print(f"Written: 10_Product_Vision.md  ({pv_lines} lines)")

    # -----------------------------------------------------------------------
    # 40_Technical_Architecture.md
    # Sections 24-37.10 (lines 1145-2210)
    # Section 41        (lines 2436-2454)
    # -----------------------------------------------------------------------
    ta = (
        TECHNICAL_ARCHITECTURE_FRONTMATTER
        + extract(lines, 1145, 2210)
        + "\n\n---\n\n"
        + extract(lines, 2436, 2454)
    )
    Path("40_Technical_Architecture.md").write_text(ta, encoding="utf-8")
    ta_lines = len(ta.splitlines())
    print(f"Written: 40_Technical_Architecture.md  ({ta_lines} lines)")

    # -----------------------------------------------------------------------
    # 50_Engineering_Handbook.md
    # Sections 42-42.5 (lines 2455-2800)
    # -----------------------------------------------------------------------
    eh = ENGINEERING_HANDBOOK_FRONTMATTER + extract(lines, 2455, 2800)
    Path("50_Engineering_Handbook.md").write_text(eh, encoding="utf-8")
    eh_lines = len(eh.splitlines())
    print(f"Written: 50_Engineering_Handbook.md  ({eh_lines} lines)")

    # -----------------------------------------------------------------------
    # Sanity check: coverage
    # -----------------------------------------------------------------------
    covered = (1144 - 1 + 1) + (2435 - 2211 + 1) + (total - 2801 + 1)  # PV
    covered += (2210 - 1145 + 1) + (2454 - 2436 + 1)                    # TA
    covered += (2800 - 2455 + 1)                                          # EH
    print(f"\nSource lines:  {total}")
    print(f"Lines covered: {covered}")
    print(f"Gap check: {total - covered} lines not assigned (expected ~0)")


if __name__ == "__main__":
    main()
