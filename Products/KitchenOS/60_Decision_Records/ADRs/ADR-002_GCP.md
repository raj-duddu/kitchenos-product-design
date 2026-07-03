---
id: ADR-002
title: Google Cloud Platform (GCP)
type: adr
status: accepted
owner: architecture
depends_on: [ADR-001]
referenced_by: [ADR-003, ADR-006, ADR-012]
operating_principles: ["9. Simplicity Is a Feature"]
tags: [cloud, gcp, firebase, cloud-run, cloud-sql, cloud-vision, infrastructure]
date: 2026
---

# ADR-002: Google Cloud Platform (GCP)

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

> **Amended 2026-07-03 by ADR-012** — scope: the receipt-OCR rationale element (Cloud Vision API, including the Rekognition comparison under the AWS alternative); decision: unchanged. Document Understanding via a multimodal LLM replaces Cloud Vision, and Gemini multimodal models keep it within the same ecosystem, so the same-cloud argument survives with a different service filling the slot. See History.

---

## Context

KitchenOS requires a cloud provider for backend compute, managed database, object storage, receipt OCR, authentication, push notifications, and secret management. The platform must be operable by a small team without dedicated DevOps, and must scale from hundreds to tens of thousands of households without architectural changes.

The main candidates were:

- **Google Cloud Platform (GCP)**
- **Amazon Web Services (AWS)**
- **Microsoft Azure**

---

## Decision

**Google Cloud Platform (GCP)** was chosen as the cloud provider for KitchenOS MVP-0 and beyond.

---

## Reasons

**Flutter and Firebase alignment.**
Flutter is a Google product. Firebase (Authentication, Cloud Messaging) integrates natively with the Flutter SDK with minimal configuration. This is not a minor convenience — it eliminates an entire class of SDK compatibility and configuration problems that arise when mixing non-Google mobile frameworks with non-Google auth and notification providers.

**Cloud Vision API for receipt OCR.**
Receipt scanning is a core MVP-0 feature. Google Cloud Vision API is the strongest commercially available OCR service for receipts and documents. Using the same cloud provider for OCR as for compute and database eliminates cross-provider networking complexity and latency.

**Cloud Run for simple serverless deployment.**
Cloud Run deploys a containerised NestJS service with automatic load balancing, HTTPS termination, and autoscaling — without Kubernetes. A small team can deploy and manage this without a dedicated DevOps engineer.

**Vertex AI and Gemini for future AI expansion.**
KitchenOS will expand its AI layer post-MVP. Staying within GCP allows integration with Vertex AI and Gemini without cross-cloud networking, billing complexity, or additional identity federation.

**Managed services reduce operational burden.**
Cloud SQL (managed PostgreSQL), Memorystore (managed Redis), Cloud Tasks (managed job queue), and Secret Manager all eliminate self-hosting operational responsibility. A founding team should not be managing database servers, Redis clusters, or secrets infrastructure.

**Firebase Authentication.**
Handles Google Sign-In and Apple Sign-In with clean Flutter SDK integration. Removes the need to build or self-host authentication infrastructure in MVP-0.

---

## Alternatives Considered

**AWS:**
Mature, largest ecosystem, widest service catalogue. Rejected for MVP-0 because the Firebase + Flutter SDK integration is significantly simpler on GCP. AWS Cognito (authentication) and AWS SNS (push notifications) require more configuration and have weaker Flutter SDK support than Firebase. AWS Rekognition is not as strong as Cloud Vision API for receipt OCR specifically.

**Azure:**
Strong enterprise integrations. Rejected because it has no meaningful advantage for a Flutter-first consumer app and adds cognitive overhead for a small team not already familiar with Azure services.

---

## Consequences

- All infrastructure is managed through GCP. Engineers should be familiar with GCP Console, Cloud Run deployments, and Cloud SQL.
- Firebase Authentication and Firebase Cloud Messaging are GCP products, not separate third-party dependencies.
- Future AI expansion (Vertex AI, Gemini) can stay within the same billing account and IAM structure.
- An explicit Cloud Load Balancer is not required in MVP-0. Cloud Run handles load balancing automatically. A CLB is introduced only when Cloud CDN or Cloud Armor is needed (MVP-1 to Phase 3 scale).
- All secrets must be stored in Secret Manager. No hardcoded credentials anywhere.

---

## History

| Date | Change | By | Evidence |
|---|---|---|---|
| 2026 | Accepted | Founders, Product Architect | pre-dates History enforcement |
| 2026-07-03 | Amended — OCR rationale element overtaken by ADR-012; decision unaffected | @raj-duddu | PR # (add on merge) |
| 2026-07-03 | Backfilled `operating_principles` (retrospective citation: Principle 9 — managed services, no DevOps burden) | @raj-duddu | PR # (add on merge) |

---

## Related

- ADR-006: Cloud Run (specific compute decision within GCP)
- Main doc, Section 37.6: Cloud Infrastructure (full service map and scaling path)
- Main doc, Section 42.1–42.4: MVP-0 Tech Stack
