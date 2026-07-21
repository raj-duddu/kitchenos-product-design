# Architecture Review Checklist

**Feature / PRD:** [PRD-XXX Feature Name]
**Reviewer:** [Architect name or role]
**Date:** YYYY-MM-DD
**Stage Gate:** Stage 5 of Product Development Lifecycle
**Operating Principles:** [Which of the 10 Operating Principles does this feature touch? List by number and name.]

---

## Operating Principles Alignment

Every architecture decision must be traceable to at least one Operating Principle. If a design choice conflicts with a principle, the conflict must be documented and escalated — not silently resolved.

- [ ] Which Operating Principles govern this feature's architecture? ___
- [ ] Does this feature's design align with all relevant principles?
  - If no, document the conflict explicitly: ___
  - Escalate to founders before proceeding.
- [ ] Does this feature involve AI output? If yes, confirm:
  - [ ] Principle 4 (AI Recommends. People Decide.) — no autonomous irreversible action
  - [ ] Principle 7 (Truth Before Convenience) — uncertainty is visible, staleness is explicit, no false certainty
- [ ] Does this feature collect or process user data? If yes, confirm:
  - [ ] Principle 8 (We Are Stewards, Not Owners) — data collected only to serve the user
  - [ ] GDR-002 (Privacy by Design) reviewed

---

## Domain Model Impact

- [ ] Does this feature introduce new domain entities?
  - If yes, which: ___
  - Action: Update `Products/KitchenOS/20_Domain_Model.md` before Stage 7.

- [ ] Does this feature introduce new domain events?
  - If yes, which: ___
  - Action: Add to Domain Events catalogue in `Products/KitchenOS/20_Domain_Model.md`.

- [ ] Does this feature introduce new business invariants?
  - If yes, which: ___
  - Action: Add to Business Invariants in `Products/KitchenOS/20_Domain_Model.md`.

- [ ] Does this feature change an existing aggregate or entity boundary?
  - If yes, explain: ___
  - Action: Architecture review required before Domain Model update.

- [ ] Does this feature touch the four-layer identity model (Auth / Person / Domain / Intelligence)?
  - If yes, confirm: dependency direction is domain → intelligence, never reversed.

---

## API Impact

- [ ] Does this feature require new API endpoints?
  - If yes, document in `Products/KitchenOS/80_API_Reference/` *(planned)*.

- [ ] Does this feature change existing API contracts?
  - If yes, assess backward compatibility and versioning.

---

## Database Impact

- [ ] Does this feature require new tables or columns?
  - If yes, which: ___

- [ ] Does this feature require a schema migration?
  - If yes, plan migration strategy and rollback.

- [ ] Does this feature require new indexes or materialized views?
  - If yes, which: ___

---

## AI / Household Decision Engine Impact

- [ ] Does this feature produce new signals for the AI?
  - If yes, what `learning_impact` value should events carry?
  - Confirm: signals are only from interactions within user-granted permissions (Principle 6).

- [ ] Does this feature change what AI recommends or how it ranks?
  - If yes, update AI Orchestrator logic accordingly.

- [ ] Does this feature require new offline-safe recommendations?
  - If yes, assess `recommendation_expires_at` strategy.

- [ ] Does this feature produce AI output with confidence levels?
  - If yes, confirm uncertainty is surfaced to the user — never hidden (Principle 7).

---

## Infrastructure Impact

- [ ] Does this feature require new infrastructure (services, queues, storage)?
  - If yes, which: ___

- [ ] Does this feature require new GCP services or Cloud Run jobs?
  - If yes, assess cost and operational overhead.

- [ ] Does this feature impact offline behaviour or the Sync Engine?
  - If yes, assess SQLite schema and conflict resolution.

- [ ] Does this feature introduce a new external dependency (AI provider, third-party API)?
  - If yes, confirm it is called through an abstraction interface — no direct provider reference in domain code.

- [ ] What operational signals does this feature need monitored (e.g. latency, error rate, queue/backlog depth, sync failure rate)? List them: ___
  - Numeric alert thresholds may be TBD until `Products/KitchenOS/90_Platform_Operations/` exists — that's fine. The point is that every feature names its own signals at design time, not that thresholds are set before there's traffic to threshold against.
  - Action: carry this list forward into `90_Platform_Operations/` once that document exists, so operational monitoring is assembled from what features actually flagged, not invented retroactively.

---

## Security Impact

- [ ] Does this feature touch user PII or household financial data?
- [ ] Does this feature require new authentication or authorization rules?
- [ ] Does this feature require new consent grants or data scope changes?
- [ ] Does this feature have an attack surface (new endpoints, file uploads, external data)?

If any above are Yes: **Security Review required before Stage 7.**

---

## ADR Decision

- [ ] Is a new architecture decision being made that is significant and non-obvious?
  - If yes, write ADR using `Templates/ADR_Template.md`.
  - The ADR must include an `operating_principles:` field citing which principles apply.
  - Add to Knowledge Map Decision Records Index.

---

## Architecture Review Outcome

- [ ] **Approved** — proceed to Stage 6.
- [ ] **Approved with conditions** — conditions: ___
- [ ] **Blocked** — reason: ___
