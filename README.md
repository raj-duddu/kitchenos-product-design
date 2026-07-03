# Amanaska — Product Design Repository

> **Every piece of information has exactly one authoritative home. Other documents may reference it but must not duplicate it.**
>
> We are a **decision intelligence company**. We surface better possibilities that users couldn't reasonably discover on their own, across every domain we enter. KitchenOS is the first product. HealthOS, FinanceOS, LearningOS, and more will follow.

**Start here:** [`00_Knowledge_Map.md`](00_Knowledge_Map.md) — it owns the repository structure, document registry, documentation manifest, dependency chain, and onboarding path. This README deliberately does not duplicate them.

---

## What This Repository Is

The operating model for the company — not code. `Company/` holds the vision, principles, and governance that constrain everything; `Products/` holds per-product knowledge (vision, domain model, architecture, decision records); `Knowledge/` holds shared concepts and patterns; `Agents/` holds role operating manuals for humans and AI alike; `Process/` defines how ideas become shipped features; `Templates/` provides the reusable formats. Decision records (GDR, ADR, PDR, UXDR) capture *why* at every level — see the Knowledge Map for what goes where.

---

## Tooling

```bash
# Validate all references: frontmatter IDs, inline paths, links, doc-ID mentions
# (exits 1 on broken references; planned-but-not-yet-created artifacts are warnings)
python knowledge_index.py --check

# Lint documents against governance rules (rules are read at runtime from
# the enforced_* frontmatter of 00_Knowledge_Map.md and Architecture_Governance.md
# — see Process/Quality_Gates.md)
python governance_check.py

# List all indexed documents / analyse dependencies
python knowledge_index.py
python knowledge_index.py --deps DOC-040     # what a document depends on
python knowledge_index.py --impact DOC-010   # what to review if it changes
python knowledge_index.py --graph            # full dependency graph
```

Requires Python 3.8+. No external dependencies.

---

## Quality Gates

Every pull request runs reference validation, governance linting, decision-record deletion protection, and downstream-impact analysis. The gate-to-rule mapping and branch-protection setup live in [`Process/Quality_Gates.md`](Process/Quality_Gates.md).
