# Chapter 1

## Introduction

`figio` is Python application that uses declarative `yml` input file
recipies to produce high quality [*MATPLOTLIB*](https://matplotlib.org)
and $\LaTeX$ figures.

The following figure types are currently supported:
* `(x, y)` data, and
* histogram data.

## Installation

Use of a [virtual environment](https://docs.python.org/3/library/venv.html)
is recommended but not necessary.

```sh
python -m venv .venv

# Activate the venv with one of the following:
source .venv/bin/activate       # for bash shell
source .venv/bin/activate.csh   # for c shell
source .venv/bin/activate.fish  # for fish shell
.\.venv\Scripts\activate        # for powershell
```

Install `figio` from the [Python Package Index (PyPI)](https://pypi.org/project/figio/).

```sh
pip install figio
```

## Getting Started

Tabular data is used as the data source of `figio` figures.  Let's get started
with a tabular data for a sine and a cosine wave.  Tabular data typically
occurs in `csv` (comma separate value) file format.  The file [data.csv](data.csv)
contains colums for `time (s),sin(t),cos(2t)`.

```sh
<!-- cmdrun more data.csv -->
```

To plot this data, we create a `yml` input file called
[`recipe.yml`](recipe.yml).

```yml
<!-- cmdrun more recipe.yml -->
```

Run `figio` on the input file to produce the figure:

```sh
figio recipe.yml

<!-- cmdrun figio recipe.yml -->
```

The following figure appears:

![recipe](recipe.svg)

Congratulations!  You just make your first `figio` figure.
