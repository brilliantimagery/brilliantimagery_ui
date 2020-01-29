from pathlib import Path
import os


def files_last_updated(folder):
    folder = Path(folder)
    files = [folder / f for f in folder.iterdir() if
             (folder / f).is_file() and f.lower().endswith('dng')]
    return max([os.stat(f).st_mtime for f in files])
