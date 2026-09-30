# SPDX-License-Identifier: GPL-3.0-only
"""Synthetic accounting and information-boundary checks, not model benchmarks."""
import copy
import random
import unittest
from unittest.mock import patch
from app import demo, evaluate


class RandomBaselineTests(unittest.TestCase):
    def test_repeatability_order_independence_and_global_rng_isolation(self):
        train, rows = demo()
        original = copy.deepcopy((train, rows))
        state = random.getstate()
        first = evaluate(train, rows, policy="random", random_seed=7)
        self.assertEqual(first, evaluate(train, rows, policy="random", random_seed=7))
        reordered = copy.deepcopy(rows)
        for row in reordered:
            row["models"] = dict(reversed(list(row["models"].items())))
        self.assertEqual(first, evaluate(train, reordered, policy="random", random_seed=7))
        self.assertEqual(state, random.getstate())
        self.assertEqual((train, rows), original)

    def test_outcomes_training_and_context_do_not_choose_models(self):
        train, rows = demo()
        first = evaluate(train, rows, policy="random", random_seed=-7)
        changed = copy.deepcopy(rows)
        for row in changed:
            row["context"] = "unseen"
            for outcome in row["models"].values():
                outcome["success"] = not outcome["success"]
        second = evaluate([], changed, target=1, policy="random", random_seed=-7)
        self.assertEqual([d["model"] for d in first["decisions"]],
                         [d["model"] for d in second["decisions"]])

    def test_budget_and_probability_reconstructed_before_each_choice(self):
        train, rows = demo()
        for seed in range(8):
            for budget in range(25):
                result = evaluate(train, rows, budget, policy="random", random_seed=seed)
                remaining = budget
                for row, decision in zip(rows, result["decisions"]):
                    eligible = [name for name, out in row["models"].items()
                                if out["cost_micro"] <= remaining]
                    self.assertEqual(decision["eligible_model_count"], len(eligible))
                    self.assertEqual(decision["selection_probability"],
                                     1 / len(eligible) if eligible else None)
                    self.assertIsNone(decision["selection_evidence"])
                    if eligible:
                        self.assertIn(decision["model"], eligible)
                        self.assertEqual(decision["cost_micro"], row["models"][decision["model"]]["cost_micro"])
                    else:
                        self.assertIsNone(decision["model"])
                    remaining -= decision["cost_micro"]
                    self.assertGreaterEqual(remaining, 0)
                self.assertEqual(result["spent_micro"], budget - remaining)

    def test_free_routes_empty_input_and_no_candidate(self):
        row = {"id": "free", "context": "new", "models": {
            "free": {"cost_micro": 0, "success": True},
            "paid": {"cost_micro": 1, "success": False}}}
        result = evaluate([], [row], 0, policy="random", random_seed=0)
        self.assertEqual(result["decisions"][0]["model"], "free")
        self.assertEqual(result["spent_micro"], 0)
        self.assertEqual(result["decisions"][0]["selection_probability"], 1)
        self.assertIsNone(evaluate([], [], policy="random", random_seed=0)["success_rate_all"])
        del row["models"]["free"]
        result = evaluate([], [row], 0, policy="random", random_seed=0)
        self.assertEqual(result["abstained"], 1)
        self.assertIsNone(result["success_rate_answered"])

    def test_invalid_inputs_fail_before_random_draw(self):
        train, rows = demo()
        with patch("app.random.Random") as rng:
            for seed in (None, True, 1.5, "7"):
                with self.assertRaises(ValueError):
                    evaluate(train, rows, policy="random", random_seed=seed)
            with self.assertRaises(ValueError):
                evaluate(train, rows, random_seed=7)
            rows[-1]["models"]["small"]["cost_micro"] = -1
            with self.assertRaises(ValueError):
                evaluate(train, rows, policy="random", random_seed=7)
            rng.assert_not_called()

    def test_no_learning_or_metadata_spoofing(self):
        train, rows = demo()
        for row in rows:
            for outcome in row["models"].values():
                outcome.update(selection_probability=42, eligible_model_count=99,
                               random_seed="secret", selection_evidence={"spoof": True})
        with patch("app.Router.observe") as observe:
            result = evaluate(train, rows, policy="random", random_seed=7,
                              learn=True, feedback_delay=2)
            observe.assert_not_called()
        self.assertFalse(result["selected_feedback_learning"])
        self.assertEqual(result["pending_feedback"], 0)
        self.assertEqual(result["random_seed"], 7)
        for d in result["decisions"]:
            self.assertNotIn("random_seed", d)
            self.assertIn(d["selection_probability"], (None, .5, 1))
            self.assertIsNone(d["selection_evidence"])
