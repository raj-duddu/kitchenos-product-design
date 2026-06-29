# Architecture Review Checklist

**Feature / PRD:** [PRD-XXX Feature Name]
**Reviewer:** [Architect name or role]
**Date:** YYYY-MM-DD
**Stage Gate:** Stage 5 of Product Development Lifecycle

---

## Domain Model Impact

- [ ] Does this feature introduce new domain entities?
  - If yes, which: ___
  - Action: Update `Knowledge/20_Domain_Model.md` before Stage 7.

- [ ] Does this feature introduce new domain events?
  - If yes, which: ___
  - Action: Add to Domain Events catalogue in `Knowledge/20_Domain_Model.md`.

- [ ] Does this feature introduce new business invariants?
  - If yes, which: ___
  - Action: Add to Business Invariants in `Knowledge/20_Domain_Model.md`.

- [ ] Does this feature change an existing aggregate or entity boundary?
  - If yes, explain: ___
  - Action: Architecture review required before Domain Model update.

---

## API Impact

- [ ] Does this feature require new API endpoints?
  - If yes, document in `Knowledge/80_API_Reference/` *(planned)*.

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

- [ ] Does this feature change what AI recommends or how it ranks?
  - If yes, update AI Orchestrator logic accordingly.

- [ ] Does this feature require new offline-safe recommendations?
  - If yes, assess `recommendation_expires_at` strategy.

---

## Infrastructure Impact

- [ ] Does this feature require new infrastructure (services, queues, storage)?
  - If yes, which: ___

- [ ] Does this feature require new GCP services or Cloud Run jobs?
  - If yes, assess cost and operational overhead.

- [ ] Does this feature impact offline behaviour or the Sync Engine?
  - If yes, assess SQLite schema and conflict resolution.

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
  - Add to Knowledge Map Decision Records Index.

---

## Architecture Review Outcome

- [ ] **Approved** — proceed to Stage 6.
- [ ] **Approved with conditions** — conditions: ___
- [ ] **Blocked** — reason: ___
