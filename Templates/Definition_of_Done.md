# Definition of Done

> A task or feature is **Done** only when every applicable criterion below is met. Partially done is not done.

**Feature / PRD:** [PRD-XXX Feature Name]
**Sprint / Release:** [Sprint or release identifier]

---

## Code

- [ ] All acceptance criteria from the PRD verified.
- [ ] Code reviewed and approved by at least one other engineer.
- [ ] No commented-out code left behind.
- [ ] No TODO comments left unresolved without a linked ticket.

---

## Testing

- [ ] Unit tests written for all new functions and methods.
- [ ] BDD scenarios from the PRD pass.
- [ ] Integration tests pass.
- [ ] No critical or blocker bugs open.
- [ ] Edge cases (empty states, error states, offline states) tested.

---

## Coverage

- [ ] Backend test coverage ≥ 80% for new code (per Engineering Handbook).
- [ ] Flutter widget tests written for all new screens.
- [ ] Flutter golden tests written for all new visual components.

---

## Domain Model

- [ ] If new entities or events were introduced: `Products/KitchenOS/20_Domain_Model.md` updated.
- [ ] If new business invariants were introduced: added to Domain Model.

---

## Documentation

- [ ] PRD acceptance criteria marked as verified.
- [ ] If an ADR was needed: written and added to Knowledge Map.
- [ ] If a PDR or UXDR was needed: written and added to Knowledge Map.
- [ ] Any new Engineering Handbook standards documented.

---

## Deployment

- [ ] Feature flagged — not live to all users automatically.
- [ ] CI/CD pipeline passes on main branch.
- [ ] Rollback plan documented.
- [ ] Monitoring alerts configured for new endpoints or features.

---

## Security *(if flagged in Architecture Review)*

- [ ] Security Review completed and cleared.
- [ ] No new PII exposed without consent.
- [ ] New auth/authorization rules tested.

---

## Sign-Off

| Role | Name | Date | Status |
|---|---|---|---|
| Engineer | | | |
| Reviewer | | | |
| QA | | | |
| Product Owner | | | |
