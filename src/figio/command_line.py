"""This module, command_line.py, is the new command line entry point, which
accepts input files of type .yml.
"""

import argparse
from pathlib import Path

# import figio.constants as cc
from figio.factory import XYFactory
import figio.histogram as hh
from figio.xymodel import XYModel, XYModelAbaqus
from figio.xyview import XYView, XYViewAbaqus
from figio.yml_to_dict import yml_to_dict


def command_line(fin: Path) -> bool:
    """Given a .yml file, processes it to create a figure.

    Args:
        fin: The fully pathed input file.

    Returns
        True if successful, False otherwise.
    """
    processed = False

    db = yml_to_dict(fin=fin)

    items = []  # cart of items is empty, fill from factory
    # factory = XYFactory()  # it's static!

    breakpoint()

    for item in db:

        if "histogram" in item:
            i = hh.histogram_new(db[item])
            items.append(i)

        else:
            kwargs = db[item]
            i = XYFactory.create(item, **kwargs)
            if i:
                items.append(i)
            else:
                warn_msg = "Item is None from factory,"
                warn_msg += " nothing added to command_line items."
                print(warn_msg)

    hists = [i for i in items if isinstance(i, hh.Histogram)]
    models = [i for i in items if isinstance(i, (XYModel, XYModelAbaqus))]
    views = [i for i in items if isinstance(i, (XYView, XYViewAbaqus))]

    breakpoint()

    for view in views:
        print(f'Creating view with guid = "{view.guid}"')

        if view.model_keys:  # register only selected models with current view
            print(f"  Adding {view.model_keys} model(s) to current view.")
            view.models = [m for m in models if m.guid in view.model_keys]
            view.figure()  # must be within this subset scope
        else:
            print("  Adding all models to current view.")
            view.models = models  # register all models with current view
            view.figure()  # must be within this subset scope

    print("====================================")
    print("End of figio execution.")

    processed = True  # overwrite
    return processed  # success if we reach this line


def main():
    """Runs the module from the command line."""
    # print(cl.BANNER)
    # print(cl.CLI_DOCS)
    parser = argparse.ArgumentParser(
        prog="figio",
        description="Generate a figure.",
        epilog="figio finished",
    )
    parser.add_argument(
        "input_file", help="the .yml recipe used to create the figure"
    )

    args = parser.parse_args()
    if args.input_file:
        aa = Path(args.input_file).expanduser()
        if aa.is_file():
            print(f"Processing file: {aa}")
            command_line(fin=aa)
        else:
            print(f"Error: could not find file: {aa}")


if __name__ == "__main__":
    main()
