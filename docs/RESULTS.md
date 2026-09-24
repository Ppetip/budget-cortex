# Reading routing results

A successful CLI command means the simulation completed, not that every request succeeded.

- `answered` and `abstained` must be interpreted together. `success_rate_all` includes abstentions in the denominator; `success_rate_answered` excludes them.
- `spent_micro` and `budget_micro` are the offline outcome matrix's cost units. They are separate from the real Jev account ledger.
- Compare each entry of `comparisons`; the adaptive result is not a summary of all policies.
- The synthetic adaptive demo currently answers eight requests, abstains on two, and spends 20 of 22 units. Its success rate across all requests is 80%.

These fixed invented costs/outcomes are not provider invoices or measured production quality. Optional learning uses selected-model feedback; that does not establish calibration or robustness to distribution shift.

## Saved-check freshness in the local AI Lab workflow

When using the optional AI Lab workspace integration, run `python lab.py status` from the workspace root. This reads saved results without rerunning tests or inference and lists the latest checks for every tool. The shared runner is a local integration, not part of a standalone clone of this repository; standalone checks remain documented in README.

`check_passed` records command/test completion. `freshness` is separate:

- `current`: the explicit source inputs and Python runtime match the completed check.
- `source-or-runtime-changed`: rerun checks after relevant code or runtime changes.
- `changed-during-checks`: inputs changed while checks ran; that run cannot verify one stable version.
- `unverified-legacy`: an older result has no source fingerprint.
- `not-run`: no saved check exists for this tool.

Fingerprints cover project Python files, tests, checked-in example JSON/JSONL paths, workflow YAML and shared runner Python files. They omit documentation, .env, databases, private run outputs and arbitrary analysis input files. Current does not prove unchanged external dependencies or OS state. Saved reports are private local cache records, not signed attestations. A later demo never replaces a check result, and a current failing check is still a failure.

A current check validates offline routing and accounting code. It does not establish live model quality or authorize this router to override Jev.

## Evidence behind a selection

Each decision includes `selection_evidence`, captured before consuming its own outcome. For adaptive routing it contains `scope: "context"`, `successes`, `observations`, and `smoothed_estimate` for the chosen model in that context. For the strongest baseline, `scope: "global"` pools that model's observations across training contexts. The estimate is `(successes + 1) / (observations + 2)`; the counts exclude those two smoothing pseudo-observations. Only released feedback can increase the counts. With frozen evaluation, only training outcomes contribute.

For example, one observed success produces an estimate of 2/3 with `observations: 1`; the sample count makes that limited support visible. Cheapest selections and abstentions report null evidence because no quality-based model selection was made. Existing `quality_at_selection` remains a contextual diagnostic even for the strongest or cheapest baseline. Use the new field to inspect the actual quality scope used for selection.

The routing rule, costs and feedback schedule are unchanged. These descriptive counts are not confidence intervals, independent samples or calibrated guarantees. Repeated or correlated outcomes can overstate the strength of evidence. This offline report does not authorize live routing or override Jev.
