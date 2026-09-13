# Archived runs

Archived 2026-09-13, not deleted (per CLAUDE.md's inviolable rule).

The four `frozen_fraction_{test,production,fitting_range}_202609120*` runs
used the original **cumulative** frozen-fraction definition (a site is
frozen if it never flipped since t=0), before the rolling-window
definition (a site re-enters the frozen set after being quiet for W
steps) was adopted on 2026-09-14. See RESEARCH_LOG.md for the full
history of why the definition changed and how the new estimator's
burn-in was validated.

`frozen_fraction_test_20260913T062742Z` is a crashed, empty run (only
`parameters.json`, no samples) -- it hit the `SeedSequence` string-entropy
bug in `run_ensemble_rolling` before that was fixed the same day.

These are kept for provenance only. Do not use them as current results;
the analysis notebooks referencing them
(`numerics/notebooks/analysis/h1_fit_frozen_fraction*.ipynb`) are
likewise from before the definition change.
