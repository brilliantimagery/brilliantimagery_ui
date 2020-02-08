import os
from pathlib import Path
import sys


def files_last_updated(folder):
    folder = Path(folder)
    files = [folder / f for f in folder.iterdir() if
             (folder / f).is_file() and f.suffix.lower() == '.dng']
    return max([os.stat(f).st_mtime for f in files])


def resource_path() -> Path:
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = Path(sys._MEIPASS)
    except Exception:
        base_path = Path(__file__).absolute().parents[1]

    return base_path

