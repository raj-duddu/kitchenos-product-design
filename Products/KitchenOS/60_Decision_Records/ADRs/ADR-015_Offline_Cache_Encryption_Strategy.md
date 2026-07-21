---
id: ADR-015
title: Offline Cache Encryption Strategy — Hardware-Backed Keys via Secure Enclave / Android Keystore
type: adr
status: accepted
owner: architecture
depends_on: [ADR-009, ADR-014]
referenced_by: []
operating_principles: ["7. Truth Before Convenience", "8. We Are Stewards, Not Owners"]
tags: [offline, encryption, sqlcipher, secure-enclave, android-keystore, security, data-at-rest]
date: 2026
---

# ADR-015: Offline Cache Encryption Strategy — Hardware-Backed Keys via Secure Enclave / Android Keystore

**Status:** Accepted
**Date:** 2026-07-21
**Deciders:** Product Architect, Founder
**Stage Gate:** Stage 5 of Product Development Lifecycle
**Operating Principles:** 7 (Truth Before Convenience), 8 (We Are Stewards, Not Owners)

---

## Context

KitchenOS is offline-first: household data (pantry, meal plans, shopping lists, budget, timeline) must be cached locally on-device and remain readable while offline, per the offline-first architecture already established (TA §35, Vision §22A). Because this cache holds sensitive household information, it must be encrypted at rest — not merely relying on OS-level protections.

An early draft of the session/offline specification (TA §37.B) derived the SQLite encryption key by combining the device passcode with a constant, `APP_SECRET`, embedded in client configuration. An external technical review identified that this provides no real additional protection: any value shipped inside an app binary can be recovered through decompilation or runtime inspection, regardless of how it is encoded or how many rounds of key-stretching are applied downstream. The "secret" is not actually secret once the app ships.

This ADR records the corrected key-management approach, and formally establishes SQLCipher — not previously listed anywhere in the Technology Stack (TA §37) — as the offline encryption library for locally cached sensitive data.

---

## Decision

**We will encrypt the offline SQLite cache at rest using SQLCipher (AES-256), with the encryption key generated and held entirely inside the platform's hardware-backed keystore — iOS Secure Enclave, Android Keystore — gated by the device's biometric/PIN lock. No key material, and no constant used to help derive it, is ever embedded in application code or configuration.**

If a device has no passcode or biometric configured, the app must explicitly warn the user that offline household data is not protected at the app level, rather than silently deriving a weaker key and implying full protection.

---

## Reasons

- A key derived even partly from a client-embedded secret provides no real protection once the app binary is available to an attacker — the apparent extra step (PBKDF2 over passcode + `APP_SECRET`) does not compensate for the fact that `APP_SECRET` itself is recoverable.
- Hardware-backed keystores (Secure Enclave, Android Keystore) are specifically designed so key material never leaves the secure hardware boundary — not even the OS can extract it; it can only request an operation be performed using it.
- Gating key access on the same biometric/PIN challenge already required for session resume (ADR-014) ties offline data access to proof of device possession, consistent with GDR-002 §7 (Breach Containment), and gives the system one consistent re-authentication boundary instead of two separate ones.
- An explicit warning when no device lock exists is more honest than a silent fallback that gives users false confidence in protection a device thief could trivially defeat — directly implementing Principle 7 (Truth Before Convenience).
- SQLCipher is a proven library (used in variants by Signal, WhatsApp, and Wire) and was already the intended choice; this ADR corrects the key management around it and formalizes the library itself as part of the technology stack, since it was previously undocumented outside TA §37.B.

---

## Alternatives Considered

### Option A: Client-embedded `APP_SECRET` combined with device passcode (original design, rejected)

A constant baked into app code or configuration, combined with the device passcode, fed through PBKDF2 to derive the SQLCipher key.

Rejected because: any value shipped inside the app binary can be extracted through decompilation or runtime inspection. This provides only the appearance of an additional security layer, not real protection — the actual key strength collapses to whatever can be derived from the device passcode alone, which an attacker with the device may already have.

### Option B: No app-level encryption; rely on OS full-disk encryption only

Do not encrypt the SQLite database file itself; rely on iOS/Android full-device encryption, which is enabled by default on most modern devices.

Rejected because: full-disk encryption only protects data while the device is powered off or locked at the OS level. Once a device is unlocked — by the account owner, or by anyone who has the passcode — any app-level exploit or direct file-system access exposes the plaintext database. Given the sensitivity of cached household data (allergies, budget, health goals), an additional app-level encryption layer independent of OS lock state is warranted.

### Option C: Server-side-only storage, no offline cache

Do not cache household data locally at all; require connectivity for all reads.

Rejected because: this directly contradicts the offline-first architecture already established (TA §35, Vision §22A) and would regress core product functionality — for example, viewing pantry or meal plans while offline, such as in a store with no signal.

### Option D: Hardware-backed key without a biometric/PIN gate

Generate the key in Secure Enclave/Keystore, but let the OS release it automatically whenever the app requests it, with no re-authentication requirement.

Rejected because: this would allow any process running as the app — or anyone who has unlocked the device even once — indefinite access to decrypt the cache, undermining the biometric re-authentication model established in ADR-014 for the exact same threat (a lost or stolen, unlocked device).

---

## Consequences

### Positive

- The offline cache is genuinely protected by hardware-backed encryption, not a client-side secret that provides false assurance.
- A single, consistent security boundary: the same biometric/PIN challenge gates both session resume (ADR-014) and offline cache access.
- SQLCipher is now formally established in the Technology Stack (TA §37) as the offline encryption library, available for any future feature that also caches sensitive data locally.

### Negative

- Devices without a passcode or biometric configured cannot receive the same protection level; the app must degrade gracefully with an explicit warning rather than pretending full protection exists.
- Slightly more platform-specific implementation work, since Secure Enclave APIs (iOS) and Android Keystore APIs differ, compared to a single cross-platform constant.

### Risks

- **Key loss on OS-level biometric reset or account changes:** some OS-level events (e.g., resetting enrolled biometrics) can invalidate hardware-backed keys. Mitigation: the local cache is a cache, not the source of truth — it can be safely wiped and re-synced from the server via the Sync Engine (TA §35) if the key becomes unrecoverable.
- **No device lock configured:** users who have not set a device passcode receive a materially weaker (or absent) protection guarantee. Mitigation: explicit in-app warning at first use; this is a deliberate degrade-with-warning, not a silent gap.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-21 | Proposed | Product Architect | Session/offline-cache architecture review and resolution conversation |
| 2026-07-21 | Accepted | Founder | Same review conversation — hardware-backed key approach confirmed, `APP_SECRET` design rejected |

---

## Related

- `Products/KitchenOS/40_Technical_Architecture.md`, §37.B.4 (Offline Cache Encryption)
- `Products/KitchenOS/40_Technical_Architecture.md`, §35 (Offline Architecture)
- ADR-014: Session Continuity Model — shares the same biometric/PIN gate
- ADR-009: Privacy-by-Design — Identity Isolation
- `Company/Governance/GDRs/GDR-002_Privacy_By_Design.md`, §7 (Breach Containment)

---
