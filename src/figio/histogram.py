"""The histogram type, constructor, and methods."""

from typing import NamedTuple
from pathlib import Path

import numpy as np
from schema import Schema, And, Or, Use, Optional, SchemaError

# Define the schema for plot_kwargs
plot_kwargs_schema = Schema(
    {
        Optional("color"): str,
        Optional("linewidth"): And(
            Or(Use(float), Use(int)),  # must be a float or an int
            lambda n: n > 0,  # must be positive
        ),  # Ensure linewidth is a positive float
    },
    ignore_extra_keys=True,
)


class Histogram(NamedTuple):
    """The histogram type."""

    # bins: int
    # density: bool
    folder: Path
    file: Path
    data: np.ndarray
    # histtype: str
    # orientation: str
    plot_kwargs: dict
    # rwidth: float
    skip_rows: int
    # stacked: bool
    # x: list[float]
    # y: list[float]
    ycolumn: int
    # yerr: list[float] | None


def validate_plot_kwargs(din: dict) -> bool:
    """Determines if the input dictionary is a valid plot_kwargs schema."""

    # TODO: DRY out code, repeated here at in figure.py
    try:
        validated_data = plot_kwargs_schema.validate(din)
        print("Valid: Validated data:", validated_data)
        return True
    except SchemaError as e:
        print("Error: Validation error:", e)
        return False


def new(db: dict) -> Histogram:
    """Given a dictionary, validates the data from the
    dictionary, and if valid, creates a Histogram."""

    if "plot_kwargs" in db:
        validate_plot_kwargs(db["plot_kwargs"])

    folder = Path(db["folder"]).expanduser()
    file = Path(db["folder"]).expanduser().joinpath(db["file"])
    assert folder.is_dir(), f"Folder does not exist: {folder}"
    assert file.is_file, f"File does not exist: {file}"

    # TODO: validate the entire schema, not just the kwargs below
    # then the next two checks are obsolete
    skip_rows = db["skip_rows"]
    ycolumn = db["ycolumn"]
    assert skip_rows >= 0, f"skip_rows must be >= 0: {skip_rows}"
    assert ycolumn >= 0, f"ycolumn must be >= 0: {ycolumn}"

    # load the data into the Histogram
    try:
        data = np.genfromtxt(
            str(file),
            dtype="float",
            delimiter=",",
            skip_header=db["skip_rows"],
            skip_footer=0,
            usecols=(db["ycolumn"]),
        )
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    except IOError as e:
        print(f"I/O error: {e}")
    except TypeError as e:
        print(f"Type error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    hh = Histogram(
        folder=Path(db["folder"]).expanduser(),
        file=Path(db["folder"]).expanduser().joinpath(db["file"]),
        data=data,
        plot_kwargs=db["plot_kwargs"],
        skip_rows=skip_rows,
        ycolumn=ycolumn,
    )

    # validate plot_kwargs

    return hh
