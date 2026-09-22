# SPDX-License-Identifier: GPL-3.0-only
"""Controlled synthetic quality shift with immediate and delayed feedback."""
import json
from app import evaluate

def fixtures():
    def row(id,success):
        return {"id":id,"context":"same-observed-context","models":{
            "small":{"cost_micro":1,"success":success},"large":{"cost_micro":4,"success":True}}}
    return [row(f"train-{i}",True) for i in range(4)], [row(f"eval-{i}",i<4) for i in range(12)]

def demo():
    training, requests = fixtures()
    runs=[]
    for label,policy,learn,delay in (("frozen","adaptive",False,0),("immediate","adaptive",True,0),
                                    ("delayed-2","adaptive",True,2),("cheap","cheapest",False,0),("strong","strongest",False,0)):
        result=evaluate(training,requests,budget_micro=40,target=.7,policy=policy,learn=learn,feedback_delay=delay)
        phase=[]
        for name,decisions in (("before-shift",result["decisions"][:4]),("after-shift",result["decisions"][4:])):
            phase.append({"phase":name,"requests":len(decisions),"successes":sum(d.get("success") is True for d in decisions),
                          "abstained":sum(d["model"] is None for d in decisions)})
        runs.append({"condition":label,**result,"phases":phase})
    return {"data":"synthetic-small-model-quality-shift","shift_at_index":4,"comparisons":runs,
            "limitation":"Hand-authored fully observed outcomes, constant visible context and synthetic cost units. Large-model outcomes stay successful by construction. No empirical model degradation, live inference or stochastic bandit experiment."}

if __name__ == "__main__":
    print(json.dumps(demo(),indent=2))
