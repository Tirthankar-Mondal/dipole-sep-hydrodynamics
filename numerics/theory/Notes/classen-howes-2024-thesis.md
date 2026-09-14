# Classen-Howes (2024) DPhil thesis — applicable details

Full paper: `numerics/theory/Papers/Classen-Howes_2024_Quantum_and_classical-2.pdf`
Relevant scope: Chapter 4 (general theory), **Chapter 5 §5.1 (exact
match to our model)**, Appendix B (derivations). Chapter 3 and the rest
of Chapter 2 are an unrelated SYK-type model — not used here.

## Why this paper is relevant: it studies our exact model

General family (Ch.4): occupation n_i in {0,...,d-1} on a chain, random
range-k hopping gates conserving total number N and dipole moment
X=sum(i*n_i), filling nu=N/L. Setting **d=2 (hardcore), k=4** forces the
*only* allowed move to be 0110<->1001 (their Eq. 5.2) — this is our
swap exactly: (1,-1,-1,1)<->(-1,1,1,-1) in 0/1 language.

## Applicable to H1 (frozen fraction)

- General-k result: continuous strong->weak fragmentation transition at
  critical filling **nu_c = 1/(k-2)**. For k=4: nu_c=1/2.
- §5.1: d=2,k=4 (and separately d=3,k=3) is one of only two (d,k) pairs
  where nu_c equals its own particle-hole mirror point d-1-nu_c — a
  degenerate case where the usually-present weakly-fragmented phase
  (nu >= nu_c) **collapses to nothing**.
- §5.1.1: proved directly — any 5 consecutive holes (or 5 consecutive
  particles) necessarily freezes the middle 3 sites, *regardless of the
  surrounding configuration* ("absolute blockage", their Eqs. 5.2-5.4).
- Consequence stated explicitly (p.95): **the model is strongly
  fragmented at every filling nu, including nu=1/2 — there is no
  weakly-fragmented/thermalizing phase at all** for this (d,k).
- This is an independent, pre-existing analytic argument (not derived
  from our numerics) that a nonzero frozen fraction at nu=1/2 is the
  expected outcome in kind. **It does not give a value** — no closed
  form for the frozen-*site* density rho_F(nu=1/2) itself appears in
  the thesis, only for a related frozen-*blockage* probability P_b(nu)
  (exact recursive closed form, Eq. 5.9 / Eq. B.31, derived in Appendix
  B.6 via a transfer-matrix-style recursion over 0/1 sequences).
  Comparing 0.36 against an actual derived number would require
  extending that same recursion to the site density — not done here,
  and not attempted by us yet.

## Applicable to H2 (active-region length distribution)

- §5.1.2 derives an **exact** active-bubble density formula for x
  particles spanning ell sites, in the d=2,k=4 case:
  `a_2(x, ell, 4, nu*L, L) -> nu^x * (1-nu)^(ell-x) * P_b(nu)^2`
  — manifestly exponential in ell. This is the likely direct
  theoretical origin of H2's empirically-fit exponential form (our
  `h2_gap_length_distribution.ipynb` full-range fit favored exponential
  over power-law at all 8 L tested) rather than an unrelated coincidence.

## Applicable to QUESTIONS.md #3 (forbidden lengths 1,2,3,5)

- General formula: `ell_max(x,k) = 1 + (k-1)(x-1)` (their Eq. 4.47).
- For x=2 (a minimal active bubble = 2 particles), k=4:
  `ell_min(x=2,4) = ell_max(x=2,4) = 4` — i.e. the *only* possible
  length for a 2-particle active bubble is exactly 4. This explains:
  - why ell=1,2,3 can never occur (too short to host any interacting
    pair at all — no valid bubble fits)
  - why ell=4 has an elevated/special count (it's the unique length for
    the minimal nontrivial bubble)
- **ell=5 is not addressed in the thesis text** — its tabulated
  multiplicity function m_2(x,ell,k) is given only for k=5, not k=4.
  [UNCERTAIN — not thesis content, not independently re-verified by us]:
  a hand-derivation (done by the agent that read this thesis, applying
  the thesis's own restricted-mobility argument from §5.1.1 to all
  x=3 particle placements in 5- and 6-site windows) found every
  candidate ell=5,x=3 configuration decomposes into a frozen site plus
  the ell=4,x=2 bubble, while genuine ell=6,x=3 configurations do
  exist — consistent with our observed ell=5-forbidden/ell>=6-allowed
  pattern, but this is an extension of the method, not a result stated
  in the document, and has not been checked against our own raw
  pooled-gap data.

## Natural next step this makes tractable (not done)

Appendix B.6's recursive/transfer-matrix technique (used to get the
closed form for P_b(nu)) looks directly extensible to:
(a) an exact rho_F(nu=1/2) to compare against our numerical ~0.36
(b) an exact m_2(x,ell,k=4) table to compare against our full pooled
    gap-length histogram, including whether ell=5 is provably forbidden
    at *every* x, not just x=3 as hand-checked above.
Neither has been attempted.
