"""Offline model routing with integer budgets and development-only estimates."""
import argparse
import json
from pathlib import Path


def validate(rows):
    ids = set()
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"] or row["id"] in ids:
            raise ValueError("unique nonempty string IDs required")
        ids.add(row["id"])
        if not isinstance(row.get("context"), str) or not row["context"]:
            raise ValueError("context required")
        if not isinstance(row.get("models"), dict) or not row["models"]:
            raise ValueError("model outcomes required")
        for name, out in row["models"].items():
            if not name or not isinstance(out, dict):
                raise ValueError("named model outcome required")
            if type(out.get("cost_micro")) is not int or out["cost_micro"] < 0:
                raise ValueError("cost_micro must be a nonnegative integer")
            if type(out.get("success")) is not bool:
                raise ValueError("success must be boolean")
    return rows


class Router:
    def __init__(self, training):
        self.stats = {}
        for row in validate(training):
            for name, outcome in row["models"].items():
                key = (row["context"], name)
                wins, count = self.stats.get(key, (0, 0))
                self.stats[key] = (wins + outcome["success"], count + 1)

    def observe(self, context, name, success):
        """Consume only the chosen model's immediate feedback."""
        if not isinstance(context, str) or not context or not isinstance(name, str) or not name or type(success) is not bool:
            raise ValueError("context, model name and boolean feedback required")
        key = (context, name)
        wins, count = self.stats.get(key, (0, 0))
        self.stats[key] = (wins + success, count + 1)

    def quality(self, context, name):
        wins, count = self.stats.get((context, name), (0, 0))
        return (wins + 1) / (count + 2) if count else None

    def global_quality(self, name):
        entries = [(w, n) for (_, model), (w, n) in self.stats.items() if model == name]
        count = sum(n for _, n in entries)
        return (sum(w for w, _ in entries) + 1) / (count + 2) if count else None

    def choose(self, context, costs, remaining, target):
        if not isinstance(context, str) or not context:
            raise ValueError("context required")
        if (not isinstance(costs, dict) or not costs
                or any(not isinstance(name, str) or not name or type(cost) is not int or cost < 0
                       for name, cost in costs.items())):
            raise ValueError("named nonnegative integer costs required")
        if type(remaining) is not int or remaining < 0:
            raise ValueError("remaining budget must be a nonnegative integer")
        if type(target) not in (int, float) or not 0 <= target <= 1:
            raise ValueError("target must lie between zero and one")
        choices = [(cost, name) for name, cost in costs.items()
                   if cost <= remaining and self.quality(context, name) is not None
                   and self.quality(context, name) >= target]
        return min(choices)[1] if choices else None


def evaluate(training, requests, budget_micro=22, target=.7, policy="adaptive", learn=False, feedback_delay=0):
    if type(budget_micro) is not int or budget_micro < 0:
        raise ValueError("nonnegative integer budget required")
    if type(target) not in (int, float) or not 0 <= target <= 1:
        raise ValueError("target must lie between zero and one")
    if policy not in {"adaptive", "cheapest", "strongest"}:
        raise ValueError("unknown policy")
    if type(learn) is not bool or type(feedback_delay) is not int or feedback_delay < 0:
        raise ValueError("boolean learn and nonnegative integer feedback_delay required")
    validate(training)
    validate(requests)
    if {r["id"] for r in training} & {r["id"] for r in requests}:
        raise ValueError("training/evaluation ID overlap")
    router = Router(training)
    remaining, wins, answered = budget_micro, 0, 0
    decisions, pending = [], []
    for index, row in enumerate(requests):
        ready = [item for item in pending if item[0] <= index]
        pending = [item for item in pending if item[0] > index]
        for _, context, name, success in ready:
            router.observe(context, name, success)
        feedback_received = len(ready)
        costs = {name: out["cost_micro"] for name, out in row["models"].items()}
        if policy == "adaptive":
            model = router.choose(row["context"], costs, remaining, target)
        elif policy == "cheapest":
            model = min((cost, name) for name, cost in costs.items())[1]
        else:
            known = [(router.global_quality(name), -cost, name)
                     for name, cost in costs.items() if router.global_quality(name) is not None]
            model = max(known)[2] if known else None
        if model is not None and costs[model] > remaining:
            model = None
        audit = {"feedback_received_before_selection": feedback_received,
                 "quality_at_selection": router.quality(row["context"], model) if model is not None else None}
        if model is None:
            decisions.append({"id": row["id"], "model": None, "cost_micro": 0, **audit})
            continue
        outcome = row["models"][model]
        remaining -= outcome["cost_micro"]
        answered += 1
        wins += outcome["success"]
        if learn and policy == "adaptive":
            if feedback_delay == 0:
                router.observe(row["context"], model, outcome["success"])
            else:
                pending.append((index + feedback_delay + 1, row["context"], model, outcome["success"]))
        decisions.append({"id": row["id"], "model": model, **outcome, **audit})
    return {"feedback_delay": feedback_delay, "pending_feedback": len(pending), "policy": policy, "selected_feedback_learning": bool(learn and policy == "adaptive"), "budget_micro": budget_micro, "spent_micro": budget_micro - remaining,
            "answered": answered, "abstained": len(requests) - answered,
            "success_rate_answered": wins / answered if answered else None,
            "success_rate_all": wins / len(requests) if requests else None,
            "decisions": decisions}


def demo():
    def row(id, context, small_ok):
        return {"id": id, "context": context, "models": {
            "small": {"cost_micro": 1, "success": small_ok},
            "large": {"cost_micro": 5, "success": True}}}
    train = [row(f"train-{c}-{i}", c, c == "simple" or i < 3)
             for c in ("simple", "complex") for i in range(12)]
    test = [row(f"eval-{i}", "simple" if i % 2 == 0 else "complex", i % 2 == 0) for i in range(10)]
    return train, test


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, help="JSON with training and evaluation arrays")
    parser.add_argument("--budget", type=int, default=22)
    parser.add_argument("--target", type=float, default=.7)
    parser.add_argument("--learn", action="store_true", help="Update adaptive estimates from chosen-model feedback only")
    parser.add_argument("--feedback-delay", type=int, default=0, help="Additional requests before selected feedback arrives")
    args = parser.parse_args()
    if args.input:
        data = json.loads(args.input.read_text(encoding="utf-8"))
        train, test = data["training"], data["evaluation"]
    else:
        train, test = demo()
    print(json.dumps({"data": "synthetic-demo" if not args.input else "user-supplied-offline-outcomes",
                      "limitation": "Fully observed offline simulation. Estimates are not calibrated guarantees. Prices are synthetic micro-units, not provider prices. No live routing or bandit learning yet.",
                      "comparisons": [evaluate(train, test, args.budget, args.target, p, learn=args.learn, feedback_delay=args.feedback_delay)
                                      for p in ("adaptive", "cheapest", "strongest")]}, indent=2))


if __name__ == "__main__":
    main()
