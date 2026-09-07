# Lab 3: Deep Learning

The lab notebook is `deep_learning.ipynb`. You can run it in Google Colab or locally with `uv`.

## Option A: Google Colab

Use Colab if you do not have a local Python setup.

1. Open `deep_learning.ipynb` in Google Colab.
2. Run the first code cell. It is commented out by default and installs the pinned dependencies.
3. Run the remaining cells from top to bottom.

Nothing else needs to be installed. A GPU is optional and not needed; training on CPU takes a few minutes.

Colab resets its runtime after inactivity. If you take a long break, reconnect and run the notebook again from the top.

## Option B: Local setup with uv

Install [uv](https://docs.astral.sh/uv/) and use Python 3.11 or 3.12. The project requires Python `>=3.11,<3.13`.

From this directory, run:

```bash
uv sync
uv run jupyter lab
```

`uv` creates the virtual environment and installs exactly the versions recorded in `uv.lock`. On Linux, the lockfile uses CPU-only PyTorch wheels from the `pytorch-cpu` index to keep the download small.

## What you hand in

Answer the two reflection questions directly in the provided Markdown cells, then submit your completed `deep_learning.ipynb` file.

## Troubleshooting

If a cell raises `NotImplementedError`, it is a task cell waiting for you to complete it, not a bug.
