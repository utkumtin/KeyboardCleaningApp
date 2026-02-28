"""
Keyboard Cleaning App — Utility Functions

Admin privilege checks and UAC elevation.
"""

import ctypes
import sys
import os


def is_admin() -> bool:
    """Check if the current process has administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except (AttributeError, OSError):
        return False


def run_as_admin() -> None:
    """Re-launch the current script with administrator privileges via UAC.

    Exits the current (non-admin) process after requesting elevation.
    """
    script = os.path.abspath(sys.argv[0])
    params = " ".join(sys.argv[1:])

    ctypes.windll.shell32.ShellExecuteW(
        None,       # hwnd
        "runas",    # operation — request elevation
        sys.executable,
        f'"{script}" {params}',
        None,       # directory
        1,          # SW_SHOWNORMAL
    )
    sys.exit(0)
