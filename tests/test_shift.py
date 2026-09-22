# SPDX-License-Identifier: GPL-3.0-only
import unittest
from shift import demo, fixtures

class ShiftTests(unittest.TestCase):
    def test_shift_labels_do_not_change_visible_context_or_overlap_training(self):
        train,requests=fixtures()
        self.assertFalse({r['id'] for r in train}&{r['id'] for r in requests})
        self.assertEqual(len({r['context'] for r in train+requests}),1)
        self.assertEqual([r['models']['small']['success'] for r in requests],[True]*4+[False]*8)
    def test_delayed_feedback_changes_after_shift_decisions(self):
        results={r['condition']:r for r in demo()['comparisons']}
        early=results['immediate']['decisions'];late=results['delayed-2']['decisions']
        self.assertEqual([d['model'] for d in early[:4]],[d['model'] for d in late[:4]])
        self.assertGreater(results['immediate']['phases'][1]['successes'],results['delayed-2']['phases'][1]['successes'])
        self.assertEqual(results['frozen']['phases'][1]['successes'],0)
    def test_each_comparison_obeys_budget_and_phase_accounting(self):
        for r in demo()['comparisons']:
            self.assertLessEqual(r['spent_micro'],r['budget_micro'])
            self.assertEqual(sum(p['requests'] for p in r['phases']),len(r['decisions']))
            self.assertEqual(sum(p['successes'] for p in r['phases']),sum(d.get('success') is True for d in r['decisions']))
