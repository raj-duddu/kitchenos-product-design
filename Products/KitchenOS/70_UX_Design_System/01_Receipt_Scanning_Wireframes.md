---
id: DOC-071
title: Receipt Scanning Wireframes
type: ux-design
status: in-review
owner: product
depends_on: [PRD-001, UXDR-001, UXDR-002, DOC-070]
referenced_by: [PRD-001]
tags: [ux, wireframes, receipt, scan, review, shop, timeline]
date: 2026
---

# Receipt Scanning Wireframes (DOC-071)

> This document is the Stage 4 UX design for `PRD-001: Receipt Scanning to Pantry Update`. It is subordinate to the PRD and the interaction records `UXDR-001` and `UXDR-002`; if this document conflicts with them, those sources win. The app-shell structure lives in `Products/KitchenOS/70_UX_Design_System/00_App_Shell_Wireframes.md` (DOC-070).

---

## Every Screen Answers a Question

Per `Products/KitchenOS/10_Product_Vision.md` Section 8.3, every screen exists to answer exactly one user question. This is the Stage 4 gate record for this flow:

| Screen | The question it answers |
|---|---|
| 1 — Capture | "Is this photo good enough to read, or should I retake it?" |
| 2 — Pending | "Do I need to do anything right now?" (answer: no — we'll tell you when) |
| 3 — Review & Confirm | "What did the system read, and which lines actually need me?" |
| 4 — Confirmation Success | "What just changed in my household, and can I take it back?" |
| 5 — Manual Quick-Entry | "How do I record this trip when the scan can't?" |
| Empty state (Receipts segment) | "What do I do first?" |

---

## Entry Points

Three doors into the scan flow, all leading to the same capture screen:

- **Shop tab primary action** — prominent in both `List` and `Receipts` segments (UXDR-002).
- **Home card** — when the system detects an unrecorded shopping trip or empty pantry / low-stock state, the Home card surfaces "Scan your receipt" as a decision moment (Vision §19.1, PDR-003).
- **Notification deep-link** — when a pending proposal is ready, the user taps the notification and lands directly on the review screen (UXDR-001).

```text
┌──────────────────────────────┐    ┌──────────────────────────────┐
│ ┌────────┬─────────┐         │    │ Home                         │
│ │ List   │▸Receipts│         │    │                              │
│ └────────┴─────────┘         │    │                              │
│                              │    │                              │
│ [📷 Scan receipt]            │    │ Suggested today              │
│                              │    │ Palak dal · 97% available    │
│ [Scan receipt] is the same   │    │                              │
│ in both List and Receipts    │    │ ⚠ Pantry is empty            │
│ segments per UXDR-002        │    │ [Scan your first receipt]    │
│                              │    │                              │
├──────────────────────────────┤    │ Shopping · 5 items · ~$24    │
│ Home  Plan ●Shop  Cook  Hshld│    ├──────────────────────────────┤
└──────────────────────────────┘    │ ●Home  Plan Shop  Cook  Hshld│ 
                                    └──────────────────────────────┘
```

---

## Screen 1 — Capture

The camera is the default state. The goal is the 15-second capture-to-pocket window from PRD-001 Story 1.

```text
┌──────────────────────────────┐
│                              │
│   ┌────────────────────┐     │
│   │                    │     │
│   │   receipt card     │     │
│   │   in view          │     │
│   │                    │     │
│   └────────────────────┘     │
│                              │
│   [ 🔲 ]   [ ○ ]   [ ✓ ]     │  ← tap-to-capture plus
│                              │    quality-check overlay
│   [ Import from photos ]     │
│                              │
│  Hold still. We’ll check     │
│  focus and edges before      │
│  accepting.                  │
└──────────────────────────────┘
```

**Quality check states (inline, not blocking):**

- **Good capture:** brief "Looks good" flash → Timeline pending card immediately; user leaves.
- **Blur / glare / cutoff:** retake prompt overlay with specific reason and a one-tap retake button.

```text
┌──────────────────────────────┐
│  ┌────────────────────┐      │
│  │  blurry edge       │      │
│  └────────────────────┘      │
│                              │
│  Edge looks cut off.         │
│  [ Retake ] [ Use anyway ]   │
│                              │
│  Retaking usually takes 2s.  │
└──────────────────────────────┘
```

- **"Use anyway"** is always offered; the user can force the capture if the receipt is too damaged.

---

## Screen 2 — Pending (Scan-and-Forget)

After a good capture, the app shows a Timeline pending card and the user is free to leave. No blocking spinner.

```text
┌──────────────────────────────┐    ┌──────────────────────────────┐
│ Timeline                     │    │ ┌────────┬─────────┐         │
│                              │    │ │ List   │▸Receipts│         │
│ Today                        │    │ └────────┴─────────┘         │
│ ◔ Reading your receipt…      │    │                              │
│   Costco · 14 items          │    │ ◔ Reading your receipt…      │
│   We’ll notify you when it   │    │   pending · 14 items         │
│   is ready to review.        │    │                              │
│                              │    │ ② Costco · review 14 items  │
│ ② Costco · review 14 items  │    │ Kroger · $32.10 · confirmed  │
│   (ready)                    │    │ Costco · $87.43 · confirmed  │
│                              │    │                              │
│ Dinner cooked · 6 deducted   │    ├──────────────────────────────┤
│                              │    │ Home  Plan ●Shop  Cook  Hshld│
├──────────────────────────────┤    └──────────────────────────────┘
│ Home  Plan  Shop  Cook  Hshld│
└──────────────────────────────┘
```

**Pending card states:**

- `◔ Reading your receipt…` — processing.
- `② Costco · review 14 items` — ready for review; the badge count is the number of items needing attention.
- Tap a ready card → review screen.
- Offline capture shows "Waiting for connection…" until the image can upload.

---

## Screen 3 — Review & Confirm

The core screen. The model's extracted values are shown; only uncertain rows are visually prominent. Settled rows are present but do not demand attention.

```text
┌──────────────────────────────┐
│ Review receipt        [ ··· ]│  ← overflow: Delete receipt
│ Costco · $87.43 · Jul 9      │
│                              │
│ ⚠ Total check                │
│ Extracted: $82.15 · Printed: │
│ $87.43 · $5.28 unaccounted   │
│ [ Mark as tax/bag deposit ]  │
│                              │
│ 14 items found               │
│                              │
│ 2 need review                │
│                              │
│ ┌─────────────────────────┐  │
│ │ Organic spinach 10 oz   │  │  ← highlighted: needs review
│ │ $3.49                   │  │
│ │ [tap to verify] · [⊘ not food]│
│ └─────────────────────────┘  │
│                              │
│ ┌─────────────────────────┐  │
│ │ Gallon milk · 1         │  │  ← settled food row
│ │ $4.29                   │  │
│ └─────────────────────────┘  │
│                              │
│ ┌─────────────────────────┐  │
│ │ Fuji apples 3 lb        │  │  ← highlighted: needs review
│ │ $5.99                   │  │
│ │ [tap to verify] · [⊘ not food]│
│ └─────────────────────────┘  │
│                              │
│ ┌─────────────────────────┐  │
│ │ Bottle deposit · $0.60  │  │  ← auto-excluded, not pantry
│ │ [↺ mark as food]        │  │
│ └─────────────────────────┘  │
│                              │
│ [ + Add item ]               │
│                              │
│ [ Add 14 items to pantry ]   │  ← primary confirm action
│                              │
└──────────────────────────────┘
```

**Review mechanics:**

- Settled rows are shown in a muted, collapsed state; they are visible but not the focus.
- Uncertain rows are highlighted with the model's extracted value pre-filled and editable inline.
- Tapping an uncertain row opens the scanned image at the relevant region (where extraction provides it) or a zoomable full-image viewer if not — the paper receipt is never needed (PDR-005).
- Totals mismatch is shown as a banner at the top, not a blocking error. The user can mark the gap as tax, deposit, or bag fee, or correct line items.
- The AI auto-classifies each line as food or non-food (e.g., tax, deposit, bag fee). Non-food rows are excluded from the pantry-add set by default and shown in a muted or grouped "not added to pantry" state.
- The user can override any auto-classification: mark a food row as "not a food item" or mark an excluded non-food row as food. Manual classification per row would violate Principles 1, 7, and 9.
- The confirm action is always available, even if uncertain rows remain unresolved — the extracted value stands and is correctable later (PantryCorrection). Uncertainty is visible, never blocking (PRD-001 Story 2).
- A top-right overflow menu (`···`) provides **Delete receipt** — visible but separated from the primary Confirm action, so destructive choice is not placed next to the happy path.

**Row edit state:**

```text
┌──────────────────────────────┐
│ Edit item                    │
│                              │
│ [Image crop at this line]    │
│                              │
│ Name      [Organic spinach]  │
│ Quantity  [10] [oz] ▼        │
│ Price     [$3.49]            │
│ Not a food item [ ]          │
│                              │
│ [ Save ]  [ Remove ]         │
└──────────────────────────────┘
```

---

## Screen 4 — Confirmation Success

After confirm, the user is returned to the Timeline / Receipts view. The pending card becomes a confirmed entry; pantry and budget update behind the scenes.

```text
┌──────────────────────────────┐    ┌──────────────────────────────┐
│ Timeline                     │    │ ┌────────┬─────────┐         │
│                              │    │ │ List   │▸Receipts│         │
│ Today                        │    │ └────────┴─────────┘         │
│ ✓ Receipt confirmed · Costco │    │                              │
│   14 items added · $87.43    │    │ Costco · $87.43 · confirmed  │
│   [Undo · 30s]               │    │   14 items · Jul 9           │
│                              │    │   [Undo · 30s]             │
│ Dinner cooked · 6 deducted   │    │                              │
│                              │    │ ② Kroger · review 12 items  │
├──────────────────────────────┤    │                              │
│ Home  Plan  Shop  Cook  Hshld│    ├──────────────────────────────┤
└──────────────────────────────┘    │ Home  Plan ●Shop  Cook  Hshld│
                                    └──────────────────────────────┘
```

**Success mechanics:**

- The confirmation card shows on the Timeline and in the Receipts segment. An **Undo** action is available for ~30 seconds on both surfaces.
- Tapping Undo reverts the pantry additions and budget spend in a single action, returning the receipt to the review state with a "Confirmation undone" banner.
- From the review screen, the user can re-confirm or open the overflow menu (`···`) and choose **Delete receipt** to delete the receipt and return to the Receipts segment. This keeps the destructive action visible but separated from the primary Confirm button.
- After the window expires, the Undo action disappears. The user can still correct individual items later via the existing pantry correction path (PantryCorrection); the receipt itself remains in the confirmed history.
- This embodies the reversibility principle: no AI action is irreversible without human confirmation, and undo is treated as trust infrastructure, not polish.

---

## Screen 5 — Manual Quick-Entry (Fallback)

The fallback for PRD-001 Story 4: reached from a failed-extraction notification, from the "We couldn't read this receipt" Timeline card, or chosen directly by the user from the capture screen. It produces **the same receipt confirmation flow and the same events** as a scanned receipt — manual entry is a different door into Screen 3, not a different feature.

```text
┌──────────────────────────────┐
│ Enter receipt         [ ··· ]│  ← overflow: Delete receipt
│                              │
│ Store     [Costco        ] ▼ │  ← recent stores suggested
│ Date      [Jul 9         ]   │
│ Total     [$87.43        ]   │
│                              │
│ Items                        │
│ ┌─────────────────────────┐  │
│ │ Gallon milk · 1 · $4.29 │  │
│ └─────────────────────────┘  │
│ ┌─────────────────────────┐  │
│ │ [name] [qty] [$    ]    │  │  ← active entry row
│ └─────────────────────────┘  │
│ [ + Add item ]               │
│                              │
│ Items don’t need to match    │
│ the total — enter what       │
│ matters to your pantry.      │
│                              │
│ [ Review N items ]           │  ← leads to Screen 3
└──────────────────────────────┘
```

**Quick-entry mechanics:**

- Optimized for speed over completeness: store, date, and total first; items are added one row at a time with name/quantity/price. Partial entry is legal — the user records what matters to the pantry.
- No totals-reconciliation banner: there is no extraction to check. All rows are user-asserted, so every row renders settled.
- "Review N items" leads into Screen 3 (Review & Confirm) with the same primary action, undo window, and overflow Delete — confirmation emits the same `ReceiptItemsConfirmed` → `PantryItemsAddedFromReceipt`, `BudgetSpendRecorded` events (PRD-001 Story 4 AC).
- If reached after a failed scan, the failed capture's image remains attached for reference where available.
- Voice input is deferred to MVP-1 (PRD-001 Open Question 4).

---

## Empty States

### First-time Shop tab (Receipts segment)

```text
┌──────────────────────────────┐
│ ┌────────┬─────────┐         │
│ │ List   │▸Receipts│         │
│ └────────┴─────────┘         │
│                              │
│ [📷 Scan receipt]            │
│                              │
│   ┌──────────┐               │
│   │ receipt  │               │
│   │ icon     │               │
│   └──────────┘               │
│                              │
│   No receipts yet            │
│   Scan your first receipt to │
│   update your pantry.        │
│                              │
├──────────────────────────────┤
│ Home  Plan ●Shop  Cook  Hshld│
└──────────────────────────────┘
```

### First-time Home card

See Entry Points: Home surfaces "Scan your first receipt" as the primary suggestion when the pantry is empty or a new household is detected (Vision §21).

---

## Error States

| Failure | UI | User action |
|---|---|---|
| Image too poor at capture | Retake overlay with specific reason | Retake or "Use anyway" |
| Extraction service failed | Timeline card: "We couldn't read this receipt" | Retake or manual quick-entry |
| Extraction service slow | Pending card: "Taking longer than usual…" | Manual entry offered; retry automatic |
| Totals mismatch | Amber totals banner on review | Correct items or mark tax/deposit |
| Duplicate receipt | Inline alert: "This receipt was already added." | No pantry change; user can dismiss |
| Offline | "Waiting for connection…" on Timeline card | Queues automatically; resume on reconnect |

All error states preserve the ADR-010 rule: **no pantry or budget change without confirmation.**

---

## Loading States

There are no blocking spiners in the receipt flow. Latency is absorbed by the pending card / Timeline (UXDR-001). The only immediate feedback is the capture-quality check, which is a brief, non-blocking overlay.

---

## Screen Flow Summary

```text
[Shop / Home / Notification]
    │
    ▼
[Capture] ─── poor quality ───► [Retake prompt]
    │  (good capture, ≤15s)          │
    ▼                                └── extraction failed ──► [Manual quick-entry]
[Timeline pending card] ─── ready ───► [Notification]               │
    │                                    │                          │
    ▼                                    ▼                          │
[Review & confirm] ◄──────────────────────┘◄────────────────────────┘
    │
    ▼
[Confirmation] ───► [Timeline confirmed entry] + [Receipts segment] + pantry/budget updated
```

---

## Related

- `PRD-001` — this wireframe is the UX design for that PRD
- `UXDR-001` — async-proposal interaction pattern (pending → notify → review → confirm)
- `UXDR-002` — Shop tab segmented as `List | Receipts`
- `DOC-070` — app-shell wireframes and tab structure
- `Products/KitchenOS/10_Product_Vision.md` — Sections 19.3, 19.5, 21 (empty states)
