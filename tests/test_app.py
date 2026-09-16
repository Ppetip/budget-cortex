import copy
import unittest
from app import demo, evaluate


class RoutingTests(unittest.TestCase):
    def test_never_overspends(self):
        train, test = demo()
        for budget in range(31):
            for policy in ("adaptive", "cheapest", "strongest"):
                self.assertLessEqual(evaluate(train, test, budget, policy=policy)["spent_micro"], budget)

    def test_no_outcome_leakage(self):
        train, test = demo()
        changed = copy.deepcopy(test)
        for row in changed:
            for outcome in row["models"].values():
                outcome["success"] = not outcome["success"]
        before, after = evaluate(train, test), evaluate(train, changed)
        self.assertEqual([d["model"] for d in before["decisions"]], [d["model"] for d in after["decisions"]])

    def test_unseen_context_abstains(self):
        train, test = demo()
        test[0]["context"] = "unknown"
        self.assertIsNone(evaluate(train, test)["decisions"][0]["model"])

    def test_zero_budget(self):
        self.assertEqual(evaluate(*demo(), budget_micro=0)["answered"], 0)

    def test_overlap_rejected(self):
        train, test = demo()
        test[0]["id"] = train[0]["id"]
        with self.assertRaises(ValueError):
            evaluate(train, test)

    def test_negative_cost_rejected(self):
        train, test = demo()
        test[0]["models"]["small"]["cost_micro"] = -1
        with self.assertRaises(ValueError):
            evaluate(train, test)

    def test_context_changes_choice(self):
        result = evaluate(*demo())
        self.assertEqual([d["model"] for d in result["decisions"][:2]], ["small", "large"])

    def test_abstention_counts_in_all_rate(self):
        result = evaluate(*demo(), budget_micro=1)
        self.assertEqual(result["success_rate_answered"], 1)
        self.assertEqual(result["success_rate_all"], .1)

    def test_strongest_baseline_is_context_independent(self):
        result = evaluate(*demo(), budget_micro=100, policy="strongest")
        self.assertEqual({d["model"] for d in result["decisions"]}, {"large"})

    def test_nan_target_rejected(self):
        with self.assertRaises(ValueError):
            evaluate(*demo(), target=float("nan"))


if __name__ == "__main__":
    unittest.main()
