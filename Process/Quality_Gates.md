---
id: PROC-002
title: Quality Gates — GitHub Flow Enforcement
type: process
status: active
owner: founders
scope: company-wide
applies_to: [KitchenOS, all future products]
depends_on: [GOV-003]
referenced_by: []
tags: [governance, ci, quality-gates, github, enforcement]
date: 2026
---

# Quality Gates — GitHub Flow Enforcement

> This document describes **how** governance rules are enforced in the GitHub flow. It does not define any rules. The rules live in `Company/Governance/Architecture_Governance.md`, the GDRs, and `00_Knowledge_Map.md`. If a rule changes, change it there — enforcement follows automatically.

Enforcement follows the same principle as agents: **gates contain enforcement, not policy.**

`governance_check.py` is a generic engine with no rules of its own: it reads every rule parameter at runtime from the `enforced_*` frontmatter fields of the documents that own the rules — documentation-system rules from `00_Knowledge_Map.md`, decision-record rules from `Company/Governance/Architecture_Governance.md`. Prose and parameters live side by side in the same file and must change in the same commit. If a parameter is deleted, CI fails with a configuration error rather than silently enforcing less.

---

## Gate Map

| # | Gate | Enforced by | Governing rule |
|---|---|---|---|
| 1 | Every inline path, link, and document ID resolves | `knowledge_index.py --check` in CI | Knowledge Map — "every piece of information has exactly one authoritative home"; references must not rot |
| 2 | Decision records are never deleted | `governance_check.py --deleted-files` in CI — protected directories read from `enforced_no_delete_dirs` | `Company/Governance/Architecture_Governance.md` — ADR Lifecycle: superseded records are kept as audit trail |
| 3 | Frontmatter completeness, unique IDs, valid status, required sections, Operating-Principles citation | `governance_check.py` in CI (strict on changed files) — parameters read at runtime from `enforced_*` frontmatter of the governing documents | `Company/Governance/Architecture_Governance.md` — Machine-Readable Enforcement + ADR Quality Requirements; `00_Knowledge_Map.md` — documentation-system rules |
| 4 | Reviewer sees downstream impact of every changed document | CI posts `knowledge_index.py --impact` output to the PR summary | Knowledge Map — Document Dependency Chain: "when a concept changes, all documents downstream must be reviewed" |
| 5 | No one approves their own change | Branch protection: PRs required, ≥1 approving review | `Company/Governance/Architecture_Governance.md` — Approval: "No single person approves their own ADR" |
| 6 | Governance changes require founder sign-off | `CODEOWNERS` on `Company/`, `60_Decision_Records/`, `Agents/`, and the gate tooling itself | `Company/Governance/Architecture_Governance.md` — Approval thresholds; GDR precedence |
| 7 | Author self-attestation of what machines cannot check | `.github/pull_request_template.md` checklist | One-home rule; three-alternatives rule; GDR conflict check |

---

## What Runs Where

**On every pull request:**

1. `knowledge_index.py --check` — fails on broken references.
2. Deletion guard — fails if a decision record is deleted.
3. `governance_check.py --strict-files <changed>` — changed decision records **must** carry `operating_principles:`; pre-existing records without it report as warnings until backfilled.
4. Impact analysis for each changed document ID, posted to the job summary.

**On push to `main`:** gates 1 and 3 (warning-level) run again as a safety net.

**Locally, before opening a PR:**

```bash
python knowledge_index.py --check
python governance_check.py
```

---

## Branch Protection Setup (manual, one-time)

GitHub → repo → Settings → Branches → Add branch protection rule for `main`:

- [x] Require a pull request before merging
- [x] Require approvals: 1
- [x] Dismiss stale pull request approvals when new commits are pushed
- [x] Require review from Code Owners *(after filling real usernames into `.github/CODEOWNERS`)*
- [x] Require status checks to pass before merging → select **docs-quality**
- [x] Do not allow bypassing the above settings

At founding stage with two founders, "require approvals: 1" plus CODEOWNERS implements the Architecture Review Board policy. Revisit when the team grows.

---

## Known Debt

- The 22 decision records that predate enforcement (11 ADRs, 9 PDRs, 2 GDRs) lack the `operating_principles:` frontmatter field and the `History` section. Both surface as CI warnings. Backfill deliberately — citing principles is a judgment call; History rows for pre-enforcement records can state `pre-dates History enforcement` with the original date.

---

## Related

- `Company/Governance/Architecture_Governance.md` — the rules these gates enforce
- `00_Knowledge_Map.md` — one-home rule and dependency chain
- `.github/workflows/docs-quality.yml` — CI implementation
- `governance_check.py`, `knowledge_index.py` — lint and reference tooling
- `.github/CODEOWNERS`, `.github/pull_request_template.md` — review-path implementation
