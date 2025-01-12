"""The figure type, constructor, and methods."""

from typing import NamedTuple
from pathlib import Path

import matplotlib.pyplot as plt
from schema import Schema, And, Optional, SchemaError

from figio import histogram

# Define the schema for the figure
figure_schema = Schema(
    {
        Optional("dpi", default=100): int,
        "folder": And(str, len),  # non-empty string
        "file": And(str, len),  # non-empty string
        Optional("size", default=[8.0, 6.0]): list[float | int],
        Optional("title", default=""): str,
        Optional("xlabel", default=""): str,
        Optional("ylabel", default=""): str,
    },
    ignore_extra_keys=True,
)


class Figure(NamedTuple):
    """The figure type."""

    dpi: int
    folder: Path
    file: Path
    models: list[str]
    size: list[float | int]
    title: str
    xlabel: str
    ylabel: str


def validate_schema(din: dict) -> bool:
    """Determines if the input dictionary is a valid Figure schema."""

    # TODO: DRY out code, repeated here at in histogram.py
    try:
        validated_data = figure_schema.validate(din)
        print("Valid: Validated data:", validated_data)
    except SchemaError as e:
        print("Error: Validation error:", e)

    return True


def new(db: dict) -> Figure:
    """Given a dictionary, validates the data from the
    dictionary, and if valid, creates a Figure."""

    validate_schema(db)

    ff = Figure(
        dpi=db["dpi"],
        folder=Path(db["folder"]).expanduser(),
        file=Path(db["folder"]).expanduser().joinpath(db["file"]),
        models=db["models"],
        size=db["size"],
        title=db["title"],
        xlabel=db["xlabel"],
        ylabel=db["ylabel"],
    )

    assert ff.folder.is_dir(), f"Folder {ff.folder} does not exist."
    ext = ff.file.suffix
    file_types = (".pdf", ".png", ".svg")
    assert ext in file_types, f"File type {ext} not in {file_types}"

    # TODO: finish
    return ff


def plot(ff: Figure, hh: histogram.Histogram) -> None:
    """Plot the figure and histogram."""

    with open(hh.file, "r") as file:
        data = file.read()

    aa = data.strip().split("\n")
    bb = [float(x) for x in aa]
    print(f"Number of elements: {len(bb)}")
    # n_neg = [x <= 0.0 for x in bb]

    # breakpoint()
    # Create the histogram
    plt.hist(bb, bins=20, color="blue", alpha=0.7, log=True)

    # Add labels and title
    plt.xlabel("Minimum Scaled Jacobian (MSJ)")
    plt.ylabel("Frequency")
    plt.title(f"{ff.file}")
    # plt.xticks(np.arange(-0.1, 1.0, 0.1))
    xt = [-0.25, 0.0, 0.25, 0.5, 0.75, 1.00]
    plt.xticks(xt)
    plt.xlim([xt[0], xt[-1]])
    plt.ylim([1, 2.0e6])

    # x_ticks = list(range(nxp))
    # y_ticks = list(range(nyp))
    # z_ticks = list(range(nzp))

    # ax.set_xlim(float(x_ticks[0]), float(x_ticks[-1]))

    # Show the plot
    # plt.show()

    # Save the plot
    fn = Path(ff.file).stem + "_msj" + ".png"
    plt.savefig(fn)
    print(f"Saved file: {fn}")

    # Clear the current figure
    # plt.clf()
