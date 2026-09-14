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

**Notes:**

**2026-09-14 — researcher's working assumption (not a formal fit result):**
The asymptotic behaviour (H1a vs H1b vs H1c) has not been established --
no model comparison has been run on the rolling-window (definition B)
data yet. However, across the N values reached so far, f_N appears to
scatter around 0.36 +/- 0.009. On this basis the researcher is, for now,
assuming a finite (nonzero) fraction and moving on to the next research
question. This is a provisional working assumption pending a proper
large-N model fit, not a claim that H1a is confirmed.

**2026-09-14 — literature:** see `LITERATURE.md` and
`numerics/theory/Notes/` for full detail; summarized here for
visibility since this bears directly on H1a vs H1b/H1c.
- Our exact model (sites +-1, 0110<->1001 swap, density 1/2) is studied
  directly in Classen-Howes (2024) thesis, Ch.5 Sec.5.1
  (`numerics/theory/Notes/classen-howes-2024-thesis.md`): our (d=2,k=4)
  case is one of only two special points where the usual
  strong-to-weak fragmentation transition's critical filling coincides
  with its own particle-hole mirror point, collapsing the
  weakly-fragmented (thermalizing) phase to nothing -- their stated
  conclusion is that the model is strongly fragmented at *every*
  filling, including ours. This is independent, pre-existing analytic
  support for H1a-in-kind (nonzero frozen fraction), not derived from
  our numerics. [UNCERTAIN: no closed-form value for the frozen-*site*
  density itself is given there, only for a related frozen-*blockage*
  probability -- deriving an exact number to compare against 0.36 would
  need extending their Appendix B.6 recursion, not yet done.]
- Our model is also exactly the hardcore-restricted invariant
  sub-sector of Morningstar, Khemani & Huse (2020)
  (`numerics/theory/Notes/morningstar-khemani-huse-2020.md`), whose
  frozen-site order parameter uses the same static/Krylov-sector
  definition our rolling-window estimator targets -- independent
  support that this is a sensible quantity to be estimating, though
  their quantitative critical theory (built around a charge reservoir
  our n_max=1 model doesn't have) does not transfer to a value or
  formula for H1.

---

## H2 — Length distribution of active regions between frozen sites
**Status:** Active
**Stated:** 14 September, 2026
**Sharpened:** 14 September, 2026

**Order parameter:** For a fixed chain length L, take one realization and
evolve it to a single post-burn-in snapshot, using the same rolling-window
frozen-site definition and self-scaling burn-in already locked in for H1
(definition B, method 1). At that snapshot, record the frozen-site
positions around the ring and, walking between consecutive frozen sites,
the gap length l_i = the number of active (non-frozen) sites strictly
between them (two adjacent frozen sites with nothing in between give
l_i = 0). One realization yields one set of gap lengths (as many as there
are frozen sites in that snapshot). Pooling these across many independent
realizations gives the empirical active-region-length distribution
P_L(l) for that L.

**Note -- the mean is not new information:** since every frozen site
starts exactly one gap going around the ring, the mean gap length is
fixed by H1's frozen fraction alone: <l>_L = (1 - f_N)/f_N. It is not an
independent observable and should be used only as a consistency check
against H1's already-measured f_N at the same L (both come from the
same rolling-window definition B, so they should agree). The genuinely
new content of H2 is the *shape* of P_L(l) -- its variance, tail, and
whether it is consistent with a memoryless (geometric/exponential-family)
process, versus carrying extra structure -- not the mean itself.

**Assumption (flagged, not verified):** a single post-burn-in snapshot
per realization is used, rather than averaging the frozen-site set over
multiple measurement windows. Gap-length samples drawn from the same
snapshot are spatially correlated (they partition the same ring and must
sum to L), not independent draws -- decorrelation comes only from
pooling over independent realizations, not within one.

**Ensemble:** density exactly 1/2, L in {100, 200, 400, 800, 1600, 3200,
6400, 12800} (doubling from 100, 7 doublings). For each L, pool gap
lengths from an ensemble of independent realizations; ensemble size to
be fixed adaptively (same target-relative-SE approach as H1) when the
numerics are designed.

**Claim:** The normalized shape of the active-region-length distribution
either stabilizes (collapses) as L grows, consistent with frozen sites
being placed as an effectively independent/uncorrelated process along the
ring, or it does not, with anomalously long active regions remaining
disproportionately likely as L grows -- signaling correlations between
frozen-site positions beyond independent placement.

**Candidate outcomes (not mutually exclusive as literally stated --
see Test below for how they're distinguished):**
- H2a: the rescaled distribution <l>_L * P_L(l) vs l/<l>_L collapses
  onto an L-independent curve as L grows, with a tail consistent with a
  memoryless (geometric/exponential) process -- consistent with
  independent random frozen-site placement.
- H2b: the rescaled distribution does not collapse, and/or the tail
  (l/<l>_L >> 1) is heavier than exponential (e.g. power-law-like) and
  does not decay away as L grows -- signaling frozen-site clustering or
  other correlations.

**Test:** For each L, build the empirical P_L(l) from the pooled
ensemble. (1) Compute <l>_L and compare against (1 - f_N)/f_N from H1's
data at that L, as a consistency check, not a test of H2 itself. (2)
Plot <l>_L * P_L(l) vs l/<l>_L for all L on one axis and check whether
the curves collapse (H2a) or systematically drift with L (H2b). (3)
Separately fit the tail (l above some cutoff) to exponential vs
power-law forms at each L and check whether the preferred form, or its
decay parameter, is stable across L or drifts.

**Would be falsified by:** H2a is falsified by a tail clearly heavier
than exponential that persists or grows (relative to <l>_L) as L
increases, or by the rescaled curves failing to converge. H2b is
falsified by the rescaled curves collapsing onto a stable
exponential/geometric tail independent of L. If neither a collapse nor a
systematic tail drift emerges with increasing L, that is inconclusive
for both and would call for a wider L range before concluding either
way.

**Range caveat:** L=100 to 12,800 spans a little over 2 decades (7
doublings) -- flagged as a limitation up front, same caveat structure as
H1.

**Notes:**
- **2026-09-14 amendment:** zero-length gaps (two frozen sites
  immediately adjacent, l_i=0) are discarded from the reported
  distribution P_L(l) per researcher instruction -- P_L(l) is over
  nonzero active-region lengths only. This means <l>_L = (1-f_N)/f_N no
  longer holds exactly as a consistency check (that identity requires
  including the zeros); the discarded-zero count/rate is reported
  alongside the pooled distribution so the size of this effect stays
  visible.
- Existing H1 raw data (`numerics/data/raw/frozen_fraction_*/`) cannot
  be reused for this -- those runs saved only the frozen-fraction time
  series per realization, not the spatial frozen-site configuration, so
  new code and new production runs are required to collect gap-length
  data.
- Edge case: a realization whose snapshot has fewer than 2 frozen sites
  (only plausible at small L; H1's f_N~0.35-0.36 makes this unlikely
  even at L=100, where ~35 sites are expected frozen) should be
  discarded from the gap-length pool rather than silently producing a
  degenerate single gap of length L or L-1; the discard rate should be
  reported, mirroring the `n_discarded` bookkeeping already used in the
  H1 pipeline.

**2026-09-14 -- researcher's claim (H2a support):** the active-region
length distribution follows an exponential distribution. Supported by
`numerics/notebooks/analysis/h2_gap_length_distribution.ipynb`: an OLS
comparison of exponential vs power-law fits to the full empirical PMF
(l=4 upward, no tail cutoff) favors the exponential form at every one of
the 8 L values tested (R^2 0.910-0.966 vs 0.872-0.906 for power-law; see
RESEARCH_LOG.md, 2026-09-14, "H2b follow-up"). This is consistent with
H2a (shape collapse onto a memoryless/exponential-family form) over H2b.
The fitted decay length was not seen to drift systematically with L
across this range (lambda ~13.3-15.0, RESEARCH_LOG.md, 2026-09-14, "H2a/
H2b analysis notebook"), though this has not been checked with a formal
model-selection criterion (AIC/likelihood-ratio) beyond R^2.

**2026-09-14 — literature:** see `LITERATURE.md` and
`numerics/theory/Notes/classen-howes-2024-thesis.md` for full detail.
Classen-Howes (2024) thesis, Ch.5 Sec.5.1.2, derives an **exact**
active-bubble density formula for our exact (d=2,k=4) model:
`a_2(x,ell,4,nu*L,L) -> nu^x * (1-nu)^(ell-x) * P_b(nu)^2` -- manifestly
exponential in ell. This is the likely direct theoretical origin of the
exponential form claimed above, not an independent coincidence. The
same thesis section also explains part of QUESTIONS.md #3 (forbidden
lengths 1,2,3,5): their general formula gives ell_min=ell_max=4 for the
minimal 2-particle active bubble at k=4, explaining why ell=1,2,3 never
occur and why ell=4 is uniquely realizable (elevated count) -- but
ell=5 specifically is not addressed in the thesis text [UNCERTAIN: a
hand-derivation using their method, done by the reviewing agent and not
independently re-verified against our raw data, is consistent with
ell=5 being forbidden and ell>=6 allowed, but this is an extension of
their method, not their stated result].