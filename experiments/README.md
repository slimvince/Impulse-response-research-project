# Experiments

Each experiment gets a new immutable directory named `E###`, for example `E001/`.

Expected contents:

```text
E001/
  README.md
  manifest.json
  config.json
  results/
```

The experiment README must state the question, status, Git commit, corpus/manifests, analysis version, interpretation, limitations, and next action. Do not place copyrighted audio in this directory unless redistribution is explicitly authorized. Generated result files may be ignored according to the repository policy, but their provenance and location must be documented.

See [docs/experiments.md](../docs/experiments.md) for the registry and contract.
