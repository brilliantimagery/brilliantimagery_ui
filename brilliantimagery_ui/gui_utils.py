import os
from pathlib import Path
import sys

from PySide2.QtCore import QRect
from PySide2.QtWidgets import QMessageBox


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


def get_cropped_qrect(point, image, radius):
    point1 = max(0, point[0] - radius)
    point2 = max(0, point[1] - radius)
    point3 = min(image.width(), point[0] + radius)
    point4 = min(image.height(), point[1] + radius)

    return QRect(point1, point2, point3 - point1, point4 - point2)


def message_box(label, text, icon='NoIcon'):
    """
    Warning, Critical, Information, NoIcon, Question
    :param label:
    :param text:
    :param icon:
    :return:
    """
    mb = QMessageBox()
    mb.setIcon(getattr(mb.icon(), icon))
    mb.setWindowTitle(label)
    mb.setText(text)
    mb.exec_()
