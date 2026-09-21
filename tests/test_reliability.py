# SPDX-License-Identifier: GPL-3.0-only
import unittest
from app import Router,demo

class DirectRoutingValidationTests(unittest.TestCase):
    def setUp(self): self.router=Router(demo()[0])
    def test_invalid_costs_rejected(self):
        for cost in (-1,True,1.5,float('nan')):
            with self.subTest(cost=cost),self.assertRaises(ValueError): self.router.choose('simple',{'small':cost},5,.7)
    def test_invalid_budget_and_target_rejected(self):
        for remaining,target in [(-1,.7),(True,.7),(1.5,.7),(5,float('nan')),(5,True),(5,1.1)]:
            with self.subTest(remaining=remaining,target=target),self.assertRaises(ValueError): self.router.choose('simple',{'small':1},remaining,target)
    def test_valid_free_route_is_allowed(self):
        self.assertEqual(self.router.choose('simple',{'small':0},0,.7),'small')
