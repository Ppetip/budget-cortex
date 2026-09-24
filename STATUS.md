# Status

Stage: command-line prototype with optional live Jev integration.
Verified: 51 offline tests and five CLI paths pass locally; all four hosted checks pass. Jev smoke results remain historical; no new live calls.

Latest: Decisions expose pre-outcome support counts with contextual or global scope.

Next: Evaluate independently authored shift patterns and observed outcomes; support counts do not establish statistical uncertainty or live reliability.

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

2026-09-21 22:45 UTC: documented how to interpret this tool's outcomes separately from command success. The local Codex runner now shows a concise outcome summary for this project. Verified through common-runner checks and synthetic demo output; histories stay local.

2026-09-22 02:46 UTC: Selected feedback can arrive after additional requests, with undelivered feedback counted. Common-runner checks, new route and all four hosted jobs pass. No new Jev calls.

Evaluation-path verification: https://github.com/Ppetip/budget-cortex/actions/runs/35681198428

2026-09-22 10:48 UTC: Each decision records `quality_at_selection`, the contextual smoothed estimate before applying that request's outcome, and `feedback_received_before_selection`, the number of delayed outcomes released immediately before this choice. Immediate feedback is applied after its own choice and is not counted as a delayed release. Abstentions retain release counts and use a null selected-model estimate. For the strongest baseline, this contextual estimate is diagnostic; selection still uses global quality. Estimates are not calibrated guarantees. Published and verified: local checks and all four hosted matrix jobs pass. No new Jev calls.

Reliability verification: https://github.com/Ppetip/budget-cortex/actions/runs/35718645844

2026-09-22 22:50 UTC: Run `python shift.py` (Codex route `shift`). This authored scenario makes the small model fail after request four while keeping the visible context constant. Across eight later requests, frozen estimates succeed 0/8, immediate feedback 5/8 and delayed feedback 3/8; total costs across all 12 requests are 12, 27 and 21 synthetic units respectively. The cheap and strongest-by-training baselines both choose small here: training qualities tie, and strongest breaks ties by lower cost. These are controlled offline outcomes, not measured model degradation. See `examples/extended-evaluation.json`. Common-runner checks pass. Published and verified: all four hosted Windows/Linux Python 3.11/3.13 jobs pass. No new Jev calls.

Extended evaluation verification: https://github.com/Ppetip/budget-cortex/actions/runs/35795065445

2026-09-23 06:53 UTC: Routing reports now select only validated cost/success fields from outcome records. Extra metadata cannot override the reported request ID, chosen model or estimate, and unused fields are excluded from results. Outcome collections must be arrays and model names must be nonempty strings before baseline comparisons. Offline synthetic cost units remain separate from live provider accounting. Checks pass; run ID b22f20218a6342da9a68daa7d1a24217. No live calls. Hosted verification passed on all four OS/Python combinations.

2026-09-23 10:54 UTC verification follow-up: Published code and all four hosted jobs verified after the earlier approval-review usage-limit interruption. Existing check suites were not rerun solely to create history. Run: https://github.com/Ppetip/budget-cortex/actions/runs/35829392965

2026-09-23 14:55 UTC: Added guidance for interpreting saved-check freshness in the optional local Codex runner. A current check validates offline routing and accounting code. It does not establish live model quality or authorize this router to override Jev. The shared runner now records check-source fingerprints and provides read-only status. All five current app checks passed (234 tests total), along with 24 local runner regressions. Run ID: 811900b822db42e390b5e1714afbbe25. App implementation unchanged; this documentation update skips redundant hosted CI. No live calls or new performance claim.

2026-09-24 06:59 UTC: Added selection_evidence snapshots with successes, observations, smoothed estimate and context/global scope. Counts include training plus feedback released before selection; cheapest choices and abstentions have null evidence. Existing routing behavior and contextual diagnostic remain unchanged. No provider calls or additional spending. Local checks pass; run ID 66f2c076ef004e688889f27a261f2c01. All four hosted Windows/Linux Python 3.11/3.13 jobs pass.

Selection-evidence verification: https://github.com/Ppetip/budget-cortex/actions/runs/35967926324
