# Knowledge Map

> **Every piece of information has exactly one authoritative home. Other documents may reference it but must not duplicate it.**

This principle governs the entire documentation system. When in doubt about where something belongs, consult the Documentation Manifest below. When in doubt about whether to copy content, don't — link instead.

---

This is the top-level navigation document for all company and product knowledge. Start here when joining the team, making a decision, or finding where something belongs.

> **This repository has evolved from KitchenOS product documentation into a company operating model.**
> The five-layer hierarchy below — Company, Products, Architecture, Engineering, Operations — is designed to scale from a solo founder to a multi-product company. Documents marked `Company-wide` apply to all current and future products. Documents marked `KitchenOS` are product-specific.

---

## Repository Structure

```text
Product Design/
├── 00_Knowledge_Map.md          ← start here (navigation anchor)
├── Company/                     ← why the company exists; governs all products
│   ├── Vision_and_Mission.md   ← company vision, mission, philosophy
│   ├── Operating_Principles.md  ← seven guiding principles; company constitution
│   └── Governance/              ← GDRs, AI Governance, Risk Register
│       ├── AI_Governance.md
│       ├── Architecture_Governance.md
│       ├── Risk_Register.md
│       └── GDRs/                ← GDR-001, GDR-002, ...
├── Products/                    ← one subfolder per product
│   └── KitchenOS/
│       ├── 10_Product_Vision.md
│       ├── 20_Domain_Model.md
│       ├── 30_PRDs/
│       ├── 40_Technical_Architecture.md
│       ├── 45_Solution_Designs/
│       ├── 50_Engineering_Handbook.md
│       ├── 60_Decision_Records/
│       │   ├── ADRs/                ← ADR-001 – ADR-011
│       │   ├── PDRs/                ← PDR-001 – PDR-009
│       │   └── UXDRs/               ← (none yet)
│       ├── 70_UX_Design_System/
│       ├── 80_API_Reference/
│       ├── 90_Platform_Operations/
│       ├── 95_Customer_Expert_Operations/
│       └── 100_Security/
├── Knowledge/                   ← shared concepts reusable across all products
│   ├── Glossary.md              ← company-wide vocabulary
│   ├── Canonical_Data_Model.md  ← shared entities: Identity, Person, ConsentGrant
│   └── Patterns/
│       ├── DDD.md
│       ├── Event_Sourcing.md
│       └── Privacy_By_Design.md
├── Agents/                      ← AI agent operating manuals
│   ├── Architect.md
│   ├── Product_Manager.md
│   └── Engineering_Manager.md
├── Research/                    ← founder research: competitors, technology, regulations, ideas
│   ├── README.md
│   ├── Competitors/
│   ├── Technology/
│   ├── Nutrition/
│   ├── Regulations/
│   └── Ideas/
├── Process/                     ← how ideas become shipped features (all products)
└── Templates/                   ← reusable formats and checklists
```

> **Future additions — do not create until there is a real need:**
> - `Platform/` — shared services (Identity, AI Platform, Billing, Notifications) extracted when a second product is built
> - `Company/Vision.md`, `Company/Mission.md`, `Company/Brand.md` — add when content exists
> - KitchenOS sub-folders (`Vision/`, `Architecture/`, `Engineering/`) — add when the product folder gets crowded
> - `Process/` expansion — `Architecture_Process.md`, `PRD_Process.md`, `Release_Process.md`, etc. — add as processes are defined

---

## Document Registry

### Layer 1 — Company *(company-wide; applies to all products)*

| Document | File | Audience | Purpose | Status |
|---|---|---|---| ---|
| Knowledge Map (this file) | `00_Knowledge_Map.md` | Everyone | Navigate all documentation | Active |
| Vision and Mission | `Company/Vision_and_Mission.md` | Everyone | Company vision, mission, philosophy — the foundation everything else serves | Active |
| Operating Principles | `Company/Operating_Principles.md` | Everyone | Seven guiding principles — the operational expression of the philosophy | Active |
| Governance | `Company/Governance/` | Founders, Legal, All Leads | GDRs, AI Governance, Risk Register | Active |

### Shared Knowledge *(company-wide)*

| Document | File | Audience | Purpose | Status |
|---|---|---|---|---|
| Shared Glossary | `Knowledge/Glossary.md` | Everyone | Company-wide vocabulary and pattern definitions | Active |
| Canonical Data Model | `Knowledge/Canonical_Data_Model.md` | Architecture, Engineering | Shared entities across all products: Identity, Person, ConsentGrant | Active |
| DDD Pattern | `Knowledge/Patterns/DDD.md` | Architecture, Engineering | Domain-Driven Design concepts as applied at Amanaska | Active |
| Event Sourcing Pattern | `Knowledge/Patterns/Event_Sourcing.md` | Architecture, Engineering | Event sourcing pattern reference | Active |
| Privacy by Design Pattern | `Knowledge/Patterns/Privacy_By_Design.md` | Architecture, Engineering, Legal | Privacy by Design as a structural pattern | Active |

### Agents *(AI agent operating manuals)*

| Agent | File | Role | Scope |
|---|---|---|---|
| Architect | `Agents/Architect.md` | Technical architecture, ADRs, Solution Design review | All products |
| Product Manager | `Agents/Product_Manager.md` | PRDs, PDRs, Product Vision, feature scoping | KitchenOS (primary) |
| Engineering Manager | `Agents/Engineering_Manager.md` | Engineering Handbook, quality gates, implementation fidelity | KitchenOS |

### Research *(founder research notes)*

| Folder | Contents |
|---|---|
| `Research/Competitors/` | Competitor analysis, market maps, positioning |
| `Research/Technology/` | AI models, LLMs, framework evaluations |
| `Research/Nutrition/` | Nutritional science, dietary guidelines, food safety |
| `Research/Regulations/` | GDPR, CCPA, AI regulation, food/health law by jurisdiction |
| `Research/Ideas/` | Founder notebook — early hypotheses, unstructured thinking |

### Layer 2 — Products *(KitchenOS-scoped)*

| # | Document | File | Audience | Purpose | Status |
|---|---|---|---|---|---|
| 10 | Product Vision | `Products/KitchenOS/10_Product_Vision.md` | Founders, PMs, Designers, Investors | What KitchenOS is and why it exists | Active |
| 20 | Domain Model | `Products/KitchenOS/20_Domain_Model.md` | Product, Engineering, QA | What business concepts exist, how they relate, and the ubiquitous language | Active |
| 30 | PRDs | `Products/KitchenOS/30_PRDs/` | Product, Engineering, QA | Per-feature requirements, acceptance criteria, BDD | Planned |
| 70 | UX Design System | `Products/KitchenOS/70_UX_Design_System/` | Designers, Frontend Engineers | Component library, design tokens, interaction patterns | Planned (post-MVP) |

### Layer 3 — Architecture *(KitchenOS-scoped)*

| # | Document | File | Audience | Purpose | Status |
|---|---|---|---|---|---|
| 40 | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md` | Architects, Senior Engineers | System-level architecture — HLD, services, patterns, principles | Active |
| 45 | Solution Designs | `Products/KitchenOS/45_Solution_Designs/` | Engineers, Architects | Feature-level technical design — module responsibilities, sequence diagrams, data flows (LLD) | Planned |
| 60 | Decision Records | `Products/KitchenOS/60_Decision_Records/` | Everyone | ADRs, PDRs, UXDRs (GDRs live in `Company/Governance/GDRs/`) | Active (11 ADRs, 9 PDRs) |
| 80 | API Reference | `Products/KitchenOS/80_API_Reference/` | Engineers, QA | How systems communicate | Planned |
| 100 | Security | `Products/KitchenOS/100_Security/` | Engineering, Legal, Compliance | Auth, encryption, privacy, threat model, incident response | Planned |

> **Future layer — Company Architecture:** When a second product is built, shared services (Identity, Billing, Notifications, AI Platform, Consent) will be extracted into a `Company/Architecture/` layer (Enterprise Architecture in TOGAF terms). Do not create this layer until the second product exists.

### Layer 4 — Engineering *(KitchenOS-scoped)*

| # | Document | File | Audience | Purpose | Status |
|---|---|---|---|---|---|
| 50 | Engineering Handbook | `Products/KitchenOS/50_Engineering_Handbook.md` | All Engineers | How we write, test, and ship code | Active |

### Layer 5 — Operations *(KitchenOS-scoped)*

| # | Document | File | Audience | Purpose | Status |
|---|---|---|---|---|---|
| 90 | Platform Operations | `Products/KitchenOS/90_Platform_Operations/` | Engineering, DevOps | How the platform runs — infrastructure, monitoring, incident response, releases, disaster recovery | Planned |
| 95 | Customer & Expert Operations | `Products/KitchenOS/95_Customer_Expert_Operations/` | Ops, Support, Marketplace | Customer support, Expert onboarding and verification, consent audits, marketplace quality, SLAs | Planned |

> **Future split — Operations:** As the company grows, Operations will split into **Customer Operations** (customer support, expert operations, trust & safety, disputes — scales with customers) and **Internal Operations** (finance, HR, procurement, compliance evidence — scales with company size). These are distinct concerns with different audiences and growth drivers. Do not create this split until the distinction becomes operational.

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
| Solution Design Template (LLD) | `Templates/LLD_Template.md` | Stage 5 — Technical Design |
| Architecture Review Checklist | `Templates/Architecture_Review_Checklist.md` | Stage 5 — Architecture Review |
| Definition of Done | `Templates/Definition_of_Done.md` | Stage 6 — Planning |

---

## Document Dependency Chain

Documents depend on the layers above them. When a concept changes, all documents downstream must be reviewed.

```text
                     Research/
                        │
                        ▼ informs
Layer 1 — Company
  Operating Principles  ←  enduring identity; never superseded
  Governance (GDRs)     ←  company-wide policies governing all layers below
  Knowledge/            ←  shared concepts, patterns, canonical data model
        │
        ▼ governs and informs everything below
Layer 2 — Products
  Product Vision (10)
        │
        ▼
  Domain Model (20)
        │
        ├────────────────────┐
        ▼                    ▼
  PRDs (30)        Layer 3 — Architecture
        │            Technical Architecture (40)
        ▼                    │
  UX Design System (70)   Solution Designs (45)
        │                    │
        └──────┬─────────────┘
               ▼
        Layer 4 — Engineering
          Engineering Handbook (50)
          API Reference (80)
          Security (100)
               │
               ▼
          Code + Tests
               │
               ▼
        Layer 5 — Operations
          Platform Operations (90)
          Customer & Expert Operations (95)
```

### How Ideas Become Software

This is the abstraction gradient from insight to running code. Every step has a document that owns it.

```text
Research/               ← raw insight, competitive intelligence, technology exploration
        │
        ▼ informs
Company/                ← Operating Principles and GDRs set the boundaries
        │
        ▼ constrains
Product Vision (10)     ← what we build and why; North Star Metric
        │
        ▼ scopes
PRDs (30)               ← what this feature does; acceptance criteria
        │
        ▼ specifies
Domain Model (20)       ← what business concepts are involved; ubiquitous language
        │
        ▼ models
Technical Architecture  ← how the system is structured at HLD level
(40)    │
        ▼ designs
Solution Designs (45)   ← how this feature is built at LLD level
        │
        ▼ implements
Code + Tests            ← the running system
        │
        ▼ operates
Operations (90, 95)     ← how we keep it running and support users
        │
        ▼ learns
Research/ (loop)        ← user feedback, data, and learning feed back into research
```

**Decision Records are cross-cutting** — they document *why* at every level of this gradient:

```text
GDRs   ← why a company-wide governance policy was made (Company level)
PDRs   ← why a product scope or strategy decision was made (Vision/PRD level)
ADRs   ← why an architecture or technology choice was made (Architecture level)
UXDRs  ← why a UX pattern or interaction design was chosen (UX level)
```

A Decision Record documents *why* — it does not replace the living document where the decision is expressed.

**Agents are the team that executes this gradient.** Each Agent document in `Agents/` defines which steps of this gradient an AI agent is responsible for and what quality gates it enforces.

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
│  Company  (why we exist; what we never violate) │
│                                                 │
│  Operating Principles constrain all stages.     │
│  GDRs constrain all AI, privacy, governance.    │
└─────────────────────────────────────────────────┘
         │ constrains ↓
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
| Product vision and mission | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 1–5 |
| North Star Metric | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 10 |
| User personas and JTBD | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Sections 12–13 |
| Screen responsibilities and UX rules | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Sections 19–20 |
| Offline UX behaviour | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 22 |
| MVP-0 scope and user flows | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Sections 38–40 |
| Post-MVP roadmap | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 47 |
| Allergy and dietary safety | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 56 |
| Nutrition goals | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 57 |
| Expert marketplace | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 58 |
| Negative flows and corrections | Product Vision | `Products/KitchenOS/10_Product_Vision.md`, Section 59 |
| Company vision, mission, philosophy | Vision and Mission | `Company/Vision_and_Mission.md` |
| Company operating principles | Operating Principles | `Company/Operating_Principles.md` |
| AI governance and decision criticality | Governance | `Company/Governance/AI_Governance.md` |
| Architecture governance (ADR rules, approval, lifecycle) | Governance | `Company/Governance/Architecture_Governance.md` |
| Risk register | Governance | `Company/Governance/Risk_Register.md` |
| Trusted decision support policy | GDR | `Company/Governance/GDRs/GDR-001_Trusted_Decision_Support.md` |
| Privacy by design policy | GDR | `Company/Governance/GDRs/GDR-002_Privacy_By_Design.md` |
| Ubiquitous language | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| Bounded contexts | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| Aggregate roots and entities | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| Data model (all tables) | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| Domain events catalogue | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| Standard event envelope | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| Business invariants | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| Household Decision Engine (architecture) | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 24 |
| Household Timeline (architecture) | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 32.8 |
| Domain event architecture | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 32 |
| Offline AI context constraint | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.8 |
| Cloud infrastructure | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.6 |
| Architecture principles | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.9 |
| Architecture building blocks | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| Feature-level technical design (LLD) | Solution Designs | `Products/KitchenOS/45_Solution_Designs/SD-XXX_Feature.md` |
| MVP-0 tech stack | Engineering Handbook | `Products/KitchenOS/50_Engineering_Handbook.md`, Section 42 |
| Engineering quality and testing | Engineering Handbook | `Products/KitchenOS/50_Engineering_Handbook.md`, Section 42.5 |
| BDD scenario format | Engineering Handbook | `Products/KitchenOS/50_Engineering_Handbook.md`, Section 42.5 |
| Engineering principles | Engineering Handbook | `Products/KitchenOS/50_Engineering_Handbook.md`, Section 42.5 |
| Feature development lifecycle | Process | `Process/Product_Development_Lifecycle.md` |
| Stage gates and governance | Process | `Process/Product_Development_Lifecycle.md` |
| Architecture governance | Knowledge Map | `00_Knowledge_Map.md` |
| Why Flutter? | ADR | `Products/KitchenOS/60_Decision_Records/ADRs/ADR-001_Flutter.md` |
| Why GCP? | ADR | `Products/KitchenOS/60_Decision_Records/ADRs/ADR-002_GCP.md` |
| Why PostgreSQL? | ADR | `Products/KitchenOS/60_Decision_Records/ADRs/ADR-003_PostgreSQL.md` |
| Why event sourcing? | ADR | `Products/KitchenOS/60_Decision_Records/ADRs/ADR-004_Event_Sourcing.md` |
| Why modular monolith? | ADR | `Products/KitchenOS/60_Decision_Records/ADRs/ADR-005_Modular_Monolith.md` |
| Why Cloud Run? | ADR | `Products/KitchenOS/60_Decision_Records/ADRs/ADR-006_Cloud_Run.md` |
| Why food before fitness? | PDR | `Products/KitchenOS/60_Decision_Records/PDRs/PDR-001_Food_Before_Fitness.md` |
| Why household not individual? | PDR | `Products/KitchenOS/60_Decision_Records/PDRs/PDR-002_Household_Not_Individual.md` |
| Why Home screen is a question? | PDR | `Products/KitchenOS/60_Decision_Records/PDRs/PDR-003_Home_Screen_Question.md` |

---

## Documentation Manifest

When creating new documentation, use this table to find the right home. **Never create a new document type without updating this manifest.**

| I need to document... | It belongs in... | File / Directory |
|---|---|---|
| An enduring company identity statement or principle | Operating Principles | `Company/Operating_Principles.md` |
| A company-wide governance policy (AI, privacy, ethics, data retention) | Governance (GDR) | `Company/Governance/GDRs/GDR-XXX_Decision.md` |
| A new feature's requirements and acceptance criteria | PRD | `Products/KitchenOS/30_PRDs/PRD-XXX_Feature_Name.md` |
| A new domain concept or entity | Domain Model | `Products/KitchenOS/20_Domain_Model.md` |
| A new API endpoint | API Reference | `Products/KitchenOS/80_API_Reference/` |
| A new UI component or design pattern | UX Design System | `Products/KitchenOS/70_UX_Design_System/` |
| A coding standard or engineering practice | Engineering Handbook | `Products/KitchenOS/50_Engineering_Handbook.md` |
| An authentication or encryption standard | Security | `Products/KitchenOS/100_Security/` |
| AI decision criticality, autonomous action thresholds, model governance | Governance | `Company/Governance/AI_Governance.md` |
| Architecture governance: when to write an ADR, approval rules, ADR lifecycle | Governance | `Company/Governance/Architecture_Governance.md` |
| Product risk register, likelihood/impact/mitigation | Governance | `Company/Governance/Risk_Register.md` |
| A production runbook or infrastructure config | Platform Operations | `Products/KitchenOS/90_Platform_Operations/` |
| Customer support workflows, SLAs, Expert onboarding and verification | Customer & Expert Operations | `Products/KitchenOS/95_Customer_Expert_Operations/` |
| Why a company-wide governance policy was decided | GDR | `Company/Governance/GDRs/GDR-XXX_Decision.md` |
| Why a technology was chosen | ADR | `Products/KitchenOS/60_Decision_Records/ADRs/ADR-XXX_Decision.md` |
| Why a product scope or strategy decision was made | PDR | `Products/KitchenOS/60_Decision_Records/PDRs/PDR-XXX_Decision.md` |
| Why a UX pattern or navigation choice was made | UXDR | `Products/KitchenOS/60_Decision_Records/UXDR-XXX_Decision.md` |
| A new ubiquitous language term | Domain Model glossary | `Products/KitchenOS/20_Domain_Model.md` |
| A company-wide non-negotiable principle (applies to all products) | Operating Principles | `Company/Operating_Principles.md` |
| A company-wide governance policy (AI, privacy, cross-cutting) | GDR | `Company/Governance/GDRs/` |
| A cross-cutting architectural principle | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.9 |
| A reusable architectural building block | Technical Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| How a specific feature is designed at module/class level | Solution Design | `Products/KitchenOS/45_Solution_Designs/SD-XXX_Feature.md` |
| A process, stage gate, or lifecycle rule | Process | `Process/Product_Development_Lifecycle.md` |
| A reusable checklist or document format | Templates | `Templates/` |

---

## Decision Records Index

Decision Records capture *why* a decision was made, not how it was implemented. Four types:

- **GDR** — Governance Decision Records. Company-wide policies that govern all products and all layers. Live in `Company/Governance/GDRs/`. Cannot be overridden by PDRs or ADRs.
- **ADR** — Architecture Decision Records. Technology, infrastructure, and system design choices. KitchenOS-scoped. Live in `Products/KitchenOS/60_Decision_Records/`.
- **PDR** — Product Decision Records. Product positioning, scope, and strategic choices. KitchenOS-scoped. Live in `Products/KitchenOS/60_Decision_Records/`.
- **UXDR** — UX Decision Records. Design philosophy, navigation, and interaction pattern choices. KitchenOS-scoped. Live in `Products/KitchenOS/60_Decision_Records/`.

> **Future record type — EDR (Engineering Decision Records):** Once the engineering organisation grows, EDRs will capture engineering process decisions (state management library, commit conventions, CI/CD tooling choices) that are distinct from architectural decisions. Not needed now.

> **GDRs are company-wide.** They are not superseded by PDRs or ADRs. A PDR may implement a GDR but cannot override it. Example: GDR-001 says "AI never diagnoses." A PDR may specify *how* KitchenOS surfaces recommendations, but may not contradict the GDR.

### Governance Decision Records

| ID | Decision | Status | Date |
|---|---|---|---|
| GDR-001 | Trusted Decision Support, Not Autonomous Diagnosis | Accepted | 2026 |
| GDR-002 | Privacy by Design | Accepted | 2026 |

### Architecture Decision Records

| ID | Decision | Status | Date |
|---|---|---|---|
| ADR-001 | Flutter for mobile | Accepted | 2026 |
| ADR-002 | Google Cloud Platform | Accepted | 2026 |
| ADR-003 | PostgreSQL as primary database | Accepted | 2026 |
| ADR-004 | Domain-driven event sourcing | Accepted | 2026 |
| ADR-005 | Modular monolith for backend | Accepted | 2026 |
| ADR-006 | Cloud Run for compute | Accepted | 2026 |
| ADR-007 | Household Intelligence Model as a separate architectural layer | Accepted | 2026 |
| ADR-008 | Collective Intelligence Model with explicit opt-in consent | Accepted | 2026 |
| ADR-009 | Privacy-by-design and identity isolation | Accepted | 2026 |
| ADR-010 | Pantry state derived only from confirmed activities | Accepted | 2026 |
| ADR-011 | Person as a global domain concept, separate from HouseholdMembership | Accepted | 2026 |

> ADR-007 through ADR-011 are not yet listed in earlier summary counts — the count above reflects all 11 accepted ADRs.

### Product Decision Records

| ID | Decision | Status | Date |
|---|---|---|---|
| PDR-001 | Food decisions before fitness features | Accepted | 2026 |
| PDR-002 | Household as primary unit, not individual | Accepted | 2026 |
| PDR-003 | Home screen answers a question, not a dashboard | Accepted | 2026 |
| PDR-004 | Personas as Household Intelligence Profiles, not UX personas | Accepted | 2026 |
| PDR-005 | Ask only what the AI cannot reasonably learn on its own | Accepted | 2026 |
| PDR-006 | Collective Intelligence participation is explicit opt-in, never default | Accepted | 2026 |
| PDR-007 | Three-object meal lifecycle — MealRecommendation, MealPlan, MealSession | Accepted | 2026 |
| PDR-008 | WeeklyMealPlan as planning horizon — AI predicts routine, asks only about exceptions | Accepted | 2026 |
| PDR-009 | Household Conflict Resolution Policy — six-level priority hierarchy | Accepted | 2026 |

### UX Decision Records

| ID | Decision | Status | Date |
|---|---|---|---|
| *(none yet)* | | | |

---

## Concept Ownership

Every major concept has one owning team and a single source of truth. When the concept changes, the owner is responsible for updating all downstream references.

| Concept | Owner | Source of Truth | Referenced By |
|---|---|---|---|
| Household | Domain Model | `Products/KitchenOS/20_Domain_Model.md` | All documents |
| Household Timeline | Product + Architecture | `Products/KitchenOS/10_Product_Vision.md` Section 59.6 (product), `Products/KitchenOS/40_Technical_Architecture.md` Section 32.8 (architecture), `Products/KitchenOS/20_Domain_Model.md` (data model) | Vision, Architecture, Engineering Handbook, Mobile UI |
| Household Decision Engine | Product + Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 24 | Vision, Domain Model, Architecture, AI Layer |
| Domain event architecture | Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 32 | Domain Model, Engineering Handbook, Tests |
| Domain events catalogue | Domain Model | `Products/KitchenOS/20_Domain_Model.md` | Architecture, Tests, ADR-004 |
| Business invariants | Domain Model | `Products/KitchenOS/20_Domain_Model.md` | Architecture, Engineering Handbook, Tests |
| Allergy safety rules | Product + Domain Model | `Products/KitchenOS/10_Product_Vision.md` Section 56 (product), `Products/KitchenOS/20_Domain_Model.md` (data model + invariants) | Vision, Architecture, Tests |
| Offline AI staleness model | Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.8 | Offline UX (`Products/KitchenOS/10_Product_Vision.md` Section 22) |
| recommendation_expires_at | Architecture | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.8 | Architecture, Mobile, Tests |
| MVP-0 scope | Product | `Products/KitchenOS/10_Product_Vision.md`, Sections 38–39 | Vision, PRDs, Architecture |
| Company vision, mission, philosophy | Company | `Company/Vision_and_Mission.md` | All layers |
| Company operating principles | Company | `Company/Operating_Principles.md` | All layers |
| AI governance policy | Governance | `Company/Governance/AI_Governance.md` | Products, Architecture, Engineering |
| Architecture governance policy | Governance | `Company/Governance/Architecture_Governance.md` | Architecture, Engineering, Agents |
| Risk register | Governance | `Company/Governance/Risk_Register.md` | All layers |
| Household conflict resolution policy | PDR | `Products/KitchenOS/60_Decision_Records/PDRs/PDR-009_Household_Conflict_Resolution.md` | Domain Model, AI Architecture |

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
3. Read: Operating Principles  →  Company/Operating_Principles.md
   Understand the company's identity and non-negotiable principles.
        │
        ▼
4. Read: Product Vision  →  Products/KitchenOS/10_Product_Vision.md (Sections 1–15)
   Understand what KitchenOS is and why it exists.
        │
        ▼
5. Read: Domain Model  →  Products/KitchenOS/20_Domain_Model.md
   Learn the ubiquitous language, bounded contexts, entities, and invariants.
        │
        ▼
6. Read: Technical Architecture  →  Products/KitchenOS/40_Technical_Architecture.md (Sections 24–32)
   Understand the AI architecture and event sourcing model.
        │
        ▼
7. Read: Technical Architecture  →  Products/KitchenOS/40_Technical_Architecture.md (Sections 33–37)
   Understand services, offline strategy, and technology stack.
        │
        ▼
8. Read: Engineering Handbook  →  Products/KitchenOS/50_Engineering_Handbook.md
   Understand how we write, test, and ship code.
        │
        ▼
9. Read: Decision Records  →  Products/KitchenOS/60_Decision_Records/
   Understand why the major technology and product decisions were made.
        │
        ▼
10. Read: Current feature PRD  →  Products/KitchenOS/30_PRDs/ (when they exist)
        │
        ▼
11. Code
```

---

## Architecture Building Blocks

These are the reusable architectural components that appear across multiple features. Each is a well-defined module within the modular monolith in MVP-0 and a natural extraction candidate as the product scales.

| Building Block | One-Line Responsibility | Detail |
|---|---|---|
| Household Decision Engine | Turns household context into safe, trusted food decisions | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| Allergy Guard | Safety check on all recommendations. Never bypassed. | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| Sync Engine | Pending event queue, conflict resolution, online/offline transitions | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| Household Timeline | Event log read model for the user-facing activity history | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| AI Provider Abstraction | Interface over AI providers. Never call a provider directly. | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| Receipt OCR Pipeline | Cloud Vision → Cloud Tasks → pantry update → event write | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| Notification Engine | FCM delivery of alerts, nudges, and sync events | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |
| Domain Event Bus | Append-only domain_events table and write/dispatch logic | `Products/KitchenOS/40_Technical_Architecture.md`, Section 37.10 |

---

## Architecture Governance

Architecture governance rules — when to write an ADR, quality requirements, approval thresholds, ADR lifecycle states, and what triggers a review — are defined in one place:

> **`Company/Governance/Architecture_Governance.md`** is the single source of truth for all architecture governance.

This section exists only as a pointer. Do not duplicate rules here.

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
Everything in `Products/KitchenOS/60_Decision_Records/`, `00_Knowledge_Map.md`, `Company/`, the main product document, and future PRDs is written and maintained by humans. This is what gets committed, reviewed, and versioned. The documents are never generated — they are written.

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
