---
id: UXDR-001
title: Async AI Proposals Follow the Scan-and-Forget, Review-Later Pattern
type: uxdr
status: accepted
owner: product
depends_on: [ADR-010, GDR-001]
referenced_by: [PRD-001]
operating_principles: ["3. Inspire Confident Action", "4. AI Recommends. People Decide.", "5. Earn Trust Through Transparency"]
tags: [uxdr, interaction-pattern, async, ai-proposals, confirmation, receipt, trust]
date: 2026
---

# UXDR-001: Async AI Proposals Follow the Scan-and-Forget, Review-Later Pattern

**Status:** Accepted
**Date:** 2026-07-03
**Deciders:** Founders
**Stage Gate:** Stage 3–4 of Product Development Lifecycle
**Operating Principles:** 3 (Inspire Confident Action), 4 (AI Recommends. People Decide.), 5 (Earn Trust Through Transparency)

---

## Context

KitchenOS repeatedly produces AI work that takes seconds to complete and requires user confirmation before touching household state (ADR-010, GDR-001): receipt extraction today; weekly meal plan generation, swap suggestions, and expert-plan reviews next. Each such feature needs an interaction shape for the gap between "user asked" and "user confirms."

The naive shape — a blocking spinner ending in a modal — makes AI latency the user's problem and turns every proposal into an interruption. Receipt scanning (PRD-001) forced the decision first: extraction takes 5–15 seconds, and the user's hands are full of groceries.

---

## Decision

**Every asynchronous AI proposal follows one pattern: initiate-and-leave → pending card in the Household Timeline → push notification when ready → review screen that highlights only low-confidence elements → one primary confirm action → state changes only on confirmation.**

Latency is absorbed by the pending state, never by a blocking UI. Attention is spent only where the AI is uncertain. Confirmation is the single moment household state changes.

---

## Reasons

- The confirmation step is mandated anyway (ADR-010, GDR-001) — placing it after an interruptible pending state makes the required review feel like control, not friction.
- Highlighting only uncertain elements respects the user's attention budget: correcting 2 rows of 14 is sustainable; auditing 14 every time is not (Principle 3).
- Per-element confidence made visible is Principle 5 rendered as UI, and it matches the AI Governance requirement to surface confidence at Medium+ criticality.
- One pattern across features compounds: users learn it once; engineering builds the pending-card, notification, and review primitives once.

---

## Alternatives Considered

### Option A: Blocking progress UI per feature
Makes seconds-long AI latency a felt cost everywhere; punishes the user for the system's work. Rejected.

### Option B: Silent auto-apply with undo
Fastest apparent UX; violates ADR-010 and GDR-001 for state-touching proposals — undo-after-the-fact is not confirmation. Rejected on governance, not taste.

### Option C: Review everything uniformly (no confidence highlighting)
Treats settled and uncertain rows identically; trains users to rubber-stamp or abandon. The founder's OCR experience showed exactly this failure. Rejected.

### Option D: Per-feature bespoke patterns (do nothing)
Each feature designs its own async shape; users relearn per feature; primitives rebuilt per feature. Rejected.

---

## Consequences

### Positive
- A reusable interaction contract: pending card, ready notification, review-with-highlights, single confirm — built once, reused by meal planning and expert flows.
- AI latency becomes architecturally irrelevant to UX quality within this pattern.

### Negative
- Requires the notification path and Timeline pending states to exist early (they are MVP-0 stack items regardless).
- Proposals the user never reviews accumulate; pending-state expiry rules are needed per feature.

### Risks
- Notification fatigue if every proposal pings. Mitigation: notify for user-initiated work (a scan) by default; batch or digest AI-initiated suggestions.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-03 | Proposed | Claude (PM role), sponsored by @raj-duddu | PR # 10 |
| 2026-07-03 | Accepted | @raj-duddu | PR # 10 |

---

## Related

- PRD-001 — first implementation of the pattern (receipt scanning)
- ADR-010 — confirmation-only state mutation (the rule this pattern wraps in UX)
- GDR-001 — trusted decision support; no autonomous action
- ADR-012 — per-field confidence output that the review screen renders
- PDR-003 — Home screen answers a question; "review your receipt" is such an answer
- `Company/Governance/AI_Governance.md` — confidence display requirements at Medium+ criticality
