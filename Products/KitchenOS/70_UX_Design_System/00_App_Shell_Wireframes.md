---
id: DOC-070
title: App Shell Wireframes
type: ux-design
status: active
owner: product
depends_on: [DOC-010, UXDR-001, UXDR-002]
referenced_by: []
tags: [ux, wireframes, app-shell, navigation, tabs, information-architecture]
date: 2026
---

# App Shell Wireframes

> This document is a **rendering, not an authority**. The navigation model is decided in `Products/KitchenOS/10_Product_Vision.md` Section 18.3; screen responsibilities in Section 19; the Shop segments in UXDR-002; the async-proposal pattern in UXDR-001. If a wireframe here disagrees with those sources, they win and this document is corrected. Low fidelity is deliberate: these exist to answer structural questions (tab count, order, placement, clarity) — visual design belongs to the design system, which remains post-MVP.

---

## The Shell

Five tabs, action-based (Vision Section 18.3):

```text
┌─────────────────────────────────────┐
│  Home │ Plan │ Shop │ Cook │ Household │
└─────────────────────────────────────┘
```

---

## Home — decision layer (Section 19.1)

Not a dashboard: a decision generator. Every card answers a Section 17 decision moment and deep-links into the tab that acts on it.

```text
┌──────────────────────────────┐
│ Good morning                 │
│                              │
│ ⚠ Milk low · 2 days left     │
│                              │
│ Suggested today              │
│ Palak dal · 97% available    │
│ [Start cooking]              │
│                              │
│ Shopping · 5 items · ~$24    │
│ Budget · $18 under average   │
│ Timeline · 3 changes  →      │
│                              │
│ [Cook] [Shop] [Plan week]    │
├──────────────────────────────┤
│ ●Home  Plan  Shop  Cook  Hshld│
└──────────────────────────────┘
```

The Timeline row is a digest pointer (PDR-003), not the Timeline itself — it deep-links to Household → Timeline.

## Plan — weekly intelligence (Section 19.2)

Planning is approving AI suggestions, not editing from scratch (PDR-008).

```text
┌──────────────────────────────┐
│ Mon Tue Wed Thu Fri Sat Sun  │
│                              │
│ [Generate week]              │
│                              │
│ Mon dinner · Palak dal  swap │
│ Tue dinner · Fried rice swap │
│ Wed dinner · — takeout night │
│                              │
│ Accept week → shopping list  │
│ auto-generated               │
├──────────────────────────────┤
│ Home ●Plan  Shop  Cook  Hshld│
└──────────────────────────────┘
```

## Shop — execution, segmented (Section 19.3 + UXDR-002)

Two views of one mission: List (intention) and Receipts (evidence of the completed ShoppingTrip). Scan stays prominent in both segments.

```text
┌──────────────────────────────┐    ┌──────────────────────────────┐
│ ┌────────┬─────────┐         │    │ ┌────────┬─────────┐         │
│ │ ▸List  │ Receipts│         │    │ │ List   │▸Receipts│         │
│ └────────┴─────────┘         │    │ └────────┴─────────┘         │
│ [📷 Scan receipt]            │    │ [📷 Scan receipt]            │
│                              │    │                              │
│ Produce · 3 items            │    │ ◔ Reading your receipt…      │
│ Dairy · 2 items              │    │   pending · you'll be        │
│ Estimated cost · ~$24        │    │   notified                   │
│                              │    │ ② Costco · review 14 items   │
│ [Start shopping trip]        │    │ Kroger · $32.10 · confirmed  │
│                              │    │ Costco · $87.43 · confirmed  │
├──────────────────────────────┤    ├──────────────────────────────┤
│ Home  Plan ●Shop  Cook  Hshld│    │ Home  Plan ●Shop  Cook  Hshld│
└──────────────────────────────┘    └──────────────────────────────┘
```

Pending-receipt review normally arrives via notification deep-link (UXDR-001); the Receipts segment is where receipts are found, not the only door.

## Cook — execution mode, the hero (Section 19.4, PDR-010)

Usually entered from Home's suggestion; visited directly, it answers "what's tonight?"

```text
┌──────────────────────────────┐
│ Tonight · Palak dal · serves 4│
│                              │
│ [Start cooking]              │
│                              │
│ Step 1 of 6 · rinse spinach  │
│ timer · 10 min               │
│                              │
│ Finish → ingredients deducted│
│ (MealSession completion —    │
│  the only pantry deduction)  │
├──────────────────────────────┤
│ Home  Plan  Shop ●Cook  Hshld│
└──────────────────────────────┘
```

## Household — system layer (Section 19.5)

Trust and correction. Timeline first; complexity only for those who seek it. Receipts moved to Shop (UXDR-002).

```text
┌──────────────────────────────┐
│ Timeline                     │
│  Receipt confirmed · Costco  │
│  Dinner cooked · 6 deducted  │
│  Milk removed by Priya       │
│  … (scroll: full history —   │
│   the event stream is        │
│   append-only; nothing is    │
│   ever lost)                 │
│                              │
│ Pantry · search, expiry      │
│ Analytics · Family           │
│ Settings · Integrations      │
├──────────────────────────────┤
│ Home  Plan  Shop  Cook ●Hshld│
└──────────────────────────────┘
```

---

## Journey Traces

**Receipt scan (PRD-001, UXDR-001):** Shop → scan → Timeline pending card → notification → review (uncertain rows highlighted, image in-app) → confirm → Home reflects pantry and budget.

**Cook dinner (PDR-010):** Home suggestion → Start cooking → Cook Mode steps → finish → pantry deducted → Timeline records it.

Both journeys cross tabs by design; notifications and Home cards are the actual navigation, not tab-hopping.

---

## Open Structural Items (being watched, not decided)

- **Pantry visibility** — Medium frequency, two taps deep in Household. Held as-is on the bet that Home surfacing ("milk low") makes pantry visits rare. Vision Section 60 open question; revisit with usage data.
- **Cook: tab or mode?** — Entered mostly from Home. Keeps its tab on PDR-010's hero argument; if direct visits feel empty in testing, revisit as a UXDR.
- **Timeline browsing depth** — full history exists by construction; filters, per-entity history, and period navigation are Timeline/Corrections PRD material (MVP-1 trust layer).

---

## Related

- `Products/KitchenOS/10_Product_Vision.md` — Sections 16–23 (the decisions these render)
- UXDR-001, UXDR-002 — interaction and navigation records
- PDR-003, PDR-010, PDR-011 — home screen, hero feature, timeline decisions
- PRD-001 — receipt scanning feature specification
