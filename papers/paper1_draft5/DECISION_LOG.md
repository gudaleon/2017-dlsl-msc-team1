# Draft 5.0 decision log

Parent branch: `cursor/paper1-draft4-methods-0ace`  
Parent commit: `b298af382523b5a14ba2e515ccdefc23326883bd`  
Working branch: `cursor/paper1-draft5-validation-0ace`  
Decision date: 17 October 2026

This file records instruction precedence and the four conflict resolutions approved before Stage 1 execution. It does not modify `papers/paper1_draft4/NEXT_AGENT_INSTRUCTIONS.md` or the Drive original of `MASTER_INSTRUCTIONS.md`.

---

## Instruction precedence

1. `papers/paper1_draft5/MASTER_INSTRUCTIONS.md` controls new analytical procedures, validation gates, and scientific acceptance criteria.
2. `papers/paper1_draft4/NEXT_AGENT_INSTRUCTIONS.md` remains the frozen research contract for Draft 4.0 baseline facts, preservation rules, forbidden inventions, and candidate series A–E.
3. Where those documents differ, the explicit decisions below apply.
4. Stage 2 (manuscript rewrite, publication figures/tables) is not authorized in this pass.

---

## Resolution 1 — Headline rule

**Conflict.** Draft 4.0 next-agent instructions treat a >2 percentage-point move after `drop_neg_residual` + `geo_cma_pr` as an automatic headline replacement. The Master Instruction treats that same 2 pp threshold as a review trigger and requires independent validation before promotion.

**Approved rule.** A change greater than 2 percentage points is a mandatory methodological review trigger, not an automatic headline replacement.

Promote a new specification only when its analytical definition, comparability across years, and independent validation justify that choice.

If neither specification is sufficiently validated, leave headline selection **PROVISIONAL** and explain why.

The two-factor variant (`drop_neg_residual` + `geo_cma_pr`) is run separately from the broader M6 closest-feasible CMHC-like specification. Incremental changes and denominator changes are reported for each. Neither variant may be described as an official CMHC calculation.

---

## Resolution 2 — High-income cap

**Conflict.** Draft 4.0 next-agent instructions require implementing an equivalized-income-above-median rule. The Master Instruction forbids an arbitrary cap and allows implementation only with a documented methodological source.

**Approved rule.** Implement a high-income cap only if an authoritative methodological source supports its definition and application.

If no defensible threshold can be documented, record `NOT IMPLEMENTED — INSUFFICIENT EVIDENCE`. Do not invent a cap.

**Stage 1 application.** CMHC Research Insight, *Introducing the Housing Hardship Concept* (January 2020), states that households with equivalized income above the median income of their province of residence cannot be classified as in housing hardship. That documented provincial-median rule is implemented as scenario M2. The same source also restricts households with investment income/losses, capital gains/losses, or farm income; those fields are not usable for that restriction on these PUMFs and remain `NOT IMPLEMENTED — INSUFFICIENT EVIDENCE`.

---

## Resolution 3 — Economic-family residual-income test

**Conflict.** Draft 4.0 next-agent instructions require repeating the residual test on `EF_ID`. The Master Instruction forbids inventing a shelter allocation across economic families that share a dwelling.

**Approved rule.** Implement the `EF_ID` analysis only when the available variables support a coherent economic-family income, shelter-cost allocation, family-size threshold, and denominator.

If these conditions are not met, document `NOT IMPLEMENTABLE` and the precise reason.

Do not assign complete household shelter costs to multiple economic families or otherwise invent missing allocations.

---

## Resolution 4 — Figure and table count

**Conflict.** Draft 4.0 next-agent instructions require five figures and five tables as part of Draft 5.0 completion. The Master Instruction treats that count as a working publication target.

**Approved rule.** Five figures and five tables are the working publication target, not a mandatory scientific constraint. Final selection occurs during Stage 2 after verification.

No publication figures or manuscript rewrite during Stage 1.

---

## Additional CMHC-comparison clarification

Run the original two-factor variant (`drop_neg_residual` + `geo_cma_pr`) separately from the broader M6 closest-feasible CMHC-like specification.

Report:

- the incremental change attributable to each assumption;
- their combined effect;
- sample exclusions and changes in denominators.

Neither variant is an official CMHC calculation.
