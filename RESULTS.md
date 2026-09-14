# Results

Summary of work to date. Status labels are load-bearing: "working
assumption" and "researcher's claim" are not the same as "confirmed" —
see HYPOTHESES.md for full statements, candidate outcomes, and what
would falsify each, and RESEARCH_LOG.md for the underlying runs.

---

## H1 — Frozen-site fraction

**Status:** researcher's working assumption, not a formal fit result.

- f_N (rolling-window definition B, self-scaling burn-in) scatters
  around **0.36 +/- 0.009** across N=100-10,000. The two settings
  variants tried gave last-5-point weighted averages of 0.3637
  (W=5L/M=10/c_selfscale=5) and 0.3601 (W=10L/M=20/c_selfscale=10) —
  consistent with each other given that W enters the definition of the
  observable itself (larger W excludes more sites from "frozen").
- On this basis, the researcher is provisionally treating f_N as
  saturating to a nonzero constant (candidate H1a) and moving on to the
  next question. The formal H1a vs H1b (power-law vanishing) vs H1c
  (log vanishing) model comparison has **not** been redone under this
  rolling-window definition — the comparison that was done previously
  used the since-superseded cumulative definition (archived).
- `production_large_scale.yaml` (N=10,000-20,000, cost estimated
  ~4.2-4.6h) is configured but **has not been run** — a scheduled
  launch was interrupted before it started.

## H2 — Active-region (gap) length distribution

**Status:** researcher's claim, supported by data; not independently
model-selected beyond R^2.

- Measured as the pooled distribution of gap lengths (active sites
  strictly between two consecutive frozen sites, one post-burn-in
  snapshot per realization), zero-length gaps excluded per researcher
  instruction.
- Full-range (l=4 upward, no tail cutoff) OLS comparison favors an
  **exponential** distribution over a power-law at every one of the 8 L
  values tested (L=100-12,800): R^2 0.910-0.966 (exponential) vs.
  0.872-0.906 (power-law).
- Mean nonzero gap length (~15.4-16.1) and the zero-gap rate
  (~0.885-0.889) are both flat across the full L range (2 decades).

## Open question — forbidden gap lengths (QUESTIONS.md #3)

- Gap lengths of exactly **1, 2, 3, and 5 sites never occur**, at any L
  tested (100-12,800), including thousands of pooled samples each at
  the extremes. Length 4 occurs with an elevated count; every length
  >=6 occurs. Not yet explained from first principles using our own
  derivation — see literature support below for a partial explanation.

## Literature support (full detail: `LITERATURE.md`, `numerics/theory/Notes/`)

- **Classen-Howes (2024) thesis, Ch.5 Sec.5.1** studies our *exact*
  model (d=2, k=4 hardcore dipole-conserving chain). Independently
  predicts the model is strongly fragmented at *every* filling,
  including ours — pre-existing analytic support for H1 in kind (not a
  derived value to compare against 0.36). Derives an exact,
  exponential-in-length active-bubble density formula — the likely
  direct theoretical origin of H2's exponential form. Explains why gap
  lengths 1-3 never occur and why 4 is special; does not address length
  5 (a hand-derivation consistent with our finding exists but is not
  independently re-verified against our raw data).
- **Morningstar, Khemani & Huse (2020):** our model is exactly their
  hardcore-restricted invariant sub-sector; their frozen-site order
  parameter uses the same static/Krylov-sector definition our
  rolling-window estimator targets. Their quantitative critical
  exponents do not transfer (require a charge reservoir our model
  doesn't have).
- **Moudgalya & Motrunich (2021):** not our exact model, but supplies a
  reusable exact-counting technique (canonical form -> tiling -> linear
  recursion) as a template for an independent derivation of H2/H3 — not
  yet attempted.
- Three papers (Han-Lake-Ro 2304.03276, Glorioso et al. 2105.13365,
  Zerba et al. PRXQuantum.6.020321) reviewed and found to be
  background/analogy only — they study the opposite (dense, ergodic)
  regime.
- **Sala, Rakovszky, Verresen, Knap & Pollmann (2020)** was flagged by
  three of the above as the likely missing reference, added by the
  researcher, and checked directly: it does **not** apply — structural
  mismatch (vacancy-mediated dynamics; their frozen blocks are exactly
  our active pattern).

## Not yet done

- `production_large_scale.yaml` run (N=10,000-20,000).
- H1a/H1b/H1c model comparison under the rolling-window definition.
- Analytic derivation of an exact rho_F(nu=1/2) and an exact
  forbidden-gap-length table, extending the Classen-Howes thesis's
  Appendix B.6 recursion — would give real numbers to compare against
  the empirical 0.36 and the forbidden-length pattern, rather than only
  qualitative agreement.
