# Contributing to bnch

Thank you for your interest in contributing to the benchmark harness. We are committed to maintaining rigorous, reproducible, and honest benchmarks.

## Pull Request Process

1. **Fork and Branch:** Fork the repository and create a descriptive branch name.
2. **Ensure Code Quality:** Follow the existing Python code style. All changes must pass `python3 tools/validate_manifests.py`, `python3 -m unittest tests.test_run`, and a smoke run (`python3 run.py --runs 1 --min-runs 1 --warmup 0`).
3. **Sign Your Commits:** We use the DCO. Add `Signed-off-by` via `git commit -s`.
4. **Submit PR:** Open a pull request against the `main` branch detailing the intent and testing strategy.

*Note: NINJI retains the right to reject contributions that do not align with our benchmark integrity standards or architectural directives.*
