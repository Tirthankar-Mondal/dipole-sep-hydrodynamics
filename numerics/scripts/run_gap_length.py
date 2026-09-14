"""Measure the active-region (gap) length distribution vs L for H2.

Usage:
    python scripts/run_gap_length.py config/gap_length_test.yaml

Single post-burn-in snapshot per realization (rolling-window definition
B, same self-scaling burn-in as H1, locked in 2026-09-13). Zero-length
gaps are discarded from the pooled distribution (researcher instruction,
2026-09-14) -- see HYPOTHESES.md, H2.

Writes, under numerics/data/raw/gap_length_<tag>_<timestamp>/:
    parameters.json      - the config used, plus the resolved tag/timestamp
    L<value>_gaps.npy    - pooled (nonzero) gap lengths, one file per L
    summary.json         - per-L n_realizations, n_pooled_gaps, mean/std,
                            zero-gap rate, discard/jam counts
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import yaml
from tqdm import tqdm

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))
from gap_length import run_ensemble_gap_lengths  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent.parent


def main(config_path):
    config_path = Path(config_path)
    with open(config_path) as f:
        config = yaml.safe_load(f)

    tag = config_path.stem
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = REPO_ROOT / "numerics" / "data" / "raw" / f"gap_length_{tag}_{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=False)

    with open(out_dir / "parameters.json", "w") as f:
        json.dump({"config_path": str(config_path), "config": config,
                    "timestamp_utc": timestamp}, f, indent=2)

    summary = []
    for L in tqdm(config["L_values"], desc="L"):
        result = run_ensemble_gap_lengths(
            L=L,
            density=config["model"]["density"],
            patience_multiplier=config["patience_multiplier"],
            max_steps_multiplier=config["max_steps_multiplier"],
            W_multiplier=config["rolling"]["W_multiplier"],
            c_selfscale=config["rolling"]["c_selfscale"],
            max_extra_windows=config["rolling"]["max_extra_windows"],
            target_relative_se=config["ensemble"]["target_relative_se"],
            min_samples=config["ensemble"]["min_samples"],
            batch_size=config["ensemble"]["batch_size"],
            max_samples_per_N=config["ensemble"]["max_samples_per_N"],
            master_seed=config["master_seed"],
        )
        np.save(out_dir / f"L{L}_gaps.npy", np.array(result["gap_lengths"], dtype=np.int64))
        summary.append({k: v for k, v in result.items() if k != "gap_lengths"})

    with open(out_dir / "summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(f"\nWrote results to {out_dir}")
    for row in summary:
        print(f"  L={row['L']:>6}  gap_mean={row['gap_length_mean']:.3f}"
              f" +- (std {row['gap_length_std']:.3f})"
              f"  n_pooled_gaps={row['n_pooled_gaps']}"
              f"  (n_realizations={row['n_realizations']},"
              f" discarded={row['n_discarded']}, jammed={row['n_jammed']},"
              f" zero_gap_rate={row['zero_gap_rate']:.3f})")


if __name__ == "__main__":
    main(sys.argv[1])
