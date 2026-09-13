# Archived notebooks

Archived 2026-09-13 alongside the data they analyze (see
`numerics/data/archive/README.md`).

These three notebooks fit models to the **cumulative** frozen-fraction
definition (a site is frozen if it never flipped since t=0), superseded
2026-09-14 by the rolling-window definition (a site re-enters the frozen
set after being quiet for W steps). They are pinned to run directories
that now live in `numerics/data/archive/`, not `numerics/data/raw/`, so
re-executing them as-is will fail to find their data.

Kept for provenance/history, not as current results:
- `h1_fit_frozen_fraction.ipynb`
- `h1_fit_frozen_fraction_fitting_range.ipynb`
- `h1_fit_frozen_fraction_combined.ipynb`
