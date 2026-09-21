import copy
import unittest
from app import Router, demo, evaluate

class FeedbackTests(unittest.TestCase):
    def test_only_selected_statistics_change(self):
        r = Router(demo()[0]); old = dict(r.stats)
        r.observe('simple', 'small', False)
        self.assertEqual(r.stats[('simple','large')], old[('simple','large')])
        self.assertEqual(r.stats[('simple','small')][1], old[('simple','small')][1]+1)
    def test_unchosen_outcomes_do_not_affect_learning(self):
        train, test = demo(); changed = copy.deepcopy(test)
        for row in changed:
            unchosen = 'large' if row['context']=='simple' else 'small'
            row['models'][unchosen]['success'] = not row['models'][unchosen]['success']
        a = evaluate(train,test,100,learn=True); b = evaluate(train,changed,100,learn=True)
        self.assertEqual(a,b)
    def test_feedback_must_be_boolean(self):
        with self.assertRaises(ValueError): Router([]).observe('x','y','yes')
    def test_online_budget_still_hard(self):
        for budget in range(25): self.assertLessEqual(evaluate(*demo(),budget_micro=budget,learn=True)['spent_micro'],budget)
