# Introduction

`figio` is a Python application that uses declarative [YAML](https://yaml.org)
input file recipes to produce high-quality [*matplotlib*](https://matplotlib.org)
and $\LaTeX$ figures.

The following figure types are currently supported:
* `(x, y)` data (or, equivalently, time series data), and
* histogram data.

## Installation

We support two types of installation: client or developer.  The **client installation** is recommended for users who will use the module but are not
interested in modifying the module's source code.

In contrast, the [**developer installation**](./development.md#developer-configuration) is recommended for users who wish to modify the module's source code.

### Client Installation

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

Tabular data is used as the data source for `figio` figures.
Let's get started with a tabular data for the inflation rate,
measured on the first day of each year.
The tabular data, [inflation.csv](inflation.csv), comes from the
[Federal Reserve Bank of St. Louis](https://fred.stlouisfed.org/series/FPCPITOTLZGUSA).

```sh
<!-- cmdrun more inflation.csv -->
```

To plot this data, we create a `yml` input file called
[`inflation.yml`](inflation.yml).

```yml
<!-- cmdrun more inflation.yml -->
```

Run `figio` on the input file to produce the figure:

```sh
figio inflation.yml

<!-- cmdrun figio inflation.yml -->
```

The following figure appears:

![](inflation.svg)

Congratulations!  You just made your first `figio` figure.
