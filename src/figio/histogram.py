"""The histogram type."""

from typing import NamedTuple

from pathlib import Path


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


def histogram_new(db: dict) -> Histogram:
    """Given a dictionary, creates a Histogram."""
    hh = Histogram(
        folder=Path(db["folder"]).expanduser(),
        file=Path(db["folder"]).expanduser().joinpath(db["file"]),
        plot_kwargs=db["plot_kwargs"],
        skip_rows=db["skip_rows"],
        ycolumn=db["ycolumn"],
    )

    assert hh.folder.is_dir(), f"Folder does not exist: {hh.folder}"
    assert hh.file.is_file, f"File does not exist: {hh.file}"
    # TODO: validate plot_kwargs
    assert hh.skip_rows >= 0, f"skip_rows must be >= 0: {hh.skip_rows}"
    assert hh.ycolumn >= 0, f"ycolumn must be >= 0: {hh.ycolumn}"

    # TODO: load the data into the Historgram

    return hh


def histogram_view(hh: Histogram):
    """Given a Histogram, creates a view."""
    # TODO:
    # reference ~/autotwin/automesh/book/analysis/sphere_with_shells/histogram.py
    pass
