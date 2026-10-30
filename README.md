# RGIC: Reliability-Gated Information Connectivity

Version `0.1.0a3` is a minimal algorithm implementation for preprocessed regional time series. It estimates reliability from reference recordings, then uses that fixed reliability to combine zero-lag and lagged correlations in target recordings.

## Install from GitHub

Requirements: Python ≥ 3.10, NumPy ≥ 1.23, and a local Git client for the commands below. The source is distributed through this GitHub repository.

```bash
python -m pip install "git+https://github.com/zhangzihan-is-good/IC.git"
rgic --help
rgic fit --help
```

To obtain the examples and tests as well, clone the source and install it locally:

```bash
git clone https://github.com/zhangzihan-is-good/IC.git
cd IC
python -m pip install .
python examples/python_example.py --out example_run
```

The example creates generic synthetic signals and writes `reference.npy`, `target.npy`, `labels.json`, `model.npz`, and `results.npz`. The output directory must be empty or not yet exist.

## Command-line workflow

```bash
rgic fit --input example_run/reference.npy --out example_run/cli_model.npz --roi-labels example_run/labels.json
rgic transform --input example_run/target.npy --model example_run/cli_model.npz --out example_run/cli_results.npz --roi-labels example_run/labels.json
rgic inspect example_run/cli_results.npz
rgic manual
```

For custom parameters, add `--config examples/sample_config.json` to `fit`. Use `--help`, `--need`, or `---need` for command help, and `rgic manual` for the complete user guide. If `rgic` is not on your executable path, replace it with `python -m rgic`.

## Python API

```python
from rgic import RGIC, RGICConfig

model = RGIC(RGICConfig(lags=(-1, 1))).fit(reference, roi_names=names)
results = model.transform(target, roi_names=names)
print(results[0].matrix("ic"))
print(results[0].matrix("strength"))
```

A recording has shape `(time_points, regions)`. Equal-length recordings can be stacked as `(recordings, time_points, regions)`; Python also accepts a list of recordings with different lengths. `transform` always returns a list and leaves reference reliability unchanged.

Read the [user guide](docs/user_guide.md) for parameters, file formats, and lag conventions, or the [design notes](docs/design_v0.1.md) for implementation boundaries. Run the included checks from the source directory:

```bash
python -m unittest discover -s tests -v
```

## AI assistance and human responsibility

Development used AI-assisted coding (vibe coding). The repository author reports human review and validation of the implementation. Automated checks cover mathematical properties, reference-state isolation, input validation, and file round trips. The author remains responsible for the code, its scientific interpretation, and release decisions.
