"""Measure f_N (frozen-site fraction) vs N for H1.

Usage:
    python scripts/run_frozen_fraction.py config/test.yaml
    python scripts/run_frozen_fraction.py config/production_intermediate.yaml
    python scripts/run_frozen_fraction.py config/production_large_scale.yaml

Set `estimator: cumulative` (definition A) or `estimator: rolling`
(definition B, method 1 / self-scaling patience, locked in 2026-09-14)
in the config to select which measurement function to use. Defaults to
`cumulative` if omitted, for backward compatibility with old configs.

Writes, under numerics/data/raw/frozen_fraction_<tag>_<timestamp>/:
    parameters.json         - the config used, plus the resolved tag/timestamp
    L<value>_samples.npy    - per-realization frozen fractions, one file per N
    summary.json            - per-N mean, SE, n_samples, n_discarded
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from frozen_fraction import run_ensemble, run_ensemble_rolling  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main(config_path):
    config_path = Path(config_path)
    with open(config_path) as f:
        config = yaml.safe_load(f)

    estimator = config.get("estimator", "cumulative")

    tag = config_path.stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = REPO_ROOT / "numerics" / "data" / "raw" / f"frozen_fraction_{tag}_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=False)

    with open(out_dir / "parameters.json", "w") as f:
        json.dump({"config_path": str(config_path), "config": config,
                    "timestamp_utc": timestamp}, f, indent=2)

    summary = []
    for L in tqdm(config["N_values"], desc="N"):
        if estimator == "rolling":
            result = run_ensemble_rolling(
                L=L,
                density=config["model"]["density"],
                patience_multiplier=config["patience_multiplier"],
                max_steps_multiplier=config["max_steps_multiplier"],
                W_multiplier=config["rolling"]["W_multiplier"],
                M=config["rolling"]["M"],
                c_selfscale=config["rolling"]["c_selfscale"],
                max_extra_windows=config["rolling"]["max_extra_windows"],
                target_relative_se=config["ensemble"]["target_relative_se"],
                min_samples=config["ensemble"]["min_samples"],
                batch_size=config["ensemble"]["batch_size"],
                max_samples_per_N=config["ensemble"]["max_samples_per_N"],
                master_seed=config["master_seed"],
            )
        else:
            result = run_ensemble(
                L=L,
                density=config["model"]["density"],
                patience_multiplier=config["patience_multiplier"],
                max_steps_multiplier=config["max_steps_multiplier"],
                target_relative_se=config["ensemble"]["target_relative_se"],
                min_samples=config["ensemble"]["min_samples"],
                batch_size=config["ensemble"]["batch_size"],
                max_samples_per_N=config["ensemble"]["max_samples_per_N"],
                master_seed=config["master_seed"],
            )
        np.save(out_dir / f"L{L}_samples.npy", np.array(result["samples"]))
        summary.append({k: v for k, v in result.items() if k != "samples"})

    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nWrote results to {out_dir}")
    for row in summary:
        print(f"  L={row['L']:>5}  f_N={row['frozen_fraction_mean']:.4f}"
              f" +- {row['frozen_fraction_se']:.4f}"
              f"  (n={row['n_samples']}, discarded={row['n_discarded']})")


if __name__ == "__main__":
    main(sys.argv[1])
