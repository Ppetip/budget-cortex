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
