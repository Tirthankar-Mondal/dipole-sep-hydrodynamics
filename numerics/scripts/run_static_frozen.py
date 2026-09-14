"""Exact static (Krylov-sector) frozen fraction vs L, by brute-force BFS.

Usage:
    python scripts/run_static_frozen.py config/static_frozen.yaml

Measures the literal H1 order parameter (constant-across-the-whole-reachable-set)
rather than a dynamical proxy -- see numerics/src/static_frozen.py. Small L only.

Writes, under numerics/data/raw/static_frozen_<tag>_<timestamp>/:
    parameters.json        - the config used, plus resolved tag/timestamp
    L<value>_samples.npy   - per-realization static frozen fractions
    summary.json           - per-L mean, SE, sector-size statistics
"""

import json
import sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from static_frozen import measure_static_frozen  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def _job(args):
    L, n, seed, cap = args
    return measure_static_frozen(L, n, seed, max_sector=cap)


def main(config_path):
    config_path = Path(config_path)
    with open(config_path) as f:
        config = yaml.safe_load(f)

    tag = config_path.stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = REPO_ROOT / "numerics" / "data" / "raw" / f"static_frozen_{tag}_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=False)

    with open(out_dir / "parameters.json", "w") as f:
        json.dump({"config_path": str(config_path), "config": config,
                   "timestamp_utc": timestamp}, f, indent=2)

    n_per_L = config["n_samples_per_L"]
    jobs = [(L, n_per_L[str(L)] if str(L) in n_per_L else n_per_L["default"],
             config["master_seed"], config["max_sector"])
            for L in config["L_values"]]

    with ProcessPoolExecutor(max_workers=config.get("workers", 8)) as ex:
        results = list(ex.map(_job, jobs))

    summary = []
    for r in results:
        np.save(out_dir / f"L{r['L']}_samples.npy", np.array(r["samples"]))
        summary.append({k: v for k, v in r.items()
                        if k not in ("samples", "sector_sizes")})

    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nWrote results to {out_dir}")
    for row in summary:
        print(f"  L={row['L']:>3}  f_static={row['f_static_mean']:.4f}"
              f" +- {row['f_static_se']:.4f}  (n={row['n_samples']},"
              f" sector med={row['sector_size_median']:.0f}"
              f" max={row['sector_size_max']}, over_cap={row['n_over_cap']})")


if __name__ == "__main__":
    main(sys.argv[1])
