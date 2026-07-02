# Amanaska — Product Design Repository

> **Every piece of information has exactly one authoritative home. Other documents may reference it but must not duplicate it.**
>
> We are a **decision intelligence company**. We surface better possibilities that users couldn't reasonably discover on their own, across every domain we enter. KitchenOS is the first product. HealthOS, FinanceOS, LearningOS, and more will follow.

**Start here:** [`00_Knowledge_Map.md`](00_Knowledge_Map.md)

---

## Repository Structure

```text
Product Design/
├── 00_Knowledge_Map.md          ← navigation anchor — start here
├── Company/                     ← why the company exists; governs all products
│   ├── Vision_and_Mission.md
│   ├── Operating_Principles.md  ← 10 guiding principles; company constitution
│   └── Governance/
│       ├── AI_Governance.md
│       ├── Risk_Register.md
│       └── GDRs/                ← GDR-001, GDR-002, ...
├── Products/
│   └── KitchenOS/               ← all KitchenOS product knowledge
│       ├── 10_Product_Vision.md
│       ├── 20_Domain_Model.md
│       ├── 30_PRDs/
│       ├── 40_Technical_Architecture.md
│       ├── 45_Solution_Designs/
│       ├── 50_Engineering_Handbook.md
│       ├── 60_Decision_Records/
│       │   ├── ADRs/            ← ADR-001 – ADR-011
│       │   ├── PDRs/            ← PDR-001 – PDR-009
│       │   └── UXDRs/
│       ├── 70_UX_Design_System/
│       ├── 80_API_Reference/
│       ├── 90_Platform_Operations/
│       ├── 95_Customer_Expert_Operations/
│       └── 100_Security/
├── Knowledge/                   ← shared concepts reusable across all products
│   ├── Glossary.md
│   ├── Canonical_Data_Model.md
│   └── Patterns/
│       ├── DDD.md
│       ├── Event_Sourcing.md
│       └── Privacy_By_Design.md
├── Agents/                      ← AI agent operating manuals
│   ├── Architect.md
│   ├── Product_Manager.md
│   └── Engineering_Manager.md
├── Research/                    ← founder research: competitors, technology, regulations, ideas
├── Process/                     ← how ideas become shipped features (all products)
│   └── Product_Development_Lifecycle.md
├── Templates/                   ← reusable formats and checklists
│   ├── PRD_Template.md
│   ├── ADR_Template.md
│   ├── PDR_Template.md
│   ├── LLD_Template.md
│   ├── Architecture_Review_Checklist.md
│   └── Definition_of_Done.md
├── Archive/                     ← superseded documents (read-only)
└── knowledge_index.py           ← dependency analysis tool
```

---

## How Ideas Become Software

```text
Research/          ← raw insight and exploration
      ↓ informs
Company/           ← Operating Principles and GDRs set the boundaries
      ↓ constrains
Product Vision     ← what we build and why
      ↓ scopes
PRDs               ← what this feature does
      ↓ specifies
Domain Model       ← what business concepts are involved
      ↓ models
Architecture       ← how the system is structured
      ↓ designs
Solution Designs   ← how this feature is built (LLD)
      ↓ implements
Code + Tests       ← the running system
      ↓ operates
Operations         ← how we keep it running
      ↓ learns
Research/ (loop)   ← feedback feeds the next cycle
```

---

## Decision Records

Every significant decision is recorded with full context, rationale, and alternatives considered. Each decision record must cite which Operating Principles it implements or trades off against.

| Type | Prefix | Covers | Lives in |
|---|---|---|---|
| GDR | `GDR-XXX` | Company-wide governance policy | `Company/Governance/GDRs/` |
| ADR | `ADR-XXX` | Architecture and technology choices | `Products/KitchenOS/60_Decision_Records/ADRs/` |
| PDR | `PDR-XXX` | Product scope and strategy choices | `Products/KitchenOS/60_Decision_Records/PDRs/` |
| UXDR | `UXDR-XXX` | UX pattern and interaction design choices | `Products/KitchenOS/60_Decision_Records/UXDRs/` |

GDRs are company-wide and cannot be overridden by ADRs or PDRs.

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
