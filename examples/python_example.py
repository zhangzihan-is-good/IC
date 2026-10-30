"""Generate generic signals, fit reference reliability, and save target results."""
import argparse
import json
from pathlib import Path

import numpy as np

from rgic import RGIC, RGICConfig
from rgic.io import save_model, save_results


def make_record(rng, n_time=200):
    """The first signal precedes its noisy delayed counterpart by one sample."""
    source = rng.normal(size=n_time + 1)
    source = np.convolve(source, np.ones(5) / 5, mode="same")
    return np.column_stack((
        source[1:],
        0.7 * source[:-1] + 0.3 * rng.normal(size=n_time),
        rng.normal(size=n_time),
    ))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, default=Path("example_run"),
                        help="empty or new output directory (default: example_run)")
    args = parser.parse_args()
    if args.out.exists() and (not args.out.is_dir() or any(args.out.iterdir())):
        parser.error("output directory must be empty or not yet exist")
    args.out.mkdir(parents=True, exist_ok=True)

    rng = np.random.default_rng(20261030)
    names = ["ROI_A", "ROI_B", "ROI_C"]
    reference = np.stack([make_record(rng) for _ in range(8)])
    target = np.stack([make_record(rng) for _ in range(2)])
    model = RGIC(RGICConfig(lags=(-1, 1))).fit(reference, roi_names=names)
    results = model.transform(target, roi_names=names)

    np.save(args.out / "reference.npy", reference)
    np.save(args.out / "target.npy", target)
    (args.out / "labels.json").write_text(json.dumps(names), encoding="utf-8")
    save_model(model, args.out / "model.npz")
    save_results(results, args.out / "results.npz")
    print("Reference reliability R:", model.reliability_)
    print("Connectivity matrix for the first target recording:\n", results[0].matrix("ic"))
    print("Lag matrix for the first target recording:\n", results[0].matrix("lag"))
    print("Saved inputs, labels, model, and results to:", args.out.resolve())


if __name__ == "__main__":
    main()
