<!-- Quality gates: see Process/Quality_Gates.md. CI enforces most of
     this automatically; the checklist covers what only a human can judge. -->

## What changed and why

<!-- One or two sentences. Link the driving PRD/ADR/PDR if one exists. -->

## Documents touched

<!-- Doc IDs, e.g. DOC-040, ADR-004. "None" for tooling-only changes. -->

## Checklist

- [ ] `python knowledge_index.py --check` passes locally
- [ ] `python governance_check.py` passes locally
- [ ] Every fact I added lives in exactly one authoritative home — other documents link to it, nothing is duplicated
- [ ] I reviewed the downstream documents listed by `knowledge_index.py --impact <id>` for every document I changed
- [ ] New/changed decision records cite the Operating Principles they implement or trade off against (`operating_principles:` frontmatter)
- [ ] No decision record was deleted — superseded records are marked `superseded` and link to their successor
- [ ] If this changes governance rules: the rule changed in its governance document, not just where it is enforced

## For decision records (ADR/PDR/UXDR) only

- [ ] At least three alternatives considered, including doing nothing
- [ ] Consequences state what becomes easier, harder, and locked in
- [ ] Does not conflict with GDR-001 or GDR-002 (or has founder sign-off)
