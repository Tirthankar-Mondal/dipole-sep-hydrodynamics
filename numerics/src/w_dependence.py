"""W-dependence of the rolling-window frozen fraction f_B(W).

Definition B makes W part of the *observable*, not just the stopping rule:
f_B(W) is the fraction of sites that have not flipped during a trailing
window of W steps, so f_B is non-increasing in W by construction (the
W'-window frozen set is a subset of the W-window one for W' > W). Every
production number quoted for H1 is therefore f_B at one particular W (5L
or 10L), and the W -> infinity limit -- the static/Krylov frozen fraction
that H1 actually defines -- has never been mapped out.

This module measures the whole curve f_B(W) from a single trajectory per
realization: after the standard self-scaling burn-in, run W_max steps while
recording each site's last-flip time, then read off every W <= W_max from
the same run. All W values are therefore perfectly paired (identical
trajectories), so differences between them carry no realization noise.

Added 2026-09-14.
"""

import numpy as np

from frozen_fraction import _self_scaling_burnin


def measure_f_of_W(L, density, patience_multiplier, max_steps_multiplier,
                   W_multipliers, c_selfscale, max_extra_windows, rng):
    """Return f_B(W) for every W = m*L with m in W_multipliers, one trajectory.

    Burn-in uses the production criterion (self-scaling patience, locked in
    2026-09-13). W_multiplier passed to the burn-in is the smallest requested
    multiplier, so the burn-in itself is identical to the production setup.
    """
    W_multipliers = sorted(W_multipliers)
    burnin = _self_scaling_burnin(L, density, patience_multiplier,
                                  max_steps_multiplier, W_multipliers[0],
                                  c_selfscale, max_extra_windows, rng)
    if burnin["status"] != "ready":
        return {"converged": False, "reason": burnin["status"],
                "burn_in_steps": burnin["burn_in_steps"]}

    chain = burnin["chain"]
    W_max = W_multipliers[-1] * L

    # last_flip[i] = step index (1-based within this span) of site i's most
    # recent flip; 0 means "never flipped during the span".
    last_flip = np.zeros(L, dtype=np.int64)
    for t in range(1, W_max + 1):
        flipped = chain.step()
        if flipped is None:
            return {"converged": False, "reason": "jammed_during_span",
                    "burn_in_steps": burnin["burn_in_steps"]}
        last_flip[flipped] = t

    # Site is frozen at scale W iff its last flip lies outside the trailing
    # window (W_max - W, W_max]; never-flipped sites (last_flip == 0) qualify
    # for every W.
    out = {}
    for m in W_multipliers:
        cutoff = W_max - m * L
        out[m] = float(np.mean(last_flip <= cutoff))

    return {"converged": True, "burn_in_steps": burnin["burn_in_steps"],
            "f_of_W": out, "W_max_steps": W_max}


def run_ensemble_f_of_W(L, density, patience_multiplier, max_steps_multiplier,
                        W_multipliers, c_selfscale, max_extra_windows,
                        n_samples, master_seed):
    """Ensemble-average f_B(W) at fixed L over n_samples trajectories."""
    seed_seq = np.random.SeedSequence([master_seed, L, 4])  # 4 = "W-scan" tag
    per_W = {m: [] for m in sorted(W_multipliers)}
    n_discarded = 0

    for child in seed_seq.spawn(n_samples):
        rng = np.random.default_rng(child)
        out = measure_f_of_W(L, density, patience_multiplier,
                             max_steps_multiplier, W_multipliers,
                             c_selfscale, max_extra_windows, rng)
        if not out["converged"]:
            n_discarded += 1
            continue
        for m, v in out["f_of_W"].items():
            per_W[m].append(v)

    rows = []
    for m in sorted(per_W):
        arr = np.array(per_W[m])
        rows.append({
            "L": L,
            "W_multiplier": m,
            "W": m * L,
            "n_samples": len(arr),
            "f_B_mean": float(arr.mean()) if len(arr) else float("nan"),
            "f_B_se": (float(arr.std(ddof=1) / np.sqrt(len(arr)))
                       if len(arr) > 1 else float("nan")),
            "samples": arr.tolist(),
        })
    return {"L": L, "n_discarded": n_discarded, "master_seed": master_seed,
            "rows": rows}
