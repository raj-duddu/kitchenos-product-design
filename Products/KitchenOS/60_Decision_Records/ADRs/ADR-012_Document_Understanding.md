---
id: ADR-012
title: Document Understanding Capability Replaces OCR-First Receipt Parsing
type: adr
status: accepted
owner: architecture
depends_on: [ADR-010, GDR-002, GOV-001]
referenced_by: [DOC-010, DOC-020, DOC-040, DOC-050]
operating_principles: ["1. Transform Complexity into Clarity", "4. AI Recommends. People Decide.", "5. Earn Trust Through Transparency", "6. Learn Continuously", "9. Simplicity Is a Feature"]
tags: [receipts, ocr, document-understanding, llm, multimodal, ai-pipeline, pantry, privacy]
date: 2026
---

# ADR-012: Document Understanding Capability Replaces OCR-First Receipt Parsing

**Status:** Accepted
**Date:** 2026-07-03
**Deciders:** Founders (proposed via Architect role)
**Stage Gate:** Stage 5 of Product Development Lifecycle
**Operating Principles:** 1 (Transform Complexity into Clarity), 4 (AI Recommends. People Decide.), 5 (Earn Trust Through Transparency), 6 (Learn Continuously), 9 (Simplicity Is a Feature). No conflicts identified.

---

## Context

The current architecture names Cloud Vision as the receipt OCR provider (`Products/KitchenOS/40_Technical_Architecture.md` Section 36, `Products/KitchenOS/50_Engineering_Handbook.md` Section 42.3) and names the building block "Receipt OCR Pipeline." Cloud Vision was adopted as part of the GCP stack without its own decision record — this is the first record in which the extraction approach is reasoned through.

The problem is misnamed. KitchenOS does not need *text extraction*; it needs *purchase understanding*: store, date, and structured line items (product, quantity, unit, price) mapped toward canonical pantry items. Classic OCR solves only the first step and creates a second, harder one:

- OCR returns raw text and positions; a custom parser must reconstruct meaning from thermal-paper layouts, store-specific abbreviations (`ORGC WHLMLK 32OZ`), multi-line items, discounts, and weights — effectively one parser per retailer format.
- Founder's direct experience building a Cloud Vision receipt parser: extraction quality required manual correction almost always, and the parser grew without bound. Switching that system to a multimodal LLM produced materially better structured extraction with far less custom code.
- The building block's technology-first name ("Receipt OCR Pipeline") violates our own naming convention — every other building block (Household Decision Engine, Allergy Guard, Sync Engine) is named for its responsibility, not its implementation.

Constraints: extraction output feeds the pantry only through user confirmation (ADR-010 — pantry state derives exclusively from confirmed activities); receipt images may contain PII fragments (loyalty numbers, partial card digits), so external processing falls under GDR-002; all AI calls must pass through the AI Provider Abstraction ("never call a provider directly").

---

## Decision

**We will introduce a Document Understanding capability — responsible for converting unstructured household documents into structured proposals, with per-field confidence, for user confirmation — implemented by a multimodal LLM behind the AI Provider Abstraction. It replaces the Cloud Vision + custom parser pipeline and the "Receipt OCR Pipeline" building block.**

Scope discipline: the capability is named generally; MVP-0 implements exactly one document type — receipts. Additional document types (nutrition labels, recipes, expiry dates) are added only when a real feature demands them, each via its own PRD.

Model selection is deliberately **not** part of this decision. Which multimodal model fills the slot (Gemini Flash-class, GPT-class, or successors) is a configuration choice governed by the Model Evaluation process in `Company/Governance/AI_Governance.md`, re-run as models evolve. This record survives model churn; the evaluation process handles it.

---

## Reasons

- **The LLM solves the actual problem.** One schema-constrained call produces structured line items with abbreviation resolution and store-format generalisation — collapsing OCR, parsing, and normalisation into a single step and eliminating the per-retailer parser entirely (Principle 9, and Decision Priority 3: least machinery that solves the problem).
- **Founder's lived experience is the strongest available evidence.** The Cloud Vision → parser → manual-correction failure mode was experienced directly; the LLM replacement was experienced to work better. This is precedent, not speculation.
- **The architecture already absorbs the new risk profile.** LLM errors are plausible fabrications rather than visible garbles — but ADR-010 already mandates that extraction output is a proposal confirmed by the user, and receipts carry their own checksum: extracted line items must reconcile against the printed total (± tax), giving a deterministic fabrication check that does not rely on model self-awareness.
- **Vendor independence is preserved by design.** The AI Provider Abstraction already exists for exactly this scenario; the domain events and confirmation flow are unchanged. Only the implementation behind the capability boundary changes.

---

## Alternatives Considered

### Option A: Keep Cloud Vision + custom parser (do nothing)

Retains a known-brittle pipeline: parser-per-retailer-format, no semantic understanding, and a correction burden that directly undermines the product's trust bar. Rejected on direct experience and Decision Priorities 2–4 (a simple-looking service hiding an ever-growing parser is not simplicity).

### Option B: Hybrid — Cloud Vision OCR text, then text-only LLM structuring

Cheaper per call and cannot misread pixels it never sees, but discards layout information (column alignment, item/price association), keeps two components plus prompt logic, and still pays both vendors. Viable fallback posture if multimodal costs spike; not the starting point.

### Option C: Dedicated receipt-extraction SaaS (Veryfi, Mindee, Taggun)

Purpose-built, strong accuracy on receipts. Rejected for MVP-0: adds a single-purpose vendor and data-processing relationship for a capability we intend to generalise beyond receipts; per-document pricing at scale is comparable or worse; and GDR-002 review of another external processor is pure overhead. Re-evaluate if LLM extraction misses the quality bar in evaluation.

### Option D: Manual entry only

Zero extraction risk, maximum user effort. Contradicts the product vision (reduce household effort and decision fatigue). Manual entry remains the *fallback* when extraction fails or confidence is low — it is the floor, not the product.

### Option E (chosen): Multimodal LLM behind the Document Understanding capability

As decided above.

---

## Consequences

### Positive

- Single-step extraction: image → structured proposal (store, date, line items, per-field confidence). No custom parser to build or maintain.
- Building block renamed to its responsibility; implementation swappable behind the capability boundary without domain change.
- Per-field confidence lets the confirmation UI highlight only uncertain rows — Principle 4 and 5 at field granularity.
- User corrections during confirmation emit correction events (already first-class in the Domain Model), becoming a learning signal for future extraction improvement (Principle 6). The prompt-improvement pipeline itself is post-MVP.
- Supports future document types without architectural change — added deliberately, one PRD at a time.

### Negative

- Higher per-receipt cost than Cloud Vision (order of cents vs. tenths of cents). Accepted: receipts are low-frequency events and the cost buys away the correction loop.
- Extraction latency (seconds) requires the existing async pipeline (Cloud Tasks) and a pending-state UX; unchanged from the current design.
- Locked in: structured-proposal contract (schema with per-field confidence) becomes the interface all consumers depend on.

### Risks

- **Fabrication:** the model may invent or misread items with high stated confidence. Primary mitigation is mechanical — line items must reconcile against the printed receipt total (± tax logic); failures mark the proposal low-confidence. Secondary: user confirmation (ADR-010) before any pantry effect.
- **Confidence calibration:** self-reported LLM confidence is poorly calibrated; AI Governance requires < 0.05 calibration error. Calibration must be established from the evaluation set (≥ 50 real receipts across store formats, per the Model Evaluation requirements), not from prompt output alone.
- **Privacy:** receipt images may contain PII fragments. The provider must operate under no-training / no-retention terms; raw images are retained only until confirmation completes, then only confirmed line items persist (GDR-002 data minimisation). This exposure existed with Cloud Vision but is recorded here for the first time.
- **Provider outage or quality regression:** fallback chain is retry → manual entry. No OCR fallback is kept — OCR output without the parser is unusable, and keeping the parser would silently retain the system this decision removes.

---

## Confidence

**High** on replacing OCR + parser with LLM extraction: direct founder experience plus broad industry precedent for semi-structured document extraction. **Medium** on cost projections and calibration effort: to be validated by the evaluation set before acceptance is implemented.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-03 | Proposed | Claude (Architect role), sponsored by @raj-duddu | PR # 6 |
| 2026-07-03 | Accepted | @raj-duddu | PR # 6 review |

---

## Related

- ADR-001, ADR-002 — this record amends the Cloud Vision elements of their rationale (Flutter and GCP decisions unaffected)
- ADR-010 — Pantry state derived exclusively from confirmed activities (the confirmation gate this capability feeds)
- GDR-002 / `Company/Governance/GDRs/GDR-002_Privacy_By_Design.md` — external processing and data minimisation constraints
- `Company/Governance/AI_Governance.md` — Model Evaluation (owns model selection), Confidence and Explanation Requirements, AI Quality Metrics
- `Products/KitchenOS/40_Technical_Architecture.md` — Sections 36 (AI Data Pipeline) and 37.10 (building blocks); to be updated on acceptance
- `Products/KitchenOS/50_Engineering_Handbook.md` — Section 42.3 (MVP-0 AI stack); to be updated on acceptance
- `Products/KitchenOS/10_Product_Vision.md` — Section 39.5 (Receipt Scan: Data Entry System, currently "Basic OCR"); to be updated on acceptance
- `Products/KitchenOS/20_Domain_Model.md` — Correction Event (the learning-signal mechanism)
