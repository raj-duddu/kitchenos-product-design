---
id: ARC-001
title: Architecture Review — PRD-001 Receipt Scanning
type: architecture-review
status: in-review
owner: architect
depends_on: [PRD-001, DOC-071, DOC-020, DOC-040, ADR-010, ADR-012, GDR-002, GOV-001]
referenced_by: []
tags: [architecture-review, stage-5, receipt, ai-review, security]
date: 2026
---

# Architecture Review — PRD-001: Receipt Scanning to Pantry Update

**Feature / PRD:** PRD-001 Receipt Scanning to Pantry Update
**Reviewer:** Architect role (founder sign-off pending — Gate 5, no self-approval)
**Date:** 2026-07-11
**Stage Gate:** Stage 5 of Product Development Lifecycle
**Operating Principles:** 1 (Transform Complexity into Clarity), 2 (Turn Information into Guidance), 4 (AI Recommends. People Decide.), 5 (Earn Trust Through Transparency), 7 (Truth Before Convenience), 8 (We Are Stewards, Not Owners)

---

## Operating Principles Alignment

- [x] Governing principles: 1, 2, 4, 5, 7, 8 (as cited in PRD-001 Product Vision Alignment plus data-stewardship for receipt images).
- [x] Design aligns with all relevant principles — no conflicts to escalate.
- [x] Feature involves AI output:
  - [x] Principle 4 — extraction is a proposal only; `ReceiptItemsConfirmed` is the sole state-changing trigger (ADR-010); confirmation is undoable within a window.
  - [x] Principle 7 — uncertainty rendered as settled / needs-review states; totals mismatch surfaced as a banner, never hidden.
- [x] Feature processes user data:
  - [x] Principle 8 — receipt images collected only to derive pantry/budget state; auto-delete with visible expiry (default 90 days) and per-receipt Keep pin.
  - [x] GDR-002 reviewed — external AI provider under no-training/no-retention terms (ADR-012).

---

## Domain Model Impact

- [x] New domain entities: **none** — Receipt, ShoppingTrip, PantryItem exist.
- [x] New domain events: `ReceiptConfirmationUndone`, `ReceiptDeleted` — **already added** to the Receipt event catalogue in `Products/KitchenOS/20_Domain_Model.md` (pending in the same PR as this review).
- [x] New business invariants: none — the ADR-010 invariant (pantry mutates only on confirmation) governs unchanged.
- [x] Aggregate boundary changes: none. Clarified: a Receipt is confirmable independently of a ShoppingTrip.
- [x] Four-layer identity model: extraction output feeds Domain (pantry, budget) only after confirmation; correction learning signals flow Domain → Intelligence. Dependency direction preserved.

---

## API Impact

- [x] New endpoints: `POST /receipts`, `GET /receipts/{id}/proposal`, `POST /receipts/{id}/confirm`, `POST /receipts/{id}/undo`, `DELETE /receipts/{id}`. Full contract in SD-001; `80_API_Reference/` remains planned.
- [x] Existing contracts changed: none.

---

## Database Impact

- [x] New tables/columns: none beyond existing Receipt-context tables (PRD-001 Architecture Impact). SD-001 verifies proposal storage fits existing schema; if a `receipt_proposals` structure proves necessary, it returns here as a condition.
- [x] Schema migration: none expected.
- [x] New indexes: duplicate-detection lookup (store + date + extraction hash) — indexing decision in SD-001.

---

## AI / Household Decision Engine Impact

- [x] New signals: corrections during review emit `correction_signal` learning impact; unedited confirmations emit `learning`; confirmed-with-unresolved-uncertainty rows are marked unverified extraction (PRD-001 BDD).
- [x] Signals only from within granted permissions (camera + household data) — Principle 6 satisfied.
- [x] Recommendation/ranking changes: none directly; pantry accuracy improves downstream recommendations.
- [x] Offline-safe recommendations: n/a — no recommendation output.
- [x] Confidence handling: per-field confidence collapsed to settled / needs-review; threshold is server-side remote config (PRD-001 OQ-1/OQ-2 resolutions). Numeric scores never shown.

### AI Architecture Review (GOV-001 addendum — required, AI-touching feature)

| Verify | Finding |
|---|---|
| Criticality assigned at design time | **Medium** (PRD-001 Technical Design): proposal + explanation + single confirm action; no autonomous effect. Uncertainty about level resolved upward already applied. |
| Autonomous Action Policy | No autonomous action: extraction runs, but no household state changes without confirmation (ADR-010). Auto-classification of non-food lines only shapes the *proposal*, never state. |
| Confidence, explanation, reversibility in output contract | Yes — per-field confidence, `is_food_item` classification with rationale, totals-check result; confirmation reversible via 30s undo window + PantryCorrection after. SD-001 output contract encodes all three. |
| Prompt ownership and versioning | Extraction prompt owned by the Receipt module; versioned; output-changing edits trigger re-classification and re-run of the ≥50-receipt evaluation set. SD-001 requirement. |
| Context boundaries | Model receives the receipt image and extraction instructions only — no household profile, member, or intelligence-layer data in the extraction context. |
| Hallucination/failure modes + fallback | Fabricated line items guarded by totals reconciliation (primary guard, ADR-012); extraction failure falls back to retake or manual quick-entry (DOC-071 Screen 5); provider outage → pending card + automatic retry. No OCR fallback by decision. |
| Human approval points (Medium+) | Explicit: the review-and-confirm screen is the approval point; one primary action. |
| Children's data constraints | Receipt images are household artifacts, not child behavioural data; no child-member signals produced. Not applicable. |

---

## Infrastructure Impact

- [x] New infrastructure: **none** — Cloud Storage, Cloud Tasks, FCM, AI Provider Abstraction are stack-standard (DOC-040).
- [x] New GCP services: none. New usage: Cloud Storage lifecycle rule for the 90-day photo auto-delete (configuration, not a component).
- [x] Offline/Sync impact: yes — offline capture queues the image via the Sync Engine; SD-001 covers queue semantics and reconnect behaviour.
- [x] External dependency: multimodal LLM provider — called exclusively through the AI Provider Abstraction (ADR-012); no direct provider reference in domain code.

---

## Security Impact

- [x] Touches PII (receipt images: loyalty numbers, partial card digits) and household financial data (spend).
- [ ] New authn/authz rules: none — household-scoped access only.
- [ ] New consent grants: none — camera permission only.
- [x] Attack surface: new endpoints + user file upload + external AI processing path.

**→ Security Review REQUIRED before Stage 7** (upload validation, image storage ACLs, provider data-handling terms, undo/delete authorization).

---

## ADR Decision

- [x] No new ADR required. Governing decisions already recorded: ADR-012 (Document Understanding), ADR-010 (confirmation-only mutation). PRD-001's photo-retention policy **amends ADR-012's delete-on-confirmation mitigation** — ADR-012 History entry to be added in this PR rather than a new record.

---

## Architecture Review Outcome

- [x] **Approved with conditions** — conditions:
  1. Security Review completed before Stage 7 (external AI path, PII in images, upload surface).
  2. SD-001 approved by Tech Lead before Stage 6 (gate criterion).
  3. PRD-001 Open Question 6 (per-line image regions vs. zoomable viewer floor) resolved in SD-001.
  4. Extraction evaluation set (≥50 receipts, GOV-001 Model Evaluation) assembled before Stage 8 exit.
  5. ADR-012 History updated to record the retention-policy amendment.
