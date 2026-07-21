---
id: PRD-002
title: Cook Mode — Guided Cooking to Confirmed MealSession
type: prd
status: draft
owner: product
depends_on: [DOC-010, DOC-020, PDR-010, PDR-007, PDR-008, PDR-002, PDR-005, PDR-011, ADR-010, ADR-004, GDR-001]
referenced_by: []
tags: [prd, cook-mode, meal-session, pantry, habit-loop, mvp-0, hero-feature]
date: 2026
---

# PRD-002: Cook Mode — Guided Cooking to Confirmed MealSession

**PRD ID:** PRD-002
**Status:** Draft
**Owner:** Product (drafted via PM role, sponsored by @raj-duddu)
**Stage Gate:** Stage 3 of Product Development Lifecycle
**Created:** 2026-07-10
**Last Updated:** 2026-07-10

---

## Problem Statement

> Households abandon home cooking under time pressure and mental load — and when they do cook, nothing records what actually happened, so the pantry drifts and every downstream recommendation decays.

---

## Background / Discovery

Cook Mode is the designated hero feature and primary habit loop of MVP-0 (PDR-010). The strategy rests on a single mechanic: a completed `MealSession` is the only event that deducts pantry state from consumption (ADR-010, PDR-007) and the richest learning event in the system — confirmed participants, actual portions, leftovers, and recipe acceptance in one confirmed activity.

Cooking recurs daily; shopping and planning recur weekly. Anchoring the habit at the highest-frequency touchpoint is what builds retention, and it makes pantry accuracy a *side effect of getting value* rather than a data-entry chore: the deduction happens because the user cooked, not because they logged anything.

The interaction bar is high and specific. Real cooking is hands-busy, time-sensitive, and interruption-prone. A clunky hero feature poisons the whole thesis (PDR-010, Risk 45.3). Cook Mode must be usable with messy hands, survive interruptions, and never make the user feel they are "operating an app" while they cook.

This PRD covers the **Execution Layer** only. Recommendation and planning (the Planning and Intention layers of PDR-007 — `MealRecommendation`, `MealPlan`, `WeeklyMealPlan`) are separate features; Cook Mode consumes a chosen meal and drives it to a confirmed `MealSession`.

---

## Product Vision Alignment

Reference: `Products/KitchenOS/10_Product_Vision.md`, Sections 1–9, 39.4, 40.1.

- **Principle 2 (Turn Information into Guidance)** — a recipe is information; step-by-step, timed, full-screen guidance that ends in a finished meal is guidance.
- **Principle 3 (Inspire Confident Action)** — the loop ends in a completed, real-world action: a meal cooked and eaten, confirmed without anxiety.
- **Principle 4 (AI Recommends. People Decide.)** — pantry deduction is a consequence of the user confirming they cooked; nothing is deducted from intention or prediction.
- **Principle 9 (Simplicity Is a Feature)** — the app absorbs timers, step tracking, and pantry bookkeeping so the user only has to cook.

**North Star (Weekly Trusted Household Decisions Completed):** every completed `MealSession` is a trusted decision completed, and it is the confirmation that keeps the pantry accurate — raising the acceptance rate of every downstream recommendation.

---

## Scope

### In Scope

- Enter Cook Mode from a chosen meal (Home suggestion, a `MealPlan`, or a directly selected `Recipe`).
- Full-screen, step-by-step recipe presentation with large hands-free-friendly targets and screen-awake behaviour.
- Step navigation (next / previous / jump to step) with clear current-step emphasis.
- One or more per-step timers running concurrently, surviving navigation and app backgrounding, with completion alerts.
- Participants confirmation for the session (who is eating) — pre-filled from the plan/routine, editable (`MealSessionParticipantsConfirmed`).
- Completion flow: user confirms the meal was cooked → `MealSessionCompleted` → `PantryItemConsumed` deductions emitted by the MealSession aggregate (ADR-010, PDR-007).
- Leftovers capture at completion (`LeftoversCreated`, optional `LeftoversStoredToPantry`).
- Abandon / exit without completion: no pantry effect (`MealSessionAbandoned` / `CookModeSessionAbandoned`).
- Resume an interrupted, not-yet-completed session (in-progress state per the Household Activity Lifecycle).
- Household Timeline entry for the completed session (PDR-011).
- Offline operation: guided cooking and completion work with no connectivity; events queue via the Sync Engine and reconcile on reconnect.

### Out of Scope

- Recipe recommendation, ranking, and generation (the Planning Layer — separate PRD; MealRecommendation is ephemeral per PDR-007).
- Weekly planning and "Accept Week" (PDR-008 — WeeklyMealPlan).
- Allergy Guard warnings inside Cook Mode (MVP-1 — Vision §39.2; safety filtering applies upstream at recommendation time).
- Goal-aware / per-person portions and add-ons (Post-MVP — Vision §39.3).
- Nutrition dashboards, cooking-skill scoring, voice control (Post-MVP).
- Post-completion `MealSessionReversed` correction flow (MVP-1 trust layer — Vision §39.2, §40.3); MVP-0 covers `MealSessionPortionsCorrected` at completion only.
- Recipe authoring / import; expert recipes (Marketplace — Post-MVP).

### MVP Boundary

Pick a meal → cook it step by step with working timers → confirm it was cooked → pantry deducts and the Timeline records it. Everything else is enhancement.

---

## User Stories

### Story 1: Cook without operating an app

**As a** household member making dinner with busy hands
**I want to** follow the recipe step by step on a screen I barely have to touch
**So that** I can cook without losing my place or wiping my hands to tap tiny controls

**Acceptance Criteria:**
- [ ] Cook Mode is full-screen; the current step is dominant and readable at arm's length.
- [ ] The screen stays awake for the duration of the session.
- [ ] Advancing and going back use large targets; no critical action requires precise or small taps.
- [ ] Navigating between steps never loses running timers or entered session data.

### Story 2: Timers that survive real cooking

**As a** household member juggling multiple pots
**I want to** start timers from the steps and trust them
**So that** nothing burns while I handle the next step

**Acceptance Criteria:**
- [ ] A step with a duration exposes a one-tap timer; multiple timers can run at once.
- [ ] Timers keep running when I move between steps, background the app, or lock the phone.
- [ ] Timer completion produces a clear alert even if the app is backgrounded.
- [ ] Each running timer is labelled with the step it belongs to.

### Story 3: Finishing the meal updates the pantry automatically

**As a** household member who just finished cooking
**I want to** confirm the meal is done in one action
**So that** the pantry updates itself without me tracking ingredients

**Acceptance Criteria:**
- [ ] One primary action completes the session.
- [ ] On completion, `MealSessionCompleted` is recorded and the recipe's ingredients are deducted via `PantryItemConsumed` (emitted by the MealSession aggregate, never by the Cook Mode UI — ADR-010).
- [ ] Participants are confirmed as part of completion, pre-filled from the plan/routine and editable.
- [ ] The completion produces one grouped Household Timeline entry describing what was cooked and what changed.
- [ ] I can adjust portions actually made before confirming (`MealSessionPortionsCorrected`), and record leftovers (`LeftoversCreated`).

### Story 4: Interrupted and resumed

**As a** household member who got pulled away mid-cook
**I want to** come back to exactly where I was
**So that** an interruption doesn't cost me my place or my timers

**Acceptance Criteria:**
- [ ] Leaving Cook Mode without completing keeps the session in progress; no pantry, no Timeline-completion effect.
- [ ] Returning restores the current step and any still-valid running timers.
- [ ] Explicitly abandoning the session records `MealSessionAbandoned` / `CookModeSessionAbandoned` and produces no pantry change.

### Story 5: Cooking offline

**As a** household member cooking in a kitchen with poor signal
**I want to** use Cook Mode and finish the meal offline
**So that** connectivity never blocks getting dinner done

**Acceptance Criteria:**
- [ ] Entering, navigating, timing, and completing a session all work with no connectivity.
- [ ] Completion events queue locally (Sync Engine) and reconcile on reconnect with no user action.
- [ ] The pantry reflects the deduction locally immediately; server state converges on sync.

---

## BDD Scenarios

### Scenario: Happy path — completing a session deducts the pantry

```gherkin
Given a household with the ingredients for "Chicken stir-fry" in the pantry
And the member has entered Cook Mode for that recipe
When the member advances through all steps
And confirms the participants
And completes the session
Then MealSessionCompleted is recorded
And PantryItemConsumed events deduct the recipe's ingredients from the pantry
And the Household Timeline shows one grouped entry for the cooked meal
```

### Scenario: Nothing is deducted until completion (ADR-010, PDR-007)

```gherkin
Given a member is midway through Cook Mode for a recipe
When they navigate between steps and start timers
But do not complete the session
Then no PantryItemConsumed event is emitted
And the pantry is unchanged
```

### Scenario: Abandoning a session has no pantry effect

```gherkin
Given a member is in Cook Mode for a recipe
When they exit and choose to abandon the session
Then MealSessionAbandoned is recorded
And no pantry, and no completion Timeline entry, is produced
```

### Scenario: Timer survives backgrounding

```gherkin
Given a member started a 10-minute timer on the "simmer" step
When they background the app for 10 minutes
Then the timer completes on schedule
And an alert fires even though the app is backgrounded
```

### Scenario: Resume an interrupted session

```gherkin
Given a member is on step 4 of 7 with a running timer
When they leave Cook Mode and return later
Then the session reopens on step 4
And the running timer reflects the elapsed time
```

### Scenario: Portions actually made differ from the plan

```gherkin
Given a recipe planned for 4 servings
When the member records that they made 6 before completing
Then MealSessionPortionsCorrected reflects the actual portions
And pantry deduction and leftovers are computed from the actual portions
```

### Scenario: Completing offline queues and reconciles

```gherkin
Given the member's device is offline
When they complete a MealSession in Cook Mode
Then the pantry deduction is applied locally immediately
And MealSessionCompleted and PantryItemConsumed events queue via the Sync Engine
When connectivity returns
Then the events sync and server state converges without user action
```

---

## UX Notes

The hands-free, interruption-tolerant Cook Mode interaction pattern is proposed as **UXDR-003** — full-screen guided execution with large targets, persistent timers, and screen-awake behaviour. It is expected to become the standard shape for any future guided, real-world "do it now" flow.

### Screen Flow

```text
[Home suggestion / MealPlan / Recipe]
    │  "Cook this"
    ▼
[Cook Mode — full screen, step 1]     ← screen stays awake; large targets
    │  step nav + timers (persist across nav/background)
    ▼
[Final step → "Finish meal"]
    │  confirm participants (pre-filled) + actual portions + leftovers
    ▼
[Completion]                          ← MealSessionCompleted → PantryItemConsumed
    │
    ▼
[Household Timeline grouped entry]     ← what was cooked, what changed
```

### Empty State

If no meal is chosen yet, Cook Mode is entered from a suggestion or recipe rather than shown empty. First-run Home surfaces "Cook something" as a primary suggestion (Vision §21 empty-state rules; onboarding path §50).

### Error State

Cook Mode must not fail because of connectivity — guidance and completion are local-first (offline scenario above). If pantry deduction cannot be computed (e.g. a recipe ingredient has no pantry match), completion still succeeds and the unmatched item is flagged for later pantry correction — cooking is never blocked by bookkeeping (Principle 9).

### Loading State

No blocking spinner during cooking. Recipe content is resident before the session starts; entering Cook Mode is instant.

---

## Technical Design

> Feature is non-trivial (new aggregate lifecycle UI, persistent background timers, offline-first completion, event emission): a full Solution Design is required at Stage 5 — planned as SD-002 in `Products/KitchenOS/45_Solution_Designs/`.

### Key Technical Decisions (already recorded)

- **PDR-007** — three-object meal lifecycle; Cook Mode operates the `MealSession` (Execution Layer) only. `MealRecommendation`/`MealPlan` are upstream.
- **ADR-010** — pantry is derived exclusively from confirmed activities; the completed `MealSession` is the confirmation, and `PantryItemConsumed` is the authoritative deduction event.
- **ADR-004** — event sourcing; the session's lifecycle is a stream (`MealSessionStarted → …Completed`), which is what makes resume, audit, and MVP-1 reversal tractable.
- **AI criticality classification: Low** — Cook Mode presents deterministic recipe content and records a user-confirmed real-world event. No AI output drives state; no autonomous or irreversible action. (Recommendation, which is AI-touching, is a separate feature.)

### Sequence (brief)

```text
[Meal chosen] → [MealSessionStarted]
  → [Cook Mode UI: steps + persistent timers]  (offline-capable)
  → [Participants + actual portions confirmed]
  → [MealSessionCompleted]
      → MealSession aggregate emits PantryItemConsumed (deductions)
      → LeftoversCreated (optional)
  → [Household Timeline grouped entry]
```

### New API Endpoints (summary)

| Method | Path | Purpose |
|---|---|---|
| POST | /meal-sessions | Start a session from a chosen meal/recipe |
| PATCH | /meal-sessions/{id} | Update in-progress session state (step, participants, portions) |
| POST | /meal-sessions/{id}/complete | Confirm completion; produce MealSessionCompleted + pantry events |
| POST | /meal-sessions/{id}/abandon | Abandon without pantry effect |

Full contract: Stage 5 Solution Design / `80_API_Reference/`.

---

## Domain Model Impact

- [ ] New entity: none — `MealSession`, `MealPlan`, `Recipe`, `PantryItem`, and the `Cook Mode` capability all exist in the Domain Model.
- [ ] New domain event: none expected — `MealSessionStarted`, `MealSessionParticipantsConfirmed`, `MealSessionCompleted`, `MealSessionAbandoned`, `MealSessionPortionsCorrected`, `LeftoversCreated`, `LeftoversStoredToPantry`, `PantryItemConsumed`, and `CookModeSessionAbandoned` all exist.
- [ ] New business invariant: none — the ADR-010 invariant (pantry from confirmed activities only) already governs; Cook Mode adds no exceptions.
- [x] Clarification only: transient Cook Mode UI session state (current step, running timers) lives in the `cook.*` context and is not domain state; only `MealSession` (`meal.*`) events are authoritative. If Stage 5 finds a need for an explicit `CookModeSessionStarted` telemetry event to pair with `CookModeSessionAbandoned`, update `Products/KitchenOS/20_Domain_Model.md` before Stage 7.

---

## Architecture Impact

- [x] New API endpoints (above).
- [x] Cook Mode + MealSession module implementation within the modular monolith (boundaries `cook.*` and `meal.*` already defined in 20_Domain_Model and 40_TA).
- [x] Client-side background timer and screen-awake handling; offline-first session with Sync Engine reconciliation.
- [ ] Database schema change: none beyond existing MealSession tables.
- [ ] New infrastructure component: none — local store, Sync Engine, and FCM (timer/alerts) are stack-standard.

Architecture Review at Stage 5 (offline-first correctness and event ordering are the review focus; not AI-touching, so the standard checklist applies rather than the AI Architecture Review checklist).

---

## Security and Privacy

- [ ] Touches user PII: minimal — session participants reference household members already known to the system; no new PII class.
- [ ] Touches household financial data: no.
- [ ] Requires new permissions or consent: notifications permission for timer alerts; no new data-consent class.
- [ ] Requires security review: no — no external processing path and no new sensitive data.

---

## Open Questions

| # | Question | Owner | Status |
|---|---|---|---|
| 1 | Does a `MealSession` require an upstream `MealPlan`, or can Cook Mode start directly from a `Recipe` in MVP-0 (ad-hoc cook)? | Product | Open — leaning "direct start allowed"; a `MealPlan` is created implicitly so the PDR-007 chain stays intact |
| 2 | How are recipe ingredients matched to `PantryItem`s for deduction when names differ (no deep normalization in MVP-0)? | Product + Architect | Open — MVP-0 deducts confident matches, flags unmatched for later pantry correction; deep normalization is MVP-1 (Vision §39.5) |
| 3 | Do partial completions (cooked, but not all steps followed) need a distinct state, or is completion binary in MVP-0? | Product | Open — leaning binary for MVP-0 |
| 4 | Timer alert delivery when the OS restricts background execution — local notifications vs. FCM vs. both? | Architect (Stage 5) | Open |
| 5 | Should `LeftoversStoredToPantry` create trackable pantry items in MVP-0, or is leftover capture display-only until MVP-1? | Product | Open |

---

## Definition of Done

- [ ] All acceptance criteria verified by QA.
- [ ] BDD scenarios pass, including the ADR-010 no-deduction-without-completion scenario and the offline completion scenario.
- [ ] Timer persistence verified across step navigation, app backgrounding, and device lock.
- [ ] Resume-after-interruption verified from a real in-progress session.
- [ ] Domain Model updated if changed (none expected).
- [ ] Architecture documentation updated if changed.
- [ ] Feature flagged for staged rollout.
- [ ] No critical bugs open.
