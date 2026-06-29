# KitchenOS Knowledge Map

> **Every piece of information has exactly one authoritative home. Other documents may reference it but must not duplicate it.**

This principle governs the entire documentation system. When in doubt about where something belongs, consult the Documentation Manifest below. When in doubt about whether to copy content, don't — link instead.

---

This is the top-level navigation document for all KitchenOS knowledge. Start here when joining the team, making a decision, or finding where something belongs.

---

## Repository Structure

The repository is organised into three top-level sections:

```text
Product Design/
├── 00_Knowledge_Map.md         ← start here (navigation anchor)
├── Knowledge/                  ← what KitchenOS is and how it works
├── Process/                    ← how ideas become shipped features
└── Templates/                  ← reusable formats and checklists
```

---

## Document Registry

### Knowledge — What We Know

| # | Document | File | Audience | Purpose | Status |
|---|---|---|---|---|---|
| 00 | Knowledge Map (this file) | `00_Knowledge_Map.md` | Everyone | Navigate all documentation | Active |
| 10 | Product Vision | `Knowledge/10_Product_Vision.md` | Founders, PMs, Designers, Investors | What we are building and why | Active |
| 20 | Domain Model | `Knowledge/20_Domain_Model.md` | Product, Engineering, QA | What business concepts exist, how they relate, and the ubiquitous language | Active |
| 30 | PRDs | `Knowledge/30_PRDs/` | Product, Engineering, QA | Per-feature requirements, acceptance criteria, BDD | Planned |
| 40 | Technical Architecture | `Knowledge/40_Technical_Architecture.md` | Architects, Senior Engineers | System-level architecture — HLD, services, patterns, principles | Active |
| 45 | Solution Designs | `Knowledge/45_Solution_Designs/` | Engineers, Architects | Feature-level technical design — module responsibilities, sequence diagrams, data flows (LLD) | Planned |
| 50 | Engineering Handbook | `Knowledge/50_Engineering_Handbook.md` | All Engineers | How we write and test software here | Active |
| 60 | Decision Records | `Knowledge/60_Decision_Records/` | Everyone | Why significant decisions were made — architecture (ADRs), product (PDRs), and UX (UXDRs) | Active (6 ADRs, 3 PDRs) |
| 70 | UX Design System | `Knowledge/70_UX_Design_System/` | Designers, Frontend Engineers | Component library, design tokens, interaction patterns | Planned (post-MVP) |
| 80 | API Reference | `Knowledge/80_API_Reference/` | Engineers, QA | How systems communicate | Planned |
| 90 | Operations | `Knowledge/90_Operations/` | Engineering, DevOps | How production runs | Planned |
| 100 | Security | `Knowledge/100_Security/` | Engineering, Legal, Compliance | Auth, encryption, privacy, threat model, incident response | Planned |

### Process — How Work Flows

| Document | File | Audience | Purpose | Status |
|---|---|---|---|---|
| Product Development Lifecycle | `Process/Product_Development_Lifecycle.md` | Everyone | How ideas become shipped features — 12 stages with gate criteria | Active |

### Templates — Reusable Formats

| Template | File | Used In |
|---|---|---|
| PRD Template | `Templates/PRD_Template.md` | Stage 3 — Product Definition |
| ADR Template | `Templates/ADR_Template.md` | Stage 5 — Architecture Review |
| PDR / UXDR Template | `Templates/PDR_Template.md` | Stage 3 or Stage 4 |
| Solution Design Template | `Templates/SD_Template.md` | Stage 5 — Technical Design |
| Architecture Review Checklist | `Templates/Architecture_Review_Checklist.md` | Stage 5 — Architecture Review |
| Definition of Done | `Templates/Definition_of_Done.md` | Stage 6 — Planning |

---

## Document Dependency Chain

Documents depend on the ones above them. When a concept changes, all documents downstream must be reviewed.

```text
Product Vision (10)
        │
        ▼
Domain Model (20)
        │
        ├────────────────────┐
        ▼                    ▼
PRDs (30)        Technical Architecture (40)
        │                    │
        ▼                    ▼
UX Design System (70)  Solution Designs (45)
        │                    │
        └──────┬─────────────┘
               ▼
      Engineering Handbook (50)
               │
        ┌──────┼──────────────┐
        ▼      ▼              ▼
  API (80)  Ops (90)    Security (100)
               │
               ▼
     Implementation (Code + Tests)
```

**Decision Records (60) are cross-cutting — not in the chain above.**
They are written when a significant decision is made at any layer:

```text
PDRs   ← decisions made at Product Vision layer (10)
ADRs   ← decisions made at Technical Architecture layer (40)
UXDRs  ← decisions made at PRD or UX Design System layer (30 / 70)
```

A Decision Record documents *why* — it does not replace the living document where the decision is expressed.

---

## Three Dimensions of the KitchenOS Engineering System

Every artifact in this system belongs to one **dimension**, is produced at a specific **process stage**, and is approved under a **governance** rule. These three dimensions are independent — confusing them causes documentation to end up in the wrong place.

```text
┌─────────────────────────────────────────────────┐
│  Knowledge  (what we know and have built)       │
│                                                 │
│  Strategic   Product Vision, Philosophy         │
│  Business    Domain Model, PRDs, UX Design      │
│  Technical   Architecture, Solution Designs,    │
│              API Reference, Security            │
│  Engineering Handbook, Design System, Ops       │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Process  (how work flows)                      │
│                                                 │
│  Idea → Discovery → PRD → UX → Architecture    │
│  → Technical Design → Dev → Test → Deploy       │
│  → Operate → Learn → Iterate                   │
└─────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────┐
│  Governance  (who approves and when)            │
│                                                 │
│  Stage gates, Definition of Done, ADR approval  │
│  Architecture review, Security review,          │
│  Release approval, Code review                  │
└─────────────────────────────────────────────────┘
```

An artifact can **belong** to Knowledge, be **produced** at a Process stage, and be **approved** under Governance simultaneously:

| Artifact | Knowledge | Produced At | Governance |
|---|---|---|---|
| Product Vision | Strategic | Discovery | Founder approval |
| PRD | Business | Product Definition (Stage 3) | Product review |
| UX Mockups | Business | UX Design (Stage 4) | UX review |
| Technical Architecture | Technical | Architecture Review (Stage 5) | Architecture review |
| Solution Design (LLD) | Technical | Technical Design (Stage 5) | Tech Lead review |
| ADR | Technical | When architecture changes | Architecture approval |
| PDR | Strategic | When product scope changes | Founder/Product approval |
| Code | Engineering | Development (Stage 7) | Code review |
| Tests | Engineering | Testing (Stage 8) | CI/CD gates |

The abstraction gradient within Knowledge flows naturally from vision to code:

```text
Product Vision  →  Domain Model  →  PRDs  →  Architecture (HLD)  →  Solution Designs (LLD)  →  Code
```

---

## Single Source of Truth

Every topic has exactly one authoritative home. Do not document the same concept in multiple places.

| Topic | Source of Truth | Location |
|---|---|---|
| Product vision and mission | Product Vision | `Knowledge/10_Product_Vision.md`, Section 1–5 |
| North Star Metric | Product Vision | `Knowledge/10_Product_Vision.md`, Section 10 |
| User personas and JTBD | Product Vision | `Knowledge/10_Product_Vision.md`, Sections 12–13 |
| Screen responsibilities and UX rules | Product Vision | `Knowledge/10_Product_Vision.md`, Sections 19–20 |
| Offline UX behaviour | Product Vision | `Knowledge/10_Product_Vision.md`, Section 22 |
| MVP-0 scope and user flows | Product Vision | `Knowledge/10_Product_Vision.md`, Sections 38–40 |
| Post-MVP roadmap | Product Vision | `Knowledge/10_Product_Vision.md`, Section 47 |
| Allergy and dietary safety | Product Vision | `Knowledge/10_Product_Vision.md`, Section 56 |
| Nutrition goals | Product Vision | `Knowledge/10_Product_Vision.md`, Section 57 |
| Expert marketplace | Product Vision | `Knowledge/10_Product_Vision.md`, Section 58 |
| Negative flows and corrections | Product Vision | `Knowledge/10_Product_Vision.md`, Section 59 |
| Ubiquitous language | Domain Model | `Knowledge/20_Domain_Model.md` |
| Bounded contexts | Domain Model | `Knowledge/20_Domain_Model.md` |
| Aggregate roots and entities | Domain Model | `Knowledge/20_Domain_Model.md` |
| Data model (all tables) | Domain Model | `Knowledge/20_Domain_Model.md` |
| Domain events catalogue | Domain Model | `Knowledge/20_Domain_Model.md` |
| Standard event envelope | Domain Model | `Knowledge/20_Domain_Model.md` |
| Business invariants | Domain Model | `Knowledge/20_Domain_Model.md` |
| Household Decision Engine (architecture) | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 24 |
| Household Timeline (architecture) | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 32.8 |
| Domain event architecture | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 32 |
| Offline AI context constraint | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 37.8 |
| Cloud infrastructure | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 37.6 |
| Architecture principles | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 37.9 |
| Architecture building blocks | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 37.10 |
| Feature-level technical design (LLD) | Solution Designs | `Knowledge/45_Solution_Designs/SD-XXX_Feature.md` |
| MVP-0 tech stack | Engineering Handbook | `Knowledge/50_Engineering_Handbook.md`, Section 42 |
| Engineering quality and testing | Engineering Handbook | `Knowledge/50_Engineering_Handbook.md`, Section 42.5 |
| BDD scenario format | Engineering Handbook | `Knowledge/50_Engineering_Handbook.md`, Section 42.5 |
| Engineering principles | Engineering Handbook | `Knowledge/50_Engineering_Handbook.md`, Section 42.5 |
| Feature development lifecycle | Process | `Process/Product_Development_Lifecycle.md` |
| Stage gates and governance | Process | `Process/Product_Development_Lifecycle.md` |
| Architecture governance | Knowledge Map | `00_Knowledge_Map.md` |
| Why Flutter? | ADR | `Knowledge/60_Decision_Records/ADR-001_Flutter.md` |
| Why GCP? | ADR | `Knowledge/60_Decision_Records/ADR-002_GCP.md` |
| Why PostgreSQL? | ADR | `Knowledge/60_Decision_Records/ADR-003_PostgreSQL.md` |
| Why event sourcing? | ADR | `Knowledge/60_Decision_Records/ADR-004_Event_Sourcing.md` |
| Why modular monolith? | ADR | `Knowledge/60_Decision_Records/ADR-005_Modular_Monolith.md` |
| Why Cloud Run? | ADR | `Knowledge/60_Decision_Records/ADR-006_Cloud_Run.md` |
| Why food before fitness? | PDR | `Knowledge/60_Decision_Records/PDR-001_Food_Before_Fitness.md` |
| Why household not individual? | PDR | `Knowledge/60_Decision_Records/PDR-002_Household_Not_Individual.md` |
| Why Home screen is a question? | PDR | `Knowledge/60_Decision_Records/PDR-003_Home_Screen_Question.md` |

---

## Documentation Manifest

When creating new documentation, use this table to find the right home. **Never create a new document type without updating this manifest.**

| I need to document... | It belongs in... | File / Directory |
|---|---|---|
| A new feature's requirements and acceptance criteria | PRD | `Knowledge/30_PRDs/PRD-XXX_Feature_Name.md` |
| A new domain concept or entity | Domain Model | `Knowledge/20_Domain_Model.md` |
| A new API endpoint | API Reference | `Knowledge/80_API_Reference/` |
| A new UI component or design pattern | UX Design System | `Knowledge/70_UX_Design_System/` |
| A coding standard or engineering practice | Engineering Handbook | `Knowledge/50_Engineering_Handbook.md` |
| An authentication or encryption standard | Security | `Knowledge/100_Security/` |
| A production runbook or infrastructure config | Operations | `Knowledge/90_Operations/` |
| Why a technology was chosen | ADR | `Knowledge/60_Decision_Records/ADR-XXX_Decision.md` |
| Why a product scope or strategy decision was made | PDR | `Knowledge/60_Decision_Records/PDR-XXX_Decision.md` |
| Why a UX pattern or navigation choice was made | UXDR | `Knowledge/60_Decision_Records/UXDR-XXX_Decision.md` |
| A new ubiquitous language term | Domain Model glossary | `Knowledge/20_Domain_Model.md` |
| A cross-cutting architectural principle | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 37.9 |
| A reusable architectural building block | Technical Architecture | `Knowledge/40_Technical_Architecture.md`, Section 37.10 |
| How a specific feature is designed at module/class level | Solution Design | `Knowledge/45_Solution_Designs/SD-XXX_Feature.md` |
| A process, stage gate, or lifecycle rule | Process | `Process/Product_Development_Lifecycle.md` |
| A reusable checklist or document format | Templates | `Templates/` |

---

## Decision Records Index

Decision Records capture *why* a decision was made, not how it was implemented. Three types:

- **ADR** — Architecture Decision Records. Technology, infrastructure, and system design choices.
- **PDR** — Product Decision Records. Product positioning, scope, and strategic choices.
- **UXDR** — UX Decision Records. Design philosophy, navigation, and interaction pattern choices.

### Architecture Decision Records

| ID | Decision | Status | Date |
|---|---|---|---|
| ADR-001 | Flutter for mobile | Accepted | 2026 |
| ADR-002 | Google Cloud Platform | Accepted | 2026 |
| ADR-003 | PostgreSQL as primary database | Accepted | 2026 |
| ADR-004 | Domain-driven event sourcing | Accepted | 2026 |
| ADR-005 | Modular monolith for backend | Accepted | 2026 |
| ADR-006 | Cloud Run for compute | Accepted | 2026 |

### Product Decision Records

| ID | Decision | Status | Date |
|---|---|---|---|
| PDR-001 | Food decisions before fitness features | Accepted | 2026 |
| PDR-002 | Household as primary unit, not individual | Accepted | 2026 |
| PDR-003 | Home screen answers a question, not a dashboard | Accepted | 2026 |

### UX Decision Records

| ID | Decision | Status | Date |
|---|---|---|---|
| *(none yet)* | | | |

---

## Concept Ownership

Every major concept has one owning team and a single source of truth. When the concept changes, the owner is responsible for updating all downstream references.

| Concept | Owner | Source of Truth | Referenced By |
|---|---|---|---|
| Household | Domain Model | `20_Domain_Model.md` | All documents |
| Household Timeline | Product + Architecture | `10_Product_Vision.md` Section 59.6 (product), `40_Technical_Architecture.md` Section 32.8 (architecture), `20_Domain_Model.md` (data model) | Vision, Architecture, Engineering Handbook, Mobile UI |
| Household Decision Engine | Product + Architecture | `40_Technical_Architecture.md`, Section 24 | Vision, Domain Model, Architecture, AI Layer |
| Domain event architecture | Architecture | `40_Technical_Architecture.md`, Section 32 | Domain Model, Engineering Handbook, Tests |
| Domain events catalogue | Domain Model | `20_Domain_Model.md` | Architecture, Tests, ADR-004 |
| Business invariants | Domain Model | `20_Domain_Model.md` | Architecture, Engineering Handbook, Tests |
| Allergy safety rules | Product + Domain Model | `10_Product_Vision.md` Section 56 (product), `20_Domain_Model.md` (data model + invariants) | Vision, Architecture, Tests |
| Offline AI staleness model | Architecture | `40_Technical_Architecture.md`, Section 37.8 | Offline UX (`10_Product_Vision.md` Section 22) |
| recommendation_expires_at | Architecture | `40_Technical_Architecture.md`, Section 37.8 | Architecture, Mobile, Tests |
| MVP-0 scope | Product | `10_Product_Vision.md`, Sections 38–39 | Vision, PRDs, Architecture |

---

## Glossary

Canonical definitions for all KitchenOS domain terms. Use these exact terms in code, tickets, tests, and documentation. Do not invent synonyms.

| Term | Definition |
|---|---|
| Household | The primary unit of KitchenOS. A group of people (1 or more) sharing a food environment. All decisions are made at household level. |
| Household Member | An individual within a Household. Has their own profile, allergies, and goals. |
| Household State | The materialised view of all household data derived from the event log: current pantry, shopping list, meal plan, budget status, and recent timeline. |
| Household Timeline | The user-facing event log of the household. Tracks what was bought, cooked, consumed, corrected, recommended, accepted, or rejected. First-class product surface. |
| Household Decision Engine | The backend coordination layer that turns household context (pantry, goals, allergies, history) into safe, trusted food decisions. Not a single AI model — an orchestration layer. |
| Domain Event | An immutable, append-only record of something that happened in the household. Written to the `domain_events` table. Never deleted, only reversed. |
| Correction Event | A domain event that reverses or amends a prior event. Not a delete. The original event remains in the log. |
| Cook Mode | The guided cooking experience in the app. Step-by-step instructions with automatic pantry deduction on completion. |
| Pantry | The household's current food inventory. A materialised view derived from receipts scanned, meals cooked, manual adjustments, and corrections. |
| Pantry Snapshot | A point-in-time record of pantry state. Used for rollback and AI context. |
| Receipt | A scanned or manually entered purchase record. Source of pantry additions and budget tracking. |
| Shopping List | A household-level list of items to buy. Derived from pantry state, meal plans, and AI recommendations. |
| Recommendation | An AI-generated suggestion for a meal, recipe, or shopping action, grounded in household context and safety constraints. |
| recommendation_expires_at | A server-set timestamp on each cached recommendation indicating when it should be suppressed offline, based on household activity level. |
| Allergy Guard | The safety layer that checks all recommendations and expert suggestions against household-level allergy rules before any suggestion reaches the user. |
| Goal | An individual household member's nutrition or fitness objective (e.g., muscle gain, weight reduction). Goals influence recommendation ranking but never override safety constraints. |
| Expert | A verified nutritionist or fitness coach on the KitchenOS marketplace. Works within the platform's safety and privacy boundaries. |
| Pending Sync Event | A domain event queued in local SQLite on a device because it has not yet synced to the backend. Does not affect backend state until synced. |
| Ubiquitous Language | The shared vocabulary used consistently by product, engineering, QA, and support. Defined in this glossary. Deviating from it causes specification bugs. |

---

## New Engineer Onboarding Path

Follow this sequence when joining the KitchenOS team:

```text
1. Start here: Knowledge Map (this document)
        │
        ▼
2. Read: Product Development Lifecycle  →  Process/Product_Development_Lifecycle.md
   Understand how ideas become shipped features before touching any code.
        │
        ▼
3. Read: Product Vision  →  Knowledge/10_Product_Vision.md (Sections 1–15)
   Understand what we build and why.
        │
        ▼
4. Read: Domain Model  →  Knowledge/20_Domain_Model.md
   Learn the ubiquitous language, bounded contexts, entities, and invariants.
        │
        ▼
5. Read: Technical Architecture  →  Knowledge/40_Technical_Architecture.md (Sections 24–32)
   Understand the AI architecture and event sourcing model.
        │
        ▼
6. Read: Technical Architecture  →  Knowledge/40_Technical_Architecture.md (Sections 33–37)
   Understand services, offline strategy, and technology stack.
        │
        ▼
7. Read: Engineering Handbook  →  Knowledge/50_Engineering_Handbook.md
   Understand how we write, test, and ship code.
        │
        ▼
8. Read: Decision Records  →  Knowledge/60_Decision_Records/
   Understand why the major technology and product decisions were made.
        │
        ▼
9. Read: Current feature PRD  →  Knowledge/30_PRDs/ (when they exist)
        │
        ▼
9. Code
```

---

## Architecture Building Blocks

These are the reusable architectural components that appear across multiple features. Each is a well-defined module within the modular monolith in MVP-0 and a natural extraction candidate as the product scales.

| Building Block | One-Line Responsibility | Detail |
|---|---|---|
| Household Decision Engine | Turns household context into safe, trusted food decisions | Main doc, Section 37.10 |
| Allergy Guard | Safety check on all recommendations. Never bypassed. | Main doc, Section 37.10 |
| Sync Engine | Pending event queue, conflict resolution, online/offline transitions | Main doc, Section 37.10 |
| Household Timeline | Event log read model for the user-facing activity history | Main doc, Section 37.10 |
| AI Provider Abstraction | Interface over AI providers. Never call a provider directly. | Main doc, Section 37.10 |
| Receipt OCR Pipeline | Cloud Vision → Cloud Tasks → pantry update → event write | Main doc, Section 37.10 |
| Notification Engine | FCM delivery of alerts, nudges, and sync events | Main doc, Section 37.10 |
| Domain Event Bus | Append-only domain_events table and write/dispatch logic | Main doc, Section 37.10 |

---

## Architecture Governance

Rules about when to create an ADR, who approves architecture changes, and what triggers a review. Governance must be lightweight and practical, not a bureaucratic bottleneck.

### When an ADR is Required

Write an ADR when any of the following is true:

- A new external dependency or service is introduced (a new cloud service, AI provider, third-party SDK).
- A technology is replaced (switching from one database, queue, or provider to another).
- A module boundary changes (a module is split, merged, or a new bounded context is introduced).
- A cross-cutting architectural pattern is established (a new pattern for error handling, auth, caching, or event processing that will be used across modules).
- A decision that was previously informal becomes a standard (e.g., agreeing on a retry policy, connection pooling strategy, or API versioning scheme).

### When an ADR is NOT Required

- Implementation details within a module (how a function is structured, variable names, algorithm choice for an internal problem).
- Library versions or minor tooling upgrades (unless they introduce a new architectural dependency).
- UI component choices within the established design system.

### Approval

- ADRs must be reviewed by at least one other engineer before being marked Accepted.
- Changes that affect two or more modules require a second reviewer.
- The founding team reviews ADRs that introduce new cloud services or external cost implications.

### ADR Lifecycle

```text
Proposed  -> under discussion, not yet in effect
Accepted  -> decision made, in effect
Superseded -> a later ADR replaces this one (link to successor)
Deprecated -> no longer relevant (document why)
```

An ADR is never deleted. Superseded ADRs are kept for historical context.

### What Triggers a Review of Existing Architecture

The following events require reviewing affected ADRs and updating the Source of Truth table:

- A module boundary changes.
- A new building block is introduced.
- A building block is extracted into a separate deployable service.
- A managed service is replaced.
- A principle is violated in practice and a deliberate exception is agreed.

---

## Future Evolution: Toward a Knowledge Index

### The Core Principle

> **Humans want stories, explanations, and hierarchy. AI agents want structured relationships and precise retrieval.**

The answer is not to force humans to think like machines or machines to read long narratives. The answer is **two interfaces over one shared body of knowledge**:

```text
                 Git Repository
                       │
                       ▼
        Human-Authored Documents
   (Vision, PRDs, Domain Model,
    Architecture, Handbook, ADRs)
                       │
                       ▼
          Knowledge Index Builder
                       │
         ┌─────────────┴─────────────┐
         ▼                           ▼
  Documentation Portal         Knowledge Index
  (file hierarchy, portal)    (machine-readable)
         │                           │
         ▼                           ▼
      Humans                     AI Agents
```

Humans never think about the index. AI agents rarely read the full documents. Each gets the interface best suited to them.

### What Each Layer Is

**Git + Human-Authored Documents — the source of truth.**
Everything in `60_ADRs/`, `00_Knowledge_Map.md`, the main product document, and future PRDs is written and maintained by humans. This is what gets committed, reviewed, and versioned. The documents are never generated — they are written.

**Knowledge Index — derived infrastructure, not source of truth.**
The index is built from YAML frontmatter in the documents. It is exactly like a search engine index or a database read model: if it gets corrupted, delete it and rebuild. It adds zero cognitive load to the team because humans never interact with it directly. Think of it the way you think of Google's index — it doesn't replace web pages, it makes them instantly discoverable.

**Documentation Portal — navigation for humans.**
This is the current file hierarchy: `00_Knowledge_Map.md` for navigation, numbered directories for organization, the Knowledge Map as the table of contents. A new engineer can immediately understand it. This structure does not change.

### The Three-Layer Separation

```text
Code             implements the system
Documents        explain the system
Knowledge Index  makes the system navigable for AI
```

Documents are the authoritative explanation. The index is an acceleration layer — it answers "where is X defined?" instantly without scanning 400 pages.

### What the Index Enables

**For a human today:** Ctrl+F through the main document.

**For an AI agent with the index:**
```text
Query: "Where is Household Timeline defined and what depends on it?"

Index reply:
  Defined in:    Main doc, Section 29
  Referenced by: Shopping PRD, Domain Model, Architecture, Mobile UI
  Implemented by: Household screen, Home screen
  Tested by:     Timeline integration tests
```

The AI reads only those sections. Not 400 pages.

### Current Tooling: knowledge_index.py

A lightweight Python script at the root of this repository implements the Knowledge Index Builder today. It parses YAML frontmatter from all knowledge documents and provides impact analysis with no database or external dependencies:

```text
python knowledge_index.py                    List all indexed documents
python knowledge_index.py --impact ADR-004   What needs review if ADR-004 changes?
python knowledge_index.py --deps ADR-005     What does ADR-005 depend on?
python knowledge_index.py --graph            Full dependency graph
python knowledge_index.py --tag ddd          Documents by tag
python knowledge_index.py --check            Validate all cross-references exist
```

The YAML frontmatter files are the data store. The script is stateless — run it any time, it always reflects the current state of the documents.

### What Moves This Forward

- Apply YAML frontmatter to every new document from day one (done on all ADRs — apply to future PRDs).
- When writing the Domain Model, structure entities with explicit `relationships`, `implemented_by`, and `tested_by` fields — these become the richest nodes in the index.
- When writing PRDs, add `depends_on`, `implemented_by`, `tested_by` — the script indexes them immediately.
- Single source of truth discipline must be maintained strictly — duplication defeats the index model.

### What to Avoid

- Never expose the index structure to humans. They should see documents, not nodes and edges.
- Do not build a Knowledge Service API or load into Neo4j before the product is validated.
- Do not generate documents from YAML. Narrative documents must be written — generated narrative is always worse than written narrative for human readers.

The Knowledge Service API (queryable by AI agents over HTTP) is a post-product-validation infrastructure project.

---

## Documentation Philosophy

> Every important decision should be discoverable, traceable, and have a single source of truth.

Rules:

1. Every concept has one authoritative home. Link to it. Do not copy it.
2. Documents link upward to strategy and downward to implementation.
3. Requirements are traceable to architecture and tests.
4. ADRs explain *why*, not *how*. Implementation details belong in architecture.
5. Documentation evolves with the product and is treated as part of the codebase.
6. The glossary is the canonical language. Use it in code, commits, tickets, and conversations.
