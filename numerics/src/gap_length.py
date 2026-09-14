"""Measurement of the active-region (gap) length distribution between
frozen sites, under the rolling-window frozen-site definition (H2 in
HYPOTHESES.md).

Uses the same self-scaling burn-in as H1's rolling-window frozen
fraction (locked in 2026-09-13; see frozen_fraction.py's
_self_scaling_burnin). After burn-in, takes exactly one measurement
window (a single post-burn-in snapshot, not averaged over multiple
windows) and reads off the site-level frozen/active mask, from which
gap lengths between consecutive frozen sites are extracted.

A gap length is the number of active (non-frozen) sites strictly
between two consecutive frozen sites on the ring; two adjacent frozen
sites give a gap length of 0.

[UNCERTAIN] As with H1, this assumes the rolling-window/self-scaling
burn-in produces a representative post-burn-in snapshot of the frozen
set (see HYPOTHESES.md, H1's flagged assumption). H2 additionally
assumes a single snapshot per realization is enough to characterize
that realization's local frozen-site structure -- gap samples from one
snapshot are spatially correlated (they partition the same ring), and
decorrelation relies on pooling across independent realizations, not
within one (see HYPOTHESES.md, H2).
"""

import numpy as np

from frozen_fraction import _self_scaling_burnin


def _gap_lengths_from_mask(frozen_mask):
    """Cyclic gap lengths between consecutive frozen sites. Returns None
    if fewer than 2 sites are frozen (gaps are not well-defined)."""
    L = len(frozen_mask)
    frozen_indices = np.flatnonzero(frozen_mask)
    n_frozen = len(frozen_indices)
    if n_frozen < 2:
        return None
    shifted = np.roll(frozen_indices, -1)
    gaps = (shifted - frozen_indices) % L - 1
    return gaps


def measure_gap_lengths(L, density, patience_multiplier, max_steps_multiplier,
                         W_multiplier, c_selfscale, max_extra_windows, rng):
    burnin = _self_scaling_burnin(L, density, patience_multiplier,
                                   max_steps_multiplier, W_multiplier,
                                   c_selfscale, max_extra_windows, rng)

    if burnin["status"] == "jammed":
        # No active sites remain at all -- every site is frozen in this
        # final static configuration, so there are zero active regions
        # (not one degenerate mega-gap). Reported separately, not pooled
        # into the ordinary gap-length distribution.
        return {"converged": True, "burn_in_steps": burnin["burn_in_steps"],
                "jammed_before_measurement": True,
                "n_frozen_sites": L, "gap_lengths": [],
                "frozen_fraction_snapshot": 1.0}
    if burnin["status"] == "t0_not_reached":
        return {"converged": False, "reason": "T0_not_reached",
                "burn_in_steps": burnin["burn_in_steps"]}
    if burnin["status"] == "self_scaling_cap_exceeded":
        return {"converged": False, "reason": "self_scaling_cap_exceeded",
                "burn_in_steps": burnin["burn_in_steps"]}

    chain = burnin["chain"]
    W = burnin["W"]

    flipped_in_window = np.zeros(L, dtype=bool)
    jammed = False
    for _ in range(W):
        flipped_sites = chain.step()
        if flipped_sites is None:
            jammed = True
            break
        flipped_in_window[flipped_sites] = True

    if jammed:
        return {"converged": True, "burn_in_steps": burnin["burn_in_steps"],
                "jammed_before_measurement": True,
                "n_frozen_sites": L, "gap_lengths": [],
                "frozen_fraction_snapshot": 1.0}

    frozen_mask = ~flipped_in_window
    gaps = _gap_lengths_from_mask(frozen_mask)

    if gaps is None:
        return {"converged": False, "reason": "too_few_frozen_sites",
                "burn_in_steps": burnin["burn_in_steps"],
                "n_frozen_sites": int(frozen_mask.sum())}

    return {
        "converged": True,
        "burn_in_steps": burnin["burn_in_steps"],
        "jammed_before_measurement": False,
        "n_frozen_sites": int(frozen_mask.sum()),
        "frozen_fraction_snapshot": float(frozen_mask.mean()),
        "gap_lengths": gaps.tolist(),
    }


def run_ensemble_gap_lengths(L, density, patience_multiplier, max_steps_multiplier,
                              W_multiplier, c_selfscale, max_extra_windows,
                              target_relative_se, min_samples,
                              batch_size, max_samples_per_N, master_seed):
    """Ensemble of gap-length snapshots at fixed L. Adaptive stopping
    reuses H1's rule (target relative SE on the mean), applied here to
    the per-realization snapshot frozen fraction (n_frozen_sites/L) --
    equivalent in spirit to H1's stopping rule since the mean gap length
    is fixed by that same quantity (see HYPOTHESES.md, H2).

    Zero-length gaps (two frozen sites immediately adjacent, nothing
    active between them) are discarded from the pooled distribution per
    researcher instruction, 2026-09-14 -- the distribution reported here
    is over *nonzero* active-region lengths only. This means
    gap_length_mean no longer matches the (1-f)/f identity noted in
    HYPOTHESES.md (that identity holds only including the zeros); the
    discarded-zero count and rate are reported so the size of that
    effect is visible rather than silently dropped.

    Realizations discarded for T0_not_reached / self_scaling_cap_exceeded
    / too_few_frozen_sites are excluded and counted in n_discarded.
    Jammed realizations (no active sites at all) are excluded from both
    the pooled gaps and the frozen-fraction-snapshot average, and
    counted separately in n_jammed -- they are a qualitatively different
    outcome (100% frozen), not part of either distribution.
    """
    seed_seq = np.random.SeedSequence([master_seed, L, 2])  # 2 = "gap_length" tag
    frozen_fraction_snapshots = []
    pooled_gaps = []
    n_discarded = 0
    n_jammed = 0
    n_drawn = 0
    n_raw_gaps = 0
    n_zero_gaps = 0

    while n_drawn < max_samples_per_N:
        n_this_batch = min(batch_size, max_samples_per_N - n_drawn)
        for child_seed in seed_seq.spawn(n_this_batch):
            rng = np.random.default_rng(child_seed)
            out = measure_gap_lengths(L, density, patience_multiplier,
                                       max_steps_multiplier, W_multiplier,
                                       c_selfscale, max_extra_windows, rng)
            n_drawn += 1
            if not out["converged"]:
                n_discarded += 1
                continue
            if out.get("jammed_before_measurement", False):
                n_jammed += 1
                continue
            frozen_fraction_snapshots.append(out["frozen_fraction_snapshot"])
            raw_gaps = out["gap_lengths"]
            n_raw_gaps += len(raw_gaps)
            nonzero_gaps = [g for g in raw_gaps if g > 0]
            n_zero_gaps += len(raw_gaps) - len(nonzero_gaps)
            pooled_gaps.extend(nonzero_gaps)

        if len(frozen_fraction_snapshots) >= min_samples:
            arr = np.array(frozen_fraction_snapshots)
            mean = arr.mean()
            se = arr.std(ddof=1) / np.sqrt(len(arr))
            if mean > 0 and se / mean < target_relative_se:
                break

    ffs = np.array(frozen_fraction_snapshots)
    gaps = np.array(pooled_gaps, dtype=np.int64)

    return {
        "L": L,
        "W": W_multiplier * L,
        "master_seed": master_seed,
        "n_realizations": len(ffs),
        "n_discarded": n_discarded,
        "n_jammed": n_jammed,
        "frozen_fraction_snapshot_mean": float(ffs.mean()) if len(ffs) else float("nan"),
        "frozen_fraction_snapshot_se": (
            float(ffs.std(ddof=1) / np.sqrt(len(ffs))) if len(ffs) > 1 else float("nan")
        ),
        "n_raw_gaps": n_raw_gaps,
        "n_zero_gaps_discarded": n_zero_gaps,
        "zero_gap_rate": n_zero_gaps / n_raw_gaps if n_raw_gaps else float("nan"),
        "n_pooled_gaps": len(gaps),
        "gap_length_mean": float(gaps.mean()) if len(gaps) else float("nan"),
        "gap_length_std": float(gaps.std(ddof=1)) if len(gaps) > 1 else float("nan"),
        "gap_lengths": gaps.tolist(),
    }
