---
id: KNOW-PAT-003
title: Privacy by Design Pattern
type: knowledge-pattern
status: active
owner: founders
scope: company-wide
related: [KNOW-PAT-001, KNOW-PAT-002]
implements: [GDR-002]
date: 2026
---

# Privacy by Design Pattern

> This document captures the Privacy by Design pattern as a reusable architectural reference for all Amanaska products. The company-wide policy is in GDR-002. The KitchenOS architectural implementation is in ADR-009. This document is the conceptual bridge between the two.

---

## The Pattern

Privacy by Design (PbD) is not a compliance checklist. It is a systems design principle: **privacy protections must be structural, not procedural.** A system that relies on engineers remembering to encrypt data, or on policies that say "don't log PII," will eventually fail. A system that is physically incapable of leaking PII from one layer to another will not.

The seven foundational principles (Ann Cavoukian, 2009) and how we apply them:

| Principle | How Amanaska applies it |
|---|---|
| **Proactive, not reactive** | Privacy is a design constraint from day one. Not retrofitted after a breach. |
| **Privacy as the default** | Collective Intelligence is opt-out by default (it is opt-in only). Data minimisation is the default collection posture. |
| **Privacy embedded into design** | Schema separation (Auth / Person / Domain / Intelligence) makes cross-layer PII exposure structurally impossible. |
| **Full functionality — positive-sum** | Privacy does not reduce product capability. Identity isolation does not prevent personalisation. It just keeps the AI layer free of PII. |
| **End-to-end security** | Data is encrypted at rest and in transit. Every layer boundary enforces access control. |
| **Visibility and transparency** | Users can see what data is held, correct AI beliefs, delete their account. The Household Timeline makes AI actions visible. |
| **Respect for user privacy** | Users control consent, data, and model state. The system does not collect, infer, or retain data without a clear user benefit. |

---

## The Four-Layer Isolation Pattern

This is the structural implementation of Privacy by Design for Amanaska products:

```text
Layer 1 — Auth (separate schema)
  ├── email        ← the only PII in the system
  ├── auth_provider
  └── created_at
  
  Never read by Layer 2, 3, or 4.

Layer 2 — Person (domain schema)
  ├── person_id    ← stable identifier, no PII
  ├── identity_id  ← bridge to Layer 1, never used in AI or analytics
  ├── age_group
  └── age_range
  
  Layer 3 and 4 use person_id only. Never identity_id.

Layer 3 — Domain (domain schema)
  ├── households, household_memberships
  ├── pantry, meals, shopping, receipts
  ├── dietary_constraints, user_goals
  └── expert_marketplace, consent_grants
  
  No PII. Keyed on person_id and household_id.

Layer 4 — Intelligence (intelligence schema, separate)
  ├── learned preferences, confidence scores
  ├── behavioural patterns
  └── collective model contributions (anonymised)
  
  No PII, no domain facts (allergies/goals live in Layer 3).
  Keyed on person_id + household_id.
  Replaceable: deleting this layer does not affect Layer 3.
```

**The invariant:** Dependency flows downward only. Layer 4 depends on Layer 3. Layer 3 depends on Layer 2. Layer 2 depends on Layer 1. The reverse is never true.

---

## Privacy in Event Sourcing

Domain events must never contain PII in their payload:

```jsonc
// WRONG — PII in event payload
{
  "event_type": "household.member.added",
  "payload": { "email": "user@example.com", "name": "Alice" }
}

// RIGHT — person_id only
{
  "event_type": "household.member.added",
  "payload": { "person_id": "uuid", "role": "admin" }
}
```

If an event needs to reference the person's display name for a Household Timeline entry, it is resolved at read time from the Person layer — never stored in the event.

---

## Consent as a Domain Concept

Consent is not a checkbox in a UI. In Amanaska products, consent is a domain entity (`ConsentGrant`) with:
- Granular scope (which data types are shared)
- Time boundary (start and end)
- Revocability (can be withdrawn at any time)
- Explicit acceptance event (`ConsentGranted`) and revocation event (`ConsentRevoked`)

A `ConsentGrant` is the only mechanism by which an Expert may access household data. The scope cannot be broadened after the grant is issued — a new grant must be created.

---

## When This Pattern Is Tested

A privacy architecture is only as strong as its tests. Required tests for every Amanaska product:

1. **AI layer never receives email or identity_id** — integration test confirming the intelligence service receives only `person_id` and `household_id`.
2. **Domain events contain no PII** — linting rule or test that scans event payloads for email-shaped strings.
3. **Account deletion removes all layers** — end-to-end test: delete account → verify Auth, Person, Domain, and Intelligence rows are removed.
4. **Collective Intelligence strips household_id before aggregation** — unit test on the anonymisation pipeline.
5. **ConsentGrant scope cannot be broadened** — domain invariant test.

---

## Related

- GDR-002 — Privacy by Design (company-wide policy)
- ADR-009 — Privacy-by-design and identity isolation (KitchenOS architectural decision)
- ADR-011 — Person as a global domain concept
- `Products/KitchenOS/40_Technical_Architecture.md`, Section 23 — four-layer model implementation
- `Knowledge/Patterns/Event_Sourcing.md` — PII in event payloads
