# KitchenOS — Product Design Repository

> **Every piece of information has exactly one authoritative home. Other documents may reference it but must not duplicate it.**

This repository contains all product design, architecture, process, and decision documentation for KitchenOS.

**Start here:** [`00_Knowledge_Map.md`](00_Knowledge_Map.md)

---

## Repository Structure

```text
Product Design/
├── 00_Knowledge_Map.md         ← navigation anchor — start here
├── Knowledge/                  ← what KitchenOS is and how it works
│   ├── 10_Product_Vision.md
│   ├── 20_Domain_Model.md
│   ├── 30_PRDs/                (planned)
│   ├── 40_Technical_Architecture.md
│   ├── 45_Solution_Designs/    (planned)
│   ├── 50_Engineering_Handbook.md
│   ├── 60_Decision_Records/    (ADRs, PDRs, UXDRs)
│   ├── 70_UX_Design_System/    (planned)
│   ├── 80_API_Reference/       (planned)
│   ├── 90_Operations/          (planned)
│   └── 100_Security/           (planned)
├── Process/                    ← how ideas become shipped features
│   └── Product_Development_Lifecycle.md
├── Templates/                  ← reusable formats and checklists
│   ├── PRD_Template.md
│   ├── ADR_Template.md
│   ├── PDR_Template.md
│   ├── SD_Template.md
│   ├── Architecture_Review_Checklist.md
│   └── Definition_of_Done.md
├── Archive/                    ← superseded documents (read-only)
└── knowledge_index.py          ← dependency analysis tool
```

---

## Knowledge Index Tool

Analyse document dependencies from the command line:

```bash
# List all indexed documents
python knowledge_index.py

# Validate all cross-references
python knowledge_index.py --check

# Show what a document depends on
python knowledge_index.py --upstream DOC-040

# Show what is affected if a document changes
python knowledge_index.py --downstream DOC-010
```

Requires Python 3.8+. No external dependencies.

---

## Three Dimensions

Every artifact in this system belongs to one **dimension**, is produced at a specific **process stage**, and approved under a **governance** rule. See [`00_Knowledge_Map.md`](00_Knowledge_Map.md) — Three Dimensions section for the full model.

---

## Decision Records

All significant decisions (architecture, product, UX) are recorded in `Knowledge/60_Decision_Records/` with full context, rationale, and alternatives considered.

| Type | Prefix | Covers |
|---|---|---|
| ADR | `ADR-XXX` | Technology and infrastructure choices |
| PDR | `PDR-XXX` | Product scope and strategy choices |
| UXDR | `UXDR-XXX` | UX pattern and design choices |
