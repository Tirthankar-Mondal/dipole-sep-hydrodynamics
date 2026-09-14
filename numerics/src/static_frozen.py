"""Exact static (Krylov-sector) frozen fraction by brute-force enumeration.

This measures the quantity H1 in HYPOTHESES.md literally defines: a site is
frozen for a given initial configuration iff it takes the same value in
*every* configuration reachable from it by any sequence of 0110<->1001 moves.
That is a property of the initial string alone, with no run time or stopping
rule involved -- unlike the production estimators in frozen_fraction.py,
which are dynamical proxies (definition A: never flipped since t=0;
definition B: not flipped within a trailing window of W steps).

Feasible only at small L, because it enumerates the whole Krylov sector.
Added 2026-09-14 to close the [UNCERTAIN] flag that H1 has carried since it
was first stated: the equivalence between the dynamical proxies and static
reachability had never been checked against actual move-sequence enumeration.

Configurations are encoded as integer bitmasks (bit i set <-> site i holds
'1', i.e. spin +1), so sector membership can use a hash set.
"""

import numpy as np

PATTERN_1001 = [1, 0, 0, 1]
PATTERN_0110 = [0, 1, 1, 0]


def _apply(state, i, L, new_bits):
    for k, v in enumerate(new_bits):
        j = (i + k) % L
        state = (state | (1 << j)) if v else (state & ~(1 << j))
    return state


def neighbours(state, L):
    """All configurations one allowed move away from `state`."""
    out = []
    for i in range(L):
        bits = [(state >> ((i + k) % L)) & 1 for k in range(4)]
        if bits == PATTERN_1001:
            out.append(_apply(state, i, L, PATTERN_0110))
        elif bits == PATTERN_0110:
            out.append(_apply(state, i, L, PATTERN_1001))
    return out


def sector_and_frozen(state0, L, max_sector):
    """BFS the Krylov sector of `state0`.

    Returns (sector_size, n_frozen_sites) or (None, None) if the sector
    exceeds max_sector states (reported, never silently truncated).
    """
    mask = (1 << L) - 1
    seen = {state0}
    stack = [state0]
    always_one = state0          # bits set in every visited configuration
    always_zero = ~state0 & mask  # bits clear in every visited configuration

    while stack:
        s = stack.pop()
        always_one &= s
        always_zero &= ~s & mask
        for ns in neighbours(s, L):
            if ns not in seen:
                if len(seen) >= max_sector:
                    return None, None
                seen.add(ns)
                stack.append(ns)

    frozen = always_one | always_zero
    return len(seen), bin(frozen).count("1")


def random_half_filled(L, rng):
    v = np.array([1] * (L // 2) + [0] * (L // 2))
    rng.shuffle(v)
    state = 0
    for i, b in enumerate(v):
        if b:
            state |= (1 << i)
    return int(state)


def measure_static_frozen(L, n_samples, master_seed, max_sector=5_000_000):
    """Ensemble-average the exact static frozen fraction at fixed L.

    Density is exactly 1/2 (L must be even). Independent per-realization
    streams come from SeedSequence.spawn, tagged 3 to keep this stream
    distinct from run_ensemble ([seed, L]) and the rolling/gap estimators
    ([seed, L, 1] / [seed, L, 2]).
    """
    if L % 2:
        raise ValueError("L must be even for density exactly 1/2")

    seed_seq = np.random.SeedSequence([master_seed, L, 3])
    fractions, sizes = [], []
    n_over_cap = 0

    for child in seed_seq.spawn(n_samples):
        rng = np.random.default_rng(child)
        s0 = random_half_filled(L, rng)
        size, n_frozen = sector_and_frozen(s0, L, max_sector)
        if size is None:
            n_over_cap += 1
            continue
        sizes.append(size)
        fractions.append(n_frozen / L)

    arr = np.array(fractions)
    sz = np.array(sizes)
    return {
        "L": L,
        "n_samples": len(arr),
        "n_over_cap": n_over_cap,
        "master_seed": master_seed,
        "f_static_mean": float(arr.mean()) if len(arr) else float("nan"),
        "f_static_se": (float(arr.std(ddof=1) / np.sqrt(len(arr)))
                        if len(arr) > 1 else float("nan")),
        "sector_size_median": float(np.median(sz)) if len(sz) else float("nan"),
        "sector_size_max": int(sz.max()) if len(sz) else 0,
        "sector_size_mean": float(sz.mean()) if len(sz) else float("nan"),
        "samples": arr.tolist(),
        "sector_sizes": sz.tolist(),
    }
