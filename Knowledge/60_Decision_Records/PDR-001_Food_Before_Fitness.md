---
id: PDR-001
title: Food Decisions Before Fitness Features
type: pdr
status: accepted
owner: product
depends_on: []
referenced_by: [PDR-002]
tags: [product-strategy, scope, food, fitness, marketplace, household-decision-engine]
date: 2026
---

# PDR-001: Food Decisions Before Fitness Features

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product

---

## Context

KitchenOS has a natural adjacency to fitness: nutrition goals, body-composition planning, and expert coaching all connect food decisions to physical outcomes. Early product discussions explored whether KitchenOS should position itself as a holistic wellness platform covering both nutrition and fitness from the start.

The Expert Marketplace feature in particular creates a path toward fitness coaches, gym trainers, and yoga instructors — not just nutritionists and dietitians.

The question was: should KitchenOS own the fitness domain alongside food, or should food come first?

---

## Decision

**KitchenOS focuses on food decisions first.** Fitness features — wearable integration, workout logging, macro targeting, fitness coaching — may exist as supporting context but must always serve food decisions, not the other way around.

The product boundary rule:

> KitchenOS owns household food decisions. Broader wellness and fitness features strengthen those food decisions. They do not replace the core product with a generic fitness, medical, or coaching platform.

---

## Reasons

**The problem space is already large.** Pantry management, receipt scanning, meal planning, shopping intelligence, Cook Mode, allergy safety, household sync, and offline support represent a full product by themselves. Adding fitness as a first-class domain during MVP splits focus before the core is proven.

**Food decisions are the defensible moat.** Household pantry context — what was bought, cooked, consumed, and corrected over time — is unique to KitchenOS. No fitness app has this context. Household food behaviour data is the foundation that makes expert advice, AI recommendations, and coaching genuinely personalised. Building the food data layer first makes every future fitness feature more valuable.

**Fitness apps already exist.** MyFitnessPal, Cronometer, Strava, and Apple Health own fitness tracking. KitchenOS competing in that space from day one means competing with mature, entrenched products on their home ground. Food intelligence, especially at the household level, is underserved.

**The Expert Marketplace connects, not competes.** Fitness coaches on the KitchenOS marketplace succeed because they can access permissioned household food data — a capability no fitness app offers. This is only valuable if the food data layer is rich, which requires food-first investment.

**Nutrition goals are food decisions.** Muscle gain, weight reduction, and healthier eating all express themselves as food choices: what to buy, what to cook, what to eat. KitchenOS can support these goals entirely through food decisions without becoming a fitness app.

---

## Alternatives Considered

**Fitness-first positioning** — Rejected. Fitness tracking is a solved market. KitchenOS has no competitive advantage in step counting or workout logging.

**Simultaneous food and fitness** — Rejected. Splitting scope during MVP increases risk without proportional benefit. Food context is prerequisite to meaningful fitness context.

**Generic wellness platform** — Rejected. Wellness is too broad a category. KitchenOS needs a specific, defensible identity. "Household food intelligence" is specific; "wellness" is not.

---

## Consequences

**Positive:**
- MVP scope stays manageable and focused on a coherent value proposition.
- Household food data accumulates before fitness features are added, making them more valuable when they arrive.
- Expert Marketplace launches with nutritionists and dietitians as primary providers — the strongest fit for the core product.

**Negative:**
- Fitness coaches who want workout tracking alongside nutrition plans will find KitchenOS incomplete at launch.
- Users with primarily fitness goals (not food goals) are a lower-priority segment in MVP.

**Scope boundary:**
- Fitness context (wearable data, workout type, activity level) may be used as *input* to food decisions (e.g., calorie-adjusted meal suggestions after a workout) post-MVP.
- KitchenOS will not own fitness logging, workout tracking, or fitness progress visualisation.

---

## Related

- `10_Product_Vision.md`, Section 5 (Product Vision)
- `10_Product_Vision.md`, Section 57 (Nutrition Goals — food-first expression of fitness goals)
- `10_Product_Vision.md`, Section 58 (Expert Marketplace — food-first coaching)
- PDR-002: Household as primary unit
