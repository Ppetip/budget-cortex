# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 26 offline tests pass; dry run and live synthetic Jev workflow pass.

Latest: Jev context classification feeds the synthetic router; a zero budget still abstains.

Next: Evaluate classification errors and delayed feedback with clearly separate provider and simulated costs.

Repository: https://github.com/Ppetip/budget-cortex
Budget: one shared $3 cumulative Jev allowance across the portfolio, never per project or cycle.
No other paid compute authorized. Eight initial calls across all projects used 3,303 input tokens;
estimated total $0.000138726, with $0.08 conservatively reserved. See README for limits.
Live smoke responses are not production benchmarks. No model training performed.

2026-09-21 CI pass: added pinned, read-only Windows/Linux Python 3.11/3.13 checks for unit tests and offline CLI contracts. Local Python 3.13 checks pass; hosted results pending publication. No additional Jev calls.
