"""This module contains various utilities."""

import os
from datetime import datetime
import socket

from tzlocal import get_localzone


def timestamp(figure_name: str) -> str:
    """Returns the current timestamp."""

    # Get the local timezone
    local_timezone = get_localzone()

    # Get the current time in the local timezone
    current_time = datetime.now(local_timezone)

    # Format the date and time stamp
    dts = current_time.strftime("%Y-%m-%d %H:%M:%S %Z%z")

    user = str(os.getlogin())
    host = socket.gethostname()

    details = figure_name + " created " + dts + " by " + user + " on " + host

    return details
