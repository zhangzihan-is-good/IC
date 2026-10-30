# RGIC v0.1 Design

Version `0.1.0a3`. The goal is a small implementation with an explicit computational interface.

## Core workflow

1. Supply preprocessed regional time series.
2. `fit(reference)` searches lagged correlations and saves edge-level `F`, `L`, `S`, and `R=FLS`.
3. `transform(target)` freezes reference reliability and computes target gain, cost, candidate, gate, and `IC`.
4. Return one result per target recording; edge vectors can be expanded to matrices.

## Module boundaries

| Module | Responsibility |
|---|---|
| `core.py` | Configuration validation, overlapping correlations, reference reliability, gated fusion, matrix output |
| `io.py` | Array inputs, region labels, model/result NPZ files, metadata |
| `cli.py` | `fit`, `transform`, `inspect`, `manual`, and command help |
| `examples/` | Generic synthetic signals and a minimal configuration |
| `tests/` | Mathematical properties, state isolation, input validation, file round trips |

## Conventions

- Lags are paired positive/negative integer offsets. Seconds mode converts cost using TR; reliability still counts exact sample offsets.
- Reference and target columns share the same region order, verified when labels are supplied.
- Normalization includes every undirected edge in the current recording, including zero-evidence edges.
- Connectivity matrices are symmetric; lag matrices are antisymmetric. Opposite-direction peak ties retain an ambiguity flag.
- Configuration is fixed after fitting; target recordings never update reference reliability.
- Preprocessing, resampling, and parameter selection remain external to the algorithm.
