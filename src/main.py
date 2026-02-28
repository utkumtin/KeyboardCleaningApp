"""
Keyboard Cleaning App — Entry Point

Checks for administrator privileges, then launches the main UI.
"""

import sys

from .utils import is_admin, run_as_admin
from .ui import App


def main() -> None:
    """Application entry point."""
    # Low-level keyboard hooks require admin privileges on Windows
    if not is_admin():
        print("Requesting administrator privileges...")
        run_as_admin()
        return  # run_as_admin calls sys.exit, but just in case

    app = App()
    app.run()


if __name__ == "__main__":
    main()
