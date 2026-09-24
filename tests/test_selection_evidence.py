# SPDX-License-Identifier: GPL-3.0-only
import unittest
from app import Router, evaluate


def row(identifier, success, context="x"):
    return {"id": identifier, "context": context,
            "models": {"small": {"cost_micro": 1, "success": success}}}


class SelectionEvidenceTests(unittest.TestCase):
    def test_immediate_feedback_is_visible_only_to_later_decisions(self):
        result = evaluate([row("train", True)], [row("a", False), row("b", True)],
                          target=0, learn=True)
        first, second = [d["selection_evidence"] for d in result["decisions"]]
        self.assertEqual(first, {"scope": "context", "successes": 1,
                                 "observations": 1, "smoothed_estimate": 2 / 3})
        self.assertEqual(second, {"scope": "context", "successes": 1,
                                  "observations": 2, "smoothed_estimate": 1 / 2})

    def test_delayed_feedback_counts_only_after_release(self):
        result = evaluate([row("train", True)], [row(str(i), False) for i in range(3)],
                          target=0, learn=True, feedback_delay=1)
        evidence = [d["selection_evidence"] for d in result["decisions"]]
        self.assertEqual([e["observations"] for e in evidence], [1, 1, 2])
        self.assertEqual([e["successes"] for e in evidence], [1, 1, 1])
        self.assertEqual([e["smoothed_estimate"] for e in evidence], [2 / 3, 2 / 3, 1 / 2])

    def test_strongest_uses_global_support_and_preserves_context_diagnostic(self):
        training = [row("x1", True), row("y1", False, "y"), row("y2", False, "y")]
        decision = evaluate(training, [row("test", True)], policy="strongest")["decisions"][0]
        self.assertEqual(decision["selection_evidence"], {"scope": "global", "successes": 1,
                         "observations": 3, "smoothed_estimate": 2 / 5})
        self.assertEqual(decision["quality_at_selection"], 2 / 3)
        unseen = evaluate(training, [row("test", True, "unseen")], policy="strongest")["decisions"][0]
        self.assertEqual(unseen["selection_evidence"], decision["selection_evidence"])
        self.assertIsNone(unseen["quality_at_selection"])

    def test_cheapest_and_abstentions_have_no_quality_selection_evidence(self):
        for options in ({"policy": "cheapest"}, {"budget_micro": 0, "target": 0},
                        {"target": 1}, {"policy": "strongest", "budget_micro": 0}):
            with self.subTest(options=options):
                decision = evaluate([row("train", True)], [row("test", True)], **options)["decisions"][0]
                self.assertIsNone(decision["selection_evidence"])

    def test_snapshot_is_detached_from_router_and_matches_selection_estimate(self):
        router = Router([row("x1", True), row("y1", False, "y")])
        context = router.selection_evidence("x", "small", "adaptive")
        global_evidence = router.selection_evidence("x", "small", "strongest")
        self.assertEqual(context["smoothed_estimate"], router.quality("x", "small"))
        self.assertEqual(global_evidence["smoothed_estimate"], router.global_quality("small"))
        router.observe("x", "small", False)
        self.assertEqual(context["observations"], 1)
        self.assertEqual(global_evidence["observations"], 2)
        context["successes"] = 999
        self.assertEqual(router.selection_evidence("x", "small", "adaptive")["successes"], 1)

    def test_outcome_metadata_cannot_spoof_support_counts(self):
        request = row("test", False)
        request["models"]["small"]["selection_evidence"] = {"observations": 999}
        decision = evaluate([row("train", True)], [request], target=0)["decisions"][0]
        self.assertEqual(decision["selection_evidence"]["observations"], 1)
