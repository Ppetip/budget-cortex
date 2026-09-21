# Reading routing results

A successful CLI command means the simulation completed, not that every request succeeded.

- `answered` and `abstained` must be interpreted together. `success_rate_all` includes abstentions in the denominator; `success_rate_answered` excludes them.
- `spent_micro` and `budget_micro` are the offline outcome matrix's cost units. They are separate from the real Jev account ledger.
- Compare each entry of `comparisons`; the adaptive result is not a summary of all policies.
- The synthetic adaptive demo currently answers eight requests, abstains on two, and spends 20 of 22 units. Its success rate across all requests is 80%.

These fixed invented costs/outcomes are not provider invoices or measured production quality. Optional learning uses selected-model feedback; that does not establish calibration or robustness to distribution shift.
