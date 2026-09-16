# Budget Cortex

An adaptive model router with an explicit quality target, spend ceiling, and abstention path.

**v0.1 development prototype · Python 3.11+ · GPL-3.0-only**

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

10 tests passed locally on Python 3.13. Other Python versions have not yet been exercised.

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
