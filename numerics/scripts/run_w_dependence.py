"""Map f_B(W), the W-dependence of the rolling-window frozen fraction.

Usage:
    python scripts/run_w_dependence.py config/w_dependence.yaml

All W values come from the same trajectories (see numerics/src/w_dependence.py),
so the W-dependence is measured without realization noise.

Writes, under numerics/data/raw/w_dependence_<tag>_<timestamp>/:
    parameters.json                  - the config used, plus tag/timestamp
    L<value>_W<mult>_samples.npy     - per-realization f_B at that (L, W)
    summary.json                     - per (L, W): mean, SE, n_samples
"""

import json
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from w_dependence import run_ensemble_f_of_W  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _job(args):
    L, cfg = args
    return run_ensemble_f_of_W(
        L=L,
        density=cfg["model"]["density"],
        patience_multiplier=cfg["patience_multiplier"],
        max_steps_multiplier=cfg["max_steps_multiplier"],
        W_multipliers=cfg["W_multipliers"],
        c_selfscale=cfg["c_selfscale"],
        max_extra_windows=cfg["max_extra_windows"],
        n_samples=cfg["n_samples_per_L"][str(L)],
        master_seed=cfg["master_seed"],
    )


def main(config_path):
    config_path = Path(config_path)
    with open(config_path) as f:
        config = yaml.safe_load(f)

    tag = config_path.stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = REPO_ROOT / "numerics" / "data" / "raw" / f"w_dependence_{tag}_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=False)

    with open(out_dir / "parameters.json", "w") as f:
        json.dump({"config_path": str(config_path), "config": config,
                   "timestamp_utc": timestamp}, f, indent=2)

    jobs = [(L, config) for L in config["L_values"]]
    with ProcessPoolExecutor(max_workers=config.get("workers", 8)) as ex:
        results = list(ex.map(_job, jobs))

    summary = []
    for res in results:
        for row in res["rows"]:
            np.save(out_dir / f"L{row['L']}_W{row['W_multiplier']}_samples.npy",
                    np.array(row["samples"]))
            r = {k: v for k, v in row.items() if k != "samples"}
            r["n_discarded"] = res["n_discarded"]
            r["master_seed"] = res["master_seed"]
            summary.append(r)

    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nWrote results to {out_dir}")
    for row in summary:
        print(f"  L={row['L']:>5}  W={row['W_multiplier']:>4}L  "
              f"f_B={row['f_B_mean']:.4f} +- {row['f_B_se']:.4f}  (n={row['n_samples']})")


if __name__ == "__main__":
    main(sys.argv[1])
