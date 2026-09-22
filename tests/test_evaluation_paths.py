# SPDX-License-Identifier: GPL-3.0-only
import unittest
from app import evaluate

def row(id,ok):return {'id':id,'context':'x','models':{'small':{'cost_micro':1,'success':ok},'large':{'cost_micro':5,'success':True}}}
class DelayedFeedbackTests(unittest.TestCase):
    def test_delay_blocks_future_feedback_from_early_decisions(self):
        training=[row('train',True)];requests=[row(str(i),False) for i in range(3)]
        immediate=evaluate(training,requests,100,.6,learn=True)
        delayed=evaluate(training,requests,100,.6,learn=True,feedback_delay=1)
        self.assertEqual([d['model'] for d in immediate['decisions']],['small','large','large'])
        self.assertEqual([d['model'] for d in delayed['decisions']],['small','small','large'])
        self.assertEqual(delayed['pending_feedback'],2)
    def test_feedback_after_horizon_remains_pending(self):
        r=evaluate([row('train',True)],[row('test',False)],1,.6,learn=True,feedback_delay=5)
        self.assertEqual(r['pending_feedback'],1);self.assertEqual(r['spent_micro'],1)
    def test_invalid_delay_and_learn_rejected(self):
        for learn,delay in [(True,-1),(True,True),(True,1.5),('yes',0)]:
            with self.assertRaises(ValueError):evaluate([],[],learn=learn,feedback_delay=delay)
