"""Measurement of the frozen-site fraction f_N (H1 in HYPOTHESES.md).

A site is frozen if its value never changes over the whole trajectory.
We estimate this empirically per realization by running the dynamics
until either (a) no active sites remain (fully jammed - the strongest
possible convergence signal), or (b) no new site has been flipped for
`patience` consecutive moves (a heuristic stabilization criterion).

[UNCERTAIN] This assumes the set of ever-flipped sites, once stabilized,
equals the true reachable set independent of move order/run length -
this equivalence has not been verified against exhaustive enumeration
(see HYPOTHESES.md, H1, "Assumption (flagged, not verified)").
"""

import numpy as np
from scipy import stats

from dipole_chain import DipoleChain


def measure_frozen_fraction(L, density, patience_multiplier,
                             max_steps_multiplier, rng):
    chain = DipoleChain(L, density, rng)
    ever_flipped = np.zeros(L, dtype=bool)

    patience = patience_multiplier * L
    max_steps = max_steps_multiplier * patience

    steps_since_growth = 0
    steps_taken = 0
    converged = False

    while steps_taken < max_steps:
        flipped_sites = chain.step()
        if flipped_sites is None:
            converged = True
            break
        steps_taken += 1

        grew = not ever_flipped[flipped_sites].all()
        ever_flipped[flipped_sites] = True

        if grew:
            steps_since_growth = 0
        else:
            steps_since_growth += 1
            if steps_since_growth >= patience:
                converged = True
                break

    return {
        "frozen_fraction": 1.0 - ever_flipped.mean(),
        "converged": converged,
        "steps_taken": steps_taken,
    }


def _trend_test(window_fractions):
    """Linear-trend test, NaN-safe: an exactly-flat batch (zero variance
    across windows) is the most stable case possible, not an undefined
    one -- report pvalue=1.0 with zero_variance=True rather than NaN.
    """
    window_fractions = np.asarray(window_fractions)
    if np.std(window_fractions) == 0.0:
        return {"slope": 0.0, "pvalue": 1.0, "zero_variance": True}
    idx = np.arange(len(window_fractions))
    trend = stats.linregress(idx, window_fractions)
    return {"slope": float(trend.slope), "pvalue": float(trend.pvalue),
            "zero_variance": False}


def _self_scaling_burnin(L, density, patience_multiplier, max_steps_multiplier,
                          W_multiplier, c_selfscale, max_extra_windows, rng):
    """Shared burn-in for the rolling-window (definition B) measurements --
    extracted 2026-09-14 so the H2 gap-length measurement can reuse the
    exact same self-scaling burn-in as H1's measure_frozen_fraction_rolling
    without duplicating it (locked in 2026-09-13, see that function's
    docstring for the burn-in's own justification). Pure extraction, no
    change in logic -- H1 results are expected to be unaffected.

    On success, returns the chain positioned immediately after burn-in
    completes, ready for a caller-specific measurement phase:
        {"status": "ready", "chain": ..., "ever_flipped": ...,
         "T0": ..., "W": ..., "burn_in_steps": ...}
    On failure, one of:
        {"status": "jammed", "burn_in_steps": ..., "ever_flipped": ...}
        {"status": "t0_not_reached", "burn_in_steps": ...}
        {"status": "self_scaling_cap_exceeded", "burn_in_steps": ...}
    """
    chain = DipoleChain(L, density, rng)
    ever_flipped = np.zeros(L, dtype=bool)

    patience = patience_multiplier * L
    max_steps = max_steps_multiplier * patience

    steps_since_growth = 0
    steps_taken = 0
    last_growth_step = 0
    reached_T0 = False

    while steps_taken < max_steps:
        flipped_sites = chain.step()
        if flipped_sites is None:
            return {"status": "jammed", "burn_in_steps": steps_taken,
                    "ever_flipped": ever_flipped}
        steps_taken += 1

        grew = not ever_flipped[flipped_sites].all()
        ever_flipped[flipped_sites] = True

        if grew:
            steps_since_growth = 0
            last_growth_step = steps_taken
        else:
            steps_since_growth += 1
            if steps_since_growth >= patience:
                reached_T0 = True
                break

    if not reached_T0:
        return {"status": "t0_not_reached", "burn_in_steps": steps_taken}

    T0 = steps_taken
    G = last_growth_step
    W = W_multiplier * L

    trigger_window = None
    k = 0
    while k < max_extra_windows:
        flipped_in_window = np.zeros(L, dtype=bool)
        grew_in_window = False
        for _ in range(W):
            flipped_sites = chain.step()
            if flipped_sites is None:
                return {"status": "jammed", "burn_in_steps": T0 + k * W,
                        "ever_flipped": ever_flipped}
            flipped_in_window[flipped_sites] = True
            if not ever_flipped[flipped_sites].all():
                grew_in_window = True
            ever_flipped[flipped_sites] = True
        t_now = T0 + (k + 1) * W
        if grew_in_window:
            G = t_now
        if (t_now - G) >= c_selfscale * G:
            trigger_window = k + 1
            break
        k += 1

    if trigger_window is None:
        return {"status": "self_scaling_cap_exceeded",
                "burn_in_steps": T0 + max_extra_windows * W}

    return {"status": "ready", "chain": chain, "ever_flipped": ever_flipped,
            "T0": T0, "W": W, "burn_in_steps": T0 + trigger_window * W}


def measure_frozen_fraction_rolling(L, density, patience_multiplier,
                                     max_steps_multiplier, W_multiplier,
                                     M, c_selfscale, max_extra_windows, rng):
    """Rolling-window frozen fraction (definition B), burn-in via
    self-scaling patience -- locked in 2026-09-13 after comparing against
    a drift-gated disjoint-window alternative (see burnin_comparison.py):
    both agreed to within ~0.0004 across 10 trials at N=30,000/100,000.
    Self-scaling was chosen as the simpler rule with no stopping-rule-bias
    risk (the trend test below is a reported diagnostic only, never a
    gate -- gating on it would bias the average toward quiet stretches).

    A site counts as frozen at time t if it has not flipped during the
    trailing window [t-W, t] -- unlike measure_frozen_fraction's
    cumulative-since-t=0 definition, a site can re-enter the frozen set
    once it has been quiet for W steps, even if it flipped earlier.

    Burn-in: see _self_scaling_burnin. After burn-in, runs M
    non-overlapping measurement windows and returns their mean plus the
    trend diagnostic.
    """
    burnin = _self_scaling_burnin(L, density, patience_multiplier,
                                   max_steps_multiplier, W_multiplier,
                                   c_selfscale, max_extra_windows, rng)

    if burnin["status"] == "jammed":
        ever_flipped = burnin["ever_flipped"]
        return {"converged": True, "burn_in_steps": burnin["burn_in_steps"],
                "frozen_fraction": 1.0 - ever_flipped.mean(),
                "frozen_fraction_std_across_windows": 0.0,
                "window_fractions": [], "trend_slope": 0.0,
                "trend_pvalue": 1.0, "zero_variance": True,
                "jammed_before_measurement": True}
    if burnin["status"] == "t0_not_reached":
        return {"converged": False, "reason": "T0_not_reached",
                "burn_in_steps": burnin["burn_in_steps"]}
    if burnin["status"] == "self_scaling_cap_exceeded":
        return {"converged": False, "reason": "self_scaling_cap_exceeded",
                "burn_in_steps": burnin["burn_in_steps"]}

    chain = burnin["chain"]
    ever_flipped = burnin["ever_flipped"]
    W = burnin["W"]

    window_fractions = []
    for _ in range(M):
        flipped_in_window = np.zeros(L, dtype=bool)
        jammed = False
        for _ in range(W):
            flipped_sites = chain.step()
            if flipped_sites is None:
                jammed = True
                break
            flipped_in_window[flipped_sites] = True
        window_fractions.append(1.0 - flipped_in_window.mean())
        if jammed:
            break

    window_fractions = np.array(window_fractions)
    trend = _trend_test(window_fractions)

    return {
        "converged": True,
        "burn_in_steps": burnin["burn_in_steps"],
        "frozen_fraction": float(window_fractions.mean()),
        "frozen_fraction_std_across_windows": (
            float(window_fractions.std(ddof=1)) if len(window_fractions) > 1 else 0.0
        ),
        "window_fractions": window_fractions.tolist(),
        "trend_slope": trend["slope"],
        "trend_pvalue": trend["pvalue"],
        "zero_variance": trend["zero_variance"],
    }


def run_ensemble(L, density, patience_multiplier, max_steps_multiplier,
                  target_relative_se, min_samples, batch_size,
                  max_samples_per_N, master_seed):
    """Ensemble-average f_N at fixed L, sampling adaptively until the
    relative standard error drops below target_relative_se or
    max_samples_per_N realizations have been drawn (whichever first).

    Non-converged realizations are discarded from the average and
    counted separately.
    """
    seed_seq = np.random.SeedSequence([master_seed, L])
    samples = []
    n_discarded = 0
    n_drawn = 0

    while n_drawn < max_samples_per_N:
        n_this_batch = min(batch_size, max_samples_per_N - n_drawn)
        for child_seed in seed_seq.spawn(n_this_batch):
            rng = np.random.default_rng(child_seed)
            out = measure_frozen_fraction(L, density, patience_multiplier,
                                           max_steps_multiplier, rng)
            n_drawn += 1
            if out["converged"]:
                samples.append(out["frozen_fraction"])
            else:
                n_discarded += 1

        if len(samples) >= min_samples:
            arr = np.array(samples)
            mean = arr.mean()
            se = arr.std(ddof=1) / np.sqrt(len(arr))
            if mean > 0 and se / mean < target_relative_se:
                break

    arr = np.array(samples)
    return {
        "L": L,
        "master_seed": master_seed,
        "n_samples": len(arr),
        "n_discarded": n_discarded,
        "frozen_fraction_mean": float(arr.mean()) if len(arr) else float("nan"),
        "frozen_fraction_se": (
            float(arr.std(ddof=1) / np.sqrt(len(arr))) if len(arr) > 1 else float("nan")
        ),
        "samples": arr.tolist(),
    }


def run_ensemble_rolling(L, density, patience_multiplier, max_steps_multiplier,
                         W_multiplier, M, c_selfscale, max_extra_windows,
                         target_relative_se, min_samples,
                         batch_size, max_samples_per_N, master_seed):
    """Ensemble-average the rolling-window frozen fraction (definition B,
    method 1 / self-scaling patience burn-in, locked in 2026-09-13) at
    fixed L. Same adaptive-sampling/discard structure as run_ensemble.

    Also aggregates each realization's trend_pvalue so insufficient-burn-in
    realizations can be flagged (not silently averaged in as if stable).
    """
    seed_seq = np.random.SeedSequence([master_seed, L, 1])  # 1 = "rolling" tag, distinct from run_ensemble's [master_seed, L]
    samples = []
    trend_pvalues = []
    n_discarded = 0
    n_drawn = 0

    while n_drawn < max_samples_per_N:
        n_this_batch = min(batch_size, max_samples_per_N - n_drawn)
        for child_seed in seed_seq.spawn(n_this_batch):
            rng = np.random.default_rng(child_seed)
            out = measure_frozen_fraction_rolling(
                L, density, patience_multiplier, max_steps_multiplier,
                W_multiplier, M, c_selfscale, max_extra_windows, rng)
            n_drawn += 1
            if out["converged"]:
                samples.append(out["frozen_fraction"])
                trend_pvalues.append(out["trend_pvalue"])
            else:
                n_discarded += 1

        if len(samples) >= min_samples:
            arr = np.array(samples)
            mean = arr.mean()
            se = arr.std(ddof=1) / np.sqrt(len(arr))
            if mean > 0 and se / mean < target_relative_se:
                break

    arr = np.array(samples)
    trend_pvalues = np.array(trend_pvalues)
    n_significant_trend = int(np.sum(trend_pvalues < 0.05)) if len(trend_pvalues) else 0

    return {
        "L": L,
        "W": W_multiplier * L,
        "M": M,
        "c_selfscale": c_selfscale,
        "master_seed": master_seed,
        "n_samples": len(arr),
        "n_discarded": n_discarded,
        "n_significant_trend": n_significant_trend,
        "frozen_fraction_mean": float(arr.mean()) if len(arr) else float("nan"),
        "frozen_fraction_se": (
            float(arr.std(ddof=1) / np.sqrt(len(arr))) if len(arr) > 1 else float("nan")
        ),
        "samples": arr.tolist(),
        "trend_pvalues": trend_pvalues.tolist(),
    }
