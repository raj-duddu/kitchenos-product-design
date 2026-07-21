---
id: ADR-014
title: Session Continuity Model — Single Active Session, Biometric-Gated Resume
type: adr
status: accepted
owner: architecture
depends_on: [ADR-009]
referenced_by: [ADR-015]
operating_principles: ["5. Earn Trust Through Transparency", "7. Truth Before Convenience", "8. We Are Stewards, Not Owners", "9. Simplicity Is a Feature"]
tags: [authentication, session-management, security, multi-device, biometric, jwt, refresh-token]
date: 2026
---

# ADR-014: Session Continuity Model — Single Active Session, Biometric-Gated Resume

**Status:** Accepted
**Date:** 2026-07-21
**Deciders:** Product Architect, Founder
**Stage Gate:** Stage 5 of Product Development Lifecycle
**Operating Principles:** 5 (Earn Trust Through Transparency), 7 (Truth Before Convenience), 8 (We Are Stewards, Not Owners), 9 (Simplicity Is a Feature)

---

## Context

KitchenOS needs a session model for a household app used across phone, tablet, and other devices. Two distinct architectural questions had to be resolved:

1. Can more than one device hold an active session for the same identity at the same time?
2. Does restarting the app force full re-authentication, or can the session resume from a stored token?

Both questions were answered inconsistently across the authentication specification. Technical Architecture §37.A originally stated a single-session-per-user policy and no session persistence across app restart. A later addition (TA §37.B, written to formalize the JWT/session-token specification) contradicted both: it described concurrent multi-device sessions as normal, and introduced a 30-day refresh token whose only purpose is to resume a session — implying persistence across restart that the same document elsewhere denied.

An external technical review surfaced both contradictions and proposed resolving them by changing the underlying product decisions (allow concurrent multi-device sessions; let the refresh token silently resume sessions with no gate). Before accepting that framing, the two questions were evaluated on their own merits — including a review of how comparable apps (productivity, banking, and household/health apps) actually handle this today — and resolved deliberately rather than adopted by default. This ADR is the permanent record of that resolution.

---

## Decision

**We will enforce a single active session per identity across all devices, and we will let sessions resume across app restart via a refresh token held in the platform's secure hardware storage, gated by a mandatory biometric/PIN challenge rather than a full re-login.**

Specifically:

- A new login on any device immediately revokes the session on every other device for that identity. There is no concurrent multi-device session in MVP-0.
- The refresh token (stored in iOS Keychain / Android Keystore) survives an app restart. On cold start (app process killed and relaunched), the app always requires a fresh biometric/PIN check before showing any household data — regardless of how much time has elapsed. This is distinct from mere backgrounding, which uses a 15-minute idle window before re-prompting (see TA §37.B.3).
- Full email/password (or social) re-login is required only when: the refresh token has expired (30-day absolute ceiling), the session was explicitly revoked ("Sign Out All Devices"), the user explicitly logged out, or refresh-token reuse is detected (indicating possible theft).

---

## Reasons

- A single-session model keeps "who currently has access to this household's sensitive data" a one-line, auditable answer at all times — directly supporting Principle 8 (We Are Stewards, Not Owners) and reducing breach surface per GDR-002 §7 (Breach Containment).
- Concurrent multi-device sessions would double the number of live sessions to track, secure, and revoke, and would require additional MVP-0 scope (an explicit "sign out other devices" control, cross-device login notifications) that was not otherwise planned.
- Biometric-gated resume — rather than forcing full re-login on every app restart — matches how apps handling sensitive-but-not-financial data behave in current industry practice (see Related). It also gives the 30-day refresh token an actual purpose; without it, the refresh token would be dead weight in the design, which was itself evidence that the original two descriptions were in genuine conflict, not just phrased differently.
- Forcing full re-login on every app restart (the strictest banking-app pattern) was evaluated and rejected as unnecessary friction for KitchenOS's data sensitivity tier.
- Leaving the two contradictory descriptions to coexist across TA §37.A and §37.B was not a viable option — an unresolved contradiction in the authoritative architecture document cannot be implemented; engineering would have to guess which policy is real.

---

## Alternatives Considered

### Option A: Concurrent multi-device sessions (no single-session restriction)

Phone and tablet both remain signed in simultaneously; only an explicit "Sign Out All Devices" action ends every session. This is the pattern proposed by the external review as more household-friendly, and is a common default for productivity and social apps.

Rejected because: this exact alternative was already evaluated once earlier in the authentication design process and intentionally rejected in favor of single-session, specifically because household data (allergies, goals, budget) is sensitive enough that keeping "current access" unambiguous outweighs the convenience of leaving multiple devices signed in simultaneously. Revisiting this remains open for MVP-1 if user research shows single-session is a significant friction point, but it is not adopted now, and would require a superseding ADR if reconsidered — not a quiet edit to a spec document.

### Option B: Strict re-login on every app restart, no refresh-token resume

The app never uses a refresh token to resume a session; every app restart (not just backgrounding) requires full email/password or social re-authentication, with tokens held in memory only.

Rejected because: research into current industry and standards guidance (OWASP MASVS-AUTH, and observed patterns in banking, productivity, and household/health apps) shows this level of strictness is reserved for the highest-sensitivity banking-grade threat models and is considered unnecessarily strict outside that tier. It would also make the 30-day refresh token pointless in the design, since it would never be used to resume anything.

### Option C: Silent full persistence (refresh token resumes session with no gate)

The refresh token silently resumes the session on any restart with no additional check, as is common in convenience-tier apps (social media, shopping).

Rejected because: this fails to re-verify that the person currently holding the device is the account owner after the app has been fully closed — exactly the scenario (a lost or stolen unlocked device, later force-quit and reopened by someone else) that GDR-002 §7 requires the system to contain. A background token refresh proves the refresh token is valid; it does not prove the current holder of the device is the account owner.

### Option D: Do nothing — leave the TA §37.A/§37.B contradiction unresolved

Rejected because: an unresolved contradiction between two sections of the same authoritative architecture document cannot be implemented as-is; it must be resolved one way or the other before engineering can build against it.

---

## Consequences

### Positive

- "Who has access to this household's data right now" is always answerable in one step (single active session, one identity, one device).
- Users are not forced to fully re-authenticate every time they close and reopen the app, while device possession is still re-verified via biometric/PIN on every cold start.
- The 30-day refresh token has a clear, justified purpose in the design rather than being vestigial.
- TA §37.A and §37.B are now internally consistent on both the multi-device and restart-persistence questions.

### Negative

- Users who intentionally want two devices signed in at once (e.g., a shared household tablet plus a personal phone) cannot do so in MVP-0; the second login always signs the first device out.
- Client logic must distinguish cold start from mere backgrounding, since they trigger different re-authentication rules (cold start always re-checks biometrics regardless of elapsed time; backgrounding only re-checks after a 15-minute idle window).

### Risks

- **User confusion on unexpected sign-out:** a household member on a shared device may be surprised to be signed out when someone else logs in on their own phone. Mitigation: the "logged out on another device" notification (TA §37.A) makes this explicit rather than silent.
- **Silent policy drift on future changes:** if MVP-1 user research pushes toward concurrent multi-device sessions, that must go through a superseding ADR — not a quiet edit to TA §37.B, which is the exact failure mode this ADR exists to close off.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026-07-21 | Proposed | Product Architect | Session/offline-cache architecture review and resolution conversation |
| 2026-07-21 | Accepted | Founder | Same review conversation — single-session and biometric-gated-resume policy confirmed |

---

## Related

- `Products/KitchenOS/40_Technical_Architecture.md`, §37.A (Authentication Layer) — Session Management, Multi-Device Policy
- `Products/KitchenOS/40_Technical_Architecture.md`, §37.B (Session Management and Offline Cache Protection) — full technical specification
- `Products/KitchenOS/70_UX_Design_System/02_Authentication_Wireframes.md` (DOC-072) — "Offline vs. Logged Out" section
- ADR-009: Privacy-by-Design — Identity Isolation
- ADR-015: Offline Cache Encryption Strategy (shares the same biometric/PIN gate)
- `Company/Governance/GDRs/GDR-002_Privacy_By_Design.md`, §7 (Breach Containment)
- OWASP MASVS-AUTH-2 (industry reference used in resolving this decision)

---
