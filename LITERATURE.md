# Literature

**Standout entry: Classen-Howes (2024) thesis, Chapter 5 -- studies the
project's exact model and directly bears on both H1 and H2. See below.**

Papers with applicable content have a corresponding note in
`numerics/theory/Notes/` (see CLAUDE.md, "Paper notes" rule) -- narrow,
just what's usable here, not a full reconstruction. Papers without a
note were judged background/analogy only; the reason is recorded inline
below instead.

Papers live in `numerics/theory/Papers/`. Each entry below is a
reconstruction of the paper's actual argument (not an abstract), plus an
explicit assessment of how it connects (or doesn't) to this project's
1D dipole-conserving chain: sites s_i = ±1, 4-site swap
(1,-1,-1,1) <-> (-1,1,1,-1) (equivalently 0110 <-> 1001), PBC, density
exactly 1/2, conserving both magnetization and dipole moment. Current
findings referenced below: H1 (frozen-site fraction f_N -> ~0.36 as
N->infinity, not vanishing), H2 (active-region-length distribution
between frozen sites appears exponential), and the question in
QUESTIONS.md #3 (active-region lengths of exactly 1, 2, 3, 5 never
occur; 4 and every length >=6 do).

---

## Morningstar, Khemani & Huse (2020) -- "Kinetically constrained
freezing transition in a dipole-conserving system," arXiv:2004.00096v3

Note: `numerics/theory/Notes/morningstar-khemani-huse-2020.md`

**This is the direct theoretical ancestor of the project's model.**

Sets up a 1D lattice with occupation n_i in {0,1,2}, evolved by random
4-site gates that replace any 4-site window with a uniformly random
configuration of the same local charge N_0 and dipole moment N_1
(infinite-temperature, detailed-balance dynamics). Tuning the average
density n-bar away from half filling (n-bar=1) drives a genuine
dynamical phase transition at n-bar_c ~ 1.5 (conjectured exact, only
proven as a lower bound): weakly fragmented/thermalizing below, strongly
fragmented with a persistent nonzero frozen-site fraction rho_F above.
Near the transition (from an idealized/heuristic coarse model, not the
literal gate dynamics): rho_F ~ (n-bar - n-bar_c)^1 (beta=1), correlation
length xi ~ (n-bar-n-bar_c)^-2 (nu=2), and a power-law active-block-length
distribution at criticality p(L_A) ~ L_A^-3/2.

**Model-level connection (exact, not analogical):** restrict the paper's
k=4, n_max=2 gate to inputs where no site ever has n_i=2 (hardcore
sector). Of all nontrivial groups in the paper's own Table I, only one
survives that restriction: {0110, 1001} -- exactly the project's move,
nothing else. So the project's chain *is* this paper's model, exactly
restricted to its own dynamically-invariant hardcore sub-manifold, at
n-bar=0.5. This also confirms the hardcore sector is itself strongly
fragmented in the paper's own sense (hardcore and n_i=2-containing
configurations are dynamically disconnected at fixed (N_0,N_1)).

**What transfers and what doesn't:**
- The paper's frozen-site order parameter rho_F is the same quantity as
  H1's f_N, and crucially uses the same *static/Krylov-sector*
  definition (frozen for all times iff constant across every
  configuration reachable from the initial state) that HYPOTHESES.md
  flags as [UNCERTAIN] for this project -- this paper uses that
  definition as its primary object throughout, which supports (without
  proving, for this project's specific numerics) that it's a reasonable
  stand-in for a patience-based dynamical estimator.
- The paper's quantitative critical exponents (beta=1, nu=2, alpha=3/2)
  do NOT transfer: that mechanism requires active regions to grow by
  absorbing charge up to a reservoir cap (n_max=2), which doesn't exist
  in the project's strictly binary (n_max=1) chain -- there is no analog
  of "tuning toward n-bar_c" since density is pinned at exactly 1/2 with
  no room to grow further locally.
- By the paper's own particle-hole symmetry n-bar <-> 2-n-bar, density
  0.5 is the mirror of their critical density ~1.5 -- suggestive but
  [UNCERTAIN]: that symmetry is a statement about the *full* n_max=2
  ensemble, not about the hardcore corner the project restricts to;
  nothing in the paper establishes the hardcore corner inherits the full
  ensemble's near-critical statistics.
- H2's exponential (short-tailed) finding is qualitatively consistent
  with this paper's *non-critical* frozen-phase active-block statistics
  (finite correlation length, steep falloff away from n-bar_c in their
  Fig. 4c) -- the project's chain has no tunable parameter to approach
  their critical point, so it structurally sits in the off-critical
  regime where their own data show short-tailed (not power-law)
  active-region lengths. Not a derivation of the exponential form, just
  a qualitative match.
- H3 (forbidden lengths 1,2,3,5) is **not addressed by this paper at
  all** -- it operates at the level of large-active-block statistics,
  never the exact short-string combinatorics of the binary swap rule.

---

## Han, Lake & Ro (2023) -- "Scaling and localization in
multipole-conserving diffusion," arXiv:2304.03276v3

Same elementary move as the project (dipole-conserving 4-site
hop/swap -- their Eq. 5-6 "out"/"in" process is exactly 0110<->1001
under the standard occupation<->spin dictionary), but studied in the
**opposite (dense, ergodic) regime**: rates are chosen proportional to
occupation-number products so the dynamics coarse-grains to a nonlinear
diffusion PDE (d_t rho = d_x^2[rho^2 d_x^2 ln rho] for dipole
conservation), giving exponentially localized steady states,
z=4+d nonlinear relaxation crossing over to ordinary z=4 fracton
subdiffusion for small fluctuations about a nonzero background, and (for
quantum statistics) real-space Fermi surfaces/BEC.

**Explicitly excludes the project's regime.** The continuum/hydrodynamic
derivation requires "a large number of particles per site, far above the
critical density for onset of non-ergodicity" -- the authors state
outright that at low density the kinetic constraints can "completely
prevent all motion" (i.e., exactly the fragmentation/freezing phenomenon
H1/H2 study), and their entropy-maximization argument for steady states
presupposes ergodicity, which fails in the project's dense-but-hardcore,
half-filled regime. No frozen fraction, active-region distribution, or
fragmentation quantity is computed anywhere in this paper.

**Practical value:** its reference list is more directly useful than its
own results -- it cites Sala-Rakovszky-Verresen-Knap-Pollmann (PRX 2020),
Khemani-Hermele-Nandkishore (PRB 2020), Rakovszky-Sala-Verresen-Knap-Pollmann
(PRB 2020), Morningstar-Khemani-Huse (PRB 2020, already in this folder,
see above), and Pozderac-Speck-Feng-Huse-Skinner (PRB 2023,
"Exact solution for the filling-induced thermalization transition in a
1D fracton system") as the papers that actually characterize the
freezing/fragmentation transition for this move -- these look more
directly on-point for H1/H2 than this paper itself. [Noting their
existence, not acquiring them or recommending action -- researcher's
call.]

---

## Moudgalya & Motrunich (2021) -- "Hilbert Space Fragmentation and
Commutant Algebras," arXiv:2108.10324v2

Note: `numerics/theory/Notes/moudgalya-motrunich-2021.md`

A formalism paper: builds a rigorous algebraic language (bond
algebra / commutant algebra) for Hilbert-space fragmentation, replacing
the previously case-by-case/heuristic characterization with a precise
criterion (dim(commutant) scaling exponentially with system size L) and
a clean distinction between *classical* fragmentation (commutant is
Abelian/diagonal in the product basis) and *quantum* fragmentation
(non-Abelian, entangled Krylov subspaces). Applies this to four model
families, computing exact commutants, exact Krylov-subspace counts, and
tight Mazur bounds via the *full* commutant (showing that minimal
generating sets like SLIOMs are generally not sufficient for tight
bounds).

**Not the project's model, but the closest available worked template.**
Its detailed dipole-conserving example is a **spin-1** (three-state,
dilute: {+,0,-}) chain (Sala/Khemani et al.'s model), structurally
different from the project's dense binary chain -- the local move
requires displacing a neutral "0" state (their Eq. 66), so this is not
an exact match. The paper only mentions, in passing and as an admitted
belief (not a derivation), that "spin-1/2 dipole-conserving pair-hopping
models" (their Refs. 38-39) have "closely resembling" Krylov structure
-- unconfirmed whether those refs are the project's exact rule.

**What is directly reusable as a technique (this is the standout part):**
- Their "blockade" (a frozen region disconnecting the chain into
  independent halves) is exactly the project's frozen-site/frozen-region
  notion; their discussion of sites sitting in a short active region
  between two blockades is exactly H2's active-region-length question.
- They derive an **exact combinatorial method**: reduce any product
  state to a canonical form, map canonical configurations onto a tiling
  problem with a small set of elementary tiles (for their model: empty
  dot, filled dot, dimer), get an exact count via a linear recursion
  (Pell numbers here) -- this is a template the project could reuse to
  derive H2's exponential form and the specific forbidden lengths
  (1,2,3,5) analytically, rather than only empirically. In their own
  model, Appendix H works out exactly which small blockade sizes are
  combinatorially achievable (a unique 2-site blockade, no 3-site
  blockade, a unique 4-site one) -- the same *flavor* of parity/packing
  question as the project's QUESTIONS.md #3, worked out for their model,
  not the project's.
- They show their blockade-only frozen-fraction estimate (2/15 ~ 0.133
  for the spin-1 model) **underestimates** the true numerically measured
  value (~0.24) because it omits sites in short active regions between
  blockades -- a direct structural analogue of the project's own task
  (getting f_N right requires accounting for the active-region-length
  distribution, not just literal blockades). [UNCERTAIN: this is a
  methodological parallel, not a claim that the project's own ~0.36 vs.
  any blockade-only estimate has the same relationship -- not checked.]
- Numbers (2/15, ~0.24) belong to their spin-1 model and should not be
  compared directly to the project's ~0.36 or exponential-fit
  parameters as if predictions for the same system.

---

---

## Glorioso, Guo, Rodriguez-Nieva & Lucas (2021) -- "Breakdown of
hydrodynamics below four dimensions in a fracton fluid," arXiv:2105.13365v1

Builds a fluctuating-hydrodynamics theory for systems that conserve
charge, dipole moment, *and* momentum together, using two continuous
classical Hamiltonian models (a chain with momentum-difference kinetic
term; a tilted cos-p lattice) -- neither resembles the project's
discrete ±1 chain (no momentum d.o.f., no discreteness). Central result:
linear theory gives ordinary z=4 fracton subdiffusion, but a KPZ-type
nonlinear coupling is relevant below 4 spatial dimensions, driving the
1D system to an anomalous z~2.5 (crude Flory-type estimate, confirmed
numerically in both models) -- a new universality class, upper critical
dimension 4 instead of ordinary KPZ's 2.

**Explicitly presupposes thermalization within the fixed charge-dipole
sector** -- its own introduction states the hydrodynamic theory applies
"if such a phase... can thermalize." The project's H1 finding (frozen
fraction -> ~0.36, not vanishing) says the project's chain does *not*
thermalize ergodically in that sector at all -- Hilbert-space
fragmentation, the opposite regime from what this paper derives.
No frozen fraction, active-region statistic, or fragmentation quantity
appears anywhere in this paper; it is background/contrast (what
transport would look like *if* the chain thermalized), not a source of
predictions for H1/H2.

**Points to the same missing references as 2304.03276v3** (see above):
its introduction cites, in passing, Pai-Pretko-Nandkishore (PRX 2019),
**Sala-Rakovszky-Verresen-Pollmann (PRX 2020)**, Khemani-Hermele-Nandkishore
(PRB 2020), and Morningstar-Khemani-Huse (PRB 2020, already reconstructed
above) as the actual discrete dipole-conserving-lattice/fragmentation
literature. [UNCERTAIN: agent flagged these as likely more relevant than
this paper itself, based on titles/context only -- not independently
verified by reading them.] Third independent pointer (after
2304.03276v3 and PRXQuantum.6.020321 below) converging on the same
missing reference, Sala et al. 2020, as probably the most direct match
for H1/H2 -- noted here as literature information, not acted on.

---

## Zerba, Seidel, Pollmann & Knap (2025) -- "Emergent Fracton
Hydrodynamics of Ultracold Atoms in Partially Filled Landau Levels,"
PRX Quantum 6, 020321

Shows that projecting a 2D interacting Bose gas (rotating BEC, or
Harper-Hofstadter lattice at a fine-tuned flat-band commensurability)
onto a single Landau level turns the residual interaction into a 1D
lattice of "squeezing" terms whose momentum-label bookkeeping
automatically conserves both total charge and Σ(position x
charge) -- i.e., real-space dipole conservation emerges from LLL
projection (proved via a resolution-of-identity argument, Appendix D).
In the "thick-torus" (long-range-squeezing) regime this gives fracton
hydrodynamics, z=4, confirmed via exact diagonalization
(density-density autocorrelations decaying as t^-1/4). In the
"thin-torus" (short-range) regime the system instead shows strong
Hilbert-space fragmentation -- addressed only qualitatively, with
eventual thermalization stated as an expectation, not proven.

**Analogy only, not a model-level match** -- five load-bearing
differences from the project: (1) coherent unitary quantum dynamics
(exact diagonalization) vs. the project's classical stochastic process;
(2) genuinely 2D system with an *emergent*, energy-restricted 1D
description (valid only under U<<hbar*omega_c and, for the lattice
case, exact flat-band fine-tuning) vs. the project's fundamentally 1D
chain; (3) a tunable-range family of squeezing terms vs. the project's
single minimal 4-site move; (4) the paper's headline z=4 result lives
in the *thick-torus/weakly-fragmented* regime, the opposite of where
the project's H1/H2 sit (strongly fragmented); (5) H2's specific
forbidden-length finding (1,2,3,5) is a classical reachability-graph
combinatorics question this paper's momentum-space framework never
touches.

**Fourth convergent pointer:** this paper's own bibliography names
ref. [53] Sala-Rakovszky-Verresen-Knap-Pollmann (PRX 10, 011047, 2020,
*Ergodicity Breaking Arising from Hilbert Space Fragmentation in
Dipole-Conserving Hamiltonians*) and ref. [56] Morningstar-Khemani-Huse
(already reconstructed above) as the closer classical/kinetically-
constrained analogs -- the same Sala et al. 2020 paper flagged
independently by the two entries above. [UNCERTAIN: pointer only, not
independently verified.]

---

---

## Classen-Howes (2024) -- DPhil thesis, "Quantum and Classical Hilbert
Space Fragmentation" (Oxford, Merton College; supervisor S. Parameswaran)

Note: `numerics/theory/Notes/classen-howes-2024-thesis.md`

150 pages; only Chapters 4-5 and Appendix B are relevant (Ch.3 is an
unrelated long-range SYK-type model; Ch.2 is general HSF background/
vocabulary). Built on Classen-Howes, Fendley, Pandey, Parameswaran, PRB
110, 125140 (2024) [Ch.3] and Classen-Howes, Senese, Prakash,
arXiv:2408.10321 [Ch.4-5].

**Chapter 5, Section 5.1 studies the project's exact model.** The
general family in Chapter 4 is: occupation n_i in {0,...,d-1} on a
chain, random range-k hopping gates conserving total number N and
dipole moment X=sum(i*n_i), filling nu=N/L. Setting d=2 (hardcore) and
k=4 forces the *only* allowed move to be 0110<->1001 (their Eq. 5.2) --
exactly the project's swap, in 0/1 language exactly matching
(1,-1,-1,1)<->(-1,1,1,-1).

**H1 connection -- direct and load-bearing, not just analogous.** For
general k, Chapter 4's main result is a continuous strong-to-weak
fragmentation transition at a universal critical filling
nu_c=1/(k-2), with frozen density rho_F -> 0 as nu -> nu_c^- and
rho_F=0 (weakly fragmented, thermalizing) for nu >= nu_c. At k=4, d=2,
nu_c=1/2 -- but this is exactly the special/degenerate point (Sec. 5.1
identifies d=2,k=4 as one of only two (d,k) pairs, the other being
d=3,k=3, where the lower critical density equals the "mirror" upper
critical density d-1-nu_c). At this degenerate point the model has
"absolute blockages": any 5 consecutive holes (or particles) necessarily
freezes its middle 3 sites *regardless of surrounding configuration*
(proved directly, Sec. 5.1.1). Consequence, stated explicitly by the
thesis (p.95): **the model is strongly fragmented at every filling nu,
including nu=1/2 -- there is no weakly-fragmented phase at all** for
this (d,k). This is a genuine theoretical prediction that the
project's H1 finding (f_N -> nonzero constant, not vanishing) is
qualitatively correct in kind, from an independent analytic argument
that predates and does not depend on the project's own numerics.
[UNCERTAIN/not yet done: the thesis does not give a closed-form value
for rho_F(nu=1/2) itself -- only for the frozen-*blockage* probability
P_b(nu) (Eq. 5.9/B.31, an exact recursive closed form). Deriving the
exact frozen-*site* density number to compare against the project's
numerical ~0.36 would need extending Appendix B.6's method, which the
agent that read this thesis explicitly says is not already worked out
in the document -- would be new analytic work, not a lookup.]

**H2 connection -- direct theoretical origin of the exponential form,
partial explanation of the forbidden lengths.** The thesis derives an
exact active-bubble density formula for x particles spanning ell sites,
d=2,k=4: a_2(x,ell,4,nuL,L) -> nu^x (1-nu)^(ell-x) * P_b(nu)^2 (Sec.
5.1.2) -- manifestly exponential in ell. This is presented as the
likely direct theoretical origin of H2's empirically-fit exponential
form, not an independent coincidence. On forbidden lengths: the
thesis's general formula ell_max(x,k)=1+(k-1)(x-1) combined with the
k=4 minimal-move requirement gives ell_min(x=2,4)=ell_max(x=2,4)=4 --
explaining why ell=1,2,3 can never occur (too short to host any
interacting pair) and why ell=4 is uniquely realizable for the minimal
active bubble (elevated count, as the project observed empirically).
**The forbidding of ell=5 specifically is not spelled out in the
thesis** (its tabulated multiplicity function m_2(x,ell,k) is only
given for k=5, not k=4). [UNCERTAIN/not thesis content: the agent that
read the thesis did its own hand-derivation, applying the thesis's
stated restricted-mobility argument to all x=3 particle placements in
5- and 6-site windows, finding every ell=5,x=3 candidate decomposes
into a frozen site plus the ell=4,x=2 bubble, while genuine ell=6,x=3
configurations do exist -- consistent with the project's observed
ell=5 forbidden / ell>=6 allowed pattern, but this specific check is
the agent's own extension of the method, not a result stated in the
document, and has not been independently re-verified by the researcher
or cross-checked against the project's own raw data.]

**Practical follow-up this thesis makes tractable (not undertaken
here):** Appendix B.6's recursive/transfer-matrix technique that
produced the closed form for P_b(nu) looks directly extensible to (a)
an exact rho_F(nu=1/2) to compare against the numerical ~0.36, and (b)
an exact m_2(x,ell,k=4) table to compare against the full empirical
gap-length histogram, including checking whether ell=5 is provably
forbidden at every x, not just x=3. Noted as a natural next step this
literature makes available, not acted on.

---

## Sala, Rakovszky, Verresen, Knap & Pollmann (2020) -- "Ergodicity
breaking arising from Hilbert space fragmentation in dipole-conserving
Hamiltonians," arXiv:1904.04266v2 (PRX 10, 011047)

Added by the researcher after three other papers in this folder
(2304.03276v3, 2105.13365v1, PRXQuantum.6.020321) each independently
cited this paper, in passing, as looking like the more relevant
reference for H1/H2 -- **checked in full; it turns out not to apply,
and the reason is concrete rather than a vague miss.**

**Structural mismatch, not just a different parameter regime.** This
paper studies **spin-1** chains (three states per site, {+,0,-}) with
Hamiltonians H_3, H_4 built from single-step raising/lowering operators
(their Eqs. 1-2) -- every term must pass through the neutral "0"
(vacancy) state; there is no vacancy-free two-state exchange move in
this model at all. Restricted to a purely hardcore {+1,-1} subspace
with no "0" ever present, both H_3 and H_4 act trivially.

**Concrete illustration of the mismatch:** the project's move, in this
paper's own +-1 notation, is (+,-,-,+)<->(-,+,+,-), i.e. 1001<->0110.
But this paper's own general rule (Sec. III B1) states that *any* block
of >=2 consecutive equal-sign charges is annihilated by H_3's terms and
becomes part of a frozen wall -- the interior "-,-" and "+,+" blocks in
1001/0110 are exactly such frozen blocks under this paper's dynamics.
**The pattern our rule treats as the only actively-moving configuration
is, under this paper's Hamiltonians, part of the frozen construction.**
The two models are not nested; this is a different constrained-exchange
dynamics (closer to a dipole-conserving SSEP/facilitated exclusion
process) than the vacancy-mediated fracton-hopping studied here.

**H1/H2/H3, checked individually -- none apply:**
- H1: this paper counts frozen product *eigenstates* (entire stationary
  configurations, e.g. ~2.11^N of them for H_3) in the full 3^N-dimensional
  Hilbert space -- a fundamentally different quantity from a per-site
  frozen *fraction* on a typical actively-evolving hardcore
  configuration. No value or formula here bears on the ~0.36 constant.
- H2: no probability distribution over active-region lengths is
  defined or computed anywhere in this paper.
- H3 (forbidden lengths): the closest analogous quantity is a minimal
  frozen-patch size 2*ell-1 as a function of the *Hamiltonian's
  interaction range* ell (a property of which Hamiltonian is assumed),
  not a length of an unfrozen/active region in a fixed hardcore rule --
  not applicable.

No `numerics/theory/Notes/` file created for this paper, per the
"skip if nothing concretely applicable" rule in CLAUDE.md -- its value
here is the mismatch itself (closing off a pointer three other papers
raised, now checked rather than left open) and, secondarily, its
general methodology (wall-invariance argument, transfer-matrix counting
of frozen patches, Mazur-bound machinery) as a template if ever needed,
not as a source of applicable numbers.
