# SPDX-License-Identifier: GPL-3.0-only
import unittest
from app import evaluate, Router

class OutcomeBoundaryTests(unittest.TestCase):
    def row(self,id):return {'id':id,'context':'x','models':{'small':{'cost_micro':1,'success':True}}}
    def test_outcome_metadata_cannot_spoof_decision_identity_or_leak_extra_fields(self):
        request=self.row('actual');request['models']['small'].update(id='spoof',model='spoof',private_note='excluded',quality_at_selection=99)
        decision=evaluate([self.row('train')],[request],target=.5)['decisions'][0]
        self.assertEqual(decision['id'],'actual');self.assertEqual(decision['model'],'small')
        self.assertNotIn('private_note',decision);self.assertAlmostEqual(decision['quality_at_selection'],2/3)
    def test_non_array_rows_rejected_instead_of_exhausting_generator(self):
        for rows in ({},None,(self.row('x') for _ in range(1))):
            with self.assertRaises(ValueError):Router(rows)
    def test_model_names_validated_before_baseline_comparison(self):
        row=self.row('bad');row['models'][1]={'cost_micro':1,'success':True}
        with self.assertRaises(ValueError):evaluate([], [row],policy='cheapest')
