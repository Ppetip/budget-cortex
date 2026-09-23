# Budget Cortex

An adaptive model router with an explicit quality target, spend ceiling, and abstention path.

**v0.1 development prototype Ãƒâ€šÃ‚Â· Python 3.11+ Ãƒâ€šÃ‚Â· GPL-3.0-only**

## What works

Fits smoothed success estimates on a development outcome table and replays a context-aware router against cheapest-model and strongest-model baselines. Uses integer micro-unit accounting and abstains when no acceptable affordable route exists.

## Run

No third-party Python dependencies. Clone this repository and run from its root:

```sh
python app.py
python app.py --input examples/outcomes.json --budget 22 --target 0.7
```

For commands using a file under `runs/`, create that directory first (`mkdir runs`). Generated files are ignored by Git. The default demo is offline and uses invented data.

## Test

```sh
python -m unittest discover -s tests -v
```

45 tests pass locally; hosted verification for this input-boundary update is pending.

## Architecture

`Router` estimates success rates by context/model from training rows. `evaluate` withholds held-out outcomes from decisions; routing sees context, known prices and remaining budget. Quality is revealed only after selecting a model. The strongest baseline uses global training quality.

## Reproduced example

On the ten synthetic requests with a 22-unit budget: adaptive routing spends 20, answers 8 and succeeds on 80% of all requests; cheapest spends 10 and succeeds on 50%; strongest spends 20, answers 4 and succeeds on 40%. These are deliberately constructed fixture outcomes, not measured provider performance.

See [the captured output](examples/demo-output.json). Rerun `python app.py` to reproduce it.

## Limits

No live API routing, online bandit, calibrated confidence, latency benchmark or real provider pricing yet. Offline data is fully observed. Different IDs alone do not guarantee independent datasets. A quality threshold is not a quality guarantee. Unanswered requests count against the all-request success rate.

## Next experiment

Add streaming partial-feedback evaluation and drift scenarios with a fixed held-out protocol.

The [design brief](docs/DESIGN.md) describes the larger goal, including unimplemented milestones.

## Contribute

Set an acceptable failure rate and identify requests where a wrong answer is worse than asking a person. Use invented or openly licensed examples. Include expected outcomes, edge cases and data provenance.

## License

Copyright (c) 2026 Ppetip. Original code is licensed under GNU GPL version 3 only; see [LICENSE](LICENSE).

## Latest development pass

Optional learning consumes only the chosen model outcome.

Run `python app.py --learn`. Updates are immediate; no exploration, delayed feedback or calibrated quality guarantee.

## Optional Jev workflow

Run `python jev_workflow.py` to preview the synthetic request without network access.
To opt into live calls, create a local `.env` using `.env.example`, set your TypeSafe key,
and point `JEV_BUDGET_DB` at one absolute SQLite path shared by all five projects.
Then run `python jev_workflow.py --live --env-file /absolute/path/to/.env`.
Do not commit the real configuration. No packages or model downloads are required.

The adapter pins `jev-1.13.0` and sends only the built-in synthetic fixture in this CLI.
Agent Black Box makes four replay calls; each other workflow makes one. The reusable
`Client.evaluate(state, questions)` interface supports bounded Choice questions.
Treat low-confidence decisions as abstentions; its 0.8 cutoff is a heuristic, not calibrated certainty.

The shared ledger allows at most $3 in cumulative reservations: one cent is permanently
reserved **before each attempt**, including timeouts and failed requests. It never retries
automatically. Concurrent processes share an atomic SQLite reservation. Never reset,
delete, replace or split the ledger to regain budget. This guard covers this client,
not unrelated account use. Provider billing remains authoritative.

[Official TypeSafe pricing](https://docs.typesafe.ai/models) checked 2026-09-21 lists
$0.042 per million input tokens and free output. One cent exceeds a full 65,536-input-token
request at that rate; the client also limits serialized input to 16KB. Estimates use
reported input tokens and exclude unknown failed-request usage. Calls fail closed on
2026-09-28 until pricing and the reservation bound are reviewed. Never extend the review
date without checking the provider's current terms.

[The HTTP API](https://docs.typesafe.ai/api) uses the fixed official TypeSafe endpoint.
Redirects are refused, responses are schema-checked, and error bodies/credentials are
not logged. Tests mock the provider and do not spend money.

`examples/jev-live-smoke.json` records a real 2026-09-21 model response on synthetic input.
It is a connectivity and workflow smoke check, not a quality benchmark or evidence of
training, generalization, speed or production reliability. Re-running it may change results.

Jev context classification feeds the synthetic router; a zero budget still abstains.

## Continuous verification

[Offline checks](https://github.com/Ppetip/budget-cortex/actions/workflows/offline.yml) run tests and JSON CLI smoke checks on Windows/Linux with Python 3.11/3.13 for pushes and pull requests. Run `python verify_demos.py` locally. Actions are pinned to immutable commits, use read-only permissions, and receive no provider secrets. Jev tests use mocks; the CLI check uses its default dry run. The workflow does not run live inference.

### First-time budget setup and recovery

For a genuinely new allowance only, run `python jev_client.py --init-budget /absolute/path/to/jev-budget.sqlite3` once, then use that exact path in `JEV_BUDGET_DB` for every app. Initialization refuses existing files, including empty files. Do not initialize a new ledger to replace lost spending history. Existing users keep their existing ledger and skip setup.

Live clients now open existing ledgers only, including at reservation time. A missing, mistyped, or empty ledger stops calls instead of silently recreating a zero balance. Restore missing history from a trusted backup; do not reset it. This prevents accidental recreation, not deliberate administrator modification or substitution of a different valid database.

## Latest reliability improvement

The reusable `Router.choose` entry point now rejects negative, fractional and boolean costs, invalid remaining budgets, and invalid quality targets. Valid zero-cost routes remain supported. Cost units in this offline router remain synthetic; the Jev account ledger is separate.

See [Reading results](docs/RESULTS.md) for outcome fields, denominators, abstentions and the limits of command success.

## New evaluation path

Run `python app.py --learn --feedback-delay 2`. Delay counts additional intervening requests: a result selected at index i with delay d > 0 becomes visible before index i+d+1. Delay zero keeps immediate after-selection updates. Late feedback remains pending at the end; no hidden flush is used for decisions. Feedback affects only adaptive learning, and spending is still charged when a model is selected. These are offline outcome simulations.

## Evaluation reliability

Each decision records `quality_at_selection`, the contextual smoothed estimate before applying that request's outcome, and `feedback_received_before_selection`, the number of delayed outcomes released immediately before this choice. Immediate feedback is applied after its own choice and is not counted as a delayed release. Abstentions retain release counts and use a null selected-model estimate. For the strongest baseline, this contextual estimate is diagnostic; selection still uses global quality. Estimates are not calibrated guarantees.

## Extended evaluation

Run `python shift.py` (Codex route `shift`). This authored scenario makes the small model fail after request four while keeping the visible context constant. Across eight later requests, frozen estimates succeed 0/8, immediate feedback 5/8 and delayed feedback 3/8; total costs across all 12 requests are 12, 27 and 21 synthetic units respectively. The cheap and strongest-by-training baselines both choose small here: training qualities tie, and strongest breaks ties by lower cost. These are controlled offline outcomes, not measured model degradation. See `examples/extended-evaluation.json`.

## Input boundaries

Routing reports now select only validated cost/success fields from outcome records. Extra metadata cannot override the reported request ID, chosen model or estimate, and unused fields are excluded from results. Outcome collections must be arrays and model names must be nonempty strings before baseline comparisons. Offline synthetic cost units remain separate from live provider accounting.
