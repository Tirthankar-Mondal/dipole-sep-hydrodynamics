# Morningstar, Khemani & Huse (2020) — applicable details

Full paper: `numerics/theory/Papers/2004.00096v3.pdf`
arXiv:2004.00096v3, "Kinetically constrained freezing transition in a
dipole-conserving system."

## Why this paper is relevant: our model is its hardcore invariant sub-sector

Their model: occupation n_i in {0,1,2}, random k=4 gates replacing any
4-site window with a uniformly random configuration of the same local
charge N_0 and dipole N_1 (their Table I enumerates all nontrivial
4-site groups). Restricting to inputs where no site ever has n_i=2, the
*only* surviving nontrivial group is {0110, 1001} — exactly our move,
nothing else. So our chain is exactly this paper's model, restricted to
its own dynamically-invariant hardcore sub-manifold, at their density
n-bar=0.5. (This restriction is also itself an instance of strong
fragmentation in their sense: hardcore configs and configs containing
any n_i=2 site are dynamically disconnected at fixed (N_0,N_1).)

## Applicable to H1 (frozen fraction)

- Their frozen-site order parameter rho_F uses the same
  **static/Krylov-sector definition** (frozen for all times iff constant
  across every configuration reachable from the initial state) that
  HYPOTHESES.md flags as [UNCERTAIN] for our own rolling-window
  dynamical estimator. This paper uses that static definition as its
  primary theoretical object throughout — independent support that it's
  a reasonable target for a dynamical estimator to approximate (does
  not prove our estimator gets it right, just that the static
  definition itself is a standard, sensible thing to be estimating).
- Their quantitative theory (critical filling n-bar_c ~ 1.5, exponents
  beta=1, nu=2, active-block tail ~L_A^-3/2) is built around active
  regions growing by absorbing charge up to their reservoir cap
  n_max=2. **This machinery does not transfer** to our model: with
  n_max=1, there is no analogous "growth toward a critical local
  density" — density is pinned at exactly 1/2 everywhere, with no room
  to grow further locally. Do not reuse their exponents or mechanism
  for our system.
- Their particle-hole symmetry n-bar <-> 2-n-bar makes n-bar=0.5 (our
  density, in their units) the mirror of their critical density ~1.5.
  [UNCERTAIN, unconfirmed]: that symmetry statement is about their
  *full* n_max=2 ensemble, not about the hardcore corner we restrict to
  — nothing in the paper establishes the hardcore corner inherits the
  full ensemble's near-critical statistics. Flagged as a suggestive
  coincidence only.

## Applicable to H2 (active-region length distribution)

- Their power-law L_A^-3/2 tail is derived and observed to hold only in
  the limit n-bar -> n-bar_c^+ (their Fig. 4a,c show a finite
  cutoff/faster-than-power-law falloff away from n-bar_c, with
  correlation length xi finite and shrinking away from criticality).
  Our model has no tunable density parameter that can approach their
  critical point (density fixed at exactly 1/2, no reservoir), so our
  active-region statistics are structurally analogous to their
  *off-critical, frozen-phase* regime — where their own data show
  short-tailed (not power-law) length distributions. This is
  qualitative support for our empirical exponential fit, **not a
  derivation of the exponential form** — their machinery does not work
  out the off-critical functional form explicitly. (The Classen-Howes
  thesis note, in this same folder, gives the actual derived exponential
  formula for our exact model — use that one for the functional form
  itself.)

## Applicable to QUESTIONS.md #3 (forbidden lengths)

- Not addressed at all. This paper operates at the level of
  large-active-block statistical/hydrodynamic scaling, never the exact
  short-string combinatorics of which small lengths are achievable
  under the binary swap rule.
