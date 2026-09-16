# Budget Cortex

An adaptive model router with an explicit quality target, spend ceiling, and abstention path.

## Problem

Startups need predictable cost and useful answers despite changing task mixes and model reliability.

## Approach

Start with static and confidence-threshold routing baselines. Add a contextual bandit trained only on available feedback, track calibration and distribution shift, and permit escalation or abstention.

## Demo concept

Move from simple extraction requests to ambiguous policy questions; show how routing responds and what cost-quality tradeoffs result.

## First implementation

Offline replay of a fully observed synthetic request/model outcome matrix, reproducible routing policies, hard-budget accounting and honest synthetic-result labels.

## Evaluation

Measure total cost, quality, abstention, tail latency and budget violations. Distinguish fully observed offline simulation from deployment with partial feedback. Compare static cheap, static strong and random routing.

## Milestones

1. Offline benchmark and budget invariants
2. Calibrated threshold router
3. Contextual bandit with logged propensities and delayed feedback
4. Optional live provider adapters and shift evaluation

## Your contribution

Set an acceptable failure rate and identify requests where a wrong answer is worse than asking a person.

## Status and license

Design brief only; no implementation or measured results yet. Original code will use GPL-3.0-only.
