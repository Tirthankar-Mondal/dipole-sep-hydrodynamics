## H1 — Frozen fraction in the thermodynamic limit
**Status:** Active
**Stated:** 12 September, 2026
**Sharpened:** 12 September, 2026

**Order parameter:** f_N = (number of statically frozen sites)/N under periodic
boundary conditions, where a site is frozen if no sequence of allowed
0110<->1001 moves, starting from the initial configuration, can ever change
its occupation. f_N is a property of the initial string alone (reachability
under the local move), not of a stochastic trajectory or run time.

**Assumption (flagged, not verified):** the static/combinatorial reachability
rule is assumed to hold under PBC without a brute-force small-N check.
[UNCERTAIN: this equivalence has not been verified against actual
move-sequence enumeration under wraparound — if the finite-size scaling later
looks anomalous, this assumption should be revisited first.]

**Ensemble:** density exactly 1/2 (equal 0s/1s), N in {100, 200, 400, 800,
1600}. For each N, draw M independent random initial strings; M is chosen
adaptively per N to hit a target standard error on f_N (threshold to be fixed
when the numerics are designed).

**Claim:** f_N converges to a nonzero constant f_infinity > 0 as N -> infinity
(candidate H1a below), as opposed to vanishing.

**Candidate outcomes:**
- H1a: f_N -> f_infinity > 0 (saturation)
- H1b: f_N ~ c * N^(-alpha), alpha > 0 (power-law vanishing)
- H1c: f_N ~ c / ln(N) (logarithmic vanishing)

**Test:** fit f_N = f_infinity + c/N^beta and f_N = c*N^(-alpha) (and the log
form) to the same data; compare via residuals/AIC; check whether the
1/N-intercept is consistent with zero.

**Would be falsified by:** intercept of f_N vs 1/N consistent with zero within
error, and/or a power-law or log fit clearly preferred over the
constant+correction fit.

**Range caveat:** N=100-1600 is under two decades of dynamic range — flagged
as a limitation up front. Extension to larger N will be proposed only if the
fits at this range are inconclusive, not built in preemptively.

**Notes:** ...