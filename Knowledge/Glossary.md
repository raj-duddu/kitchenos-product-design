---
id: KNOW-001
title: Shared Glossary
type: knowledge
status: active
owner: founders
scope: company-wide
date: 2026
---

# Shared Glossary

> Terms and concepts that are referenced across multiple products, documents, and agents. This glossary defines the **company-level** vocabulary. Product-specific ubiquitous language lives in each product's Domain Model.
> When a term appears here and in a product glossary, the product glossary takes precedence for that product's bounded context.

---

## Architectural Patterns

| Term | Definition |
|---|---|
| **Domain-Driven Design (DDD)** | A software development approach that models complex business domains using a rich domain model, ubiquitous language, bounded contexts, and aggregates. All Amanaska products use DDD as their primary modelling approach. See `Knowledge/Patterns/DDD.md`. |
| **Bounded Context** | A well-defined boundary within which a domain model is consistent and unambiguous. Different bounded contexts may use the same word with different meanings; the boundary makes each meaning explicit. |
| **Aggregate** | A cluster of domain objects treated as a single unit for data changes. Only the aggregate root may be referenced from outside the aggregate. |
| **Aggregate Root** | The single entry point for operations on an aggregate. All external access goes through the root. |
| **Ubiquitous Language** | The shared vocabulary used consistently by product, engineering, QA, and support within a bounded context. Deviating from it causes specification bugs. |
| **Event Sourcing** | A persistence pattern where the state of an entity is derived by replaying a sequence of immutable events rather than storing the current state directly. See `Knowledge/Patterns/Event_Sourcing.md`. |
| **CQRS** | Command Query Responsibility Segregation — separating the model for writes (commands that change state) from the model for reads (queries that return state). |
| **Domain Event** | An immutable record of something that happened in the domain. Named in past tense. Never deleted — only reversed by a correction event. |
| **Correction Event** | A domain event that reverses or amends a prior event. Not a delete. The original event remains in the log. |
| **Saga** | A sequence of domain events and compensating transactions used to coordinate a long-running business process across multiple bounded contexts. |

---

## Data Architecture

| Term | Definition |
|---|---|
| **Four-Layer Model** | The Amanaska data architecture: Auth (PII isolation) → Person (stable domain facts) → Domain (business entities and relationships) → Intelligence (AI beliefs, confidence scores, learned patterns). No layer depends on a layer above it. |
| **PII** | Personally Identifiable Information. In Amanaska systems, PII is isolated to the Auth layer (email only). The domain and intelligence layers never contain PII. |
| **Identity** | An authentication mechanism. Not a business entity. Identity ≠ Person. |
| **Person** | A business entity representing a human being in the Amanaska platform. Global across all products. Keyed by `person_id`. Never contains email or auth credentials. |
| **Intelligence Layer** | The AI belief system for a product or household. Contains learned preferences, confidence scores, and behavioural patterns. Keyed on `person_id` + context identifier. Never contains PII or authoritative domain facts. |
| **Canonical Data Model** | The shared schema for concepts that exist across multiple Amanaska products (Person, Identity, HouseholdMembership). Documented in `Knowledge/Canonical_Data_Model.md`. |

---

## AI and Intelligence

| Term | Definition |
|---|---|
| **Decision Support** | An AI posture where the system generates recommendations to assist human judgment, not to replace it. All Amanaska products are decision support systems. See GDR-001. |
| **Confidence Score** | A probability estimate (0.0–1.0) attached to an AI recommendation indicating the system's certainty. Must be surfaced to users for Medium+ criticality outputs. |
| **Decision Criticality** | A four-level classification (Low, Medium, High, Critical) that determines the safeguards required for an AI output. Defined in `Company/Governance/AI_Governance.md`. |
| **Hallucination** | An AI output that is confidently stated but factually incorrect or unsupported by the input context. Monitoring for hallucinations is a governance requirement. |
| **Model Governance** | The policies and processes that govern AI model selection, evaluation, deployment, and monitoring. Defined in `Company/Governance/AI_Governance.md`. |
| **Prompt Versioning** | The practice of versioning AI prompts alongside feature code so that changes to prompts are traceable, reviewable, and rollback-able. |

---

## Privacy

| Term | Definition |
|---|---|
| **Privacy by Design** | A principle that privacy protections are built into a system from the start, not added as a compliance layer. Implemented as GDR-002. |
| **Data Minimisation** | Collecting only the data required for a stated purpose. A core principle of Privacy by Design. |
| **Consent** | Explicit, informed, and freely given agreement to use data for a specific purpose. All Amanaska products require explicit consent for data use beyond primary purpose. |
| **ConsentGrant** | A domain entity representing a scoped, time-bounded, revocable permission granted by a user for a specific data use (e.g., expert access to household data). |
| **Right to Erasure** | A user's right to have their data deleted. Amanaska products must support full account and data deletion, including deletion of intelligence models. |
| **Breach Containment** | The architectural principle that a breach of one system layer must not expose data from another layer. Achieved via schema separation and least-privilege access. |

---

## Process

| Term | Definition |
|---|---|
| **Stage Gate** | A decision point in the Product Development Lifecycle at which a specific set of criteria must be met before work progresses to the next stage. |
| **Definition of Done** | The complete set of criteria that must be satisfied for a feature to be considered complete. Not a checklist of tasks — a quality contract. |
| **GDR** | Governance Decision Record. Company-wide policy decision. Cannot be overridden by ADRs or PDRs. |
| **ADR** | Architecture Decision Record. Records a significant architectural choice for a specific product. |
| **PDR** | Product Decision Record. Records a significant product scope or strategy decision. |
| **UXDR** | UX Decision Record. Records a significant UX pattern or interaction design decision. |
| **EDR** | Engineering Decision Record (future). Will record engineering process decisions when the engineering organisation grows. |
