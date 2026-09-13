## 2026-09-12 — Frozen-fraction pipeline: smoke test on test.yaml

**Question:** Does the frozen-fraction (f_N) measurement pipeline for H1 run
end-to-end without crashing, and do results look sane at small N?

**Hypothesis:** No hypothesis about physics being tested here — this is a
code smoke test, not a production measurement.

**Method:** Static reachability of frozen sites is estimated empirically per
realization by running the stochastic 0110<->1001 dynamics (PBC, density
0.5) until either no active sites remain, or no new site has been flipped
for `patience = 20*L` consecutive moves (safety cap `max_steps = 10*patience`).
Ensemble-averaged over realizations, sampled adaptively until
SE(f_N)/f_N < 0.10 or `max_samples_per_N = 200` is reached. Config:
`numerics/config/test.yaml` (at the time of this run, N_values =
[50, 100, 200, 400]; subsequently edited to [50, 100, 200] — this run
predates that edit). Master seed: 12345 (recorded in the run's
`parameters.json`). Runtime: ~6.6s total for 4 values of N.

**Result:**
- L=50: f_N = 0.3710 +- 0.0257 (n=40, discarded=0)
- L=100: f_N = 0.3545 +- 0.0218 (n=40, discarded=0)
- L=200: f_N = 0.3605 +- 0.0164 (n=20, discarded=0)
- L=400: f_N = 0.3325 +- 0.0142 (n=20, discarded=0)

All realizations converged (zero discarded) within the patience/max_steps
budget. Raw per-realization samples and parameters are in
`numerics/data/raw/frozen_fraction_test_20260912T062103Z/`.

**Interpretation:** [left blank]

**Next question:** Whether this pipeline's assumptions hold up at
production scale (N up to 1600) and what the cost estimate looks like
before that run is approved. The static/combinatorial reachability
equivalence used to justify the patience-based stopping criterion is still
unverified against brute-force enumeration (see HYPOTHESES.md, H1,
flagged [UNCERTAIN]).

**Git commit:** uncommitted (all pipeline code, config, and this log entry
are currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-12 — H1 production run: f_N vs N, N=100..4800

**Question:** For equal density of 0/1 particles under PBC, does the frozen
fraction f_N saturate to a nonzero constant as N -> infinity, or vanish
(power-law / logarithmically)? (H1, HYPOTHESES.md)

**Hypothesis:** H1 as stated — f_N -> f_infinity > 0 (see HYPOTHESES.md for
the three candidate functional forms being distinguished).

**Method:** Same static-reachability/patience-based estimator as the
smoke test above (patience=20*L, max_steps=10*patience — empirically
checked up to L=4800 the same day: steps_taken stayed at ~16-22% of the
max_steps cap and steps/L stabilized around ~29-30, so no change made to
these multipliers). Ensemble-averaged over realizations, sampled
adaptively per N until SE(f_N)/f_N < 0.01 or max_samples_per_N=5000.
Config: `numerics/config/production.yaml`, N_values = [100, 200, 400,
800, 1600, 2400, 4800], density=0.5, PBC. Master seed: 20260912 (recorded
in the run's parameters.json). Runtime: 7m03s total for all 7 values of N.

Cost was estimated before running (realistic ~7 min, conservative ~15-20
min, absolute worst case ~5.8h if every N hit the sampling cap) and
approved by the researcher before execution.

**Result:**
- L=100: f_N = 0.3490 +- 0.0035 (n=1420, discarded=0)
- L=200: f_N = 0.3523 +- 0.0035 (n=760, discarded=0)
- L=400: f_N = 0.3567 +- 0.0034 (n=400, discarded=0)
- L=800: f_N = 0.3640 +- 0.0036 (n=160, discarded=0)
- L=1600: f_N = 0.3638 +- 0.0034 (n=100, discarded=0)
- L=2400: f_N = 0.3587 +- 0.0033 (n=80, discarded=0)
- L=4800: f_N = 0.3574 +- 0.0030 (n=40, discarded=0)

All realizations converged (zero discarded) at every N; the target 1%
relative SE was reached everywhere without hitting max_samples_per_N.
Raw per-realization samples and parameters are in
`numerics/data/raw/frozen_fraction_production_20260912T063128Z/`.

**Interpretation:** [left blank]

**Next question:** Whether these f_N values, plotted vs 1/N or ln(N),
support saturation (H1a) vs. power-law (H1b) vs. logarithmic (H1c)
vanishing per the fitting/comparison procedure in HYPOTHESES.md — not yet
done. The static/combinatorial reachability equivalence remains
unverified against brute-force enumeration (flagged [UNCERTAIN] in H1).

**Git commit:** uncommitted (pipeline code, config, and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-12 — H1 production run (extended): f_N vs N, N=100..102400

**Question:** Same as the previous production run (does f_N saturate,
power-law, or log-decay as N -> infinity), extended to a much wider range
of N to get more decades of dynamic range for the fits.

**Hypothesis:** H1 as stated in HYPOTHESES.md.

**Method:** Same estimator as the previous production run (patience=20*L,
max_steps=10*patience; steps/L checked empirically up to L=102400 this
same day — it climbed further than the previous check up to L=4800 (from
~30 up to ~53 at L=102400), but max_steps usage stayed at <=33.5% of cap
in all pre-run timing trials, so the multipliers were left unchanged).
Ensemble-averaged, adaptive sampling to SE(f_N)/f_N < 0.01 or
max_samples_per_N=5000. Config: numerics/config/production.yaml,
N_values = [100, 200, 400, 800, 1600, 3200, 6400, 12800, 25600, 51200,
102400], density=0.5, PBC. Master seed: 20260912. Runtime: 46m57s total
for all 11 values of N.

Cost was re-estimated before running (realistic ~53min, conservative
1.5-2.5h, absolute worst case ~199h/~8 days if every N hit the sampling
cap — driven by the much larger per-realization cost at N=51200/102400)
and approved by the researcher before execution.

**Result:**
- L=100: f_N = 0.3490 +- 0.0035 (n=1420, discarded=0)
- L=200: f_N = 0.3523 +- 0.0035 (n=760, discarded=0)
- L=400: f_N = 0.3567 +- 0.0034 (n=400, discarded=0)
- L=800: f_N = 0.3640 +- 0.0036 (n=160, discarded=0)
- L=1600: f_N = 0.3638 +- 0.0034 (n=100, discarded=0)
- L=3200: f_N = 0.3603 +- 0.0032 (n=40, discarded=0)
- L=6400: f_N = 0.3605 +- 0.0036 (n=20, discarded=0)
- L=12800: f_N = 0.3621 +- 0.0033 (n=20, discarded=0)
- L=25600: f_N = 0.3615 +- 0.0016 (n=20, discarded=0)
- L=51200: f_N = 0.3606 +- 0.0013 (n=20, discarded=0)
- L=102400: f_N = 0.3580 +- 0.0010 (n=20, discarded=0)

All realizations converged (zero discarded) at every N; the target 1%
relative SE was reached everywhere without hitting max_samples_per_N.
Raw per-realization samples and parameters are in
`numerics/data/raw/frozen_fraction_production_20260912T074229Z/`.

Note: this run supersedes the previous production run
(`frozen_fraction_production_20260912T063128Z/`, N up to 4800 only,
target relative SE 5%) as the wider/tighter dataset — both are kept on
disk, neither has been deleted.

Also note (process, not physics): the mobile-notification pushes
(notify.sh info/done) configured for this run silently failed — the
background shell running this job did not have NTFY_TOPIC set, even
though it's exported in ~/.zshrc. No physics result is affected; flagged
here only because RESEARCH_LOG is the record of what actually happened
during the run, and "notified via phone" did not actually happen despite
being stated as expected beforehand.

**Interpretation:** [left blank]

**Next question:** The fitting/model-comparison step (H1a vs H1b vs H1c)
from HYPOTHESES.md still hasn't been run on this data. The
static/combinatorial reachability equivalence remains unverified against
brute-force enumeration (flagged [UNCERTAIN] in H1).

**Git commit:** uncommitted (config change and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-12 — H1: fitting f_N vs N (constant vs power-law correction)

**Question:** Does a constant model f(N)=f_inf fit the data as well as a
power-law-correction model f(N)=f_inf + a/N^alpha, per the H1 test
procedure?

**Hypothesis:** N/A — this is a fit/model-comparison step, not a new
simulation.

**Method:** Weighted least squares (weights = 1/SE^2) on the 11-point
f_N vs N dataset from `frozen_fraction_production_20260912T074229Z/`
(N=100..102400). Model 1 (constant, 1 param) fit as the inverse-variance
weighted mean. Model 2 (f_inf + a/N^alpha, 3 params) fit via
scipy.optimize.curve_fit with sigma=SE, absolute_sigma=True. chi^2 =
sum(((f_N-model)/SE)^2), reduced chi^2 = chi^2/dof. Notebook:
`numerics/notebooks/analysis/h1_fit_frozen_fraction.ipynb`.

**Result:**
- Model 1 (constant): f_inf = 0.35923 +- 0.00060. chi^2=22.673, dof=10,
  reduced chi^2=2.267.
- Model 2 (f_inf + a/N^alpha): f_inf = 0.35983 +- 0.00066,
  a = -4.674 +- 18.651, alpha = 1.301 +- 0.844. chi^2=10.100, dof=8,
  reduced chi^2=1.263.
- Full per-N residuals for both models are in the notebook output.
- Note: an intermediate overflow warning ("overflow encountered in
  power") occurred during curve_fit's search over trial parameter
  values; the final fit converged without error and residuals look
  reasonable, but this is reported as-is rather than silently
  suppressed.
- Note: model 2's `a` and `alpha` parameters both have very large
  relative uncertainty compared to their fitted values.

**Interpretation:** [left blank]

**Next question:** Whether these two model-comparison results (reduced
chi^2 values, parameter uncertainties) are sufficient to distinguish
H1a/H1b/H1c, or whether additional models (log decay, H1c) and/or more
rigorous comparison (e.g. AIC/BIC) are needed — not yet done. The
static/combinatorial reachability equivalence remains unverified against
brute-force enumeration (flagged [UNCERTAIN] in H1).

**Git commit:** uncommitted (analysis notebook and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1 fitting-range run: f_N vs N, N=10,000..300,000

**Question:** Get a denser, real-data-calibrated large-N dataset for
H1's power-law fit (f_N = f_inf + a/N^alpha), specifically to better
constrain `a` and `alpha` (which came out with very large relative
uncertainty from the earlier 11-point production dataset).

**Hypothesis:** H1 as stated in HYPOTHESES.md.

**Method:** Same estimator as both previous production runs
(patience=20*L, max_steps=10*patience). Config:
`numerics/config/fitting_range.yaml`, N_values = 20 linearly equally
spaced values from 10,000 to 300,000 (rounded to nearest even integer),
density=0.5, PBC, target relative SE=0.01, min_samples=20,
max_samples_per_N=5000. Master seed: 20260912. Runtime: 11h29m for all
20 values of N.

This config was originally specced as 100 points up to N=1e6, but a
real (non-extrapolated) timing calibration at N=300k/600k/1M on
2026-09-12 confirmed that would cost ~11.7 days -- scoped down to 20
points capped at N=300,000 (a real calibrated data point) for a
realistic estimate of ~12.8h, approved by the researcher before running.
Actual runtime (11h29m) came in under that estimate.

**Result:**
- L=10000: f_N = 0.3602 +- 0.0029 (n=20, discarded=0)
- L=25264: f_N = 0.3577 +- 0.0015 (n=20, discarded=0)
- L=40526: f_N = 0.3610 +- 0.0013 (n=20, discarded=0)
- L=55790: f_N = 0.3601 +- 0.0013 (n=20, discarded=0)
- L=71054: f_N = 0.3598 +- 0.0010 (n=20, discarded=0)
- L=86316: f_N = 0.3612 +- 0.0011 (n=20, discarded=0)
- L=101580: f_N = 0.3591 +- 0.0010 (n=20, discarded=0)
- L=116842: f_N = 0.3595 +- 0.0007 (n=20, discarded=0)
- L=132106: f_N = 0.3590 +- 0.0006 (n=20, discarded=0)
- L=147368: f_N = 0.3595 +- 0.0006 (n=20, discarded=0)
- L=162632: f_N = 0.3618 +- 0.0006 (n=20, discarded=0)
- L=177896: f_N = 0.3598 +- 0.0008 (n=20, discarded=0)
- L=193158: f_N = 0.3601 +- 0.0006 (n=20, discarded=0)
- L=208422: f_N = 0.3600 +- 0.0005 (n=20, discarded=0)
- L=223684: f_N = 0.3593 +- 0.0005 (n=20, discarded=0)
- L=238948: f_N = 0.3602 +- 0.0006 (n=20, discarded=0)
- L=254212: f_N = 0.3593 +- 0.0006 (n=20, discarded=0)
- L=269474: f_N = 0.3607 +- 0.0005 (n=20, discarded=0)
- L=284738: f_N = 0.3596 +- 0.0006 (n=20, discarded=0)
- L=300000: f_N = 0.3601 +- 0.0005 (n=20, discarded=0)

All realizations converged (zero discarded) at every N. Raw
per-realization samples and parameters are in
`numerics/data/raw/frozen_fraction_fitting_range_20260912T102036Z/`.
Mobile notifications (info at launch, done at completion) both fired
correctly this time (the ~/.zshenv fix from 2026-09-12 held).

**Interpretation:** [left blank]

**Next question:** Re-run (or extend) the H1a/H1b fitting notebook
(`numerics/notebooks/analysis/h1_fit_frozen_fraction.ipynb`) against
this denser dataset -- not yet done. The static/combinatorial
reachability equivalence remains unverified against brute-force
enumeration (flagged [UNCERTAIN] in H1).

**Git commit:** uncommitted (config and this log entry are currently
unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1: fitting f_N vs N on fitting_range dataset alone

**Question:** Same constant-vs-power-law-correction fit as before, this
time on the fitting_range dataset (N=10,000..300,000) by itself, per the
researcher's explicit choice not to combine it with the earlier
100..102400 production dataset.

**Hypothesis:** N/A — fit/model-comparison step.

**Method:** Identical procedure to the earlier fit (weighted least
squares, chi^2 with weights=1/SE^2). Notebook:
`numerics/notebooks/analysis/h1_fit_frozen_fraction_fitting_range.ipynb`,
pinned to `frozen_fraction_fitting_range_20260912T102036Z/` (20 points).

**Result:**
- Model 1 (constant): f_inf = 0.35992 +- 0.00015. chi^2=23.254, dof=19,
  reduced chi^2=1.224.
- Model 2 (f_inf + a/N^alpha): f_inf = 0.35992 +- inf, a = 0.39379 +- inf,
  alpha = 127.465 +- inf. chi^2=23.254 (identical to Model 1), dof=17,
  reduced chi^2=1.368.
- `curve_fit` raised `OptimizeWarning: Covariance of the parameters
  could not be estimated` and a `RuntimeWarning: overflow encountered in
  power` during the fit.

As anticipated before running this (per the dataset-choice question
asked of the researcher): with every N >= 10,000, the correction term
a/N^alpha is negligible everywhere in this range for any alpha the
optimizer can reach without overflowing, so Model 2 collapsed onto
Model 1 (identical chi^2, degenerate/unconstrained a and alpha,
undefined parameter uncertainties). This dataset only usefully
constrains f_inf; it does not constrain the power-law correction. This
is reported as a property of the data, not an error in the fit
procedure.

**Interpretation:** [left blank]

**Next question:** Whether to redo this fit on the combined dataset
(100..102400 production + 10,000..300,000 fitting_range) to get a
meaningful constraint on a/alpha, since fitting_range alone cannot
provide one. The static/combinatorial reachability equivalence remains
unverified against brute-force enumeration (flagged [UNCERTAIN] in H1).

**Git commit:** uncommitted (new notebook and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1: fitting f_N vs N on combined dataset (31 points)

**Question:** Same constant-vs-power-law-correction fit, now combining
the production (100..102400) and fitting_range (10,000..300,000)
datasets, per the researcher's request after the fitting_range-only fit
came out degenerate.

**Hypothesis:** N/A — fit/model-comparison step.

**Method:** Identical procedure (weighted least squares,
weights=1/SE^2). Combined 31 points: 11 from
`frozen_fraction_production_20260912T074229Z/` + 20 from
`frozen_fraction_fitting_range_20260912T102036Z/`, N=100..300,000, no
duplicate N values across the two datasets (checked programmatically).
Notebook: `numerics/notebooks/analysis/h1_fit_frozen_fraction_combined.ipynb`.

**Result:**
- Model 1 (constant): f_inf = 0.35988 +- 0.00015. chi^2=47.157, dof=30,
  reduced chi^2=1.572.
- Model 2 (f_inf + a/N^alpha): f_inf = 0.35992 +- 0.00015,
  a = -4.184 +- 15.568, alpha = 1.275 +- 0.781. chi^2=33.364, dof=28,
  reduced chi^2=1.192.
- No overflow/covariance-estimation issues this time (unlike the
  fitting_range-only fit) — the small-N production points restore
  leverage on the correction term.
- Full per-N residuals for both models are in the notebook and log
  source.

**Interpretation:** [left blank]

**Next question:** Whether to add a third model (H1c, logarithmic decay)
to this comparison, per the original H1 test procedure in
HYPOTHESES.md — not yet done. The static/combinatorial reachability
equivalence remains unverified against brute-force enumeration (flagged
[UNCERTAIN] in H1).

**Git commit:** uncommitted (new notebook and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1: investigating apparent overshoot/oscillation in f_N vs N

**Question:** The combined-dataset plot showed an apparent overshoot
(rise then settle) around N~800-1600. Is this (c) a commensuration
effect (N mod 4, given the 4-site active window), (a) explainable by a
second power-law correction term, or (b) genuine log-periodic
oscillation?

**Hypothesis:** N/A — diagnostic/model-comparison step.

**Method:** All three investigated in
`numerics/notebooks/analysis/h1_fit_frozen_fraction_combined.ipynb`
(same 31-point combined dataset, N=100..300,000):
(c) grouped existing points by N mod 4, compared weighted-mean Model-1
residuals per group (no new simulation).
(a) fit f(N) = f_inf + a/N^alpha + b/N^beta via curve_fit (5 params).
(b) log-periodic form, planned only if (a)'s residual chi^2 p-value
indicated structure inconsistent with noise (p<0.05) — pre-registered
criterion, stated before running.

Before this, a model-independent check: two near-duplicate N pairs in
the dataset (25264 vs 25600; 101580 vs 102400) differ by 1.73 sigma and
0.78 sigma respectively — a genuine smooth function of N with period ~1
in ln(N) could not produce that at such close spacing, indicating at
least part of the apparent structure is point-to-point scatter.

**Result:**
- (c) All 31 N values are even, so N mod 4 only takes values 0 (n=22)
  or 2 (n=9) in this dataset. Weighted mean Model-1 residual: 0 group
  = -0.00002 +- 0.00020, 2 group = +0.00003 +- 0.00023 (~0.16 sigma
  apart). No evidence of an N mod 4 effect.
- (a) Fit converged numerically but is degenerate: a = -223197 +-
  489632753, alpha = 2.986 +- 203, b = 1150709 +- 56149298, beta = 3.352
  +- 277 (relative errors >1000x on all four correction-term
  parameters). chi^2=32.141, dof=26, reduced chi^2=1.236 — worse than
  Model 2's reduced chi^2 (1.192) despite 2 extra free parameters.
  RuntimeWarnings (divide by zero, overflow) fired during the fit. The
  two correction terms are unconstrained/non-identifiable with 31
  points; these parameter values are not reported as physically
  meaningful.
- (b) Skipped per the pre-registered criterion: Model 3's chi^2
  p-value = 0.189 (dof=26), not significant at the 5% level, so the
  residual structure left after (a) is already statistically consistent
  with noise.

**Interpretation:** [left blank]

**Next question:** No commensuration effect and no statistically
supported second correction term or oscillation, given current error
bars. If the researcher wants to pursue this further, the next step
would be tightening SE at a handful of specific N (e.g. re-running with
larger ensembles, n~200 instead of n~20, at points that currently show
large |residual|/sigma) rather than adding more model parameters to
noise. The static/combinatorial reachability equivalence remains
unverified against brute-force enumeration (flagged [UNCERTAIN] in H1).

**Git commit:** uncommitted (updated notebook and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1: vanishing forms (H1b, H1c) + model-free decay bound

**Question:** Does f_N saturate to a nonzero constant or vanish as
N -> infinity? Every model fit previously (M1/M2/M3) had f_inf as a free
parameter, i.e. all assumed a nonzero floor, so none of them could test
the vanishing alternatives. This fits H1b and H1c for the first time.

**Hypothesis:** H1 as stated in HYPOTHESES.md (three candidates H1a/H1b/H1c).

**Method:** Same 31-point combined dataset (N=100..300,000), same
weighted least squares / chi^2 convention. Notebook:
`numerics/notebooks/analysis/h1_fit_frozen_fraction_combined.ipynb`.
Models added:
- H1b: f(N) = c * N^(-alpha)          (2 params)
- H1c: f(N) = c / ln(N)               (1 param)
- H1c variant: f(N) = c / (ln(N) + d) (2 params)
Plus two form-free diagnostics: the local log-log slope
s = d ln(f)/d ln(N) fit over the last decade of data, and the resulting
95% upper bound on any asymptotic decay exponent alpha (where
f_N ~ N^(-alpha)).

**Result:** Full model comparison —

| model | params | chi^2 | dof | reduced chi^2 |
|---|---|---|---|---|
| M1 constant | f_inf=0.35988 | 47.157 | 30 | 1.572 |
| M2 f_inf+a/N^alpha | f_inf=0.35992, a=-4.184, alpha=1.275 | 33.364 | 28 | 1.192 |
| M3 two-corr | f_inf=0.35992 (rest degenerate) | 32.141 | 26 | 1.236 |
| H1b c*N^-alpha | c=0.35632, alpha=-0.000829 | 44.389 | 29 | 1.531 |
| H1c c/lnN | c=4.21778 | 83288.634 | 30 | 2776.288 |
| H1c c/(lnN+d) | c=1.313e8, d=3.649e8 | 47.157 | 29 | 1.626 |

- H1b's fitted alpha = -0.000829 +- 0.000500 (1.66 sigma from zero, and
  negative-signed, i.e. the best fit is a very slight *increase* with N,
  not a decay). 95% CI on alpha: [-0.001809, +0.000151].
- H1c in its rigid form (c/ln N) gives reduced chi^2 = 2776.
- H1c's less rigid variant c/(ln N + d) only fits by running d to
  ~3.6e8 (uncertainties ~1e13, i.e. unconstrained), where
  c/(ln N + d) -> c/d = 0.35988 — numerically identical chi^2 to the
  constant model M1 (47.157). It fits only in the limit where it stops
  vanishing.
- Model-free local log-log slope over the last decade (N >= 3e4, 20
  points): s = +0.000081 +- 0.000946, i.e. alpha = -s =
  -0.000081 +- 0.000946, 0.09 sigma from zero. 95% upper bound:
  alpha < 0.001774, at which f_N would fall by at most 0.41% per decade
  of N. Same diagnostic over N >= 1e4 gives alpha < 0.001433, and over
  N >= 1e3 gives alpha < 0.001544.

**Interpretation:** [left blank]

**Next question:** All of the above presumes the frozen-fraction
estimator is unbiased. That is still unverified, and there is a specific
reason for concern: the patience window is a fixed 20*L, but the
measured growth-phase duration in units of L has grown with N (steps/L
~24 at N=100 vs ~70 at N=1e6), so the patience/growth-phase ratio fell
from ~5.0x to ~0.4x across the studied range. If that biases f_N upward
increasingly with N, apparent flatness could mask a real decay, and a
tight alpha bound from biased data would be a confident wrong answer.
Two checks proposed but not yet run: (i) patience-sensitivity test
(same seeds, patience = 20L/100L/500L, compare f_N), (ii) exact BFS
enumeration of the reachable set at small N (16-24) against the
estimator's output — the latter also closes the long-standing
[UNCERTAIN] flag in H1.

**Git commit:** uncommitted (updated notebook and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1: redefining "frozen" as a rolling window (definition B)

**Question:** N/A -- methodology change, prompted by the researcher
clarifying what "frozen" should mean operationally.

**Method:** All prior H1 measurements used a *cumulative* definition: a
site is frozen if it has never flipped since t=0 (a monotonic,
sticky-once-flipped quantity). The researcher instead wants: start from
many initial configs, evolve under the dynamics, and once the frozen
fraction is stable (small deviations) over a window of length W, average
over that window to get the estimate for that configuration -- repeated
over configs. Clarified with the researcher that this requires a
*rolling* definition: a site counts as frozen at time t if it has not
flipped in the trailing window [t-W, t], so a site can re-enter the
frozen set after being quiet for W steps, unlike the cumulative
definition where one flip permanently disqualifies it. Researcher set
W = 5*L and M = 10 (number of trailing windows averaged for the final
per-realization estimate).

**Result:** Implemented `measure_frozen_fraction_rolling` /
`run_ensemble_rolling` in `numerics/src/frozen_fraction.py`: burn-in via
the existing fixed-patience criterion, then M non-overlapping
measurement windows of length W, frozen fraction = mean over windows.
Sanity check at L=1000: f_A (cumulative) = 0.3400 <= f_B (rolling) =
0.3446 with the same seed, consistent with the required inequality
(cumulative-frozen sites are a subset of rolling-frozen sites).

Checked the choice of W=5L against a physical requirement: W needs to be
large relative to the typical number of currently-active sites
n_active(t) (since only one active site flips per step, chosen
uniformly from n_active(t) candidates), or a still-active site could be
missed by chance within the window. Measured n_active(t) in steady
state at L=100/1,000/10,000/100,000: mean ~12.5-13.6% of L at every
scale, giving a consistent ~37-40x margin of W=5L over typical
n_active(t) across the whole range (not shrinking with N).

**Interpretation:** [left blank]

**Next question:** Validate that the rolling estimator's burn-in
(reusing the old fixed-patience criterion before starting the M
measurement windows) is actually sufficient -- not yet checked.

**Git commit:** uncommitted (frozen_fraction.py changes and this log
entry are currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1: rolling-window stability check, N=500-8000

**Question:** Does the rolling-window estimator (fixed-patience burn-in,
W=5L, M=10) show any systematic trend across its 10 measurement windows
at small-to-medium N, or is burn-in adequate there?

**Hypothesis:** N/A -- validation step.

**Method:** Ran `measure_frozen_fraction_rolling` for 3 trials each at
N=500,1000,2000,4000,8000, fit a line to the 10 window values vs window
index per trial, recorded the p-value of that slope (H0: no trend).

**Result:** 15 trials total (5 N-values x 3 trials). Trend p-values:
N=500: 1.000, 0.107, 0.501. N=1000: 0.052, 0.201, 0.805. N=2000: 0.318,
0.375, 0.151. N=4000: 0.746, 0.531, 0.760. N=8000: 0.456, 0.825, 0.964.
Only 1/15 came near the 0.05 threshold (and did not cross it) -- roughly
what pure chance would produce at a 5% significance level across 15
tests (expected ~0.75 false positives). `std_across_windows` also shrank
with N (0.0007-0.0059 range), consistent with self-averaging.

**Interpretation:** [left blank]

**Next question:** This range (N<=8000) looked clean, but it was
comfortably inside the range where the fixed-patience/growth-phase ratio
was still large (>=3-5x, per the earlier patience-margin analysis).
Needed to check the large-N range (N>=10,000) where that ratio had
fallen to <1x before trusting the estimator there too.

**Git commit:** uncommitted (this log entry is an unstaged working-tree
change on top of 832ba5c)

---

## 2026-09-13 — H1: broader rolling-window validation reveals burn-in failure at large N

**Question:** Does the rolling-window estimator's fixed-patience burn-in
remain adequate at N=10,000-100,000, where the patience/growth-phase
ratio was already known to be thin?

**Hypothesis:** Based on the earlier patience-margin concern, expected
possible drift at the largest N tested.

**Method:** Ran `measure_frozen_fraction_rolling` (fixed patience=20L,
W=5L, M=10) at N=100,300,1000,3000,10000,30000,100000 with trial counts
scaled down at larger N (10,10,10,8,8,5,3) to keep cost modest (~13 min
total, estimated beforehand). Recorded trend p-value and
std_across_windows per trial.

**Result:**
- N=100: 0/10 significant trends, but 4/10 trials returned NaN
  trend_pvalue (std_across_windows exactly 0 -- linregress divides by
  zero on zero-variance input; a real code bug, not a physics result --
  fixed same day, see below).
- N=300: 1/10 significant. N=1000: 0/10. N=3000: 0/8. N=10000: 0/8.
- **N=30000: 1/5 significant, p=0.001** (a strong signal, not a
  borderline false positive).
- **N=100000: 2/3 significant** (p=0.019, p=0.045) -- the majority of
  trials at the largest N tested.
- std_across_windows shrank monotonically with N throughout (0.0002 at
  N=100,000 vs 0.0135 at N=100) while the trend-significance rate did
  the *opposite* -- confirmed via sqrt(N)*std rescaling (collapsed
  fluctuation spread from 61x to 2.1x across the N range) that
  fluctuation size and drift are anti-correlated (r=-0.537): the
  quietest-looking runs (by fluctuation) were the ones most likely to
  still be drifting.

**Interpretation:** [left blank]

**Next question:** The fixed patience=20L burn-in is failing exactly
where the earlier concern predicted (large N, thin patience/growth
ratio) -- majority of N=100,000 trials still drifting when measurement
started. Needed a burn-in fix before trusting any rolling-window
production run at this scale. Separately, the NaN trend_pvalue bug
(zero-variance case) needed fixing regardless of N.

**Git commit:** uncommitted (this log entry is an unstaged working-tree
change on top of 832ba5c)

---

## 2026-09-13 — H1: comparing two burn-in fixes, locking in method 1

**Question:** Which burn-in fix resolves the large-N drift found above:
(1) self-scaling patience -- extend burn-in until (t-G) >= c*G, where G
is the time of the most recent first-flip event, pinning the
patience/growth ratio at c for every N; or (2) drift-gated disjoint
probe/measure windows -- probe batches of M windows for a significant
trend, discard and re-probe if found, measure on fresh windows once a
probe batch passes?

**Hypothesis:** Both should fix the drift; agreement between them on
identical trajectories would be evidence the fix is not itself an
artifact of which stopping rule was chosen.

**Method:** Implemented both in `numerics/src/burnin_comparison.py`,
run on identical trajectories (same rng, same sequence of moves --
not just same seed) so both methods' estimates come from literally the
same physical realization. c_selfscale=5 (chosen so it reproduces the
already-clean small-N behavior: at N=100, G~4L, so 5L+G~24L, close to
the old fixed patience=20L). Fixed the NaN trend_pvalue bug in the same
pass (zero-variance case now reports pvalue=1.0, zero_variance=True,
instead of NaN; also fixed run_ensemble_rolling's SeedSequence call,
which rejected a string entropy element). Ran 5 trials each at
N=30,000 and N=100,000.

**Result:**
- Method 1: 0/10 significant trends across all 10 trials (vs. 1/5 and
  2/3 with the old fixed patience at these same N).
- Method 1 and Method 2 agreed on f_B to within -0.0002 to +0.0004 in
  every one of the 10 trials -- small compared to the natural
  realization-to-realization spread (~0.01-0.02).
- One flagged exception: N=100,000 trial 4 -- method 2 discarded one
  drifting probe batch, passed the next, but the *measurement* batch
  that followed still showed a significant trend (p=0.010) -- the
  "probe once, then measure" design does not fully guarantee the
  immediately-following batch is also stable (plausibly a false
  negative from limited power at M=10 windows). Method 1 and Method 2
  still agreed on the value in this exact case (diff=+0.0001).
- Cost: Method 1's burn-in was consistently longer than Method 2's in
  every trial (e.g. at N=100,000: method 1 mean ~220L vs method 2 mean
  ~108L), roughly 2x slower on average, up to 2.6x in the worst trial.

**Interpretation:** [left blank]

**Next question:** Researcher chose Method 1 (self-scaling patience) as
the production burn-in criterion -- simpler, no stopping-rule-bias risk,
slightly more conservative (0/10 vs 9/10 clean). Implemented as the
production `measure_frozen_fraction_rolling`/`run_ensemble_rolling` in
`frozen_fraction.py`, cross-checked bit-for-bit against
`burnin_comparison.py`'s method-1 path (exact match, 3/3 trials) --
`burnin_comparison.py` itself kept as-is, documenting the comparison.
Also noted: for N<=10,000 (the range covered by
`production_intermediate.yaml`), the plain fixed-patience burn-in had
already shown 0 significant trends in the earlier validation, so method
1's extra cost there is a safety margin, not a fix for an observed
problem at that scale.

**Git commit:** uncommitted (frozen_fraction.py, burnin_comparison.py,
and this log entry are currently unstaged working-tree changes on top
of 832ba5c)

---

## 2026-09-13 — Archived pre-rolling-definition runs (not deleted)

**Question:** N/A -- data-provenance housekeeping, not an experiment.

**Method:** The researcher asked to delete the old data since it used
"wrong estimations" (superseded by the rolling-window frozen-fraction
definition). Per CLAUDE.md's inviolable rule ("Never delete previous
results. Archive to archive/ instead" -- explicitly not overridable by a
later instruction), archived rather than deleted.

**Result:** Moved to `numerics/data/archive/` (see the README.md added
there):
- `frozen_fraction_test_20260912T062103Z/` (cumulative-definition smoke test)
- `frozen_fraction_production_20260912T063128Z/` (cumulative, N=100-4800)
- `frozen_fraction_production_20260912T074229Z/` (cumulative, N=100-102400)
- `frozen_fraction_fitting_range_20260912T102036Z/` (cumulative, N=10,000-300,000)
- `frozen_fraction_test_20260913T062742Z/` (crashed/empty -- hit the
  SeedSequence string-entropy bug in run_ensemble_rolling before it was
  fixed the same day; only parameters.json, no samples)

Left in place (not archived): `frozen_fraction_test_20260913T062809Z/`
(current rolling/method-1 test.yaml result) and
`frozen_fraction_production_intermediate_20260913T064716Z/` (in-progress
background run at the time of this entry).

**Interpretation:** [left blank]

**Next question:** The analysis notebooks
(`h1_fit_frozen_fraction*.ipynb`) still reference the now-archived
cumulative-definition data by their old `data/raw/...` paths -- these
will fail to re-execute until/unless someone points them at
`data/archive/...` or they're accepted as historical artifacts from the
superseded definition, not updated.

**Git commit:** uncommitted (archive move and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — Archived pre-rolling-definition analysis notebooks

**Question:** N/A -- data-provenance housekeeping, follow-up to the data
archiving above.

**Method:** Researcher asked to move the three analysis notebooks tied
to the now-archived cumulative-definition data into their own archive
location.

**Result:** Moved from `numerics/notebooks/analysis/` to a new
`numerics/notebooks/archive/` (README.md added there explaining why):
- `h1_fit_frozen_fraction.ipynb`
- `h1_fit_frozen_fraction_fitting_range.ipynb`
- `h1_fit_frozen_fraction_combined.ipynb`

`numerics/notebooks/analysis/` is now empty. These notebooks are pinned
to run directories that no longer exist under `data/raw/` (moved to
`data/archive/`), so they will fail if re-executed as-is -- kept for
provenance only, not maintained.

**Interpretation:** [left blank]

**Next question:** New analysis notebooks fitting H1a/H1b/H1c under the
rolling-window definition still need to be written once
production_intermediate.yaml (and eventually production_large_scale.yaml)
finish running.

**Git commit:** uncommitted (notebook move and this log entry are
currently unstaged working-tree changes on top of 832ba5c)

---

## 2026-09-13 — H1 production run (rolling-window/method 1): f_N vs N, N=100..10,000

**Question:** First production measurement of f_N under the rolling-window
definition (method 1, self-scaling patience burn-in) rather than the
superseded cumulative definition.

**Hypothesis:** H1 as stated in HYPOTHESES.md.

**Method:** `numerics/config/production_intermediate.yaml`: 20 linearly
spaced N values from 100 to 10,000 (rounded to nearest int), density=0.5,
PBC. Rolling estimator: W=5L, M=10, c_selfscale=5, max_extra_windows=200.
Ensemble: target relative SE=1%, min_samples=20, max_samples_per_N=5000.
Master seed: 20260914 (as recorded in the run's parameters.json -- note
this seed value predates the same-day date-string correction described
two entries above; the seed itself is just an integer and unaffected).
Runtime: 1h28m for all 20 values of N (estimated beforehand: ~2.2h
realistic).

**Result:**
- L=100: f_N=0.3538 +- 0.0035 (n=1340, discarded=0)
- L=621: f_N=0.3602 +- 0.0036 (n=220, discarded=0)
- L=1142: f_N=0.3656 +- 0.0036 (n=120, discarded=0)
- L=1663: f_N=0.3624 +- 0.0035 (n=80, discarded=0)
- L=2184: f_N=0.3628 +- 0.0035 (n=60, discarded=0)
- L=2705: f_N=0.3646 +- 0.0034 (n=60, discarded=0)
- L=3226: f_N=0.3583 +- 0.0028 (n=60, discarded=0)
- L=3747: f_N=0.3671 +- 0.0034 (n=20, discarded=0)
- L=4268: f_N=0.3638 +- 0.0028 (n=60, discarded=0)
- L=4789: f_N=0.3623 +- 0.0036 (n=20, discarded=0)
- L=5311: f_N=0.3656 +- 0.0034 (n=20, discarded=0)
- L=5832: f_N=0.3643 +- 0.0025 (n=20, discarded=0)
- L=6353: f_N=0.3605 +- 0.0029 (n=40, discarded=0)
- L=6874: f_N=0.3620 +- 0.0031 (n=20, discarded=0)
- L=7395: f_N=0.3682 +- 0.0035 (n=20, discarded=0)
- L=7916: f_N=0.3623 +- 0.0019 (n=20, discarded=0)
- L=8437: f_N=0.3631 +- 0.0028 (n=20, discarded=0)
- L=8958: f_N=0.3676 +- 0.0026 (n=20, discarded=0)
- L=9479: f_N=0.3619 +- 0.0024 (n=20, discarded=0)
- L=10000: f_N=0.3652 +- 0.0025 (n=20, discarded=0)

All realizations converged (zero discarded) at every N. Raw
per-realization samples and parameters are in
`numerics/data/raw/frozen_fraction_production_intermediate_20260913T064716Z/`.

**Interpretation:** [left blank]

**Next question:** Build a saturation visualization combining this data
with test.yaml's (N=200-1600) in an exploratory notebook -- requested by
researcher, not yet done at the time of this entry. Longer-term:
production_large_scale.yaml (N up to 100,000) still needs rescoping
before it can run (previously estimated at ~37 days as specified).

**Git commit:** uncommitted (this log entry is an unstaged working-tree
change on top of 832ba5c)

---

## 2026-09-13 — Exploratory saturation visualization (rolling-window data)

**Question:** Combine the two rolling-window/method-1 runs so far
(test.yaml + production_intermediate.yaml) into a single visualization
of f_N vs N, per researcher request.

**Hypothesis:** N/A -- visualization, not an experiment.

**Method:** New notebook
`numerics/notebooks/exploratory/rolling_window_saturation.ipynb`,
combining `frozen_fraction_test_20260913T062809Z/` (4 points,
N=200-1600) and `frozen_fraction_production_intermediate_20260913T064716Z/`
(20 points, N=100-10,000) -- 24 points total, checked programmatically
for no duplicate N. Plots: pure f_N vs N (linear), then log-x, 1/N, and
ln(N) views, plus a naive inverse-variance-weighted mean across all 24
points as a reference line (explicitly not a fit).

**Result:** Weighted mean f_N across all 24 points: 0.36303 +- 0.00065.
Full per-N table and plots are in the notebook. Placed in
`notebooks/exploratory/` (tied to these two specific runs, not a final
citable analysis -- no model fitting done here).

**Interpretation:** [left blank]

**Next question:** A proper model comparison (constant vs power-law vs
log decay, as done previously for the now-archived cumulative-definition
data) has not yet been redone for the rolling-window data -- belongs in
`notebooks/analysis/` when undertaken.

**Git commit:** uncommitted (new notebook and this log entry are
currently unstaged working-tree changes on top of 832ba5c)
