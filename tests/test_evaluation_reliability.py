# SPDX-License-Identifier: GPL-3.0-only
import unittest
from app import evaluate

def row(id,ok):
    return {'id':id,'context':'x','models':{'small':{'cost_micro':1,'success':ok}}}

class FeedbackAuditTests(unittest.TestCase):
    def test_estimate_captured_before_current_label(self):
        result=evaluate([row('train',True)],[row('test',False)],target=0,learn=True)
        self.assertAlmostEqual(result['decisions'][0]['quality_at_selection'],2/3)

    def test_delay_release_and_estimate_are_visible(self):
        result=evaluate([row('train',True)],[row(str(i),False) for i in range(3)],target=0,learn=True,feedback_delay=1)
        decisions=result['decisions']
        self.assertEqual([d['feedback_received_before_selection'] for d in decisions],[0,0,1])
        self.assertEqual([d['quality_at_selection'] for d in decisions],[2/3,2/3,.5])

    def test_abstention_still_records_arriving_feedback(self):
        result=evaluate([row('train',True)],[row(str(i),False) for i in range(3)],budget_micro=1,target=0,learn=True,feedback_delay=1)
        last=result['decisions'][-1]
        self.assertIsNone(last['model']);self.assertIsNone(last['quality_at_selection'])
        self.assertEqual(last['feedback_received_before_selection'],1)
