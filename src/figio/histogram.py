"""The histogram type, its constructor, and methods."""

from typing import NamedTuple
from pathlib import Path

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


def valid_plot_kwargs(kw: dict) -> bool:
    """Validates whether or not the supplied kwargs are able to
    be processed here."""
    try:
        validated_data = plot_kwargs_schema.validate(kw)
        print("Valid: Validated data:", validated_data)
        return True
    except SchemaError as e:
        print("Error: Validation error:", e)
        return False


def new(db: dict) -> Histogram:
    """Given a dictionary, validates the data from the
    dictionary, and if valid, creates a Histogram."""
    hh = Histogram(
        folder=Path(db["folder"]).expanduser(),
        file=Path(db["folder"]).expanduser().joinpath(db["file"]),
        plot_kwargs=db["plot_kwargs"],
        skip_rows=db["skip_rows"],
        ycolumn=db["ycolumn"],
    )

    assert hh.folder.is_dir(), f"Folder does not exist: {hh.folder}"
    assert hh.file.is_file, f"File does not exist: {hh.file}"
    # validate plot_kwargs
    valid_plot_kwargs(hh.plot_kwargs)

    assert hh.skip_rows >= 0, f"skip_rows must be >= 0: {hh.skip_rows}"
    assert hh.ycolumn >= 0, f"ycolumn must be >= 0: {hh.ycolumn}"

    # TODO: load the data into the Histogram

    return hh


def histogram_view(hh: Histogram):
    """Given a Histogram, creates a view."""
    # TODO:
    # reference ~/autotwin/automesh/book/analysis/sphere_with_shells/histogram.py
    pass
