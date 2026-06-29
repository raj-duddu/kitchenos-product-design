---
id: ADR-006
title: Cloud Run for Backend Compute
type: adr
status: accepted
owner: architecture
depends_on: [ADR-002, ADR-005]
referenced_by: [ADR-005]
tags: [cloud, cloud-run, gcp, serverless, deployment, load-balancing, cdn, cloud-armor]
date: 2026
---

# ADR-006: Cloud Run for Backend Compute

**Status:** Accepted
**Date:** 2026
**Deciders:** Founders, Product Architect

---

## Context

KitchenOS requires a compute platform to run the NestJS backend. The platform must be managed by a small team without a dedicated DevOps engineer, support containerised deployments, scale automatically with demand, and integrate with the rest of the GCP service ecosystem.

The main candidates within GCP were:

- **Cloud Run** (serverless containers, fully managed)
- **Google Kubernetes Engine (GKE)** (managed Kubernetes)
- **Compute Engine** (raw VMs)
- **App Engine** (platform-as-a-service)

---

## Decision

**Cloud Run** was chosen as the compute platform for KitchenOS MVP-0.

---

## Reasons

**No server management.**
Cloud Run is fully managed. There are no VMs, no node pools, no operating system patches, and no cluster upgrades to manage. The team deploys a Docker container and Cloud Run handles the rest.

**Implicit load balancing, HTTPS, and autoscaling.**
Cloud Run provides load balancing, HTTPS termination, and automatic scaling (including scale-to-zero) without any configuration. A small team does not need to configure a load balancer, SSL certificates, or autoscaling policies for MVP-0. These are handled by the platform.

**Container-native deployment.**
The NestJS backend is packaged as a Docker image, pushed to Artifact Registry, and deployed to Cloud Run in a single GitHub Actions pipeline step. No Kubernetes manifests, Helm charts, or node pool configuration required.

**Native GCP service integration.**
Cloud Run integrates directly with Cloud SQL (via Cloud SQL Proxy), Secret Manager (environment variable injection), Cloud Tasks (for async OCR jobs), and Cloud Logging — all without additional networking configuration.

**Custom domains without a load balancer.**
Cloud Run supports custom domain mapping natively. A custom domain can be configured without an explicit Cloud Load Balancer in MVP-0. A CLB is only introduced when Cloud CDN or Cloud Armor is required (at Phase 2–3 scale).

**Pay-per-request pricing.**
Cloud Run charges per request and per compute time. At MVP-0 scale (hundreds to low thousands of households), the cost is minimal. Scale-to-zero means no idle compute cost.

---

## Alternatives Considered

**Google Kubernetes Engine (GKE):**
Powerful, flexible, industry-standard. Rejected for MVP-0 because Kubernetes requires significant operational knowledge to manage (node pools, pod autoscaling, ingress controllers, network policies, persistent volume claims). The operational overhead is unjustifiable for a small team building an MVP. GKE is the natural migration target if Cloud Run becomes insufficient at high scale.

**Compute Engine (VMs):**
Maximum control, lowest abstraction. Rejected because it requires the team to manage the operating system, network configuration, load balancers, and all infrastructure manually. This is the wrong tradeoff at MVP-0.

**App Engine:**
Simple PaaS deployment. Rejected because it has less flexibility than Cloud Run for containerised deployments, and the Cloud Run ecosystem is more actively developed and better integrated with the rest of GCP.

---

## Load Balancer and CDN Clarification

Cloud Run handles load distribution automatically at every scale. An explicit **Cloud Load Balancer (CLB)** is NOT required for scaling or custom domains.

A CLB is introduced only when the following features are needed:

| Feature | When Needed | Phase |
|---|---|---|
| Cloud CDN | Caching receipt images and static assets at edge | MVP-1 to Phase 3 |
| Cloud Armor | DDoS protection and WAF rules | Post-Phase 3 |
| Multi-region global routing | Anycast routing across regions | Post-Phase 3 |
| Canary deployments | Traffic splitting between versions | Post-Phase 3 |

Cloud CDN cannot attach directly to a Cloud Run backend — it requires a CLB. Therefore a CLB is introduced at the same time as Cloud CDN, not before.

---

## Scaling Path

```text
MVP-0 (0–5,000 households)
  Cloud Run: automatic load balancing, HTTPS, autoscaling
  Custom domain via Cloud Run domain mapping
  No CLB required

MVP-1 to Phase 3 (5,000–50,000 households)
  Cloud Run continues to autoscale without changes
  Cloud SQL read replicas added
  Cloud CDN introduced for receipt images and static assets
  Cloud Load Balancer introduced at this point (required for CDN)

Post-Phase 3 (50,000+ households)
  Cloud Armor added behind CLB (DDoS, WAF)
  Multi-region Cloud Run with CLB global anycast routing
  Dedicated AI service (AIModule extracted from monolith)
```

---

## Consequences

- Deployment pipeline is: GitHub → GitHub Actions → Docker build → Artifact Registry → Cloud Run deploy.
- Cloud Run revision-based deployment supports zero-downtime rollout and instant rollback by directing traffic to a prior revision.
- Cloud SQL is connected via Cloud SQL Proxy, not direct IP. This is the required connection method for Cloud Run.
- All environment variables and secrets are injected from Secret Manager at runtime. No secrets in the Docker image or environment files.
- Cloud Run concurrency settings must be tuned for the NestJS application. Default concurrency is 80 requests per instance; adjust based on observed load.

---

## Related

- ADR-002: GCP (Cloud Run is within the GCP ecosystem decision)
- ADR-005: Modular Monolith (the monolith deploys as a single Cloud Run service)
- Main doc, Section 37.6: Cloud Infrastructure (full architecture diagram and service map)
- Main doc, Section 42.2: MVP-0 Backend Stack
