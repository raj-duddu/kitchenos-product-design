---
id: PROC-001
title: KitchenOS Product Development Lifecycle
type: process
status: active
owner: product
depends_on: []
referenced_by: []
tags: [process, lifecycle, stage-gates, delivery, development, ai-agents, governance]
date: 2026
---

# KitchenOS: Product Development Lifecycle

> This document defines how KitchenOS transforms an idea into a shipped product feature. It governs how all other knowledge documents get created, reviewed, and updated. Every team member — human or AI agent — follows this lifecycle.

---

## Two Dimensions of Documentation

KitchenOS documentation has two distinct dimensions that must not be confused:

| Dimension | Purpose | Documents |
|---|---|---|
| **Knowledge** | What we know — static, enduring facts about product and technology | `Knowledge/` — Vision, Domain Model, Architecture, etc. |
| **Process** | How work flows — dynamic, operational, from idea to production | `Process/` — this document |

Knowledge documents describe *what exists*. This document describes *what happens next*.

---

## The Three Sections

```text
Product Design/
├── Knowledge/      What KitchenOS is, how it works, why decisions were made
├── Process/        How ideas become shipped features
└── Templates/      Reusable formats and checklists
```

---

## Lifecycle Overview

```text
1. Idea
        │
        ▼
2. Discovery
        │
        ▼
3. Product Definition (PRD)
        │
        ▼
4. UX Design
        │
        ▼
5. Architecture Review
        │
        ▼
6. Planning
        │
        ▼
7. Development
        │
        ▼
8. Testing
        │
        ▼
9. Release
        │
        ▼
10. Operate
        │
        ▼
11. Learn
        │
        ▼
12. Iterate  ──────────────────► back to Stage 3 or Stage 1
```

**Current vs. Future:**
Stages 1–9 are active at MVP. Stages 10–12 become operational post-launch. All stages are documented now so the process is ready when needed.

---

## Stage 1 — Idea

**Question:** Is this worth exploring?

**Activities:**
- Articulate the problem in one sentence.
- Check alignment with Product Vision principles (`Knowledge/10_Product_Vision.md`, Sections 1–9).
- Check alignment with North Star Metric: does this increase Weekly Trusted Household Decisions Completed?
- Check the Open Questions register (`Knowledge/10_Product_Vision.md`, Section 60) — is this already logged?
- Quick competitor check.

**Gate criteria — cannot proceed to Stage 2 until:**
- [ ] Problem statement written in one sentence.
- [ ] Aligned with at least one Product Vision principle.
- [ ] Not a duplicate of an existing feature or open question.

**Outputs:**
- Epic (1 paragraph: problem, hypothesis, success signal).

**Responsible:** Product Owner / Product Agent.

---

## Stage 2 — Discovery

**Question:** Do we understand the problem well enough to define a solution?

**Activities:**
- User research or interview synthesis (for human users).
- Review existing household behaviour data if available.
- Review any related PRDs already in `Knowledge/30_PRDs/`.
- Document findings in discovery notes.
- Assess effort vs. value at a high level.

**Gate criteria — cannot proceed to Stage 3 until:**
- [ ] Discovery notes written.
- [ ] Problem validated (not just assumed).
- [ ] Effort-value assessment completed.

**Outputs:**
- Discovery Notes (informal, may live in the PRD as a "Background" section).

**Responsible:** Product Owner / Research Agent.

---

## Stage 3 — Product Definition

**Question:** What exactly are we building and how do we know it's done?

**Activities:**
- Write a PRD using `Templates/PRD_Template.md`.
- Define user stories with acceptance criteria.
- Write BDD scenarios (Given / When / Then).
- Identify any new domain entities or events — if found, flag for Domain Model review (Stage 5).
- Review against Product Vision principles.
- If this is a significant product scope or strategy decision, write a PDR using `Templates/PDR_Template.md`.

**Gate criteria — cannot proceed to Stage 4 until:**
- [ ] PRD written and reviewed.
- [ ] Acceptance criteria defined for all user stories.
- [ ] BDD scenarios written for all critical paths.
- [ ] PDR written if a significant product decision is being made.

**Outputs:**
- `Knowledge/30_PRDs/PRD-XXX_Feature_Name.md`
- `Knowledge/60_Decision_Records/PDR-XXX_Decision.md` (if applicable)

**Responsible:** Product Owner / Product Agent.

---

## Stage 4 — UX Design

**Question:** What will the user see and how will they interact with it?

**Activities:**
- Create wireframes and screen flows referenced in the PRD.
- Validate every screen against the "Every Screen Answers a Question" principle (`Knowledge/10_Product_Vision.md`, Section 8.3).
- Reference — do not modify — `Knowledge/70_UX_Design_System/` for existing components.
- Identify any new reusable components needed — document them in `Knowledge/70_UX_Design_System/` if they qualify.
- If a significant UX pattern decision is made, write a UXDR using `Templates/PDR_Template.md` (adapted for UX).

**Gate criteria — cannot proceed to Stage 5 until:**
- [ ] Wireframes or screen flows exist for all user stories in the PRD.
- [ ] Each screen's question is identified.
- [ ] Empty states, error states, and loading states designed.
- [ ] UX aligned with Product Vision principles (Sections 8–23).

**Outputs:**
- Wireframes / flows (attached to PRD or in Design System).
- `Knowledge/60_Decision_Records/UXDR-XXX_Decision.md` (if applicable).

**Responsible:** Designer / Design Agent.

---

## Stage 5 — Architecture Review and Technical Design

**Question:** Does this feature change how the system is built? How specifically will it be implemented?

Stage 5 has two parts that may overlap for simple features or run sequentially for complex ones.

### Part A — Architecture Review

**Activities:**
- Review the PRD and UX for new domain entities, events, or services.
- If new domain entities or events are needed: update `Knowledge/20_Domain_Model.md`.
- If new services, infrastructure, or technology choices are needed: update `Knowledge/40_Technical_Architecture.md`.
- Use `Templates/Architecture_Review_Checklist.md` to assess impact.
- If a significant technology or infrastructure decision is made, write an ADR using `Templates/ADR_Template.md`.
- Security review: does this feature touch auth, encryption, consent, or PII? Flag for Security review.

### Part B — Technical Design (LLD)

> **Terminology:** Technical Design is the activity. The document it produces is called a **Solution Design (SD)**. These terms are interchangeable in conversation; use "Solution Design" when referring to the document.

**Activities:**
- For **simple features**: add a brief Technical Design section to the PRD.
- For **complex features** (new services, non-trivial data flows, significant domain model changes): write a full Solution Design using `Templates/SD_Template.md`.
- Solution Design covers: module responsibilities, sequence diagrams, data model changes, API contract, offline behaviour, testing strategy.
- Tech Lead review of Solution Design required before proceeding.

**Gate criteria — cannot proceed to Stage 6 until:**
- [ ] Architecture Review Checklist completed.
- [ ] Domain Model updated if new entities or events are introduced.
- [ ] ADR written if a significant technology decision is being made.
- [ ] Security impact assessed (flag or clear).
- [ ] Technical Design written (brief in PRD, or full Solution Design for complex features).
- [ ] Tech Lead has approved the Technical Design.

**Outputs:**
- Updated `Knowledge/20_Domain_Model.md` (if changed).
- Updated `Knowledge/40_Technical_Architecture.md` (if changed).
- `Knowledge/60_Decision_Records/ADR-XXX_Decision.md` (if applicable).
- `Knowledge/45_Solution_Designs/SD-XXX_Feature.md` (for complex features).

**Responsible:** Architect / Tech Lead / Architect Agent.

---

## Stage 6 — Planning

**Question:** How do we break this into executable work?

**Activities:**
- Break the PRD into engineering tasks.
- Estimate effort.
- Identify dependencies between tasks.
- Assign tasks to engineers or AI agents.
- Confirm Definition of Done is agreed (`Templates/Definition_of_Done.md`).

**Gate criteria — cannot proceed to Stage 7 until:**
- [ ] Tasks created with estimates.
- [ ] Dependencies identified.
- [ ] Definition of Done confirmed for all tasks.

**Outputs:**
- Sprint tasks / engineering tickets.

**Responsible:** Engineering Lead / Scrum Agent.

---

## Stage 7 — Development

**Question:** Are we building it correctly?

**Activities:**
- Follow `Knowledge/50_Engineering_Handbook.md` for all engineering practices.
- TDD: write failing tests before implementation.
- BDD: validate acceptance criteria from PRD using BDD scenarios.
- Code review required before merge.
- Feature flag all new features (no dark launches without flags).

**Gate criteria — cannot merge until:**
- [ ] All tests pass.
- [ ] BDD scenarios from PRD pass.
- [ ] Code review approved.
- [ ] Feature flagged.

**Outputs:**
- Code + tests.
- Feature flag configuration.

**Responsible:** Engineer / Flutter Agent + Backend Agent.

---

## Stage 8 — Testing

**Question:** Does it work correctly for users at every level?

### Testing Taxonomy

| # | Type | What It Validates | Who Runs It | When |
|---|---|---|---|---|
| 1 | **Unit tests** | Individual functions, methods, business rules | Engineer | Stage 7 (before merge) |
| 2 | **Widget tests** | Flutter UI components in isolation | Engineer | Stage 7 (before merge) |
| 3 | **Golden tests** | Visual regression for Flutter components | Engineer | Stage 7 (before merge) |
| 4 | **Integration tests** | API endpoints, service ↔ database interactions | Engineer / QA | Stage 8 |
| 5 | **BDD / Acceptance tests** | PRD acceptance criteria end-to-end | QA | Stage 8 |
| 6 | **E2E tests** | Full user journey across mobile + backend | QA | Stage 8 |
| 7 | **Regression tests** | Existing features not broken by the change | QA | Stage 8 |
| 8 | **Offline / Sync tests** | Feature works offline; sync resolves correctly | QA | Stage 8 |
| 9 | **AI recommendation tests** | AI output is safe, contextually correct, not stale | QA + Product | Stage 8 |
| 10 | **Accessibility tests** | Screen reader, contrast, tap target size | Engineer / QA | Stage 8 |
| 11 | **Security tests** | Auth, permissions, PII exposure (if Stage 5 flagged) | Security / QA | Stage 8 |
| 12 | **Performance tests** | Latency, memory, load (for data-heavy or AI features) | Engineer / QA | Stage 8 |
| 13 | **UAT (User Acceptance Testing)** | Feature meets real user needs — validated with actual users or founder | Product | Stage 8 (pre-release) |
| 14 | **Smoke tests** | Critical paths working immediately after deployment | QA / DevOps | Stage 9 (post-deploy) |

Types 1–3 run in Stage 7 and are gates for merge. Types 4–13 run in Stage 8 and are gates for release. Type 14 runs post-deploy in Stage 9.

---

### Bug Severity Classification

Every bug found at any testing level is classified by severity before routing.

| Severity | Definition | Example | Release Impact |
|---|---|---|---|
| **P1 — Blocker** | Feature cannot be used at all; data loss or safety risk | Receipt scan crashes app; allergy check skipped | Blocks release entirely |
| **P2 — Critical** | Core functionality broken for most users; no workaround | Pantry not updating after cook; shopping list not saving | Blocks release |
| **P3 — Major** | Significant degradation with a workaround; affects many users | Wrong item count displayed; offline mode shows stale data | Deferred to next sprint unless close to fix |
| **P4 — Minor** | Cosmetic or edge-case issue; low user impact | Spacing inconsistency; tooltip typo | Deferred to backlog |

---

### Bug Routing by Test Level

| Found At | Severity | Routes To | Gate |
|---|---|---|---|
| Unit / Widget / Golden | Any | Fix before merge — stay in Stage 7 | Blocks merge |
| Integration / BDD / E2E | P1 or P2 | Back to Stage 7 → re-run Stage 8 | Blocks Stage 9 |
| Integration / BDD / E2E | P3 or P4 | Log in backlog, proceed with release | Does not block |
| Offline / Sync tests | P1 or P2 | Back to Stage 7 → re-run offline tests | Blocks Stage 9 |
| AI recommendation tests | P1 (safety) | Back to Stage 7 — safety issues always block | Blocks Stage 9 |
| AI recommendation tests | P3 or P4 | Log and tune post-release | Does not block |
| Accessibility / Security | Any | Back to Stage 7 → re-test | Blocks Stage 9 |
| UAT | P1 or P2 | Back to Stage 7 | Blocks Stage 9 |
| UAT | P3 or P4 | Captured as new Epic (Stage 1) or PRD amendment | Does not block |
| Post-deploy Smoke (Stage 9) | P1 | Trigger rollback immediately | Rollback |
| Post-deploy Smoke (Stage 9) | P2 | Hotfix sprint → Stages 7→8→9 | Monitor closely |
| Production (Stage 10) | P1 | Hotfix — bypass Stages 1–6, go to 7→8→9 | Freeze other releases |
| Production (Stage 10) | P2 | Hotfix sprint next cycle | Does not freeze |
| Production (Stage 10) | P3/P4 | Backlog | Scheduled normally |

---

### Regression Gate

When a P1 or P2 bug is fixed, the following test types must re-run before proceeding:

```text
Fix committed
      │
      ▼
Unit tests (mandatory)
      │
      ▼
Integration + BDD tests (mandatory)
      │
      ▼
E2E tests (mandatory for P1; recommended for P2)
      │
      ▼
Regression tests (mandatory)
      │
      ▼
Re-verify the specific test that originally failed (mandatory)
```

P3 / P4 fixes only require the directly affected test type to re-run.

---

**Gate criteria — cannot proceed to Stage 9 until:**
- [ ] All PRD acceptance criteria verified (BDD pass).
- [ ] No P1 or P2 bugs open.
- [ ] All P3/P4 bugs logged in backlog with owner.
- [ ] Offline/sync tests pass.
- [ ] Security items from Stage 5 cleared.
- [ ] UAT sign-off from Product Owner.
- [ ] Accessibility tests pass for all new screens.

**Outputs:**
- QA sign-off with bug log.
- Test results summary (pass/fail per type).
- P3/P4 backlog items created.

**Responsible:** QA / Product Owner / QA Agent.

---

## Stage 9 — Release

**Question:** Are we deploying safely?

**Activities:**
- CI/CD pipeline runs automatically on merge to main.
- Enable feature flag for staged rollout (internal → beta → all users).
- Monitor error rates, latency, and user signals in the first 24 hours.
- Rollback plan documented and tested before release.

**Gate criteria — cannot release until:**
- [ ] CI/CD pipeline passes.
- [ ] Rollback plan documented.
- [ ] Monitoring alerts configured.

**Outputs:**
- Deployed feature.
- Release notes (internal).

**Responsible:** DevOps / DevOps Agent.

---

## Stage 10 — Operate *(Post-MVP)*

**Question:** Is the feature running healthily in production?

**Activities:**
- Monitor logs, metrics, and alerts in `Knowledge/90_Operations/`.
- Incident response if issues arise.
- Runbook updated for any new operational procedures.

**Responsible:** SRE / SRE Agent.

---

## Stage 11 — Learn *(Post-MVP)*

**Question:** Did we solve the right problem?

**Activities:**
- Review feature analytics against acceptance criteria and North Star Metric.
- Collect user feedback and support signals.
- Update the Open Questions register (`Knowledge/10_Product_Vision.md`, Section 60) with findings.

**Responsible:** Product Owner / Analytics Agent.

---

## Stage 12 — Iterate *(Post-MVP)*

**Question:** What should we do differently next?

**Activities:**
- Feed findings back into Stage 3 (new PRD iteration) or Stage 1 (new idea).
- Update the PRD with learnings if the feature continues to evolve.

**Responsible:** Product Owner.

---

## Document Output Per Stage

Every stage produces or updates exactly one class of documents. Nothing gets lost.

| Stage | Document(s) Updated or Created |
|---|---|
| 1 — Idea | Epic (informal) |
| 2 — Discovery | Discovery notes (in PRD background) |
| 3 — Product Definition | `30_PRDs/PRD-XXX.md`, `60_Decision_Records/PDR-XXX.md` |
| 4 — UX Design | Wireframes in PRD, `60_Decision_Records/UXDR-XXX.md` |
| 5 — Architecture Review | `20_Domain_Model.md`, `40_Technical_Architecture.md`, `60_Decision_Records/ADR-XXX.md` |
| 6 — Planning | Engineering tickets |
| 7 — Development | Code + tests |
| 8 — Testing | QA sign-off |
| 9 — Release | Release notes, monitoring config |
| 10 — Operate | `90_Operations/` runbooks |
| 11 — Learn | Open Questions register, analytics |
| 12 — Iterate | Updated PRD or new Epic |

---

## AI Agent Assignments *(Future State)*

When AI agents are introduced, each stage has a designated responsible agent. Stage gates become agent handoff contracts: an agent cannot pass output to the next agent until all gate criteria are met.

| Stage | Responsible Agent | Inputs | Outputs |
|---|---|---|---|
| 1 — Idea | Product Agent | Product Vision, North Star | Epic |
| 2 — Discovery | Research Agent | Epic, existing PRDs | Discovery notes |
| 3 — Product Definition | Product Agent | Discovery notes | PRD, BDD scenarios |
| 4 — UX Design | Design Agent | PRD, Design System | Wireframes, UXDR |
| 5 — Architecture Review | Architect Agent | PRD, Domain Model | Updated Domain Model, ADR |
| 6 — Planning | Scrum Agent | PRD, Architecture | Engineering tickets |
| 7 — Development | Flutter Agent + Backend Agent | Tickets, Engineering Handbook | Code + tests |
| 8 — Testing | QA Agent | PRD acceptance criteria, code | QA sign-off |
| 9 — Release | DevOps Agent | Tested code, rollback plan | Deployed feature |
| 10 — Operate | SRE Agent | Monitoring config | Incident runbooks |
| 11 — Learn | Analytics Agent | Metrics, feedback | Learnings report |
| 12 — Iterate | Product Agent | Learnings | Updated PRD or new Epic |

---

## Governance Summary

Three types of governance activity and where they are defined:

| Activity | When It Happens | Defined In |
|---|---|---|
| Stage Gate approval | Between every stage | This document |
| Definition of Done | Stage 7 (Development) | `Templates/Definition_of_Done.md` |
| Architecture Review | Stage 5 | `Templates/Architecture_Review_Checklist.md` |
| Security Review | Stage 5 (flagged) | `Knowledge/100_Security/` *(planned)* |
| Release approval | Stage 9 | `Knowledge/90_Operations/` *(planned)* |
