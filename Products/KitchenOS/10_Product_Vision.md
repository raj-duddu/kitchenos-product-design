---
id: DOC-010
title: KitchenOS Product Vision
type: product-vision
status: active
owner: product
depends_on: []
referenced_by: [DOC-020, DOC-040, DOC-050]
tags: [product-vision, ux, features, mvp, marketplace, household, personas, onboarding, growth]
date: 2026
---

# KitchenOS: Product Vision

> This document is the authoritative source for what KitchenOS is, why it exists, how it looks to users, and the phased plan to build it. Technical implementation decisions live in `40_Technical_Architecture.md`. Engineering practices live in `50_Engineering_Handbook.md`. Architectural decisions live in `60_Decision_Records/ADRs/`.

---

# KitchenOS 2.0: Product Vision, UX, Architecture, and MVP Blueprint

**Document version:** 0.1.0 cleaned Markdown rewrite  
**Source document:** `older version of kitchen OS product vision`  
**Original source version:** 0.1 living document  
**Status:** Cleaned and consolidated product strategy draft  
**Primary audience:** Founder, product, design, engineering, AI, and launch teams  

---

## 1. Purpose of This Rewrite

This document rewrites the older KitchenOS product vision into a readable Markdown blueprint. It preserves the original strategic direction while removing conversational artifacts, duplicate transitions, and loosely formatted sections.

The older document is valuable because it is more product-focused and execution-focused than the later LifeOS blueprint. It clearly defines:

- The standalone KitchenOS vision.
- The household lifecycle loop.
- The five-tab action-based information architecture.
- The Household Decision Engine concept.
- The UX screen system.
- The event-driven backend model.
- The Flutter-first technology recommendation.
- The 8–12 week MVP execution plan.
- The differentiation and market positioning strategy.

---

## 2. Relationship to LifeOS

This document treats **KitchenOS** as the original standalone product vision.

A later product direction may position **LifeOS** as the broader household operating system and **KitchenOS** as the first domain inside it. In that structure:

- **LifeOS** = broader household intelligence platform.
- **KitchenOS** = food, pantry, shopping, cooking, budget, and meal intelligence module.

For this older product vision, KitchenOS is described as the complete product.

---

## 3. Executive Summary

KitchenOS is an AI-powered household food operating system that helps families answer one simple question:

> What should we do next?

The external positioning is **AI-powered household food operating system**. The product category is **household food intelligence platform**. The internal intelligence layer is the **Household Decision Engine**. The memory and trust layer is the **Household Timeline**.

Unlike grocery list apps, pantry trackers, recipe apps, budget tools, calorie trackers, or generic wellness marketplaces, KitchenOS connects the complete household food lifecycle with safety, personal goals, and optional expert guidance.

It understands:

- What has been purchased.
- What is currently available.
- What is consumed.
- What is planned.
- What should be purchased next.
- How much is being spent.
- Which recipes best use available ingredients.
- Which allergies and dietary constraints must be respected.
- Which individual nutrition goals should influence meals, portions, and shopping.
- When expert guidance from nutritionists or fitness coaches can improve a user's plan.

The objective is to reduce household effort, food waste, unnecessary spending, unsafe recommendations, and daily decision fatigue while helping households make healthier food decisions.

KitchenOS should not ask users to manage disconnected lists or interpret raw health data alone. It should maintain a living household model, proactively guide food decisions, respect safety constraints, support individual goals, and connect users with experts only when useful.

---

## 4. Problem Statement

Today, families manage food through disconnected tools.

```text
Recipe App
  -> Shopping List App
  -> Grocery Store
  -> Receipt
  -> Pantry
  -> Budget App
```

Every transition loses information.

Common problems:

- Users repeatedly enter the same data.
- Pantry state becomes inaccurate quickly.
- Receipts are ignored after purchase.
- Shopping lists do not know what is already at home.
- Meal planning does not know actual pantry state.
- Budget tools do not understand food behavior.
- No single system connects planning, shopping, cooking, and learning.

KitchenOS solves this by turning household food management into one connected intelligence loop.

---

## 5. Product Vision

KitchenOS becomes the household food intelligence layer that connects pantry, shopping, cooking, Household Timeline, nutrition goals, dietary safety, corrections, and optional expert support into one closed-loop experience.

```text
KitchenOS Household Food Loop
  |
  +-- Acquire Food
  |     +-- Shopping
  |     +-- Receipt Scan
  |
  +-- Understand Household
  |     +-- Pantry
  |     +-- Consumption
  |     +-- Household Timeline and Event History
  |
  +-- Decide
  |     +-- Meal Planning
  |     +-- Recipes
  |     +-- Budget
  |     +-- Individual Goals
  |     +-- Allergies and Dietary Safety
  |     +-- Expert Guidance
  |
  +-- Act
  |     +-- Shop
  |     +-- Cook
  |     +-- Notify
  |
  +-- Learn
        +-- Corrections
        +-- Preferences
        +-- Reversals
        +-- Expert Feedback

Household Decision Engine
  |
  +-- Reads household state and Household Timeline
  +-- Applies safety, goals, budget, preferences, and expert context
  +-- Recommends what to buy, cook, adjust, or avoid
  +-- Explains why each action matters
  +-- Supports approval, correction, reversal, and learning
```

KitchenOS owns food decisions. Nutrition goals and expert coaching improve those food decisions. Fitness coaching is connected where it supports food, goals, and household wellness, without turning KitchenOS into a full workout-tracking platform.

The Household Timeline should be treated as a first-class product concept, not a secondary history screen. It is the event memory of the household: what was bought, consumed, cooked, expired, corrected, recommended, accepted, rejected, or reversed.

The user should no longer manage data directly as the primary behavior.

The user should:

- See safe, goal-aware recommendations.
- Understand the reason.
- Approve or reject actions.
- Work self-guided by default.
- Add expert guidance when useful.
- Use the Household Timeline to understand what changed, why it changed, and how to reverse it.
- Undo or correct wrong actions.
- Trust the system more over time.

---

## 6. Mission Statement

> Help every household make safer, healthier, and easier food decisions with less effort.

---

## 7. Product Philosophy

KitchenOS should behave like an experienced household member, not spreadsheet software.

Instead of saying:

> Pantry contains 214 items.

KitchenOS should say:

> You are running low on milk.

Instead of saying:

> Budget is 62% used.

KitchenOS should say:

> You are on track to stay $47 under budget this month.

The product philosophy is:

> Information should always become guidance.

---

## 8. Core Product Principles

### 8.1 AI Recommends, Users Decide

KitchenOS should not silently perform important actions.

Good:

> Add yogurt to this week's shopping list?

Bad:

> Yogurt added automatically.

### 8.2 Never Ask for Information Twice

A single receipt scan should update:

- Pantry.
- Budget.
- Shopping.
- Price history.
- Purchase history.

### 8.3 Every Screen Answers a Question

Each screen must have a clear user question.

| Screen | Question |
|---|---|
| Home | What should I do today? |
| Plan | What should we eat this week? |
| Shop | What do I need to buy? |
| Cook | How do I prepare this meal? |
| Pantry | What do I currently have? |
| Household Timeline | What changed, why did it happen, and can I reverse it? |
| Analytics | Where is my money going? |

### 8.4 AI Should Be Contextual

Avoid generic AI entry points like:

> Ask AI

Prefer contextual intelligence:

> You already have 93% of the ingredients.

Or:

> Bananas usually run out after 8 days.

### 8.5 Minimize User Effort

Every feature should reduce work, not create more work.

### 8.6 Decisions, Not Data

Users do not want to manage inventory. They want decisions:

- What should I cook?
- What do I need to buy?
- What is running low?
- What is expiring?
- Am I overspending?

### 8.7 Manual Entry Is a Fallback, Not the Intended Experience

Manual entry should exist as a fallback, not the core product behavior.

This matters because some food enters the household without receipts, barcode scans, or store records.

Examples:

- Vegetables from a family member.
- Farmers market purchases.
- Eggs from a neighbor.
- Leftovers from another meal.
- Food brought from a party or event.

The UX should make these entries quick and lightweight while still optimizing the product around automation.

### 8.8 The Kitchen Comes First

Every recommendation should improve at least one of these outcomes:

- Save time.
- Save money.
- Reduce waste.
- Improve meals.

### 8.9 Household Timeline Is the Product Memory

The Household Timeline is not just a history view. It is the user-facing event log of the household.

Examples:

- Milk purchased.
- Milk consumed.
- Eggs expired.
- Recipe cooked.
- Budget updated.
- Shopping generated.
- Nutrition goal improved.
- Expert recommendation accepted.

This gives KitchenOS two advantages:

- AI can learn from a sequence of actions, not only static pantry state.
- Users can understand, trust, and reverse changes when something is wrong.

### 8.10 Collect Only What Is Required to Improve the Experience

> **Collect only the information required to improve the user's experience.**

Not: collect everything because AI might use it later.

Data minimisation is an engineering principle, not just a compliance posture. Every field in the data model should have a clear answer to: what recommendation or decision does this enable? If there is no clear answer, the field should not exist.

Applied examples:

- Store age range (25–35), not exact birth date. Nutrition estimation does not need a birthday.
- Store role (Adult, Child), not name. Recommendations do not care who someone is called.
- Allow optional local nicknames for display — but store nothing that identifies a person internally.
- Allergies are stored because they affect safety. Height and weight are stored only if a nutrition goal requires them — and only on the member who set that goal.

### 8.11 Four Layers: Identity, Person, Domain, Intelligence

KitchenOS separates four distinct layers that are commonly conflated in simpler systems:

```text
Identity Layer     ← email, auth token, account recovery only
        ↓
Person Layer       ← stable domain facts: age group, allergies, goals, dietary restrictions
        ↓
Domain Layer       ← household, memberships, pantry, meals, shopping, receipts, budget
        ↓
Intelligence Layer ← AI-learned beliefs: cuisine affinity, habits, confidence scores
```

**Why this matters:**

- **Identity ≠ Person.** A Person is a business entity. An Identity is an auth mechanism. The same person can sign in via Google or Apple — the Identity changes, the Person does not.
- **Person ≠ Intelligence.** A Person's peanut allergy is a domain fact stated explicitly. A Person's 92% mushroom rejection rate is an AI-learned belief. They are fundamentally different kinds of knowledge. Domain facts are authoritative. Intelligence beliefs are probabilistic and replaceable.
- **Breach isolation.** A breach of the intelligence layer exposes no domain facts. A breach of the domain layer exposes no auth data. The layers cannot be cross-joined to re-identify a person.

The domain never depends on the intelligence layer. The intelligence layer depends on the domain. That dependency direction must never be reversed.

### 8.13 AI Should Predict the Routine and Ask Only About the Exceptions

> **AI should predict the routine and ask only about the exceptions.**

This is the operational expression of "AI recommends, people decide." The Household Intelligence Model builds enough confidence over time that asking becomes rare — not because we removed confirmation, but because the AI already knows the answer with high confidence.

**The three-layer cooking lifecycle:**

```text
MealRecommendation   ← AI output. Ephemeral. No commitment.
                        "Chicken pasta for 4 tonight — 25 min, uses pantry."

        ↓ user taps "Start Cooking"

MealPlan             ← Committed intention. Confirmed participants and portions.
                        "Cooking for everyone tonight? ✓ Yes  Edit"
                        One tap if the AI is right. Editable if not.

        ↓ cooking completes, user confirms

MealSession          ← Reality. Actual portions, actual participants, leftovers.
                        Pantry updated. Nutrition recorded. Household Timeline updated.
```

**Progressive disclosure rule:**
- Show the recommendation immediately — no questions upfront.
- Ask about participants only at "Start Cooking" — pre-filled from AI prediction.
- Ask about portions and leftovers only at completion — pre-filled from actual cooking.
- The AI fills in everything it can. The user corrects only what is wrong.

**Confidence-based questioning:**

| Confidence | Behaviour |
|---|---|
| ≥ 90% | Pre-fill silently. User can edit but is not prompted. |
| 70–89% | Pre-fill with soft prompt: "Is everyone eating tonight?" |
| < 70% | Ask explicitly before starting. |

As household patterns establish, most weekday evenings reach ≥ 90% confidence within 4–6 weeks of use. The product becomes progressively less demanding over time.

This principle directly supports the **meal planning in under 30 seconds** goal. The AI makes an informed assumption based on household patterns. The user only intervenes when tonight is different from the norm.

### 8.14 Weekly Meal Planning: Strategy, Not Seven Recipes

Most meal-planning apps generate seven recipes. KitchenOS generates a **weekly meal strategy** that adapts to the household as the week unfolds.

**Goal: weekly meal planning in under 2 minutes.**

```text
Sunday evening

KitchenOS proposes:

  Monday Dinner    🍝 Chicken Pasta         For 4 · 25 min · uses pantry
  Tuesday Dinner   🌮 Chicken Tacos         For 4 · 20 min
  Wednesday Dinner 🍛 Lentil Curry          For 4 · 35 min
  Thursday Dinner  🍲 Vegetable Soup        For 3 · 25 min (Adult 1 travels)
  Friday           🍕 Family Pizza Night    Takeout suggested

  [Accept Week]   [Edit]
```

One tap. Done. Every meal pre-filled with participants the AI already knows.

**The week unfolds as a living plan, not a static document:**

```text
Tuesday morning — KitchenOS notices:
  • Monday leftovers still available
  • Bananas expiring in 2 days
  • Calendar shows a late meeting Wednesday

Proactive suggestion:
  "Swap Wednesday's Lentil Curry with Thursday's Vegetable Soup?
   Uses expiring ingredients and fits your Wednesday schedule better."
  [Swap]  [Keep original]
```

**Each evening — lightweight execution:**

```text
6:10 PM notification:
  "Tonight: Chicken Pasta"
  Uses pantry · Ready in 25 min · For 4 people

  [Start Cooking]  [Swap Meal]  [Skip Tonight]
```

**The closed loop:**

```text
Weekly Plan accepted
        ↓
Each evening: meal reminder shown
        ↓
User taps "Start Cooking" → MealSession created, participants confirmed
        ↓
Cooking completes, user confirms
        ↓
Pantry updated · Nutrition recorded · Leftovers tracked
        ↓
Learning Engine updates Household Intelligence Model
        ↓
Next week's plan is more accurate
```

**What makes this different:**
- The plan is accepted once, not rebuilt nightly.
- The AI assumes the household routine and asks only about exceptions.
- Swaps are AI-suggested, not user-initiated.
- The pantry and schedule inform every swap suggestion.
- The loop closes: each completed meal improves the next week.

### 8.12 Multiple Households, One Experience

KitchenOS supports users who manage more than one household — a family home and a parents' home, a primary residence and a vacation property. This is handled without adding complexity to the primary experience.

**The rule:**

- **One household:** No switcher is ever shown. The app feels like "my kitchen."
- **Two or more households:** A lightweight household switcher appears in the header — like switching workspaces in Slack.

```text
🏠 Home ▼

  ✓ Home
    Parents
    Vacation Home
```

Switching household is an application-level action. It changes which household all subsequent actions are directed to. It does not modify any domain data. It does not require re-authentication.

**Notifications for multi-household users** must include the household name to avoid confusion:

> "Home: Your spinach expires tomorrow."
> "Parents: Milk is running low."

**Important distinction:** "Active Household" is a session concept, not a business concept. It exists while the user is using the app. It does not persist when the app is closed. The domain model — Household, HouseholdMembership, Pantry, Events — exists regardless of whether anyone is logged in. The application layer resolves the active household at login and holds it in session context. See `Products/KitchenOS/40_Technical_Architecture.md`, Section 23A.

---

## 9. Long-Term Vision

Today, KitchenOS starts with food.

The long-term vision is to become the household food, nutrition, and wellness decision layer while keeping food as the core wedge.

Near-term expansion areas:

- Allergy-safe meal planning.
- Individual nutrition goals.
- Goal-aware shopping and Cook Mode.
- Nutrition coaching.
- Fitness coaching where it affects food, goals, and household wellness.
- Expert marketplace for individuals and organizations.
- Family meal coordination.
- Smart refrigerator integration.
- Voice assistant.

Later household operating system expansion areas:

- Cleaning supplies.
- Pet food.
- Household inventory.
- Appliance maintenance.
- Family calendar integration.
  - ability to get reminders about expiring items before vacation
  - what kind of food choices to make on a road trip
  - location based suggestions for nearby food options

The architecture should support these future modules without redesigning the core system, but the product boundary should remain clear:

> KitchenOS owns household food decisions first. Broader wellness and expert features should strengthen those food decisions, not replace the core product with a generic fitness, medical, or coaching platform.

### 9A. The Amanaska Platform Architecture

KitchenOS is the first product in a larger platform. The architectural decisions made here define the patterns all future Amanaska products will follow.

The layered stack discovered through KitchenOS design is not KitchenOS-specific:

```text
Identity Layer       ← how you sign in (auth only)
        ↓
People Layer         ← who you are (Person, global facts)
        ↓
Relationship Layer   ← how you connect to groups (HouseholdMembership, teams, families)
        ↓
Domain Layer         ← what happens (events, activities, transactions, entities)
        ↓
Event Layer          ← immutable record of everything that occurred
        ↓
Intelligence Layer   ← what the system has learned (beliefs, patterns, confidence scores)
        ↓
Decision Layer       ← recommendations, guidance, safe suggestions
        ↓
Experience Layer     ← the product surface the person interacts with
```

This stack is product-agnostic. It could power:

- **HealthOS** — Person + health events + health intelligence + care decisions
- **FinanceOS** — Person + financial events + spending intelligence + budget decisions
- **LearningOS** — Person + learning events + skill intelligence + curriculum decisions

The key architectural principles that travel across all Amanaska products:

- Identity is always isolated from domain and intelligence.
- Person is always a domain concept, not an auth or AI concept.
- Facts belong to the domain. Beliefs belong to the intelligence layer.
- The domain never depends on the intelligence layer.
- Pantry state (and equivalents in other products) is always derived from confirmed real-world activities, never from predictions.
- Collective intelligence is always opt-in, never silent collection.

KitchenOS establishes these principles in concrete form. Every future Amanaska product inherits them.

---

## 10. Success Metrics

### 10.1 North Star Metric

**Weekly Trusted Household Decisions Completed**

A trusted household decision is an AI-assisted recommendation that is accepted by the user and followed by a meaningful household action.

This avoids measuring raw prompt volume or low-value suggestions. KitchenOS should not win by generating more recommendations. It should win by helping households make better decisions that they trust enough to act on.

Examples:

- Accepting a meal recommendation and cooking or scheduling it.
- Accepting a shopping suggestion and adding, buying, or confirming the item.
- Confirming a pantry update that improves household accuracy.
- Starting and completing a recommended recipe.
- Accepting a safety-aware or goal-aware substitution.
- Approving an expert-supported recommendation after reviewing the context.

This metric measures whether KitchenOS is genuinely influencing household behavior, not just creating prompts.

A recommendation should count only when it is:

- Relevant to the household context.
- Accepted or approved by the user.
- Followed by a meaningful action.
- Not immediately undone, corrected, or rejected as wrong.

### 10.2 Secondary Metrics

| Metric | Target |
|---|---:|
| Pantry accuracy | 95% |
| Meal planning time | Less than 2 minutes |
| Shopping list creation | Less than 30 seconds |
| Food waste reduction | 30% reduction |
| Budget forecast accuracy | 90% |
| Daily active usage | Becomes part of daily routine |

Each metric should define:

- Measurement window.
- Event source.
- Numerator.
- Denominator.
- Exclusion rules.
- Minimum sample size.

Example: pantry accuracy should be measured on recently verified items, corrected items, receipt-derived items, and Cook Mode deductions rather than every stale item ever added.

---

## 11. Competitive Positioning

| Product Category | Primary Focus | KitchenOS Difference |
|---|---|---|
| AnyList and grocery list apps | Shopping lists | KitchenOS connects shopping to pantry, recipes, cooking, and learning. |
| Paprika and recipe apps | Recipes | KitchenOS knows what is available and what should be cooked now. |
| YNAB and budget apps | Budget | KitchenOS understands item-level household food behavior. |
| Samsung Food and meal planning apps | Meal planning | KitchenOS closes the loop through pantry, shopping, cooking, and receipts. |
| Pantry apps | Inventory | KitchenOS minimizes manual tracking through automation and event learning. |

KitchenOS does not win by having more features. It wins by connecting the household food lifecycle into one intelligent system.

---

## 12. Household Intelligence Profiles

KitchenOS is not a static app with the same behaviour for everyone. The Household Decision Engine adapts to each household's context, goals, constraints, and habits. These profiles define not just who the users are, but **how KitchenOS must reason differently for each type of household**.

Each profile answers five questions:

1. **Primary Goal** — What are they trying to achieve?
2. **Daily Friction** — What repeatedly gets in their way?
3. **KitchenOS Must Understand** — What intelligence and context is required?
4. **KitchenOS Behaviors** — What should the AI proactively do for this household?
5. **Success Looks Like** — How does life measurably improve?

---

### 12.1 Busy Family

**Age range:** 35–50  
**Household:** Parents with children  
**Priority:** Highest — largest household size, highest decision complexity, highest data richness

#### Primary Goal

Spend less time managing food so more time is available for the family. Reduce the mental load of weekly meal planning, grocery trips, and budget tracking without sacrificing healthy meals.

#### Daily Friction

- Forgetting what is already at home leads to duplicate purchases.
- Kids change their minds, making meal plans obsolete before the week starts.
- Weekly meal planning takes 20–30 minutes and still produces suboptimal results.
- Grocery budget is unpredictable across multiple store trips.
- Multiple family members with different preferences, ages, and sometimes allergies must all be accommodated.

#### KitchenOS Must Understand

- Full household member roster including children.
- Per-member allergies, intolerances, and dietary preferences.
- Weekly cooking schedule and who is home each night.
- Current pantry state across all categories.
- Historical shopping frequency and store preferences.
- Budget envelope and spending pace.
- Which meals the family actually completed versus abandoned.

#### KitchenOS Behaviors

KitchenOS should prioritize automation and approval over manual entry.

> Your pantry is low on 6 staples. Based on this week's plan, you will likely need to shop by Thursday. Estimated cost: $52 at Costco.

> Kids meal night is Tuesday. Here are three meals the whole family has eaten before — all allergy-safe, ready in under 30 minutes.

> Priya has a peanut allergy. This recipe contains peanuts and has been removed from the suggestion list.

> You planned 5 meals this week but only cooked 3. Two portions of chicken are expiring tomorrow. One 15-minute meal can use both.

KitchenOS should generate a full weekly meal plan and shopping list that the family approves rather than builds from scratch.

#### Success Looks Like

- Weekly meal planning takes less than 5 minutes.
- Duplicate grocery purchases drop by more than 50%.
- Budget forecast accuracy is within 10% of actual spend.
- No allergy-unsafe meal is ever suggested.
- Family returns to the app every week as a household habit.

---

### 12.2 Working Professional

**Age range:** 22–35  
**Household:** Lives alone or with a partner  

#### Primary Goal

Eat home-cooked meals more often without spending time planning, shopping, or deciding what to cook. Reduce takeout frequency and food waste.

#### Daily Friction

- Food expires unused because consumption is irregular and unpredictable.
- Shopping requires too many micro-decisions: what do I need, which store, is it worth going, what's on sale.
- Not knowing what to cook is not a recipe problem — it is a recommendation problem that requires pantry, time, skill, and energy context.
- Takeout is the path of least resistance when decision fatigue sets in after a long workday.

#### KitchenOS Must Understand

- Pantry state and expiration patterns.
- Consumption habits and how quickly items get used.
- Available cooking time on different days.
- Preferred cuisines and cooking skill level.
- Grocery schedule and typical shopping day.
- Takeout patterns, including frequency, cost, and trigger context.
- Budget and weekly spend pace.
- Nutrition goals if set.

#### KitchenOS Behaviors

KitchenOS should prioritize speed and proactive guidance over manual interaction.

> You already have everything needed for a 15-minute dinner tonight.

> Your spinach expires tomorrow. Two meals can use it — here is the faster one.

> You worked late today. Here is a 12-minute dinner using what is already in your pantry.

> Ordering takeout tonight would put you over your weekly food budget. You can cook this in about the same time.

> You have not shopped in 8 days. Pantry confidence is dropping. Here are 3 meals you can still make, and a short shopping list for tomorrow.

KitchenOS should eliminate shopping micro-decisions by generating a ready-to-go list based on what is running low and what meals are planned.

#### Success Looks Like

- Eats home-cooked meals at least four nights a week.
- Takeout frequency drops by half.
- Less than 10 minutes per week spent on meal planning.
- Food waste drops noticeably within the first month.
- Never opens the app unsure of what to cook tonight.

---

### 12.3 Budget Household

#### Primary Goal

Reduce grocery spending without sacrificing healthy, satisfying meals. Understand where money is going and prevent overspending before it happens.

#### Daily Friction

- Budget is set but never tracked in real time — overspending is only discovered after the fact.
- No visibility into whether a shopping trip is better at one store vs another.
- Impulse purchases at the store are not connected to pantry or meal reality.
- Expensive items are repurchased unnecessarily when equivalent items are already at home.

#### KitchenOS Must Understand

- Household grocery budget and spend pace.
- Price history per item and per store.
- Shopping frequency and store preferences.
- Which items are purchased habitually versus occasionally.
- Pantry state — what is already available before generating a shopping list.
- Spending anomalies and pattern changes.
- Which meals deliver the best nutrition-to-cost ratio for this household.

#### KitchenOS Behaviors

KitchenOS should make the budget visible before it is exceeded, not after.

> Buying produce at Aldi and pantry items at Costco would likely save you about $18 this week.

> You have already spent $84 this week. Based on your plan, you are on track to finish $11 under budget.

> Chicken thighs are $2.10 less per kilogram at Costco this week compared to your usual store.

> You already have chickpeas, rice, and spinach. These 4 meals need no additional shopping and would cost you nothing this week.

> Unusual spend detected: grocery spend is 40% higher than your last four weeks. Three bulk purchases at Costco account for most of it.

#### Success Looks Like

- Monthly grocery spend drops by 15–25% within the first two months.
- Budget overruns become rare rather than routine.
- Shopping trips become more targeted and less impulsive.
- Household can see, in plain language, where food money goes each week.

---

### 12.4 Health-Focused Household

#### Primary Goal

Eat meals aligned with individual health and nutrition goals without turning every meal into a calorie-counting exercise. Make healthy eating the default, not a manual discipline.

#### Daily Friction

- Individual members have different goals — one wants muscle gain, another wants weight reduction — making shared meal planning difficult.
- Nutrition-aware cooking requires checking labels, calculating macros, and researching substitutions, which is too much effort daily.
- Healthy intentions break down under time pressure and decision fatigue.
- Allergy and dietary constraints interact with nutrition goals in complex ways that are hard to reason about manually.

#### KitchenOS Must Understand

- Individual nutrition goals per household member.
- Goal hierarchy: safety and medical constraints come before optimization.
- Which meals and ingredients align or conflict with each member's goals.
- Pantry state and which available ingredients support or undermine current goals.
- Cooking skill and time availability — healthy eating must remain practical.
- Progress signals: are goal-supporting meals actually being cooked?

#### KitchenOS Behaviors

KitchenOS should translate goals into concrete meal and shopping actions — not dashboards.

> Suggested: Paneer quinoa bowl. High protein, uses spinach and yogurt already in pantry. Supports Raj's muscle gain goal. Safe for all household members.

> Priya's weight reduction goal: this week's plan includes 4 high-satiety, lower-calorie dinners using ingredients already at home.

> Greek yogurt is running low. It is a key protein source for Raj's goal. Add to shopping list?

> Base meal tonight: chicken rice bowl. Raj: add extra chicken and yogurt side. Priya: reduce rice, add salad. Arjun: standard portion, mild sauce.

KitchenOS should resolve goal conflicts through shared base meals with individual modifiers rather than generating separate plans per person.

#### Success Looks Like

- Goal-aligned meals become the household default without requiring daily effort.
- No unsafe or goal-conflicting meal is ever suggested.
- Individual members see their goals reflected in what is actually cooked, not just planned.
- Household does not need a separate nutrition app to eat with intention.

---

### 12.5 Cooking Enthusiast

#### Primary Goal

Cook more ambitiously, discover new recipes, and use the full range of ingredients available at home. Make Cook Mode the richest part of the experience.

#### Daily Friction

- Finding recipes that match both skill level and exact pantry contents is time-consuming.
- Ingredient substitutions require external research when one item is missing.
- Ambitious meals require planning ahead — but the planning is scattered across recipe apps, notes, and memory.
- No single system connects ingredient availability, recipe selection, meal planning, and cooking execution.

#### KitchenOS Must Understand

- Cooking skill level and preferred cuisines.
- Pantry state at ingredient level — what is available, in what quantity, and when it expires.
- Cooking history — which recipes have been completed, modified, or abandoned.
- Ingredient substitution knowledge for common missing items.
- Time available for cooking on different days.
- Interest in new ingredients and cuisine exploration.

#### KitchenOS Behaviors

KitchenOS should act as a knowledgeable cooking companion, not just a step-by-step executor.

> You have 94% of the ingredients for Chicken Tikka Masala. The only missing item is heavy cream — Greek yogurt works as a substitute.

> You have not cooked Italian this month. Based on your pantry, here are 3 Italian recipes you can make tonight.

> Your saffron has been in the pantry for 9 months and expires soon. Here are two recipes that would use it well.

> Cook Mode is ready. Tonight: Palak Dal. Estimated time: 28 minutes. Steps adjusted for 4 servings.

This household spends the most time inside Cook Mode. The product should reward depth — better suggestions, richer substitution guidance, and a growing recipe history that reflects what the household actually enjoys cooking.

#### Success Looks Like

- Cooks more varied, ambitious meals without external recipe research.
- Uses pantry ingredients more fully and creatively.
- Cook Mode becomes the primary cooking companion, replacing recipe apps.
- Household builds a personal recipe history that gets better over time.

---

## 13. Jobs To Be Done

### 13.1 Job 1: I Need Dinner

Current flow:

```text
Google
  -> Recipe
  -> Pantry
  -> Shopping
  -> Cook
```

KitchenOS flow:

```text
Open App
  -> Recommended Dinner
  -> Start Cooking
```

Goal:

> User gets to a dinner decision in less than 20 seconds.

### 13.2 Job 2: I Am Going Shopping

Current flow:

```text
Open List
  -> Remember Pantry
  -> Estimate Budget
  -> Shop
```

KitchenOS flow:

```text
Shopping Ready
  -> Best Store
  -> Estimated Cost
  -> Buy
```

### 13.3 Job 3: I Just Got Home

Current flow:

```text
Paper Receipt
  -> Forget
  -> Pantry Wrong
```

KitchenOS flow:

```text
Scan Receipt
  -> Pantry Updated
  -> Done
```

### 13.4 Job 4: What Can I Cook?

Current flow:

```text
Search
  -> Recipes
  -> Ingredients
  -> Pantry
```

KitchenOS flow:

```text
Open App
  -> Cook Recommendations
```

### 13.5 Job 5: My Budget Feels High

KitchenOS flow:

```text
Analytics
  -> AI Explanation
  -> Suggestions
```

---

## 14. Household Lifecycle

KitchenOS optimizes the household lifecycle.

```text
Plan
  -> Shop
  -> Store
  -> Cook
  -> Consume
  -> Timeline Event
  -> Learn
  -> Plan Again
```

Every product surface should contribute to this loop.

### 14.1 Current Broken Journey

```text
Recipe
  -> Shopping
  -> Forget Ingredients
  -> Buy
  -> Receipt
  -> Ignore
  -> Cook
  -> Pantry Wrong
  -> Repeat
```

### 14.2 KitchenOS Journey

```text
AI Builds Week
  -> Shopping Generated
  -> Go Shopping
  -> Receipt Scan
  -> Pantry Updated
  -> Timeline Updated
  -> Dinner Reminder
  -> Cook Mode
  -> Inventory Updated
  -> Budget Updated
  -> Timeline Updated
  -> AI Learns
```

Every action improves the next action.

---

## 15. Household State Machine

KitchenOS should maintain a live household state instead of treating the household as static lists.

Example states:

```text
Ready
  Pantry stocked
  Meals planned
  Shopping complete

Attention Needed
  Milk low
  2 meals unplanned

Action Required
  No dinner planned
  5 critical items missing

Ready Again
```

This household state drives:

- Home screen priority.
- Notifications.
- Recommendations.
- Shopping prompts.
- Cook Mode suggestions.
- Household Timeline entries.

---

## 16. Feature Frequency Map

Feature prominence should follow usage frequency and business value.

| Feature | Frequency | Priority |
|---|---|---:|
| Home | Multiple times per day | Highest |
| Cook | Daily | Highest |
| Shopping | Weekly | High |
| Planner | Weekly | High |
| Household Timeline | Weekly and whenever trust is needed | High |
| Pantry Search | Weekly | Medium |
| Receipt Scan | Weekly | Medium |
| Analytics | Monthly | Low |
| Settings | Rarely | Lowest |

This frequency map drives navigation decisions.

---

## 17. Decision Points

KitchenOS should focus on recurring household decision moments.

| Decision | Frequency |
|---|---|
| What should we eat? | Daily |
| What should we cook tonight? | Daily |
| What is expiring? | Daily |
| Do we need groceries? | Weekly |
| What store should we visit? | Weekly |
| Are we overspending? | Weekly |

Every Home recommendation should map to one of these decisions.

---

## 18. Information Architecture

The recommended navigation model is action-based.

```text
Home | Plan | Shop | Cook | Household
```

This model aligns with user intent rather than database modules.

The five-tab model should remain simple, but the product model should treat Household Timeline as a first-class surface alongside Pantry, Shopping, Receipts, and Budget. In mobile navigation, Timeline can live inside Household and be surfaced from Home after important changes.

### 18.1 Rejected Model: Feature-Based Navigation

```text
List | Pantry | Meals | Receipts | Analytics | Settings
```

Problems:

- Too many mental models.
- No clear flow between features.
- Users must assemble their own workflow.
- AI has no natural entry point.

### 18.2 Rejected for MVP: AI-Centric Navigation

```text
Assistant | Actions | Cook | Shop | Profile
```

Pros:

- Strong AI identity.
- Futuristic.
- Reduces navigation.

Cons:

- Lower predictability.
- Harder discoverability.
- Risk of black-box experience.

Recommendation:

> Too early for MVP, useful as a future direction.

### 18.3 Final Navigation Decision

```text
Home
Plan
Shop
Cook
Household
```

Reasons:

- Aligns with user intent.
- Supports AI layering.
- Minimizes cognitive load.
- Scales to future modules.
- Preserves offline-first architecture.

---

## 19. Screen Responsibilities

### 19.1 Home: Decision Layer

Home is not a dashboard. It is a decision generator.

Purpose:

- Show what needs attention.
- Show recommended actions.
- Surface household health.
- Link directly into Plan, Shop, Cook, Household, or Household Timeline.

Example structure:

```text
Good Morning

Attention Needed
Milk low: 2 days left

Suggested Today
Dinner: Palak Dal
97% ingredients available

Shopping
5 items needed, about $24

Budget
On track, $18 under average

Household Timeline
3 meaningful changes since yesterday

Quick Actions
[Start Cooking] [View Shopping] [Plan Week]
```

### 19.2 Plan: Weekly Intelligence Layer

Purpose:

- Turn chaos into structured meals.
- Generate weekly plans.
- Use pantry and budget context.
- Allow quick approval or adjustment.

UX principle:

> Planning is not editing. Planning is approving AI suggestions.

Example flow:

```text
Generate Week
  -> AI Plan Created
  -> User Adjusts
  -> Shopping List Auto-Generated
```

### 19.3 Shop: Execution Layer

Purpose:

- Convert plans into real-world action.
- Show a grouped shopping list.
- Estimate cost.
- Prevent duplicate purchases.
- Provide receipt scan entry point.

UX principle:

> Shopping is not a list. It is a guided mission.

### 19.4 Cook: Execution Mode

Purpose:

- Transform recipes into real-time guided action.
- Provide step-by-step flow.
- Support timers.
- Deduct pantry items after completion.

Cook Mode is the MVP hero feature.

Example flow:

```text
Open Cook Mode
  -> Follow Steps
  -> Finish Cooking
  -> Ingredients Deducted
  -> Pantry Updated
  -> Timeline Updated
```

### 19.5 Household: System Layer

Household is the control center for system understanding, trust, and correction.

Contains:

- Household Timeline.
- Pantry.
- Receipts.
- Analytics.
- Family.
- Settings.
- Integrations.

Purpose:

> Only expose complexity to users who need it.

Household Timeline should answer:

```text
What changed in my household?
Who or what changed it?
Why did it happen?
Can I undo or correct it?
```

Timeline is especially important after receipt scans, pantry deductions, budget updates, AI recommendations, goal changes, safety warnings, expert recommendations, and corrections.

---

## 20. UX Design Rules

### 20.1 No Data Dumps

Avoid:

- Full tables.
- Raw logs.
- Long lists without grouping.

### 20.2 Default to Decisions

Every screen should answer:

> What should I do next?

### 20.3 Collapse Complexity

Use progressive disclosure. Show deeper detail only when the user asks for it.

### 20.4 AI Is Invisible Until Needed

AI appears as:

- Suggestion cards.
- Insights.
- Warnings.
- Explanations.

Not as a permanent chat window.

### 20.5 One Screen, One Purpose

| Screen | Purpose |
|---|---|
| Home | Decide |
| Plan | Organize |
| Shop | Buy |
| Cook | Execute |
| Household | Manage |
| Household Timeline | Review and trust |

### 20.6 Performance UX

KitchenOS should feel instant, even when intelligence is still processing.

Core flows must not wait for AI, OCR, sync, or marketplace systems.

Performance principles:

- Shopping, cooking, pantry, and meal plan viewing should work from local state first.
- User actions should receive immediate visual feedback.
- Safe optimistic updates should be used for low-risk actions.
- Pending states should be clear when accuracy matters.
- Cook Mode and Shopping Mode should never feel blocked by network latency.
- AI suggestions can arrive progressively after the core screen is usable.
- Receipt OCR can process asynchronously while the user continues other tasks.
- Sync should feel calm and recoverable, not alarming.

Product rule:

> If the user is cooking or shopping, speed matters more than intelligence.

### 20.7 Visual Design Philosophy

KitchenOS should look and feel:

- Calm.
- Warm.
- Trustworthy.
- Household-friendly.
- Lightweight.
- Practical.

KitchenOS should not feel:

- Clinical.
- Spreadsheet-like.
- Overly technical.
- Overly gamified.
- Like a generic AI chatbot.

Visual design principles:

- Prefer cards over dense tables.
- Prefer grouped timelines over raw logs.
- Prefer plain-language explanations over technical labels.
- Use whitespace to reduce cognitive load.
- Show the recommended action first, then supporting context.
- Keep safety, budget, freshness, and goal indicators visually consistent.
- Place explanations near the recommendation they support.
- Make undo, edit, and correction actions visible but not distracting.

### 20.8 Status, Feedback, and Trust Indicators

KitchenOS needs a consistent visual language for household state.

Recommended status language:

| Status | Meaning | Example |
|---|---|---|
| Green | Safe, available, on track | Recipe is allergy-safe and ingredients are available |
| Yellow | Needs attention or review | Item expires soon or AI confidence is medium |
| Red | Blocked or unsafe | Allergy conflict or unsafe recommendation |
| Blue | AI suggestion or insight | Suggested meal, substitution, or budget insight |
| Gray | Offline, stale, pending, or unavailable | Sync pending or cached data |
| Purple or teal | Expert-related guidance | Nutritionist recommendation or coach-supported plan |

Feedback principles:

- Every tap that changes household state should produce visible confirmation.
- Every automated suggestion should explain why it appeared.
- Every risky or safety-related action should show a clear warning.
- Every correction should show what changed and what was reversed.
- Every offline or pending state should show whether the user can continue safely.
- Every expert recommendation should show source, consent context, and approval state.

Trust rule:

> Users should always know what changed, why it changed, whether it is safe, and how to correct it.

---

## 21. Empty States

### 21.1 Empty Pantry

```text
Your pantry is empty.
Start by scanning a receipt or adding your first items.
```

### 21.2 Empty Plan

```text
No meals planned yet.
Let AI generate a weekly plan.
[Generate Plan]
```

### 21.3 Empty Shop

```text
No shopping needed.
You are fully stocked for 4 days.
```

---

## 22. Offline UX

Offline mode must preserve core flows.

Available offline:

- Pantry browsing.
- Shopping list editing.
- Cook Mode.
- Meal plan viewing.
- Local pantry deduction.

Unavailable or limited offline:

- New AI generation.
- Receipt OCR.
- Cloud sync insights.

Offline indicators:

- Cached data badge.
- Sync pending indicator.
- Disabled or stale AI suggestions.

Offline AI context constraint:

Any changes made while offline — pantry updates, cook completions, corrections — are queued as pending sync events in local SQLite. These changes have not reached Cloud SQL yet. AI recommendations served from cache during offline periods will not reflect these changes.

When connectivity is restored:

- Pending events sync to the backend first.
- Redis cache is invalidated for the household.
- The next AI recommendation request reads fresh context.

The app must show a visible stale indicator on any cached recommendation and must not silently serve outdated suggestions as current.

Cache staleness model:

The local pending queue on a single device is not a reliable staleness signal for multi-member households. Other household members may have cooked meals, consumed pantry items, or scanned receipts on their own devices, and those changes may already be synced to the backend. A device that is offline has no visibility into those actions.

Staleness ownership belongs to the backend at recommendation generation time, not to the device at display time.

How it works:

- The backend sets a `recommendation_expires_at` timestamp when generating each recommendation.
- Expiry is based on household activity level: an active multi-member household gets a shorter window; a single low-activity household gets a longer window.
- The device caches the recommendation together with `recommendation_expires_at` in local SQLite.
- While offline, the device respects `recommendation_expires_at` as the primary staleness signal.
- The local pending queue can only move expiry earlier, never extend it.
- On reconnect, the device always requests a fresh recommendation regardless of expiry status.

The UX degradation scale:
- Fresh: within `recommendation_expires_at`, no local high-impact pending events.
- Stale warning: within expiry but local high-impact pending events exist.
- Suppressed: past `recommendation_expires_at` or reconnected and refresh pending.

See Section 37.8 for the full architectural explanation.

---

## 23. Motion and Interaction Philosophy

KitchenOS should feel:

- Calm.
- Predictable.
- Lightweight.

Recommended transitions:

- Home to Cook = full immersion.
- Shop to receipt scan = slide-up modal.
- Plan to Shop = flow transition.
- Pantry item to detail = expand card.

The user should not feel like they are navigating an app. They should feel guided through the household lifecycle.

---



---

## 38. MVP Strategy

The product should be built in three scope layers:

```text
MVP-0
  -> Prove the household food loop

MVP-1
  -> Add trust, correction, and safety

Post-MVP
  -> Add advanced goals, marketplace, optimization, and automation
```

The first release should prove one core loop.

```text
Cook
  -> Consume
  -> Track
  -> Shop
  -> Plan
  -> Repeat
```

If this loop works, the product works. If not, nothing else matters.

### 38.1 MVP-0 Success Definition

MVP-0 is successful if:

- User can complete a meal using Cook Mode.
- Pantry updates after cooking.
- Shopping list reflects basic pantry reality.
- Receipt scanning or quick pantry entry can update the system.
- Home gives simple useful suggestions.
- Household Timeline shows meaningful changes in plain language.

### 38.2 MVP-1 Success Definition

MVP-1 is successful if:

- Users can correct or reverse common system mistakes.
- Duplicate or wrong-household receipts do not corrupt pantry, budget, shopping, or learning.
- Allergy and safety rules block unsafe recommendations.
- Household Timeline explains what changed, why it changed, and how to undo or correct it.
- The system avoids learning from corrected, duplicate, or wrong-household events.

### 38.3 What Not to Build in MVP-0

Exclude from MVP-0:

- Advanced AI orchestration.
- Full budget analytics.
- Multi-household sharing.
- Complex nutrition system.
- Goal-aware portions and body-composition planning.
- Expert marketplace.
- Optimization engine.
- Microservices backend.
- Perfect knowledge graph.

Principle:

> MVP-0 is about habit and basic trust. MVP-1 is about correction, safety, and confidence. Post-MVP is about intelligence and expansion.

---

## 39. MVP Feature Scope

### 39.1 MVP-0: Core Closed Loop

Build:

- Cook Mode.
- Pantry add/remove and simple quantities.
- Pantry deduction after cooking.
- Shopping list add/remove and basic grouping.
- Basic receipt scan or quick receipt-assisted pantry entry.
- Manual correction UI for receipt items.
- Simple Home suggestions using static rules.
- Basic Household Timeline entries for cooking, pantry, shopping, and receipt actions.

Skip:

- Predictive pantry models.
- Advanced analytics.
- Store optimization.
- Price intelligence.
- Advanced AI recommendations.
- Detailed nutrition dashboards.
- Expert marketplace.

### 39.2 MVP-1: Trust, Correction, and Safety Layer

Build:

- Duplicate receipt detection using minimum receipt metadata.
- Remove receipt and reverse effects.
- Undo for shopping list deletion.
- Pantry removal reason.
- Correction events instead of hard deletes.
- Allergy severity.
- Household-level hard-block derivation.
- Ingredient-level allergy filtering.
- Cook Mode allergy warning.
- Basic ingredient synonym mapping for safety-critical ingredients.
- Household Timeline details for corrections and reversals.

Skip:

- Receipt merge.
- Move receipt to another household.
- Advanced audit tooling.
- Full nutrition goal system.
- Fitness integrations.
- Organization/provider accounts.

### 39.3 Post-MVP: Intelligence and Expansion

Build after the core loop and trust layer are validated:

- Full Household Decision Engine.
- Predictive shopping.
- Budget intelligence.
- Goal-aware meal ranking.
- Goal-aware shopping suggestions.
- Per-person portions and add-ons.
- Curated expert marketplace.
- Fitness-context coordination.
- Advanced nutrition, wearable, and medical integrations.

### 39.4 Cook Mode: Hero Feature

Build in MVP-0:

- Step-by-step recipes.
- Full-screen mode.
- Timers.
- Step navigation.
- Pantry deduction on completion.

Why this matters:

> Cook Mode is where users feel value immediately.

### 39.5 Receipt Scan: Data Entry System

Build in MVP-0:

- Basic OCR.
- Item extraction.
- Manual correction UI.
- Pantry update.
- Receipt image storage.

Build in MVP-1 if duplicate receipt detection is required:

- Store name extraction.
- Receipt date and time extraction.
- Total amount extraction.
- Receipt image hash.
- OCR text hash.
- Item similarity check.

Skip in MVP-0:

- Price analytics.
- Store comparison.
- Advanced AI classification.

### 39.6 Home Screen: Light AI Layer

Build simple insights in MVP-0:

- Low-stock items.
- Suggested meal.
- Shopping needed.
- Recent Household Timeline changes that need review.

Use static rules first, not a full AI system.

---

## 40. MVP User Flows

### 40.1 MVP-0 Daily Flow

```text
Open App
  -> See Home Suggestion
  -> Tap Cook Dinner
  -> Cook Mode
  -> Ingredients Deducted
  -> Meal Completed
  -> Pantry Updated
  -> Household Timeline Updated
```

### 40.2 MVP-0 Weekly Flow

```text
Plan Meals
  -> Generate Shopping List
  -> Go Shopping
  -> Scan Receipt or Update Pantry
  -> Pantry Updated
  -> Household Timeline Updated
```

### 40.3 MVP-1 Correction Flow

```text
System Change
  -> User Reviews Household Timeline
  -> User Corrects or Reverses
  -> Current State Updates
  -> Learning Impact Updated
```

This is the staged MVP closed loop.

---



---

## 43. Three-Month MVP-0 Build Plan

### Month 1: Core App Foundation

Deliverables:

- Authentication.
- Pantry system.
- Shopping list.
- Basic navigation.
- Local database setup.

Goal:

> App is usable manually.

### Month 2: Cook and Receipt Loop

Deliverables:

- Full Cook Mode UX.
- Recipe system.
- Receipt scanning MVP.
- Pantry deduction logic.

Goal:

> First full closed loop exists.

### Month 3: Intelligence Layer

Deliverables:

- Rule-based Home suggestions.
- Basic AI recipes.
- Weekly planning UI.
- UX refinement and polish.

Goal:

> App feels smart enough to be useful.

---

## 44. Recommended Team Structure

Minimum team:

### Mobile Engineer: Flutter Lead

Responsibilities:

- Cook Mode.
- Offline system.
- Local state management.

### Backend Engineer

Responsibilities:

- APIs.
- Database.
- Receipt ingestion.

### Full-Stack Engineer

Responsibilities:

- Integration.
- Sync logic.
- UI support.

### AI Engineer: Part-Time Initially

Responsibilities:

- Prompts.
- Recipe generation.
- Later orchestration.

### Product / Design Owner

Responsibilities:

- UX consistency.
- Core flows.
- User validation.

---

## 45. Key Risks and Mitigations

### 45.1 Risk: Overbuilding AI

Mitigation:

- Keep AI minimal until Month 3.
- Use rules first.
- Avoid orchestration until the loop is validated.

### 45.2 Risk: Complex Sync

Mitigation:

- Build offline-first local DB first.
- Add sync gradually.
- Keep conflict rules simple in MVP-0.

### 45.3 Risk: Cook Mode UX Failure

Mitigation:

- Build Cook Mode early.
- Test real cooking sessions.
- Optimize for hands-free, messy, time-sensitive use.

### 45.4 Risk: Scope Explosion

Mitigation:

- Enforce strict MVP-0 and MVP-1 boundaries.
- Treat advanced AI, budget intelligence, and marketplace features as post-MVP.

### 45.5 Risk: Data Trust Issues

Mitigation:

- Show explanations.
- Let users correct data quickly.
- Avoid silent destructive changes.

---

## 46. MVP-0 and MVP-1 Success Metrics

Measure only the behaviors that prove trust and habit.

| Metric | Scope | Question |
|---|---|---|
| Cook completion rate | MVP-0 | Did users finish recipes? |
| Pantry update accuracy | MVP-0 | Does pantry reflect reality? |
| Shopping list usage | MVP-0 | Do users trust the list? |
| Weekly retention | MVP-0 | Do users return weekly? |
| Receipt scan usage | MVP-0 | Do users scan receipts? |
| Correction completion rate | MVP-1 | Can users fix wrong system changes? |
| Duplicate receipt recovery | MVP-1 | Can duplicate receipts be detected or reversed? |
| Allergy block accuracy | MVP-1 | Are unsafe recommendations blocked before display? |
| Household Timeline review rate | MVP-1 | Do users use Timeline for trust and correction? |

Key MVP-0 conclusion:

> KitchenOS succeeds only if Cook Mode becomes habit-forming.

Everything else supports Cook Mode until the core loop is proven.

---

## 47. Post-MVP Roadmap

### Phase 2: MVP-1 Trust and Safety Layer

- Correction and reversal flows.
- Duplicate receipt detection.
- Allergy Guard.
- Household Timeline maturity.
- Learning suppression for corrected or reversed events.

### Phase 3: Household Decision Engine

- Full Household Decision Engine.
- Predictive shopping.
- Budget intelligence.
- Goal-aware meal ranking.
- Goal-aware shopping suggestions.
- Per-person portions and add-ons.

### Phase 4: Marketplace and Expert Support

- Curated nutrition experts.
- Expert recommendations with KitchenOS safety checks.
- Permissioned household data sharing.
- Fitness-context coordination.
- Provider profiles and plan offerings.

### Phase 5: Advanced Household Automation

- Multi-household system.
- Grocery optimization.
- Voice assistant.
- Smart fridge integration.
- Advanced event projections.
- Automation layer.

### Phase 6: Broader Household OS Expansion

- Cleaning supplies.
- Household maintenance.
- Family coordination.
- LifeOS expansion beyond food.

---

## 48. Differentiation Strategy

KitchenOS is different because it is a closed-loop household intelligence system.

```text
Plan
  -> Shop
  -> Cook
  -> Consume
  -> Learn
  -> Improve
```

Most competitors stop at Plan or Shop. KitchenOS completes the loop.

### 48.1 Why KitchenOS Wins

KitchenOS wins because:

- It owns the household food lifecycle, not one feature.
- It builds memory of the household over time.
- It reduces cognitive load.
- It is event-driven.
- Every action improves the next action.

### 48.2 The Real Moat

The moat is not:

- AI models.
- UI design.
- Feature count.

The moat is:

> Household behavioral data over time.

After 30 days, KitchenOS understands:

- Consumption cycles.
- Shopping needs.
- Meal preferences.
- Waste patterns.

After 6 months, the product becomes difficult to replace because the household model is personalized.

---

## 49. Product Narrative

Do not position KitchenOS as:

> An AI pantry app.

Position KitchenOS as:

> Your household's food intelligence system.

Users should feel:

- It already knows what I need.
- I do not have to think anymore.
- This saves me time every day.

---

## 50. Onboarding Strategy

The first five minutes define retention.

### 50.0 Household Auto-Creation

A household is never something the user sets up manually. It is created automatically the moment a new account is confirmed.

```text
Sign up
  → Identity created (identities table)
  → Default household auto-created (households table)
  → User added as first household member — Adult 1, role: admin
  → Onboarding begins inside that household context
```

The user never sees a "create household" step. They just start using the app. A person living alone is a household of one. If they later invite a partner or family member, that person joins the existing household — no migration required.

**If the user abandons onboarding early:**
The household and default member record still exist. The system operates in a low-confidence state — generic suggestions, no allergy rules, no goals. The home screen guides them toward the next useful action rather than showing an empty state. Context accumulates as they use the product.

**Household confidence state at sign-up:**

| What exists | What is unknown |
|---|---|
| Household ID | Pantry contents |
| Member ID (Adult 1) | Allergies and dietary restrictions |
| Auth identity | Goals |
| | Preferred stores |
| | Budget |

The Household Intelligence Model starts empty and builds from first use. Every receipt scan, meal cooked, or preference confirmed raises confidence. The product must be useful before confidence is high — not after.

KitchenOS should not assume it has enough context on day one. Onboarding should offer three cold-start paths.

### 50.1 Receipt-First Path

Best for users who just shopped.

```text
Scan Recent Receipt
  -> Confirm uncertain items
  -> Pantry Created
  -> Shopping and meal suggestions appear
```

### 50.2 Pantry-Light Path

Best for users who want fast setup without OCR.

```text
Add 5 to 10 Staples
  -> Choose common household items
  -> Pantry Created
  -> First cookable meals appear
```

### 50.3 Recipe-First Path

Best for users who want immediate cooking value.

```text
Pick a Meal
  -> KitchenOS checks assumed pantry items
  -> User confirms what they have
  -> Missing items become shopping suggestions
```

### 50.4 Quick Setup

Capture:

- Household size.
- Basic preferences.
- Critical allergies or dietary restrictions.

### 50.5 Immediate Value

Show the best available next action based on the selected cold-start path.

Examples:

- Here is what you can cook today.
- Here are the items we found from your receipt.
- Here are three meals that match your starter pantry.
- Here is what you need to buy for the meal you selected.

### 50.6 Instant Feedback Loop

System updates:

- Pantry.
- Suggestions.
- Shopping list.
- Household Timeline.

---

## 50A. Household Intelligence Model

> The Household Intelligence Model is the AI's continuously evolving understanding of a household. It combines explicit profile information, observed behaviours, learned preferences, contextual signals, and confidence scores to produce personalised guidance.

This is not a user profile. It is not a settings screen. It is how KitchenOS reasons about a household — and it starts forming on day one.

### Three Layers That Must Not Be Confused

**Layer 1 — Domain Model (Business Facts)**

The Domain Model stores what *is*. Facts. Entities. Events.

```text
Milk
  Quantity: 2 litres
  Expiration: June 10
  Added by: receipt_scan
```

No AI here. No inference. Just recorded truth.

**Layer 2 — Household Intelligence Model (AI Beliefs)**

The Intelligence Model stores what the AI *thinks* — beliefs derived from observed behaviour, weighted by confidence.

```text
Milk consumption
  Estimated cycle: every 8 days
  Confidence: 91%
  Evidence: 14 purchase events, 6 cook completions using milk
```

This is completely different from the Domain Model. One is factual. One is inferred.

**Layer 3 — User Profile (Account Identity)**

The User Profile is small and static — name, email, timezone, notification settings, privacy settings. It belongs to Account Management, not to intelligence.

These three layers must stay separate. The Domain Model should contain no AI-specific concepts. The Intelligence Model should contain no business domain logic.

---

### The Three Stages of Learning

KitchenOS does not ask users to configure an intelligence model. It builds one progressively.

**Stage 1 — Explicit Knowledge (Onboarding)**

Ask only the minimum needed to provide value immediately. These are questions the AI cannot safely infer on its own.

| What to ask | Why |
|---|---|
| Household size (adults, children) | Cannot be inferred reliably at the start |
| Allergies and dietary restrictions | Safety-critical — never guess |
| Primary goal (eat healthier, save money, reduce waste, save time, manage medical diet) | Personal intention — must be stated |
| Cooking skill level (beginner, comfortable, experienced) | Calibrates recipe complexity from day one |
| Preferred stores | Bootstraps shopping suggestions before behavior data exists |

Do not ask during onboarding:
- Favorite cuisine — learn it.
- Preferred shopping day — learn it.
- Typical cooking time — learn it, then confirm if needed.
- Whether they like mushrooms — learn it, then ask if unsure.

> **Rule: Ask only what the AI cannot reasonably learn on its own.**

This keeps onboarding short, reduces abandonment, and reinforces from the first minute that KitchenOS is an intelligent assistant — not a questionnaire.

**Stage 2 — Behavioural Learning**

The AI observes without asking.

```text
Observed signals:
  Always skips fish recipes
  Buys bananas every week
  Shops at Costco roughly monthly
  Cooks on Sundays
  Orders takeout on Fridays
  Never finishes lettuce
  Consistently rejects spicy meals
```

None of these were asked. All were learned. Behavioural signals are far more accurate than self-reported preferences, which go stale or are given carelessly during onboarding.

**Stage 3 — Confidence-Based Intelligence**

Instead of storing static preferences, KitchenOS stores probabilistic beliefs with evidence.

```text
Indian cuisine
  Confidence: 94%
  Evidence: 57 recipes accepted, 42 grocery purchases, 18 restaurant orders

Typical weekday cooking time
  Estimate: 18 minutes
  Confidence: 89%
  Evidence: 31 completed sessions

Milk consumption cycle
  Estimate: 8 days
  Confidence: 91%
  Evidence: 14 purchase events
```

This model evolves continuously. It is never finished.

---

### Household Intelligence Model Structure

```text
Household Intelligence Model
│
├── Static Facts (from onboarding)
│   ├── Household size
│   ├── Allergies and restrictions
│   ├── Goals
│   └── Initial preferences (stores, skill)
│
├── Learned Preferences (from behaviour)
│   ├── Favourite cuisines
│   ├── Cooking time patterns
│   ├── Shopping habits
│   ├── Pantry depletion rates
│   └── Meal acceptance and rejection patterns
│
├── Current Context (live signals)
│   ├── Pantry state
│   ├── Budget and spend pace
│   ├── Season and weather
│   └── Calendar (if integrated)
│
└── Confidence Scores
    (attached to every learned preference)
```

---

### Transparency: KitchenOS Knows...

Every learned preference must be explainable, editable, and resettable by the user. The AI is not a black box.

Example transparency screen under Household settings:

```text
KitchenOS has learned...

✓ You usually cook on Sundays.
  [Confirm] [Edit] [Forget]

✓ You prefer quick meals on weekdays — under 20 minutes.
  [Confirm] [Edit] [Forget]

✓ You shop at Costco roughly once a month.
  [Confirm] [Edit] [Forget]

✓ You rarely finish spinach before it expires.
  [Confirm] [Edit] [Forget]

✗ You avoid spicy food.
  [Confirm] [Edit] [Forget]
```

When the AI is unsure, it asks — but only after observing enough signals to make the question useful.

> After two months: "I have noticed you skip mushroom recipes. Should I recommend them less often?"

This ties directly to the product principle: **Trust is earned through transparency.**

---

### Relationship to the Household Decision Engine

The Household Intelligence Model is the reasoning layer that sits inside the Household Decision Engine.

```text
Household Decision Engine
  │
  ├── Domain Model  ←  business facts (pantry, events, receipts)
  │
  ├── Household Intelligence Model  ←  AI beliefs (patterns, preferences, confidence)
  │
  └── Recommendation Engine  ←  uses both to produce guidance
```

Full architectural specification: `Products/KitchenOS/40_Technical_Architecture.md`, Section 24A.

---

## 51. Growth Loops

### 51.1 Cooking Loop

```text
Cook
  -> Pantry changes
  -> Better suggestions
  -> More cooking
```

### 51.2 Receipt Loop

```text
Scan receipt
  -> System learns
  -> Better predictions
  -> More value
```

### 51.3 Planning Loop

```text
Plan meals
  -> Optimized shopping
  -> Better cooking
  -> Better planning
```

---

## 52. Retention Strategy

Retention should come from daily household usefulness, not AI novelty.

Daily retention drivers:

- What should I cook?
- What do I need to buy?
- What is running out?

---

## 53. Viral Strategy

KitchenOS can spread through:

### Shared Household Usage

Families and roommates invite others into the shared household workflow.

### Shared Shopping Lists

Shopping collaboration creates organic adoption.

### Meal Sharing

Users share meals or recipes with others.

### The “It Already Knows” Effect

Users tell others:

> It literally knows what I need to buy.

---

## 54. Long-Term End State

Eventually, users should not manage food directly.

They should:

- Cook what is suggested.
- Approve what is needed.
- Trust the system.

Final architecture statement:

```text
Events
  -> Knowledge
  -> Intelligence
  -> Decisions
  -> Actions
  -> Learning
```

That is KitchenOS.

---

## 54A. Collective Intelligence and Strategic Moat

KitchenOS improves as more households use it.

This is not a tagline. It is an architectural property — and it is the most defensible long-term moat available to the platform.

### The Two Intelligence Models

KitchenOS operates with two distinct intelligence layers that work together.

**Household Intelligence Model**

Learns from one household:

- My pantry habits.
- My goals.
- My cooking style.
- My shopping patterns.
- My budget behaviour.

This is personal. It stays within the household context.

**Collective Intelligence Model**

Learns from all participating households:

- Regional grocery prices and price trends.
- Seasonal availability and cost patterns.
- Recipe success rates by household type.
- Pantry depletion rates by item category.
- Food waste patterns.
- Shopping behaviour patterns.
- Recommendation acceptance and rejection rates.

This is aggregated and anonymised. It never exposes individual households.

**The Recommendation Engine combines both.**

```text
Household Intelligence Model
        +
Collective Intelligence Model
        ↓
Recommendation Engine
        ↓
Personalised guidance for this household
```

A recommendation is personalised to what this household prefers, and calibrated by what thousands of similar households have learned.

---

### Why This Is a Strategic Moat

A price comparison feature can be copied in a sprint.

A Collective Intelligence Model built from millions of household events over years cannot be copied. The data, the training signal, the learned patterns — they compound with every new household, every new receipt scan, every meal cooked.

This is the same pattern that made Google Maps better than MapQuest, Waze better than static GPS, and Spotify recommendations better than radio. The product improves not just from engineering — but from use.

KitchenOS gets a stronger competitive position every week it runs.

---

### Company-Level Architectural Pattern

This intelligence architecture is not specific to food. It is a pattern Amanaska can apply to every future product.

```text
KitchenOS
  Personal Food Intelligence  +  Collective Food Intelligence

Amanaska Health (future)
  Personal Health Intelligence  +  Collective Health Intelligence

Amanaska Finance (future)
  Personal Financial Intelligence  +  Collective Financial Intelligence

Amanaska Learning (future)
  Personal Learning Intelligence  +  Collective Learning Intelligence
```

The Household Intelligence Model and Collective Intelligence Model are a company-level architectural pattern, not a KitchenOS feature.

---

### Consent Principle

> **Collective intelligence is built through informed participation, never silent collection.**

This is a company principle, not an implementation detail.

Implementation:

- **Default:** All household data is private. Nothing contributes to the collective model without explicit opt-in.
- **Opt-in framing:** "Help improve recommendations for everyone — including yours."
- **What is shared:** Anonymised, non-identifiable observations only.
- **What is never shared:** Names, emails, household identities, or any data that can be traced back to a specific household.
- **Granularity:** Item-level observations are permitted — because the learning value requires them — but only when stripped of all identifying context.
- **Transparency:** Users can see which categories of observations are being shared.
- **Control:** Users can opt out at any time. Opting out stops future contributions and removes previously contributed observations from the learning pipeline.

### What an Anonymised Observation Looks Like

```text
Price observation
  Item:     Organic Whole Milk
  Store:    Costco
  Region:   Austin Metro
  Price:    $3.99
  Month:    July 2026
```

No household identifier. No name. No purchase date. No quantity. Just a useful signal.

```text
Recipe observation
  Recipe:          Chicken Stir Fry
  Accepted:        Yes
  Cook time:       22 minutes
  Household type:  2 adults
  Region:          Texas
```

Again — useful for collective learning. Nothing that identifies a person.

The distinction that matters is not item-level versus aggregate. It is **identifiable versus non-identifiable**.

---

### Price Intelligence Phases

| Phase | Price data source |
|---|---|
| MVP-0 | Receipt-derived only. Personal price history per household. "You paid $3.49 for milk last time at Costco." |
| MVP-1 | Collective price observations from opted-in households. "Milk at Costco is averaging $3.79 in your region this month." |
| Post-MVP | Grocery API partnerships where available to supplement collective data with real-time shelf prices. |

The Collective Intelligence Model is the primary long-term price strategy. Grocery API partnerships are supplementary, not foundational.

Full architectural specification: `Products/KitchenOS/40_Technical_Architecture.md`, Section 36A.

---

## 55. Product Reality Check

If executed correctly:

- MVP-0 is achievable in approximately 8–12 weeks.
- Differentiation appears within 2–3 weeks of usage.
- Retention grows naturally from system learning.

---

## 56. Allergies, Dietary Safety, and Household Profiles

KitchenOS should treat allergies as a first-class safety system, not as ordinary taste preferences.

The recommendation pipeline should always apply safety before optimization.

```text
Candidate Recipes
  -> Normalize Ingredients
  -> Apply Allergy and Safety Filter
  -> Apply Household Preferences
  -> Apply Pantry Match
  -> Apply Budget, Nutrition, and Time Ranking
  -> Generate Explanation
```

Allergy filtering should be deterministic. The AI model may suggest meals, recipes, or substitutions, but a rules-based Allergy Guard must validate outputs before they reach the user.

### 56.1 Allergy Is Not the Same as Preference

| Type | Example | Product Behavior |
|---|---|---|
| Allergy | Peanut, shellfish, tree nut | Hard block by default |
| Intolerance | Lactose intolerance, gluten sensitivity | Warning or block depending on severity |
| Medical restriction | Low sodium, diabetic diet | Constraint-based recommendation |
| Religious or ethical diet | Vegetarian, halal, kosher | Household or individual rule |
| Preference | Dislikes mushrooms | Ranking factor |
| Goal | Muscle gain, weight reduction | Optimization target after safety |

Allergies and medical restrictions should not be stored as casual preferences. They need severity, enforcement level, ownership, and visibility rules.

### 56.2 Allergy UX Behavior

When suggesting meals, KitchenOS should explain safety clearly.

Example safe recommendation:

```text
Suggested: Veggie Stir Fry
Safe for: Raj, Priya, Arjun
Excludes: peanuts, shellfish
Uses: rice, carrots, spinach already in pantry
```

Example blocked recommendation:

```text
Not recommended: Thai Peanut Noodles
Reason: Contains peanuts, blocked for Arjun's severe allergy
```

Ingredient substitutions must also pass allergy checks.

Example:

```text
Need dairy-free substitute
  -> Reject almond milk if tree nut allergy exists
  -> Suggest oat milk instead
```

### 56.3 Profile Architecture Decision

KitchenOS should store both individual profiles and household profiles.

```text
User Profile
  -> Identity, allergies, preferences, goals, privacy settings

Household Profile
  -> Shared pantry, shopping, meal plans, budget, store preferences

Household Member Profile
  -> User-to-household role, permissions, meal participation, visibility
```

This supports real household complexity. One person can belong to multiple households while retaining their own personal dietary and safety profile.

Example:

```text
Raj
  -> Home Household
  -> Parents Household
  -> Vacation Household
```

Raj's allergies and personal goals stay with Raj. Pantry, shopping, receipts, meal plans, and budgets belong to each household.

### 56.4 Individual User Profile

Individual profiles should store personal and sensitive data.

Recommended fields:

- Name.
- Age group.
- Allergies.
- Intolerances.
- Medical dietary restrictions.
- Diet type.
- Nutrition goals.
- Food dislikes.
- Favorite cuisines.
- Privacy settings.

Example:

```text
User: Arjun
Allergy: peanuts
Severity: severe
Reaction: anaphylaxis
Applies to: all meal suggestions
Visibility: household admins and meal planners
```

### 56.5 Household Profile

Household profiles should store shared operating context.

Recommended fields:

- Household name.
- Members.
- Pantry.
- Shopping lists.
- Meal plans.
- Receipts.
- Budget.
- Default cuisines.
- Store preferences.
- Cooking schedule.
- Household safety policy.

Example:

```text
Household: Duddu Family
Default meal audience: all household members
Hard-block ingredients: peanuts, shellfish
Preferred stores: Costco, Walmart
Cooking days: Monday through Friday
```

### 56.6 Household Member Profile

The household member profile links a person to a household.

Recommended fields:

- Role: admin, adult, child, guest.
- Can edit pantry.
- Can approve shopping.
- Included in meal planning.
- Included in allergy safety checks.
- Allergy visibility.
- Goal visibility.

Example:

```text
User: Arjun
Household: Duddu Family
Role: child
Included in meal planning: yes
Can edit pantry: no
Allergy visibility: visible to meal planners
```

### 56.7 Household-Level Allergy Aggregation

For default household meals, KitchenOS should derive a household safety profile from active eaters.

```text
Household Allergy Guard = union of all active members' hard allergies
```

Example:

```text
Raj: no allergies
Priya: lactose intolerance
Arjun: peanut allergy

Household hard blocks:
- peanut

Household warnings:
- dairy
```

KitchenOS should also support meal-specific audiences.

Example prompt:

```text
Who is eating this meal?

- Whole household
- Adults only
- Kids only
- Just me
- Custom members
```

The Allergy Guard should evaluate only the selected eaters for that meal.

### 56.8 MVP-1 Safety Scope

MVP-0 should capture critical allergies during onboarding if users provide them, but MVP-1 is the point where safety becomes a formal product layer.

MVP-1 must include:

- Individual member allergies.
- Allergy severity.
- Household-level hard-block derivation.
- Ingredient-level allergy filtering.
- Cook Mode allergy warning.
- Manual confirmation for risky recipes.
- Basic ingredient synonym mapping.

Post-MVP can add:

- Cross-contamination warnings.
- Packaged food label scanning.
- Store product allergen detection.
- Pediatric safety profiles.
- Allergy-safe substitutions.
- Caregiver permissions.

### 56.9 Suggested Data Model

```text
users
  id
  name
  email

households
  id
  name

household_members
  id
  household_id
  user_id
  role
  included_in_meal_planning
  allergy_visibility
  goal_visibility

dietary_constraints
  id
  user_id
  type
  ingredient_or_category
  severity
  enforcement_level
  notes

household_safety_rules
  id
  household_id
  rule_type
  ingredient_or_category
  enforcement_level
  derived_from_user_id
```

Important distinction:

- `dietary_constraints` are owned by individuals.
- `household_safety_rules` are computed or explicitly configured for the household.

### 56.10 AI Safety Contract

AI should receive a safe context pack.

```text
Meal audience:
- Raj
- Priya
- Arjun

Hard blocks:
- peanuts
- shellfish

Warnings:
- dairy for Priya

Preferences:
- vegetarian preferred twice per week
- avoid mushrooms if possible
```

After AI generation, deterministic validation still runs.

```text
AI Suggestion
  -> Allergy Guard
  -> Unsafe rejected
  -> Safe options shown
```

The final product rule:

> Store allergies at the individual profile level, derive household safety rules at the household level, and enforce allergy checks before any AI-generated recipe, shopping item, or substitution reaches the user.

---

## 57. Nutrition Goals and Body-Composition Planning

KitchenOS should support goals such as muscle gain, weight reduction, maintenance, healthier eating, and medical nutrition, but goals should not override safety.

The goal hierarchy should be:

```text
Safety
  -> Medical Constraints
  -> Household Constraints
  -> Individual Goals
  -> Preferences
  -> Pantry, Budget, and Convenience Optimization
```

This means a high-protein goal can influence recommendations only after allergy and medical constraints pass.

### 57.1 Goal Types

| Goal Type | Example | Product Behavior |
|---|---|---|
| Muscle gain | Higher protein, calorie surplus | Recommend protein-rich meals and snacks |
| Weight reduction | Calorie deficit, higher satiety | Recommend lower-calorie, high-fiber, high-protein meals |
| Maintenance | Stable calories and balanced macros | Keep meals consistent and sustainable |
| General health | More vegetables, less processed food | Rank meals by quality and variety |
| Medical nutrition | Low sodium, diabetic-friendly | Treat as stronger constraint than preference |
| Performance | Pre-workout / post-workout meals | Time meals around activity when data exists |

### 57.2 Individual Goals vs Household Meals

Goals should be stored at the individual level because each member can have different needs.

Example:

```text
Raj: muscle gain
Priya: weight reduction
Arjun: normal child nutrition
Household dinner: shared base meal with individual adjustments
```

KitchenOS should avoid creating totally separate meals unless needed. The better UX is to recommend one shared meal with variations.

Example:

```text
Base meal: Chicken rice bowl

Raj adjustment:
- Add extra chicken
- Add Greek yogurt side

Priya adjustment:
- Reduce rice portion
- Add extra vegetables

Arjun adjustment:
- Standard portion
- No spicy sauce
```

### 57.3 Goal Setup UX

Goal setup should be lightweight and non-clinical in MVP.

Recommended setup flow:

```text
Choose Goal
  -> Set Intensity
  -> Set Dietary Constraints
  -> Set Meal Participation
  -> Confirm Recommendation Style
```

Example fields:

- Goal type.
- Target direction: gain, lose, maintain, improve.
- Intensity: gentle, moderate, aggressive.
- Protein priority.
- Calorie awareness level.
- Meal types included: breakfast, lunch, dinner, snacks.
- Start date.
- Review cadence.

KitchenOS should avoid promising medical outcomes. It should frame goals as meal planning support unless a future clinical integration is added.

### 57.4 Recommendation Behavior for Muscle Gain

For muscle gain, KitchenOS should optimize for:

- Higher protein per meal.
- Calorie adequacy.
- Post-workout meal suggestions if workout timing is known.
- Protein snacks.
- Pantry staples like eggs, Greek yogurt, lentils, chicken, paneer, tofu, beans, and protein-rich grains.

Example recommendation:

```text
Suggested: Paneer quinoa bowl
Reason: High protein, uses spinach and yogurt already in pantry, supports Raj's muscle gain goal.
```

### 57.5 Recommendation Behavior for Weight Reduction

For weight reduction, KitchenOS should optimize for:

- Higher satiety.
- Protein and fiber.
- Lower calorie density.
- Portion guidance.
- Reduced impulse shopping.
- Fewer ultra-processed snacks.

Example recommendation:

```text
Suggested: Lentil vegetable soup
Reason: High fiber, lower calorie density, uses expiring carrots, supports Priya's weight reduction goal.
```

### 57.6 Goal Conflict Resolution

Households often have conflicting goals. KitchenOS should resolve conflicts through shared meals plus individual modifiers.

Conflict examples:

```text
One member wants weight reduction.
Another wants muscle gain.
Child needs normal calories.
One member has dairy intolerance.
```

Resolution pattern:

```text
Shared Safe Base Meal
  -> Individual Portion Guidance
  -> Optional Add-ons
  -> Optional Exclusions
```

Example:

```text
Shared base: Turkey chili

Muscle gain add-on:
- Extra turkey
- Add avocado

Weight reduction adjustment:
- Smaller rice portion
- Add salad

Dairy intolerance adjustment:
- Skip cheese topping
```

### 57.7 Goal-Aware Shopping

Goals should influence shopping lists.

Examples:

- Muscle gain adds protein staples when low.
- Weight reduction reduces snack replenishment frequency.
- General health increases produce variety.
- Medical nutrition flags high-sodium packaged foods.

Shopping recommendation example:

```text
Add Greek yogurt?
Reason: Supports Raj's protein goal and usually runs out every 6 days.
```

### 57.8 Goal-Aware Cook Mode

Cook Mode should support per-person portions and substitutions.

Example:

```text
Serving Raj:
- Add 1 extra egg

Serving Priya:
- Use half rice portion
- Add extra vegetables

Serving Arjun:
- Mild spice level
```

This turns goals into practical cooking actions instead of abstract nutrition dashboards.

### 57.9 Goal Tracking Without Becoming a Fitness App

KitchenOS should not become a calorie tracker in MVP-0, MVP-1, or post-MVP.

MVP-1 goal tracking, if included, should focus on simple adherence signals:

- Goal-supporting meals cooked.
- Protein-forward meals per week.
- Vegetable-forward meals per week.
- Reduced takeout frequency.
- Pantry purchases aligned with goals.

Avoid in MVP-1:

- Detailed calorie counting.
- Complex macro dashboards.
- Weight logging.
- Medical claims.

### 57.10 Suggested Data Model

```text
user_goals
  id
  user_id
  goal_type
  target_direction
  intensity
  status
  start_date
  review_cadence

nutrition_preferences
  id
  user_id
  protein_priority
  calorie_awareness_level
  preferred_meal_types
  avoided_foods

meal_audience_goals
  id
  meal_plan_id
  user_id
  goal_id
  portion_strategy
  add_on_strategy
  exclusion_strategy
```

### 57.11 Goal Scope

MVP-0 should not include a complex goal system.

MVP-1 can include:

- Simple individual goal selection.
- Basic goal labels that influence explanation language.
- Conservative meal ranking signals after safety constraints.

Post-MVP can add:

- Goal-aware shopping suggestions.
- Basic portion guidance.
- Shared meal with individual add-ons.
- Macro targets.
- Wearable integration.
- Weight trend integration.
- Fitness app integration.
- Dietitian review workflows.
- Medical nutrition plans.

The final product rule:

> Store goals at the individual profile level, apply them after safety constraints, and translate them into meal suggestions, shopping suggestions, portions, and add-ons rather than forcing the household into separate meal plans.

---

## 58. Expert Marketplace for Nutritionists and Fitness Coaches

KitchenOS can expand into a marketplace where users work with nutritionists, dietitians, fitness coaches, gym trainers, strength coaches, yoga instructors, and wellness organizations.

This should be treated as a post-MVP growth layer, not a dependency for the core product. The marketplace becomes much more defensible after KitchenOS has household context such as goals, allergies, pantry patterns, cooking history, shopping behavior, and adherence signals.

The marketplace should strengthen food decisions. It should not turn KitchenOS into a generic fitness, medical, or coaching platform.

The marketplace should not feel like a generic expert directory. It should feel like:

> KitchenOS connects users with experts who can use permissioned household data to create practical nutrition and fitness plans.

### 58.1 Strategic Role

The expert marketplace extends KitchenOS from self-guided household intelligence into human-assisted coaching.

```text
KitchenOS Household Context
  -> User Goal
  -> Expert Match
  -> Plan Selection
  -> Permissioned Data Sharing
  -> Expert Chat and Plan
  -> KitchenOS Safety and Goal Checks
  -> User Approval
  -> Meal, Shopping, and Fitness-Context Coordination
```

This creates a strong loop:

```text
Household Data
  -> Better Expert Advice
  -> Better Plans
  -> Better User Outcomes
  -> More Household Data
```

### 58.2 Provider Architecture: Individuals and Organizations

KitchenOS should support both individual providers and organizations in the data model.

Supported provider types:

- Independent nutritionist.
- Independent dietitian.
- Independent personal trainer.
- Independent yoga instructor.
- Gym or fitness studio.
- Nutrition clinic.
- Wellness company.
- Dietitian group.
- Corporate wellness organization.

Example structure:

```text
Provider Organization: FitLife Gym
  -> Coach: Arjun, Strength Trainer
  -> Coach: Maya, Yoga Instructor

Provider Organization: HealthyPlate Nutrition
  -> Nutritionist: Priya, Registered Dietitian
  -> Nutritionist: Neha, Weight Loss Coach

Independent Provider:
  -> Ravi, Personal Trainer
```

Recommended product decision:

> Support both individuals and organizations in the backend from day one, but launch with curated individual experts first.

This avoids future rework while keeping marketplace operations simple at launch.

### 58.3 Expert Categories

Nutrition expert categories:

- Registered dietitian.
- Certified nutritionist.
- Weight reduction coach.
- Sports nutrition coach.
- Pediatric nutritionist.
- Diabetes nutrition specialist.
- Family meal planning expert.

Fitness expert categories:

- Strength training coach.
- Personal trainer.
- Yoga instructor.
- Pilates instructor.
- Mobility coach.
- Running coach.
- Senior fitness coach.
- Postpartum fitness coach.
- Sports performance coach.

KitchenOS should distinguish licensed professionals from general wellness coaches. Medical nutrition therapy should require verified credentials.

### 58.4 Marketplace User Flow

Recommended user flow:

```text
User Opens Marketplace
  -> Select Goal
  -> Browse Experts
  -> View Expert Profile
  -> Select Plan
  -> Grant Data Access
  -> Start Chat or Onboarding
  -> Receive Meal or Fitness Plan
  -> Track Progress in KitchenOS
  -> Weekly Check-In
```

Example goal entry points:

- Lose weight.
- Gain muscle.
- Eat healthier.
- Improve family meals.
- Build strength.
- Improve flexibility.
- Manage dietary restrictions.
- Improve protein intake.

### 58.5 Plan Types

Experts should sell structured plans, not only open-ended chat.

Nutrition plan examples:

- One-time meal plan review.
- Monthly weight reduction plan.
- Muscle gain nutrition plan.
- Family nutrition plan.
- Pantry reset plan.
- Diabetes-friendly meal planning.
- Kids lunch planning.

Fitness plan examples:

- 4-week strength training plan.
- Yoga flexibility plan.
- Beginner gym plan.
- Home workout plan.
- Muscle gain coaching.
- Weight reduction fitness plan.
- Mobility and recovery plan.

Hybrid plan examples:

- 12-week muscle gain plan with nutrition and strength training.
- 8-week weight reduction plan with meal planning and workouts.
- Family wellness reset with nutritionist and coach.

### 58.6 Expert Profile Design

Each expert profile should include structured information.

Recommended fields:

- Name.
- Photo.
- Provider type.
- Individual or organization affiliation.
- Credentials.
- Certifications.
- Specialty.
- Languages.
- Location or timezone.
- Remote availability.
- Rating.
- Review count.
- Response time.
- Plan offerings.
- Pricing.
- Accepted goals.
- Safety limitations.
- Verification status.

Example:

```text
Name: Priya Sharma
Type: Registered Dietitian
Specialties:
- Weight reduction
- Family nutrition
- Vegetarian meal planning

Plans:
- 30-day nutrition coaching
- Pantry review
- Weekly meal plan review

Verified: yes
Response time: usually within 12 hours
```

### 58.7 Data Sharing and Privacy

Experts should not automatically see household data. Users must grant explicit access.

Data scopes:

- Goals.
- Allergies.
- Dietary restrictions.
- Meal history.
- Cooked meals.
- Pantry summary.
- Shopping patterns.
- Progress notes.
- Fitness activity if integrated later.

Sensitive data requiring separate approval:

- Medical restrictions.
- Child profiles.
- Receipt details.
- Spending data.
- Weight data.
- Full household member data.

Recommended permission levels:

```text
No Access
Summary Access
Detailed Access
Recommend Access
```

Example:

```text
Nutritionist can view:
- Raj's goal: muscle gain
- Pantry summary
- Meal history
- Allergies

Nutritionist cannot view:
- Full receipts
- Household budget
- Other members' private goals
```

### 58.8 Expert Permissions

Experts should recommend actions, but they should not silently change household data.

Allowed:

- Suggest meal plans.
- Suggest shopping additions.
- Suggest pantry staples.
- Suggest portion changes.
- Send chat messages.
- Create weekly check-ins.
- Review progress.
- Upload plan documents.

Not allowed by default:

- Modify pantry directly.
- Change allergies.
- Change medical constraints.
- Purchase items.
- Modify household budget.
- Edit another member's profile.

Expert recommendations should follow this flow:

```text
Expert Suggestion
  -> KitchenOS Safety Check
  -> User Approval
  -> Applied to Plan, Shopping, or Cook Mode
```

### 58.9 Safety and Legal Boundaries

The marketplace introduces trust, safety, and legal responsibilities.

Nutrition safety requirements:

- Distinguish general wellness coaching from licensed medical nutrition therapy.
- Verify credentials for registered dietitians and medical specialists.
- Escalate sensitive cases such as diabetes, kidney disease, pregnancy, eating disorders, pediatric nutrition, or other medical conditions.
- Avoid medical claims unless the provider is licensed and the product flow is designed for regulated care.

Fitness safety requirements:

- Capture injury history when relevant.
- Capture fitness level.
- Capture equipment availability.
- Capture pregnancy or medical limitations when relevant.
- Include warm-up, cool-down, modifications, and contraindications.

KitchenOS safety guards still apply.

```text
Expert Plan
  -> Ingredient Normalization
  -> Allergy Guard
  -> Medical Constraint Guard
  -> Goal Fit Check
  -> User Approval
```

### 58.10 Provider Data Model

Suggested marketplace data model:

```text
providers
  id
  provider_type
  name
  legal_entity_type
  verification_status

provider_members
  id
  provider_id
  user_id
  role
  status

expert_profiles
  id
  provider_member_id
  expert_type
  specialties
  credentials
  bio
  verification_status

service_offerings
  id
  expert_profile_id
  title
  category
  duration
  price
  includes_chat
  includes_video
  includes_plan_review

client_provider_relationships
  id
  household_id
  user_id
  expert_profile_id
  service_offering_id
  status

consent_grants
  id
  user_id
  household_id
  expert_profile_id
  data_scope
  expires_at

expert_plans
  id
  expert_profile_id
  user_id
  household_id
  plan_type
  status

expert_recommendations
  id
  expert_plan_id
  recommendation_type
  payload
  safety_status
  user_approval_status

chat_threads
  id
  relationship_id
  thread_type
```

This model supports both independent experts and organizations with multiple experts.

### 58.11 Marketplace Launch Phasing

#### Phase 1: Curated Nutrition Experts

- Invite 5–20 verified experts manually.
- Support nutrition coaches first.
- Add expert profiles.
- Add plan purchase.
- Add chat.
- Add expert recommendations with user approval.

#### Phase 2: Fitness Coaches

- Strength training coaches.
- Yoga instructors.
- Home workout plans.
- Goal-linked meal and workout coordination.

#### Phase 3: Organizations

- Gyms.
- Nutrition clinics.
- Wellness companies.
- Multi-coach plans.
- Organization admin dashboards.

#### Phase 4: Open Marketplace

- Public expert onboarding.
- Credential verification workflow.
- Reviews and ratings.
- Search ranking.
- Revenue share.
- Dispute handling.

### 58.12 Navigation Placement

The marketplace should not become a primary tab in the first version.

Recommended placements:

```text
Household
  -> Experts and Coaches
```

Or contextual entry points:

```text
Goal: Muscle Gain
  -> Need help?
  -> Work with a nutritionist or strength coach
```

This keeps the core KitchenOS navigation focused on Home, Plan, Shop, Cook, and Household.

### 58.13 Business Model

Possible monetization paths:

- KitchenOS Premium includes marketplace access.
- Transaction fee on expert plan sales.
- Expert SaaS for client management.
- Organization SaaS for gyms, clinics, and wellness companies.
- Bundled programs such as 8-week muscle gain or 12-week weight reduction plans.

The final product rule:

> Build KitchenOS as the household intelligence layer first, then add a curated expert marketplace where individual experts and organizations can sell plans, chat with users, and make recommendations using permissioned household data.

---

## 59. Negative Flows, Corrections, and Household Timeline

KitchenOS must work when the system or household gets something wrong.

Food systems are messy. Receipts can be scanned twice. A receipt may belong to another household. A shopping item may be added and then removed. Pantry items may be thrown away, spilled, expired, or corrected rather than actually consumed.

The product rule:

> Every automated action must be explainable, reversible, and traceable to its source.

KitchenOS should treat these cases as normal product flows, not edge cases.

These flows rely on the domain-driven event architecture in Section 32. Section 32 defines how events, reversals, read models, and activity entries work; this section defines the user-facing correction behavior.

### 59.1 Correction Philosophy

KitchenOS should not treat every scanned receipt, pantry update, or shopping action as permanent truth.

The architecture should follow this pattern:

```text
Original Event
  -> Correction Event
  -> Updated Household State
  -> Household Timeline Entry
  -> Audit Trail
```

The user-facing language should stay simple:

```text
Costco receipt removed.
8 pantry additions and $84.31 grocery spend were reversed.
```

The backend should preserve enough event history to understand what changed and why.

### 59.2 Duplicate Receipt Flow

Problem:

```text
User scans the same receipt twice.
```

Possible bad outcomes:

- Duplicate pantry additions.
- Duplicate grocery spend.
- Incorrect shopping item completion.
- Wrong consumption and purchase pattern learning.

KitchenOS should detect likely duplicates using:

- Store name.
- Receipt date and time.
- Total amount.
- Item list similarity.
- Receipt image hash.
- OCR text similarity.
- Recently scanned receipts.

Recommended UX:

```text
This looks like a receipt you already scanned from Costco for $84.31.

What would you like to do?

[Ignore Duplicate]
[Merge Missing Items]
[Keep as Separate Receipt]
```

If a duplicate receipt was already applied, KitchenOS should reverse its effects:

```text
receipt_scanned
  -> pantry_items_added_from_receipt
  -> budget_spend_recorded
  -> shopping_items_matched

receipt_marked_duplicate
  -> pantry_receipt_additions_reversed
  -> budget_spend_reversed
  -> shopping_matches_unlinked_if_needed
```

The receipt should be marked as duplicate rather than hard-deleted immediately.

### 59.3 Wrong Household Receipt Flow

Problem:

```text
User scans a receipt that belongs to another household, friend, office, or trip.
```

This is not the same as a duplicate. The receipt is real, but it should not affect this household.

Recommended UX:

```text
This receipt added:
- 12 pantry items
- $64.20 grocery spend
- 3 completed shopping items

Remove this receipt from this household?

[Remove Receipt Effects]
[Keep Receipt]
```

Optional future action:

```text
[Move to Another Household]
```

Only show this if the user belongs to more than one household.

Backend behavior:

```text
receipt_removed_from_household
  -> pantry_items_from_receipt_reversed
  -> budget_spend_reversed
  -> shopping_matches_unlinked
  -> household_learning_suppressed_for_receipt
```

The Household Timeline should show:

```text
Receipt removed by Raj.
Reason: Wrong household.
```

### 59.4 Shopping List Deletion Flow

Shopping list removal is a normal behavior, not always a data error.

A user may remove an item because:

- It is no longer needed.
- The meal plan changed.
- It is already available at home.
- It is too expensive this week.
- The item was added by mistake.
- The AI suggestion was not useful.

Recommended lightweight UX:

```text
Milk removed from shopping list.
[Undo]
```

Optional reason capture:

```text
Why remove this?

[Already Have It]
[Not Needed]
[Too Expensive]
[Wrong Item]
```

Backend behavior:

```text
shopping_item_added
shopping_item_removed
removal_reason_optional
```

If the item was AI-suggested, the system should record:

```text
ai_suggestion_rejected
```

KitchenOS should learn gently from removals. One deletion should not permanently suppress future suggestions.

### 59.5 Pantry Removal Reason Flow

Pantry quantity reductions must distinguish real consumption from loss, waste, and correction.

Removal reasons:

- Used in cooking.
- Eaten directly.
- Expired.
- Spoiled.
- Thrown away.
- Spilled.
- Given away.
- Moved.
- Incorrect entry.

Recommended UX:

```text
Why is this item gone?

[Used in Cooking]
[Eaten]
[Expired]
[Spoiled]
[Thrown Away]
[Incorrect Entry]
```

Fast UX option:

```text
Removed yogurt.
Reason: Used/Eaten
[Change Reason]
[Undo]
```

Learning behavior:

```text
Consumed
  -> affects usage pattern

Cooked
  -> affects recipe and meal learning

Expired or Spoiled
  -> affects waste analytics

Thrown Away or Spilled
  -> affects loss/waste, not preference

Incorrect Entry
  -> correction only, should not affect consumption learning
```

This prevents KitchenOS from learning the wrong behavior when kids spill food or items are trashed accidentally.

### 59.6 Household Timeline as Event Log

The Household Timeline is the user-facing event log of the household.

It answers:

```text
What changed?
Who changed it?
Why did it change?
Can I undo or correct it?
```

Recommended placement:

```text
Household
  -> Activity
```

Example timeline:

```text
Today

Receipt scanned from Costco
8 pantry items added · $84.31 recorded
[View] [Undo] [Mark as duplicate]

Milk removed from shopping list
Removed by Priya
[Undo]

Greek yogurt quantity changed
2 tubs -> 0 tubs
Reason: Thrown away
[Change reason]

Dinner completed
Chicken rice bowl cooked
Pantry updated automatically
[View changes]
```

The Household Timeline should show grouped human-readable actions, not raw technical events.

### 59.7 Household Timeline vs Audit Log

The Household Timeline is for user trust.

The audit log is for system truth.

```text
Event Ledger
  -> detailed technical events
  -> immutable or append-only
  -> used for sync, debugging, compliance, and state reconstruction

Household Timeline
  -> grouped user-readable timeline
  -> supports view, undo, change reason, and remove effects
  -> used for trust and correction
```

Example technical events:

```text
receipt_scanned
receipt_ocr_completed
receipt_items_detected
pantry_items_added
budget_spend_recorded
shopping_items_matched
```

User-facing Household Timeline entry:

```text
Costco receipt scanned.
8 pantry items added, 3 shopping items completed, $84.31 recorded.
```

### 59.8 Event Provenance

Every meaningful state change should record where it came from.

Suggested source types:

```text
receipt_scan
manual_entry
ai_suggestion
shopping_action
cook_mode
expert_recommendation
correction
sync_conflict_resolution
```

Example:

```text
Pantry item: Greek yogurt
Added by: receipt_scan
Receipt ID: r_123
Confidence: high
Applied by: Raj
```

This lets KitchenOS reverse only the affected changes.

### 59.9 MVP-1 Trust Scope

MVP-0 should include basic Household Timeline entries and simple undo for low-risk actions where practical.

MVP-1 should include the minimum correction layer needed for trust.

MVP-1 must have:

- Duplicate receipt detection if receipt metadata extraction is included.
- Remove receipt and reverse effects.
- Undo for shopping list deletion.
- Pantry removal reason.
- Household Timeline under Household.
- Correction events instead of hard deletes.

Post-MVP can add:

- Receipt merge.
- Move receipt to another household.
- Advanced audit trail.
- AI anomaly detection.
- Child-specific pantry events.
- Waste analytics by reason.
- Learning suppression for corrected events.

The final product rule:

> The household state is not just what happened. It is what happened, why it happened, who or what caused it, and whether it should affect future recommendations.

---

## 60. Decision Register and Open Questions

### Locked Product Decisions

- Cook Mode is the primary MVP-0 habit loop.
- Household Timeline is a first-class product surface under Household and can be surfaced from Home after important changes.
- Events should be captured from day one through an append-only `domain_events` table.
- MVP-0 should prove the core food loop before advanced nutrition, marketplace, or automation.
- MVP-1 should add correction, reversal, trust, and safety layers.
- Expert marketplace is post-MVP and should not become a primary navigation tab at launch.
- Expert recommendations require KitchenOS safety checks and user approval before affecting plans, shopping, or Cook Mode.

### Product Open Questions

- Should Pantry remain visible or stay inside Household?
- How much budget functionality belongs in MVP-0 versus MVP-1?
- Which nutrition goals should MVP-1 support first, if any?
- Should expert access be part of KitchenOS Premium or a separate marketplace purchase?

### UX Open Questions

- Should users review all receipt items or only uncertain items?
- Should Cook Mode auto-deduct pantry quantities or require confirmation?
- How prominently should the Household Confidence / State indicator appear?
- Should meal planning always ask who is eating, or only when safety or goals require it?
- Should goals appear in onboarding or after the first successful meal loop?
- How should users approve expert recommendations before they affect meal plans or shopping lists?
- Which actions should support one-tap undo?

### AI Open Questions

- How proactive should AI recommendations be?
- Should users see confidence scores?
- Should there be conservative vs aggressive AI modes?
- How should AI explain conflicts between goals, allergies, pantry, and budget?
- Should AI summarize household context for experts, and how much user approval is required?
- How should AI avoid learning from corrected, duplicate, or wrong-household events?

### Engineering Open Questions

- Should MVP use NestJS or Express for speed?
- How strict should MVP event sourcing be beyond the append-only `domain_events` table?
- What is the minimum sync engine required for MVP?
- How should offline conflicts be handled in the first release?
- How deep should ingredient normalization be in MVP-1?
- Should marketplace chat be built in-house or integrated through a third-party messaging provider?
- How should expert recommendations be represented in the event ledger?
- How should receipt effect reversal be modeled across pantry, shopping, budget, and learning systems?
- Which Household Timeline entries should be persisted as a read model versus generated from grouped events on demand?

### Privacy Open Questions

- Which household members can see spending?
- Which household members can edit pantry and meal plans?
- Should receipt OCR be cloud-only at MVP?
- What data should be encrypted locally?
- Which household members can view allergies, medical restrictions, and body goals?
- What household data can experts access by default?
- Should expert data access expire automatically?
- How should child profile access be protected?
- Which household members can view the full Household Timeline?

### Marketplace Governance

- What credentials are required for each expert category?
- Who verifies nutritionist, dietitian, trainer, and yoga instructor credentials?
- How are refunds, disputes, and low-quality plans handled?
- What safety disclaimers are required for nutrition and fitness plans?
- Can organizations manage multiple experts under one account?

---

## 61. Recommended Next Documents

The older source suggested several next directions. Based on product readiness, the recommended sequence is:

1. **Sprint-by-sprint engineering execution plan.**
2. **Database schema and API contracts in full detail.**
3. **Clickable UI wireframes screen-by-screen.**
4. **First production-ready architecture repo structure.**
5. **Investor pitch deck version.**

---

## 62. One-Line Product Summary

KitchenOS is an AI-powered household food operating system that learns from what a household buys, stores, cooks, consumes, and corrects to help people make safer, healthier, and easier food decisions with less effort.
