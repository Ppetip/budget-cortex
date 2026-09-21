# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 33 offline tests pass; dry run and live synthetic Jev workflow pass.

Latest: Direct Router.choose calls validate costs, remaining budget and quality targets before selection.

Next: Evaluate delayed feedback and context-classification errors.

Repository: https://github.com/Ppetip/budget-cortex
Budget: one shared $3 cumulative Jev allowance across the portfolio, never per project or cycle.
No other paid compute authorized. Eight initial calls across all projects used 3,303 input tokens;
estimated total $0.000138726, with $0.08 conservatively reserved. See README for limits.
Live smoke responses are not production benchmarks. No model training performed.

2026-09-21 CI pass: added pinned, read-only Windows/Linux Python 3.11/3.13 checks for unit tests and offline CLI contracts. Local checks and all four hosted Windows/Linux Python 3.11/3.13 jobs pass. No additional Jev calls.

Hosted verification: https://github.com/Ppetip/budget-cortex/actions/runs/35590278682

2026-09-21 14:42 UTC budget fix: live clients require an existing ledger; explicit initialization refuses overwrite. Added four regression cases for missing/deleted/empty ledgers and preserved spending. All local tests, CLI checks, and four hosted Windows/Linux Python 3.11/3.13 jobs pass. No additional Jev calls.

Budget-fix hosted verification: https://github.com/Ppetip/budget-cortex/actions/runs/35614384278

2026-09-21 18:44 UTC: Direct Router.choose calls validate costs, remaining budget and quality targets before selection. Local tests, offline CLI checks, and all four hosted matrix jobs pass. No additional Jev calls.

Feature-pass verification: https://github.com/Ppetip/budget-cortex/actions/runs/35640895462
