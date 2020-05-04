"""
Useful utilities used across the library
"""

import logging
import os
import shutil
import tempfile
import contextlib


@contextlib.contextmanager
def enter_temp_directory(remove=True):
    """Create and enter a temporary directory; used as context manager."""
    temp_dir = tempfile.mkdtemp()
    cwd = os.getcwd()
    os.chdir(temp_dir)
    yield cwd, temp_dir
    os.chdir(cwd)
    if remove:
        shutil.rmtree(temp_dir)


class PerLevelFormatter(logging.Formatter):
    """
    Adapted from https://stackoverflow.com/a/14859558
    """

    FORMATS = {
        logging.ERROR: "ERROR! %(message)s",
        logging.WARNING: "WARNING: %(message)s",
        logging.INFO: "%(message)s",
        logging.DEBUG: "Debug: %(message)s",
        101: "%(message)s",
    }

    def __init__(self, fmt="%(levelName)d: %(message)s", datefmt=None, style="%", **kwargs):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style, **kwargs)

    def format(self, record):

        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt
        self._style._fmt = self.FORMATS.get(record.levelno, self._style._fmt)
        # Call the original formatter class to do the grunt work
        result = super().format(record)
        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result
