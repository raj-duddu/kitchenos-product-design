---
id: COMPANY-001
title: Operating Principles
type: company-constitution
status: active
owner: founders
scope: company-wide
applies_to: [KitchenOS, HealthOS, FinanceOS, LearningOS, all future products]
date: 2026
---

# Operating Principles

> **These are not product requirements. They are not architecture decisions. They are not governance rules.**
> They are enduring statements of company identity. They shape everything else — products, governance, architecture, and engineering.
> They do not have "alternatives considered." They are not superseded by PDRs or ADRs.
> When a product decision, architecture choice, or engineering practice conflicts with these principles, the principle wins.

See `Company/Vision_and_Mission.md` for the Vision, Mission, and Philosophy that these principles operationalise.

---

## 0. Reveal Better Possibilities

People often know what they are trying to accomplish, but not what is actually possible. Our role is to reveal it.

The best products we can build will not be answers to questions users consciously asked. They will be opportunities users couldn't reasonably have discovered on their own. A household doesn't think "I have an information orchestration problem involving pantry state, nutrition goals, expiry risk, and decision fatigue." They think cooking dinner is just part of life. Our job is to reveal that it doesn't have to be that hard — and that a better path exists.

This is why we are a **decision intelligence company**, not merely a problem-solving company. The distinction matters:

- A conventional problem-solving company waits for users to articulate pain, then removes it.
- A decision intelligence company surfaces better possibilities that users couldn't easily see for themselves — preventing future problems, uncovering hidden opportunities, reducing cognitive load before it becomes friction.

> *"You can cook four meals this week without shopping."*
> *"This habit is affecting your sleep."*
> *"You're two concepts away from understanding this topic."*

In every case, we are not responding to a stated complaint. We are revealing a better decision the user couldn't have made without us.

This principle is the foundation beneath all others. Transforming complexity, turning information into guidance, inspiring confident action — all of these presuppose that we are revealing something genuinely worth seeing. A product that is beautifully designed, technically excellent, and ethically built, but reveals nothing of value to anyone, is not a product. It is an exercise.

This principle governs product discovery, research, feature prioritisation, and the validation gate in the Product Development Lifecycle.

---

## 1. Transform Complexity into Clarity

Life is complex. Information is abundant. Understanding is scarce.

Our job is not to give users more data — it is to transform the complexity of their context (pantry state, nutrition goals, household constraints, finances, learning paths) into clear, actionable understanding. A user should leave every interaction knowing something useful that they did not know before, or having made a decision they would not have made as confidently without us.

If a feature adds complexity without reducing it elsewhere, it is not aligned with this principle.

---

## 2. Turn Information into Guidance

Raw information has no value to users. Guidance does.

A list of ingredients is information. "You can make three dinners this week without shopping" is guidance. A calorie count is information. "This meal keeps you on track for your goal and works for everyone in your household" is guidance.

Every product surface we build must answer the implicit question the user is standing in front of: *what should I do?* Not: *here is what we know.*

We measure success not by data collected but by decisions improved.

---

## 3. Inspire Confident Action

The outcome of good guidance is confident action — a decision made with enough understanding and trust that the user acts on it without anxiety or second-guessing.

We do not build products that make users feel surveilled, optimised, or dependent. We build products that make users feel capable. The user who has relied on our products for a year should feel more confident about their decisions — not more reliant on the app to make them.

This principle governs how recommendations are framed, how uncertainty is communicated, and how much agency the user retains at every step.

---

## 4. AI Recommends. People Decide.

We build intelligence that assists human judgment — not intelligence that replaces it.

No AI action in any product we build is irreversible without human confirmation. No AI output is presented as a directive. Every recommendation carries the implicit message: *here is what we know; you decide what to do with it.*

This applies equally whether we are recommending a dinner, a financial action, a health protocol, or a learning path. We do not diagnose, prescribe, or act as a licensed professional in any regulated field.

This principle is implemented as GDR-001.

---

## 5. Earn Trust Through Transparency

Trust is not claimed. It is earned — through accuracy, explainability, and respect for user agency.

Every recommendation must be explainable. If the system cannot explain why it made a recommendation, it should not make it. The user must always be able to ask "why?" and receive a meaningful answer. The Household Timeline, correction events, undo, and confidence indicators are all trust infrastructure — not UX polish.

Trust is also lost through overreach: collecting data beyond what serves the user, personalising beyond what the user has consented to, or acting autonomously in ways the user did not expect. We do not build in ways that erode trust for short-term engagement gains.

Privacy is designed in, not added later. This principle is implemented as GDR-002 and ADR-009.

---

## 6. Learn Continuously

Our products get smarter over time — and so does the company. But learning must be earned, not extracted.

At the product level: we learn from interactions that produce better outcomes for the user, within the permissions they have granted. An accepted recommendation is a signal. A correction is a stronger one. A rejection tells us something important. We do not treat every user action as surveillance data — we treat it as feedback within a relationship of consent.

At the company level: we treat research, user feedback, and market signals as first-class inputs. `Research/` is a first-class folder in this repository for a reason. Decisions made without current evidence are assumptions, not strategy.

At the AI level: models are evaluated, monitored, and updated. A model that was good enough last year may not be good enough today. We do not treat AI deployment as a one-time act.

---

## 7. Truth Before Convenience

We build systems that respect reality, even when reality is inconvenient.

If the AI is uncertain, we say so — we do not present a low-confidence recommendation as if it were certain. If pantry data is stale, we show it — we do not silently serve outdated context. If a recommendation changed because the household's situation changed, we explain why — we do not pretend continuity where there is none. If a model cannot produce a good answer, we say nothing — we do not hallucinate a plausible one.

This is one of our strongest competitive differentiators. Users trust systems that acknowledge what they do not know. The Household Timeline, correction events, confidence scores, staleness indicators, and the event sourcing architecture are all expressions of this principle. They exist because reality is the source of truth — not the system's best guess.

We never fake certainty. We never suppress inconvenient facts to make an interface feel cleaner. We build systems that tell the truth.

---

## 8. We Are Stewards, Not Owners

Users entrust us with their household's pantry, their children's dietary needs, their health goals, their spending habits, their routines. This is not data. It is trust.

We treat that trust as something entrusted to us — not owned by us. We collect it to serve the user. We hold it only as long as it continues to serve them. We protect it as if it were our own. We make it exportable and deletable on request, completely and promptly, subject only to legitimate legal, security, or operational retention requirements.

This distinction matters because ownership implies rights. Stewardship implies responsibility. We have no rights over user data. We have a responsibility to protect and serve it.

This principle governs data retention policies, deletion architecture, consent design, and every decision about what we collect and why. It is stronger than privacy compliance — privacy is an implementation of stewardship, not a substitute for it.

---

## 9. Simplicity Is a Feature

Every interaction should feel effortless. Complexity that we absorb on the user's behalf is the product. Complexity we expose to the user is a failure.

When we must choose between a richer feature and a simpler experience, we choose simplicity unless there is a compelling, evidence-based reason not to. The most valuable thing we can do for a user is reduce the number of decisions they need to make consciously — not increase the number of features they need to navigate.

This principle governs product scope, UX design, onboarding, and AI interaction patterns.

---

## Derived Principles

These are not independent principles — they are direct consequences of the ten above. They are stated explicitly because they govern specific architectural and product decisions, and we want the connection to the parent principle to be traceable.

### Privacy is designed in, not added later

A consequence of Principle 8 (We Are Stewards, Not Owners) and Principle 5 (Earn Trust Through Transparency). User data is collected only when it enables a better outcome for that user. Identity is isolated from intelligence. The system is built so that a breach of one layer does not expose another.

Implemented as GDR-002 and ADR-009.

### Wellbeing over engagement

A consequence of Principle 3 (Inspire Confident Action) and Principle 9 (Simplicity Is a Feature). We do not optimise for time-in-app, notification volume, or engagement metrics that conflict with user wellbeing. A product that helps a household make one better decision per week and then stays out of the way is more successful than one that generates daily engagement through anxiety or friction.

### The household is the unit. The person is the agent.

A consequence of Principle 4 (AI Recommends. People Decide.) applied to our specific domain. Our products are built for households — shared living contexts where decisions affect multiple people. But the individual person retains agency, privacy, and control. The tension between household-level intelligence and individual-level privacy is a design constraint we embrace, not a problem we avoid.

Implemented as PDR-002, ADR-011, and the Domain Model.

---

## How These Principles Are Used

Operating Principles are evaluated in every significant decision.

When writing a **GDR, ADR, PDR, UXDR**, or **EDR**, the author must identify which operating principles influenced the decision. This is not a checkbox — it is a quality signal. A decision record that cannot trace itself to at least one operating principle is probably not grounded in the company's purpose.

**When a proposed decision conflicts with an operating principle:**
The conflict must be explicitly documented in the decision record. It must be escalated to the founders. It cannot be resolved by ignoring the principle — it can only be resolved by a deliberate, documented exception that explains why the specific circumstance justifies the deviation.

This turns these principles from an inspirational document into an operational one. They are part of the engineering workflow — not something written once and forgotten.

```text
Better possibility identified (Principle 0)
        │
        ▼
Decision required (GDR / ADR / PDR / UXDR / EDR)
        │
        ▼
Which principles apply?
        │
        ▼
Does the proposed decision align with them?
        │
    Yes │         No
        │          └──► Document the conflict explicitly
        ▼                 └──► Escalate to founders
Proceed                         └──► Deliberate exception or redesign
```

---

## How These Principles Relate to Other Documents

| Principle | Implemented in |
|---|---|
| Reveal Better Possibilities | Product Development Lifecycle (`Process/Product_Development_Lifecycle.md`), Discovery stage; `Research/` |
| Transform Complexity into Clarity | Product Vision (`Products/KitchenOS/10_Product_Vision.md`), North Star Metric |
| Turn Information into Guidance | Product Vision, Household Decision Engine (`Products/KitchenOS/40_Technical_Architecture.md` Section 24) |
| Inspire Confident Action | Product Vision, UX Design System, Recommendation framing |
| AI Recommends. People Decide. | GDR-001, AI Governance (`Company/Governance/AI_Governance.md`) |
| Earn Trust Through Transparency | GDR-001, GDR-002, Household Timeline, Correction architecture (ADR-004, ADR-010) |
| Learn Continuously | Intelligence Layer (`Products/KitchenOS/20_Domain_Model.md`), AI Governance, `Research/` |
| Truth Before Convenience | Confidence scores, staleness indicators, correction events, event sourcing (ADR-004), AI Governance |
| We Are Stewards, Not Owners | GDR-002, ADR-009, data retention policy (`Company/Governance/Risk_Register.md`) |
| Simplicity Is a Feature | Product Vision, UX Design System, PDR-005 |
| Privacy by design | GDR-002, ADR-009 |
| Wellbeing over engagement | Product Vision, North Star Metric, Risk Register |
| Household as unit, person as agent | PDR-002, ADR-011, Domain Model |
