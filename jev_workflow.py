# SPDX-License-Identifier: GPL-3.0-only
import argparse
import json
from pathlib import Path
from jev_client import Client, JevError, MODEL, choice, selected
import app

def request_data():
    return {"request": "Extract the order number from: order AB-104 ships tomorrow."}, choice(
        "Classify routing context without access to model outcomes: simple extraction versus ambiguous multi-step policy reasoning.",
        {"simple": "Direct unambiguous extraction", "complex": "Ambiguous policy or multi-step reasoning", "abstain": "Insufficient evidence"})

def guarded_route(context, remaining):
    training, _ = app.demo()
    return app.Router(training).choose(context, {"small": 1, "large": 5}, remaining, .7)

def run(client):
    state, questions = request_data()
    response = client.evaluate(state, questions)
    context = selected(response, "abstain")
    return {"context": context, "selected_model": guarded_route(context, 2),
            "model_with_zero_budget": guarded_route(context, 0), "synthetic_routing_budget_micro": 2,
            "usage": [response["usage"]],
            "limitation": "Live context classification feeds an offline router. Routing prices/outcomes are synthetic; Jev spending is accounted separately. No selected model is called."}

def main():
    parser = argparse.ArgumentParser(description="Preview the synthetic Jev request; --live explicitly opts into paid calls.")
    parser.add_argument("--live", action="store_true")
    parser.add_argument("--env-file", type=Path)
    args = parser.parse_args()
    if not args.live:
        state, questions = request_data()
        print(json.dumps({"mode": "dry-run-no-network", "model": MODEL, "state": state, "questions": questions}, indent=2))
        return
    if args.env_file is None:
        parser.error("--live requires --env-file with the shared budget ledger")
    try:
        client = Client(args.env_file)
        result = run(client)
        print(json.dumps({"mode": "live-model-on-synthetic-data", "model": MODEL, **result, "budget": client.budget.summary()}, indent=2))
    except JevError as exc:
        parser.exit(1, str(exc) + "\n")

if __name__ == "__main__":
    main()
