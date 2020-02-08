import sys
import time
from pathlib import Path

from brilliantimagery.sequence import Sequence
import numpy as np
from PySide2 import QtGui
from PySide2.QtCore import QFile, QSettings, QSize, Qt
from PySide2.QtGui import QImage, QMouseEvent
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog

from brilliantimagery_ui.gui_mainwindow import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.default_converter_path_name = 'adobe_dng_converter_path'
        self.default_source_folder_name = 'source_folder'
        self.default_destination_folder_name = 'destination_folder'
        self.default_values = QSettings('Brilliant Imagery', 'CR2 Processor')

        self.point1 = ()
        self.point2 = ()
        self.last_points = ((), ())

        self.sequence = None
        self.image = None

        # Ramp Tab Setup
        self.ui.ramp_folder_button.clicked.connect(self.open_sequence)

    def open_sequence(self):
        folder = self.open_folder(self.ui.ramp_folder_edit,
                                  self.default_values.value(self.default_source_folder_name))
        self.load_sequence(folder)

    def load_sequence(self, folder):
        if not Path(folder).is_dir():
            return
        if not self.sequence or folder != self.sequence.path:
            self.sequence = Sequence(folder)
            self.files_last_parsed = time.time()

        image = self.sequence.get_reference_image(index_order='yxc').astype(np.uint8)
        h, w, _ = image.shape
        image = np.reshape(image, (image.size, ))
        self.image = QImage(image, w, h, QImage.Format_RGB888)

        self.draw_image()

    def mousePressEvent(self, QMouseEvent):
        # print mouse position
        print(QMouseEvent.pos())

    def draw_image(self):
        canvas = QtGui.QPixmap(self.image)
        self.ui.ramp_image.setPixmap(canvas)

    def open_folder(self, line_edit, start_location):
        folder = QFileDialog.getExistingDirectory(self, "Open Directory",
                                                  start_location)
        line_edit.setText(folder)
        self.default_values.setValue(self.default_source_folder_name, folder)
        return folder


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

# to update gui_mainwindow.py with bash ($ bash)
# /mnt/c/Users/<user>/AppData/Local/pypoetry/Cache/virtualenvs/brilliantimagery-ui-ks1vM-kE-py3.8/Scripts/pyside2-uic.exe gui_mainwindow.ui | tr -d '\000' > gui_mainwindow.py
