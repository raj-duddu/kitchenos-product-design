---
id: DOC-072
title: Authentication Flows — Signup, Login, Password Reset Wireframes
type: ux-design
status: active
owner: design
depends_on: [DOC-010, TA-037A, ADR-009, ADR-014, ADR-015, GDR-002]
referenced_by: []
tags: [ux, wireframes, authentication, signup, login, password-reset, onboarding, month-1]
date: 2026
---

# Authentication Flows — Signup, Login, Password Reset Wireframes

**Stage:** MVP-0 (Month 1 Foundation)  
**Owner:** UX Designer  
**Related:** Technical Architecture §37.A (Authentication Layer)

---

## Flow Summary

| Flow | Screens | Notes |
|------|---------|-------|
| **Sign In** | 1.1–1.2 | Single email+password screen (password manager optimized) |
| **Signup** | 2.1–2.3 | Method selection → email/password → email verification |
| **Password Reset** | 3.1–3.4 | Request → confirmation → new password → success |
| **Logout** | 4.1–4.2 | Confirmation → cache cleared, redirects to Sign In |

**Total screens in MVP-0:** 9 (reduced from 11 by consolidating sign-in to single screen)

---

## Design Principles

All authentication screens follow these principles:

1. **Simplicity is a Feature** (Operating Principle 9) — Minimal fields, clear next steps
2. **Truth Before Convenience** (Operating Principle 7) — Clear error messages, no hidden failures
3. **Transform Complexity into Clarity** (Operating Principle 1) — Users understand what they're doing at each step
4. **Privacy by Design** (GDR-002) — No unnecessary data collection
5. **Earn Trust Through Transparency** (Operating Principle 5) — Clear session state, explicit logout

---

## Offline vs. Logged Out

**Critical Distinction:** Offline and logged out are two different states.

### While Logged In + Offline (Normal)
- **What works:** Full read access to all cached household data (pantry, meal plans, shopping lists, budget, timeline)
- **Actions:** Edits, receipts, shopping list updates are queued locally by the Sync Engine
- **User feedback:** App shows "Waiting for connection…" or "Sync pending" where relevant
- **Behavior:** Transparent to user — app continues to function normally
- **Security:** Device-level auth (biometric/PIN) protects cache; re-authentication triggered after 15 minutes of background inactivity (per TA §37.A §Session Lifecycle)
- **Duration:** Until device reconnects to network (then automatic sync) or user explicitly signs out

### After Signing Out (Security Break)
- **What works:** Public sign-in screen only
- **Session:** Token invalidated, session ends
- **Cached data:** Cleared from this device for security (per GDR-002 §7 Breach Containment)
- **User feedback:** Must see sign-in screen, not app home
- **Behavior:** Explicit, deliberate termination of access
- **Security:** Data is erased; device is no longer trusted
- **Recovery:** User must re-authenticate to restore access

**Why this matters:** "Sign out" must mean what users expect — a definitive end to access. Saying "you're logged out but can still see everything" weakens security and creates confusion. If users need offline access, they should stay logged in.

---

## 1. Sign In Flow (Default)

### Screen 1.1: Sign In

**Purpose:** User enters email and password (single screen for password manager compatibility)

```
┌─────────────────────────────┐
│                             │
│      KitchenOS              │
│  Household Food             │
│  Operating System           │
│                             │
│  Sign In                    │
│                             │
│  Email Address              │
│  ┌─────────────────────────┐│
│  │ name@example.com        ││
│  └─────────────────────────┘│
│                             │
│  Password                   │
│  ┌─────────────────────────┐│
│  │ ••••••••••              ││
│  └─────────────────────────┘│
│  [Show Password]            │
│                             │
│  ┌─────────────────────────┐│
│  │  Sign In                ││
│  └─────────────────────────┘│
│                             │
│  ────── or ──────           │
│  [Continue with Google]     │
│  [Continue with Apple]      │
│                             │
│  ┌─────────────────────────┐│
│  │  Forgot Password?       ││
│  │  [Reset]                ││
│  └─────────────────────────┘│
│                             │
│  Don't have an account?     │
│  [Create Account]           │
│                             │
└─────────────────────────────┘
```

**Design Rationale:**
- Email + password on single screen (optimized for password managers)
- One tap to sign in (better mobile UX)
- Social auth as alternative
- Password field includes show/hide toggle (Principle 9: Simplicity)
- "Forgot Password?" and signup link clearly accessible
- Faster for returning users (primary use case)

**Design Details:**
- Single sign-in button (not progressive disclosure)
- Show password toggle for visibility
- Social auth options available without additional steps

**Error States:**
```
No account found for that email, or the password is incorrect
[Try Again] [Create Account] [Forgot Password?]

Too many failed attempts
[Try again in 15 minutes]
[Forgot Password?]
```

**Security Note:** Generic error message prevents account enumeration attacks. Single-screen design works with password managers (FIDO2 Autofill spec) without compromising security.

---

### Screen 1.2: Sign In Success

**Purpose:** User logged in; proceed to app

```
┌─────────────────────────────┐
│                             │
│  ✓ Signing You In...        │
│                             │
│  (brief pause, then         │
│   redirect to Home screen)  │
│                             │
│  Session created.           │
│  You're logged in.          │
│                             │
└─────────────────────────────┘
```

---

## 2. Signup Flow (Secondary)

### Flow Overview
- Screen 2.1: Signup method selection (email or social)
- Screen 2.2: Email + password entry (if email signup chosen)
- Screen 2.3: Email verification (check inbox, auto-redirect on verify)

### Screen 2.1: Signup Start

**Purpose:** New user chooses signup method (triggered from "Create Account" link)

```
┌─────────────────────────────┐
│                             │
│      KitchenOS              │
│  Household Food             │
│  Operating System           │
│                             │
│  Create Account             │
│                             │
│  ┌─────────────────────────┐│
│  │  Continue with Google   ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │  Continue with Apple    ││
│  └─────────────────────────┘│
│                             │
│  ────── or ──────           │
│                             │
│  ┌─────────────────────────┐│
│  │  Sign up with Email     ││
│  └─────────────────────────┘│
│                             │
│  Already have an account?   │
│  [Sign In]                  │
│                             │
└─────────────────────────────┘
```

**Copy Rationale:**
- "Create Account" is the primary heading
- Social auth first (less friction for new users)
- Email option clearly available
- Link back to Sign In for existing users

---

### Screen 2.2: Email Signup

**Purpose:** User enters email and creates password

```
┌─────────────────────────────┐
│                             │
│  Create Your Account        │
│                             │
│  Email Address              │
│  ┌─────────────────────────┐│
│  │ name@example.com        ││
│  └─────────────────────────┘│
│                             │
│  Password                   │
│  ┌─────────────────────────┐│
│  │ ••••••••••              ││
│  └─────────────────────────┘│
│  (Minimum 8 characters;     │
│   passphrases welcome)      │
│                             │
│  ☐ I agree to Terms of      │
│    Service and Privacy      │
│    Policy                   │
│                             │
│  ┌─────────────────────────┐│
│  │  Create Account         ││
│  └─────────────────────────┘│
│                             │
│  ────── or ──────           │
│  [Continue with Google]     │
│  [Continue with Apple]      │
│                             │
└─────────────────────────────┘
```

**Design Details:**
- Single email field (no "confirm email")
- Single password field with indicator ("At least 8 characters")
- Checkbox for ToS/Privacy (required, not optional)
- Create Account button is primary CTA
- Social auth as fallback below

**Error States:**
```
Check your email
We've sent instructions to name@example.com

Password too short
[Requirements: Minimum 8 characters]

This password appears in public data breaches
[Try a different password]

Network error
[Please try again]
```

**Security Note:** The app shows the same "Check your email" message regardless of whether the email is already registered. The backend sends a different email only to the inbox owner:
- If registered: "Sign in to your account"
- If not registered: "Confirm your email / finish creating account"

This prevents account enumeration through the app UI. Timing and bounce handling are mitigated at the API layer.

---

### Screen 2.3: Email Verification

**Purpose:** User submitted signup; email verification sent

```
┌─────────────────────────────┐
│                             │
│  ✓ Account Created          │
│                             │
│  We've sent you an email at │
│  name@example.com           │
│                             │
│  Click the link in your     │
│  email to verify your       │
│  address and sign in.       │
│                             │
│  ┌─────────────────────────┐│
│  │  Didn't get the email?  ││
│  │  [Resend]               ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │  Change Email Address   ││
│  │  [Edit]                 ││
│  └─────────────────────────┘│
│                             │
│  Checking for verification..│
│  (auto-refreshes)           │
│                             │
│  [← Back to Signup]         │
│                             │
└─────────────────────────────┘
```

**Copy Rationale:**
- "✓ Account Created" — confirms success immediately
- Clear action required (click email link)
- "Didn't get the email?" — anticipates user frustration
- Auto-refresh with polling (JavaScript) — seamless when verified
- Upon verification: auto-redirect to Vision §50 onboarding (no intermediate confirmation screen)
- Verification required before app access; user cannot proceed without verified email
- Household auto-created silently per ADR-010; admin status explained in onboarding
- Edit option for email typos

**Invite Code Handling (Deep-Link Integration):**
- If user arrives via invite deep-link (`?invite_code=XXXXXXXX`), household binding occurs during email verification
- ADR-010 auto-creation is skipped; user joins the inviting household directly
- If no invite code present, standard ADR-010 household auto-creation applies
- See the forthcoming Onboarding Wireframes document (not yet created — planned as the next UX artifact) for the post-verification decision tree

---

## 3. Password Reset Flow

### Flow Overview
- Screen 3.1: User enters email to request reset
- Screen 3.2: Confirmation screen (same for registered/unregistered emails; only inbox owner sees actual email)
- Screen 3.3: User clicks email link, enters new password
- Screen 3.4: Success confirmation, redirect to sign-in

---

### Screen 3.1: Reset Request

**Purpose:** User requests password reset. The app UI is identical whether or not the email is registered; only the inbox owner sees any actual email.

```
┌─────────────────────────────┐
│                             │
│  Reset Password             │
│                             │
│  Enter your email and we    │
│  'll send you a link to     │
│  reset your password.       │
│                             │
│  Email Address              │
│  ┌─────────────────────────┐│
│  │ name@example.com        ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │  Send Reset Link        ││
│  └─────────────────────────┘│
│                             │
│  [← Back to Sign In]        │
│                             │
└─────────────────────────────┘
```

**Copy Rationale:**
- "Reset Password" is clear
- Explains what happens next
- Back link to Sign In

---

### Screen 3.2: Reset Link Sent

**Purpose:** Confirm reset request received. Same screen is shown whether or not the email is registered; only the inbox owner sees any actual email.

```
┌─────────────────────────────┐
│                             │
│  Check Your Email           │
│                             │
│  If name@example.com is     │
│  registered, we sent a      │
│  password reset link.       │
│                             │
│  The link expires in        │
│  30 minutes. Check your     │
│  spam folder if you don't   │
│  see it.                    │
│                             │
│  Click the link in your     │
│  email to create a new      │
│  password.                  │
│                             │
│  ┌─────────────────────────┐│
│  │  Didn't get an email?   ││
│  │  [Send another link]    ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │  Try a different email  ││
│  │  [Back]                 ││
│  └─────────────────────────┘│
│                             │
│  [← Back to Sign In]        │
│                             │
└─────────────────────────────┘
```

**Design Details:**
- "Check Your Email" is clear CTA
- Explains link expiry (30 min)
- Resend option visible
- Back options clear

**Security Note:** The app never reveals whether the email is registered. The same screen is shown for registered and unregistered emails; an actual reset email is sent only when the email is registered. Timing and bounce handling are mitigated at the API layer.

---

### Screen 3.3: Password Reset Confirmation

**Purpose:** User clicks email link; enter new password

```
┌─────────────────────────────┐
│                             │
│  Create New Password        │
│                             │
│  New Password               │
│  ┌─────────────────────────┐│
│  │ ••••••••••              ││
│  └─────────────────────────┘│
│  (Minimum 8 characters;     │
│   passphrases welcome)      │
│  [Show Password]            │
│                             │
│  ┌─────────────────────────┐│
│  │  Reset Password         ││
│  └─────────────────────────┘│
│                             │
│  This link expires in       │
│  25 minutes                 │
│                             │
└─────────────────────────────┘
```

**Design Details:**
- Single password field with show/hide toggle (consistent with signup screen 2.2)
- Minimum 8 characters shown
- Expiry countdown visible

**Error States:**
```
Password too short
[Requirements: Minimum 8 characters]

This password appears in public data breaches
[Try a different password]

Link expired
[Request new reset link]
[← Back to Sign In]

Link already used
[Request new reset link]
```

---

### Screen 3.4: Reset Success

**Purpose:** Password reset complete; user can sign in

```
┌─────────────────────────────┐
│                             │
│  ✓ Password Reset           │
│                             │
│  Your password has been     │
│  updated.                   │
│                             │
│  ┌─────────────────────────┐│
│  │  Sign In with New       ││
│  │  Password               ││
│  └─────────────────────────┘│
│                             │
│  (Redirects to login)       │
│                             │
└─────────────────────────────┘
```

---

## 4. Logout Flow

### Flow Overview
- Screen 4.1: User confirms logout (with option to sign out all devices)
- Screen 4.2: Confirmation, cache cleared, redirect to sign-in

---

### Screen 4.1: Logout Confirmation

**Purpose:** User initiates logout (from Settings or Household screen)

```
┌─────────────────────────────┐
│                             │
│  Sign Out?                  │
│                             │
│  You'll be logged out on    │
│  this device. Your session  │
│  will end, and you'll need  │
│  to sign in again to access │
│  your household data.       │
│                             │
│  ┌─────────────────────────┐│
│  │  Sign Out               ││
│  └─────────────────────────┘│
│                             │
│  [Cancel]                   │
│                             │
│  ┌─────────────────────────┐│
│  │  Sign Out All Devices   ││
│  │  (log out phone, tablet,││
│  │   etc. simultaneously)  ││
│  └─────────────────────────┘│
│                             │
└─────────────────────────────┘
```

**Design Details:**
- "Sign Out?" is clear and unambiguous
- Explains what logout means: session ends, data access revoked
- "Sign Out" for this device only (session invalidated on this device)
- "Sign Out All Devices" invalidates all active sessions (per ADR-009, GDR-002 §7)
- Cancel option

---

### Screen 4.2: Logout Complete

**Purpose:** Confirmation of logout; redirects to sign-in screen

```
┌─────────────────────────────┐
│                             │
│  ✓ Signed Out               │
│                             │
│  Your session has ended.    │
│  Cached household data has  │
│  been cleared for security. │
│                             │
│  ┌─────────────────────────┐│
│  │  Sign Back In           ││
│  └─────────────────────────┘│
│                             │
│  (Redirects to Sign In      │
│   screen)                   │
│                             │
└─────────────────────────────┘
```

**Design Details:**
- Clear confirmation of logout completion
- Explains that cached data is cleared (security by design, per GDR-002 §7)
- No "read-only" access after logout — logout means no access until re-auth
- Redirects to Sign In screen

---

## 5. Error Handling

### Rate Limiting (Security)

```
┌─────────────────────────────┐
│                             │
│  Too Many Attempts          │
│                             │
│  We've locked this account  │
│  for security.              │
│                             │
│  Try signing in again in    │
│  15 minutes, or reset your  │
│  password now.              │
│                             │
│  ┌─────────────────────────┐│
│  │  Reset Password         ││
│  └─────────────────────────┘│
│                             │
│  [← Back]                   │
│                             │
└─────────────────────────────┘
```

---

### Social Auth Error

```
┌─────────────────────────────┐
│                             │
│  ✗ Sign In Failed           │
│                             │
│  We couldn't connect to     │
│  Google. Please try again.  │
│                             │
│  ┌─────────────────────────┐│
│  │  Try Again              ││
│  └─────────────────────────┘│
│                             │
│  ┌─────────────────────────┐│
│  │  Sign In with Email     ││
│  └─────────────────────────┘│
│                             │
│  [← Back]                   │
│                             │
└─────────────────────────────┘
```

---

## 6. UX Copy Guidelines

| Scenario | Good | Avoid |
|---|---|---|
| Signup success | "Account Created" | "Success" |
| Password requirement | "Minimum 8 characters (passphrases welcome)" | "Needs uppercase, number, symbol" |
| Password too short | "Minimum 8 characters" | "Password strength insufficient" |
| Breached password | "This password appears in public breaches" | "Password is not strong enough" |
| Email used for signup | "Check your email" | "Email already registered" |
| Password reset request | "If name@example.com is registered, we sent a reset link" | "We've sent a reset link to your email" |
| Rate limit | "Try again in 15 minutes" | "Access denied" |
| Social auth fail | "Couldn't connect to Google" | "Authentication failed" |
| Logout | "You're logged out" | "Session terminated" |

**Principle:** Plain language, explain the next action.

---

## 7. Related Documentation

- **Technical Architecture §37.A** — Full auth layer spec, data model, API contracts
- **Technical Architecture §37.B** — Session management, token lifecycle, offline cache protection
- **Operating Principle 9** — Simplicity is a Feature (guides screen minimalism)
- **GDR-002** — Privacy by Design (guides data minimalism)
- **ADR-009** — Identity Isolation (guides architecture)
- **ADR-014** — Session Continuity Model (single-session policy; biometric-gated resume behind the "Offline vs. Logged Out" distinction in this document)
- **ADR-015** — Offline Cache Encryption Strategy (hardware-backed keys protecting the cached data referenced in this document)
- **Vision §50** — Onboarding flow (what happens after login)

---

