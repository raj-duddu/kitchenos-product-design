---
id: ADR-001
title: Flutter for Mobile
type: adr
status: accepted
owner: architecture
depends_on: []
referenced_by: [ADR-002, ADR-012]
tags: [mobile, flutter, dart, offline, firebase, riverpod, sqlite]
date: 2026
---

# ADR-001: Flutter for Mobile

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

> **Amended 2026-07-03:** the mention of Cloud Vision API among the Google-integration benefits is overtaken by ADR-012 — receipt extraction is now Document Understanding via a multimodal LLM behind the AI Provider Abstraction. The Flutter decision is unaffected. See History.

---

## Context

KitchenOS is a mobile-first consumer application. The primary surfaces — Home, Cook Mode, Pantry, Shopping, Household Timeline — are all native mobile experiences requiring fluid animation, offline capability, camera access (receipt scanning), and push notifications.

A cross-platform mobile framework was required. The main candidates were:

- **Flutter** (Google, Dart)
- **React Native** (Meta, JavaScript)
- **Native iOS + Android** (Swift + Kotlin, two separate codebases)

---

## Decision

**Flutter** was chosen as the mobile framework for KitchenOS.

---

## Reasons

**Single codebase, native performance.**
Flutter compiles to native ARM code. It does not use a JavaScript bridge like React Native. This gives Cook Mode, animations, and camera flows the performance consistency that a kitchen-facing app requires.

**Widget-level UI control.**
Flutter owns every pixel it renders. KitchenOS requires custom UI surfaces (Cook Mode step cards, Household Timeline event entries, pantry cards) that are difficult to build reliably with native component wrappers.

**Firebase and Google ecosystem integration.**
Firebase Authentication, Firebase Cloud Messaging (push notifications), and Google Cloud Vision API (receipt OCR) are all core to the MVP-0 stack. Flutter has first-class Firebase SDKs with minimal configuration. Flutter is a Google product; the Firebase Flutter SDK is maintained by the same organisation.

**Offline-first capability.**
Flutter pairs with SQLite via the Drift library, enabling local database persistence, pending sync event queuing, and offline pantry and shopping list access — all required for the offline-first architecture.

**Dart is learnable.**
Dart is a typed, structured language. Engineers familiar with TypeScript, Kotlin, or Swift can become productive quickly. The learning curve is lower than switching from JavaScript to native Swift/Kotlin.

**Single team, single codebase.**
A small founding team cannot maintain two separate native codebases. Flutter enables one team to ship both iOS and Android simultaneously.

---

## Alternatives Considered

**React Native:**
Mature ecosystem, large community, JavaScript/TypeScript familiarity. Rejected because the JavaScript bridge introduces performance unpredictability for animation-heavy flows (Cook Mode). The Metro bundler and bridge architecture are also a source of debugging complexity that a small team does not want to manage.

**Native iOS + Android:**
Best possible performance and platform integration. Rejected because it requires two separate codebases, two separate engineering tracks, and significantly higher hiring cost for a startup with limited engineering headcount.

---

## Consequences

- All mobile engineers must know Dart and Flutter.
- State management uses Riverpod (reactive, testable, compile-safe).
- Local database uses SQLite via Drift (type-safe, migration-aware).
- The offline sync layer (pending event queue, local SQLite ↔ Cloud SQL) must be designed and maintained as part of the Flutter app architecture.
- Flutter widget tests provide fast UI testing without a device — this is a significant advantage for CI/CD pipeline speed.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026 | Accepted | Founders, Product Architect | pre-dates History enforcement |
| 2026-07-03 | Amended — Cloud Vision mention overtaken by ADR-012; decision unaffected | @raj-duddu | PR # (add on merge) |

---

## Related

- ADR-002: GCP (Firebase is a GCP product; the two decisions are aligned)
- Main doc, Section 37.1: Mobile Technology Stack
- Main doc, Section 42.1: MVP-0 Mobile Stack
- Main doc, Section 22: Offline UX
- Main doc, Section 37.8: Offline AI Context Constraint
