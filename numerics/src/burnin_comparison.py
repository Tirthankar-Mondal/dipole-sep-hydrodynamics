"""Compare two burn-in criteria for the rolling-window frozen fraction
(H1, definition B), on identical trajectories (same rng, same sequence
of moves) rather than just identical seeds -- both methods read off
their estimate from the same underlying random process, so any
disagreement is attributable to the stopping rule, not to sampling luck.

Method 1 (self-scaling patience): stop the initial burn-in, then keep
extending until (t - G) >= c_selfscale * G, where G is the step index of
the most recent first-time flip (tracked at window granularity). No
adaptive gate beyond this -- the trend test is a reported diagnostic
only, never used to decide when to stop.

Method 2 (drift-gated, disjoint probe/measure windows): after the same
initial burn-in, test consecutive batches of `M` probe windows for a
significant linear trend; discard a batch and probe again if significant;
once a batch is not significant, discard those probe windows and measure
on the next M fresh windows. Kept disjoint from the probe windows
specifically to avoid stopping-rule bias (the average must not be taken
over windows that were selected for looking flat).

Both use W = W_multiplier * L windows and average over M windows for
the final frozen-fraction estimate.
"""

import numpy as np
from scipy import stats

from dipole_chain import DipoleChain


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


def compare_burnin_methods(L, density, patience_multiplier,
                            max_steps_multiplier, W_multiplier, M,
                            c_selfscale, max_extra_windows, trend_alpha,
                            rng):
    chain = DipoleChain(L, density, rng)
    ever_flipped = np.zeros(L, dtype=bool)

    patience = patience_multiplier * L
    max_steps = max_steps_multiplier * patience
    W = W_multiplier * L

    # --- initial (old, fixed) burn-in: shared starting point T0 for both methods ---
    steps_since_growth = 0
    steps_taken = 0
    last_growth_step = 0
    reached_T0 = False

    while steps_taken < max_steps:
        flipped_sites = chain.step()
        if flipped_sites is None:
            return {"converged": False, "reason": "jammed_before_T0"}
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
        return {"converged": False, "reason": "T0_not_reached", "steps_taken": steps_taken}

    T0 = steps_taken
    G = last_growth_step

    # --- continuous window stream from T0 onward, shared by both methods ---
    window_fractions = []
    method1_trigger_window = None   # first window index k where self-scaling criterion holds
    method2_measure_start = None    # first window index j+1 after a clean disjoint probe batch
    probe_batch_start = 0
    jammed = False

    k = 0
    while len(window_fractions) < max_extra_windows:
        flipped_in_window = np.zeros(L, dtype=bool)
        grew_in_window = False
        for _ in range(W):
            flipped_sites = chain.step()
            if flipped_sites is None:
                jammed = True
                break
            flipped_in_window[flipped_sites] = True
            if not ever_flipped[flipped_sites].all():
                grew_in_window = True
            ever_flipped[flipped_sites] = True
        window_fractions.append(1.0 - flipped_in_window.mean())
        t_now = T0 + (k + 1) * W
        if grew_in_window:
            G = t_now

        # Method 1: self-scaling patience (no gate, just a stopping condition)
        if method1_trigger_window is None and (t_now - G) >= c_selfscale * G:
            method1_trigger_window = k + 1

        # Method 2: drift-gated disjoint probe/measure
        if method2_measure_start is None and (k + 1 - probe_batch_start) == M:
            probe_batch = window_fractions[probe_batch_start:k + 1]
            probe_trend = _trend_test(probe_batch)
            if probe_trend["pvalue"] >= trend_alpha:
                method2_measure_start = k + 1
            else:
                probe_batch_start = k + 1

        need1 = method1_trigger_window is not None and len(window_fractions) >= method1_trigger_window + M
        need2 = method2_measure_start is not None and len(window_fractions) >= method2_measure_start + M
        if need1 and need2:
            break
        if jammed:
            break
        k += 1

    result = {"converged": True, "T0": T0, "jammed_in_measurement": jammed}

    if method1_trigger_window is not None and len(window_fractions) >= method1_trigger_window + M:
        m1_windows = window_fractions[method1_trigger_window:method1_trigger_window + M]
        m1_trend = _trend_test(m1_windows)
        result["method1"] = {
            "converged": True,
            "burn_in_steps": T0 + method1_trigger_window * W,
            "frozen_fraction": float(np.mean(m1_windows)),
            "std_across_windows": float(np.std(m1_windows, ddof=1)),
            "sqrtN_std": float(np.sqrt(L) * np.std(m1_windows, ddof=1)),
            "trend_pvalue": m1_trend["pvalue"],
            "zero_variance": m1_trend["zero_variance"],
        }
    else:
        result["method1"] = {"converged": False, "reason": "cap_exceeded"}

    if method2_measure_start is not None and len(window_fractions) >= method2_measure_start + M:
        m2_windows = window_fractions[method2_measure_start:method2_measure_start + M]
        m2_trend = _trend_test(m2_windows)
        result["method2"] = {
            "converged": True,
            "burn_in_steps": T0 + method2_measure_start * W,
            "frozen_fraction": float(np.mean(m2_windows)),
            "std_across_windows": float(np.std(m2_windows, ddof=1)),
            "sqrtN_std": float(np.sqrt(L) * np.std(m2_windows, ddof=1)),
            "trend_pvalue": m2_trend["pvalue"],
            "zero_variance": m2_trend["zero_variance"],
            "n_probe_batches_discarded": probe_batch_start // M,
        }
    else:
        result["method2"] = {"converged": False, "reason": "cap_exceeded"}

    return result
