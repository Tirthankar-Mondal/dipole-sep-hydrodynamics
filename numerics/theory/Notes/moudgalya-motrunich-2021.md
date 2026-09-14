# Moudgalya & Motrunich (2021) — applicable details

Full paper: `numerics/theory/Papers/2108.10324v2.pdf`
arXiv:2108.10324v2, "Hilbert Space Fragmentation and Commutant Algebras."

## Why this paper is relevant: a reusable exact-counting technique, not our model

Not our exact model — their detailed dipole-conserving example (Sec.
VI) is a **spin-1 (three-state {+,0,-}, dilute)** chain where the local
move displaces a neutral "0" state (their Eq. 66), structurally
different from our dense binary chain. (They mention, only as an
unproven belief, that "spin-1/2 dipole-conserving pair-hopping models"
in their Refs. 38-39 have "closely resembling" structure — unconfirmed
whether that's our exact rule; not followed up here since the
Classen-Howes thesis gives an actual exact match instead.)

## What is directly reusable: the exact-counting method

- Method (Sec. VI + App. F): reduce any product state to a canonical
  form via the local moves; map canonical configurations onto a tiling
  problem with a small set of elementary tiles (for their model: empty
  dot, filled dot, dimer); get an exact count via a linear recursion —
  for their model this gives Pell numbers for the Krylov-subspace count.
- This is a template applicable to our own exact rule (0110<->1001),
  though we have not attempted it — the Classen-Howes thesis (see that
  note file) already carries out the equivalent derivation directly for
  our model via a different route (a transfer-matrix recursion in
  Appendix B.6), so this paper's main remaining value is as a second,
  independent worked example of the same style of technique, useful if
  the thesis's specific recursion needs cross-checking or extending.

## Applicable to H1 (frozen fraction) — methodological parallel

- Appendix H: their blockade-only frozen-fraction estimate for the
  spin-1 model (2/15 ~ 0.133) **underestimates** the true numerically
  measured Mazur bound (~0.24) because it excludes sites sitting in
  short active regions between blockades.
- This is a direct structural parallel to our own H1 task: getting f_N
  right requires accounting for the full active-region-length
  distribution, not just literal blockades/frozen runs. [UNCERTAIN]:
  this is a methodological caution, not a claim that our own ~0.36 has
  the same relationship to any blockade-only estimate — not checked,
  and the numbers (2/15, ~0.24) belong to their different model, not
  ours; do not compare them directly to 0.36.

## Applicable to QUESTIONS.md #3 (forbidden lengths) — same flavor of question, different model

- Their Appendix H works out exactly which small "blockade" sizes are
  combinatorially achievable for the spin-1 model (a unique 2-site
  blockade, no 3-site blockade, a unique 4-site one) — the same flavor
  of parity/packing question as our forbidden-length finding
  (1,2,3,5 absent), but worked out for their model, not ours. The
  Classen-Howes thesis addresses this question for our actual model
  (see that note file); this entry is kept mainly to record that the
  *type* of argument needed (small-size combinatorial enumeration under
  the local move) is a known, standard move in this literature.
