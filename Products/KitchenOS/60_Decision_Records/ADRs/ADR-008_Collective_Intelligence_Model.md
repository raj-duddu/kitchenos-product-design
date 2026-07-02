---
id: ADR-008
title: Collective Intelligence Model with Explicit Opt-In Consent
type: adr
status: accepted
owner: architecture
depends_on: [ADR-004, ADR-007]
referenced_by: []
tags: [ai-architecture, collective-intelligence, privacy, consent, anonymisation, strategic-moat, price-intelligence]
date: 2026
---

# ADR-008: Collective Intelligence Model with Explicit Opt-In Consent

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS wants to provide price intelligence, seasonal trend awareness, recipe success rates, and pantry depletion benchmarks that go beyond what any single household can learn from its own events. For example:

- "Chicken thighs are $2.10 cheaper at Costco this week compared to your usual store."
- "Most households in your region finish spinach within 4 days of purchase."
- "This recipe has a 91% completion rate for households with 2 adults."

These signals require data from many households, not just one. There are three ways to source this data:

1. **Grocery API partnerships** — integrate with Kroger, Walmart, Instacart APIs for current shelf prices.
2. **Third-party price data providers** — license regional price data from aggregators.
3. **Collective household observations** — derive signals from anonymised observations contributed by KitchenOS households.

Options 1 and 2 provide price data but not behavioural signals (recipe success, waste patterns, depletion rates). They also create external dependencies, licensing costs, and coverage gaps for stores without APIs. Neither compounds with product usage.

Option 3 creates a data asset that grows with every new household and every receipt scanned. It is the only approach that simultaneously solves price intelligence, behavioural intelligence, and long-term competitive moat. It requires a consent and anonymisation architecture to be trustworthy.

A key architectural question is whether item-level observations should be permitted. The conservative position ("no item-level data") would protect privacy but destroy most of the network value — price intelligence requires knowing what item costs how much at which store. The correct distinction is not item-level versus aggregate, but **identifiable versus non-identifiable**.

---

## Decision

**We will build a Collective Intelligence Model fed by anonymised, non-identifiable item-level observations contributed by explicitly opted-in households.**

Contribution is opt-in, never the default. The governing principle is: **collective intelligence is built through informed participation, never silent collection.**

---

## Reasons

**The data moat is the most defensible long-term competitive asset.**
A price comparison feature can be built in a sprint. A Collective Intelligence Model trained on years of regional household behaviour cannot be replicated by a competitor who does not have the data. This is the same compounding advantage that makes Google Maps, Waze, and Spotify recommendations defensible.

**Item-level observations are required for price intelligence.**
To learn that "organic whole milk costs $3.99 at Costco in Austin in July 2026," the system must record item, store, region, price, and month. Restricting to aggregate-only data loses the signal needed for per-item price intelligence. The privacy concern is correctly addressed by removing household identity, not by removing item detail.

**Grocery API partnerships are supplementary, not foundational.**
APIs have regional coverage gaps, licensing costs, and shelf-price accuracy limitations. They should supplement collective data where available, not replace it. Collective observations cover any store where a household shops and scans a receipt — far broader than any API partnership portfolio.

**Behavioural signals are not available from any external source.**
Recipe success rates, pantry depletion patterns, food waste reasons, and recommendation acceptance rates are KitchenOS-native signals. No external data provider can supply them. They are only available through collective household observations.

**Explicit opt-in aligns with company principles.**
The product principle "Trust is earned through transparency" requires that users understand what the system is doing with their data. Silent collection — even of anonymised data — violates this principle. Explicit opt-in, with visible controls and opt-out, reinforces trust and differentiates KitchenOS from data-harvesting competitors.

**The pattern applies to all future Amanaska products.**
Collective Intelligence alongside Personal Intelligence is a company-level architectural pattern. Establishing it correctly in KitchenOS defines how Amanaska Health, Finance, and Learning will handle collective learning.

---

## Consent Model

| Rule | Detail |
|---|---|
| Default | All household data is private. No contribution to the Collective Intelligence Model without explicit opt-in. |
| Opt-in timing | Presented after the first meaningful household action (e.g. first receipt scanned). Never during onboarding. |
| Framing | "Help improve recommendations for everyone — including yours." |
| What is contributed | Anonymised, non-identifiable observations only. |
| What is never contributed | Household ID, user ID, names, emails, device identifiers, timestamps precise enough to identify a household. |
| Governing distinction | Identifiable versus non-identifiable. Item-level observations are permitted when stripped of all identifying context. |
| Opt-out | Any time. Stops future contributions immediately. Schedules removal of prior contributions from the learning pipeline. |
| Transparency | Users can see which observation categories they are contributing to. |

---

## Anonymised Observation Examples

```text
PriceObservation
  item_category:  Organic Whole Milk
  store_chain:    Costco
  region:         Austin Metro
  price_usd:      3.99
  month:          2026-07
```

```text
RecipeObservation
  recipe_id:        chicken-stir-fry
  outcome:          accepted
  actual_cook_time: 22
  household_type:   2 adults
  region:           Texas
```

No `household_id`. No `user_id`. No exact date. No quantity. Nothing that identifies a person or household.

---

## Alternatives Considered

### Option A: Grocery API partnerships only

Integrate with Kroger, Walmart, Instacart, and similar APIs to source shelf prices.

Rejected as primary strategy because:
- Coverage is limited to stores with developer APIs; independent and regional chains are excluded.
- Does not provide behavioural signals (recipe success, waste, depletion rates).
- Creates external dependencies and potential licensing costs.
- Does not compound with product usage — the data asset does not grow as more households join.

Retained as a supplementary option post-MVP where APIs are available and accurate.

### Option B: Third-party price data licensing

License regional price data from aggregators such as Datasembly or Basket.

Rejected as primary strategy for the same reasons as Option A, plus ongoing data licensing costs. Does not provide behavioural signals.

### Option C: Aggregate-only observations (no item-level data)

Contribute only aggregate signals — total weekly spend, number of trips — without item-level detail.

Rejected because item-level observations are required for price intelligence. Aggregate-only data cannot tell the system that a specific product costs a specific amount at a specific store. The privacy concern is correctly addressed by removing household identity, not item detail.

### Option D: Default opt-in (opt-out available)

Collect observations from all households by default with an opt-out mechanism.

Rejected because it violates the product principle "Trust is earned through transparency." Silent collection of household data — even anonymised — conflicts with the founding principle that the platform earns trust through visible, understandable behaviour. Explicit opt-in is the correct stance even if it reduces initial participation rates.

---

## Consequences

### Positive

- Creates a compounding data asset that grows with every household and every receipt scan.
- Enables price intelligence, regional trend signals, and behavioural benchmarks unavailable from any external source.
- Establishes the company-level pattern for Personal + Collective Intelligence across all Amanaska products.
- Aligns with "Trust is earned through transparency" — users understand and consent to participation.
- Reduces external API dependency for core intelligence.

### Negative

- Collective Intelligence Model provides no value in MVP-0 — it requires a meaningful user base before signals are useful.
- Opt-in rates may be lower than opt-out rates; early collective model coverage will be limited.
- Requires a dedicated anonymisation pipeline, Collective Intelligence Store, and Learning Engine — infrastructure that does not exist in MVP-0.
- Opt-out deletion pipeline adds operational complexity.

### Risks

- **Re-identification risk:** Even anonymised item-level observations could theoretically be re-identified if granularity is too fine (e.g. exact purchase timestamp + rare item + small region). Mitigation: timestamps are truncated to month/year, regions are generalised to metro area, item categories are normalised, and k-anonymity thresholds are applied before any observation is written to the collective store.
- **Low opt-in rate:** If few users opt in, the collective model provides limited value in early phases. Mitigation: demonstrate value clearly at opt-in prompt ("Help us tell you where chicken is cheapest this week in Austin").
- **Boundary enforcement:** Engineers building features may be tempted to write household-identifiable data into the collective store for convenience. Mitigation: Collective Intelligence Store must be a separate database with no foreign key relationships to the operational database.

---

## MVP Scope

| Phase | Collective Intelligence Scope |
|---|---|
| MVP-0 | Not active. No observations collected. Recommendation Engine uses Household Intelligence Model only. |
| MVP-1 | Consent UI built. Anonymisation pipeline live. Price and recipe observations collected. Collective model used to bootstrap new households with thin personal history. |
| Post-MVP | Full Learning Engine. Seasonal models. Regional price forecasting. Recipe and waste models. Recommendation Engine uses full two-model input. |

---

## Related

- ADR-004: Domain-Driven Event Sourcing (domain events are the raw input to the anonymisation pipeline)
- ADR-007: Household Intelligence Model (the per-household counterpart to this collective model)
- `Knowledge/10_Product_Vision.md`, Section 54A: Collective Intelligence and Strategic Moat (product explanation)
- `Knowledge/40_Technical_Architecture.md`, Section 36A: Collective Intelligence Architecture (architectural specification)
