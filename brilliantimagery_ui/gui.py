import sys
import time
from pathlib import Path

from brilliantimagery.dng import DNG
from brilliantimagery.sequence import Sequence
import numpy as np
from PIL import Image
from PySide2 import QtGui
from PySide2.QtCore import QSettings, QPoint
from PySide2.QtGui import QImage, QMouseEvent, QColor, QPixmap
from PySide2.QtWidgets import QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, \
    QPlainTextEdit, QHBoxLayout, QLineEdit, QRadioButton, QSlider, QCheckBox
from skvideo.io import FFmpegWriter
from tqdm import tqdm

from brilliantimagery_ui.gui_mainwindow import Ui_MainWindow
from brilliantimagery_ui.gui_utils import files_last_updated, get_cropped_qrect, message_box, \
    has_dngs


class MainWindow(QMainWindow):
    CORNER_RADIUS = 2
    COLOR = QColor(255, 0, 0)
    WATCH_WAIT_TIME = 1

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.default_values = QSettings('BrilliantImagery', 'BrilliantImagery_UI')

        self.point1 = ()
        self.point2 = ()
        self.last_points = ((), ())

        self.sequence = None
        self.image = None

        # Ramp Tab Setup
        self.default_ramp_folder_name = 'ramp_folder'
        self.ui.ramp_folder_edit.editingFinished.connect(lambda: self.load_sequence(
            self.ui.ramp_folder_edit.text()))
        self.ui.ramp_folder_button.clicked.connect(self.open_sequence)
        self.ui.reload_image_button.clicked.connect(lambda: self.load_sequence(
            self.ui.ramp_folder_edit.text()))
        self.ui.ramp_button.clicked.connect(self.process_sequence)

        # Video Export Tab Setup
        self.default_dng_folder_name = 'dng_folder'
        self.default_rendered_images_folder_name = 'rendered_images_folder'
        self.default_rendered_video_name = 'rendered_video_file'
        self.link_to_video_render_processes(self.ui.export_tab)
        self.ui.tabs.currentChanged.connect(self.update_dng_sequence_folder)
        self.ui.dng_folder_button.clicked.connect(self.open_reference_dng_folder)
        self.ui.dng_folder_edit.editingFinished.connect(self.sequence_stats)
        self.ui.rendered_image_folder_button.clicked.connect(lambda: self.open_folder(
            self.ui.rendered_image_folder_edit, self.default_rendered_images_folder_name))
        self.ui.output_file_button.clicked.connect(self.save_render_output_file)
        self.ui.watch_render_button.clicked.connect(self.watch_render_folder)
        self.ui.render_now_button.clicked.connect(self.render_video)

        self.calculate_ffmpeg_input()

        # Image Render Tab Setup
        self.default_render_image_name = 'render_image'
        self.ui.image_render_button.clicked.connect(self.render_image_w_dialog)
        self.ui.image_render_edit.editingFinished.connect(lambda: self.render_image(
            self.ui.rendered_image_folder_edit.text()))

    def watch_render_folder(self):
        image_count = int(self.ui.image_count_edit.text())
        extension = f".{self.ui.rendered_format_edit.text().lower().replace('.', '')}"
        files_present = 0

        while files_present < image_count:
            files_present = len([f for f
                                 in Path(self.ui.rendered_image_folder_edit.text()).iterdir()
                                 if f.suffix.lower() == extension])
            time.sleep(MainWindow.WATCH_WAIT_TIME)

        print('Rendering!')

        self.render_video()

    def render_video(self):
        extension = f".{self.ui.rendered_format_edit.text().lower().replace('.', '')}"
        files = [f for f in Path(self.ui.rendered_image_folder_edit.text()).iterdir()
                 if f.suffix.lower() == extension]

        output = dict()
        input = self.ui.ffmpeg_inputs_edit.toPlainText().replace(' ', '').replace('\n', ',')
        for command in input.split(','):
            com, val = command.split(':')
            output[com.strip()] = val.strip()

        if output['-s'] == 'source':
            pic = Image.open(str(files[0]))
            w, h = pic.size
            output['-s'] = f'{w}x{h}'

        writer = FFmpegWriter(str(Path(self.ui.output_file_edit.text())), outputdict=output)

        for file in tqdm(files):
            pic = Image.open(file)
            pic = np.array(pic).astype(np.uint8)
            writer.writeFrame(pic)

        writer.close()

        print('Done Rendering!')

    def open_reference_dng_folder(self):
        self.open_folder(self.ui.dng_folder_edit, self.default_dng_folder_name)
        self.sequence_stats()

    def update_dng_sequence_folder(self):
        if self.ui.tabs.currentIndex() != 1:
            return
        if not self.ui.dng_folder_edit.text():
            self.ui.dng_folder_edit.setText(self.ui.ramp_folder_edit.text())
        self.sequence_stats()

    def sequence_stats(self):
        path = Path(self.ui.dng_folder_edit.text())
        if not path.is_dir():
            return
        count = len(list(f for f in path.iterdir() if f.suffix.lower() == '.dng'))
        self.ui.image_count_edit.setText(str(count))

    def link_to_video_render_processes(self, widget):
        if (isinstance(widget, QLabel)
                or isinstance(widget, QPushButton)
                or isinstance(widget, QPlainTextEdit)
                or isinstance(widget, QHBoxLayout)):
            return
        elif isinstance(widget, QLineEdit):
            if widget.objectName() == 'frame_rate' or widget.objectName() == 'bitrate':
                widget.editingFinished.connect(self.calculate_ffmpeg_input)
                widget.editingFinished.connect(self.set_video_render_options)
        elif isinstance(widget, QRadioButton):
            widget.setEnabled(True)
            widget.toggled.connect(self.calculate_ffmpeg_input)
            widget.toggled.connect(self.set_video_render_options)
        elif isinstance(widget, QCheckBox):
            widget.setEnabled(True)
            widget.stateChanged.connect(self.calculate_ffmpeg_input)
            widget.stateChanged.connect(self.set_video_render_options)
        children = widget.children()
        if children:
            for child in children:
                self.link_to_video_render_processes(child)

    def set_video_render_options(self):
        def loop_and_set_enabled(widget):
            children = widget.children()
            if children:
                for child in children:
                    loop_and_set_enabled(child)
            if isinstance(widget, QRadioButton) or isinstance(widget, QCheckBox):
                widget.setEnabled(True)

        loop_and_set_enabled(self.ui.export_tab)
        codec = self.ui.codec_buttons.checkedButton().objectName()
        if codec == 'libx264':
            self.disable_prores_buttons()
            self.ui.alpha.setChecked(False)
            self.ui.alpha.setEnabled(False)
        elif codec == 'libx265':
            self.disable_prores_buttons()
            self.ui.alpha.setChecked(False)
            self.ui.alpha.setEnabled(False)
        elif codec == 'prores_ks':
            self.ui.lossless.setEnabled(False)
            self.ui.lossless.setChecked(False)
            self.ui.pf_420.setEnabled(False)
            self.ui.color_10_bit.setChecked(True)
            self.ui.color_10_bit.setEnabled(False)
        elif codec == 'libvpx':
            self.disable_prores_buttons()
            self.ui.pf_420.setChecked(True)
            self.ui.pf_422.setEnabled(False)
            self.ui.pf_444.setEnabled(False)
            self.ui.color_10_bit.setChecked(False)
            self.ui.color_10_bit.setEnabled(False)

    def disable_prores_buttons(self):
        self.ui.pr__1.setEnabled(False)
        self.ui.pr_0.setEnabled(False)
        self.ui.pr_2.setEnabled(False)
        self.ui.pr_3.setEnabled(False)
        self.ui.pr_4.setEnabled(False)
        self.ui.pr_5.setEnabled(False)

    def calculate_ffmpeg_input(self):
        values = dict()
        values['-vcodec'] = self.ui.codec_buttons.checkedButton().objectName()
        values['-r'] = self.ui.frame_rate.text()
        values['-s'] = self.ui.resolution_buttons.checkedButton().objectName().replace('res_', '')

        colorspace = self.ui.colorspace_buttons.checkedButton().objectName()
        pixel_format = self.ui.pixel_format_buttons.checkedButton().objectName().replace('pf_', '')
        bits = '10le' if self.ui.color_10_bit.isChecked() else ''
        alpha = 'a' if self.ui.alpha.isChecked() else ''

        if values['-vcodec'] == 'libx264':
            if self.ui.lossless.isChecked():
                values['-crf'] = '0'
                values['-qp'] = '0'
            values['-pix_fmt'] = f'yuv{pixel_format}p{bits}'
        if values['-vcodec'] == 'libx265':
            if self.ui.lossless.isChecked():
                values['-x265-params'] = 'lossless=1'
            values['-pix_fmt'] = f'yuv{pixel_format}p{bits}'
        if values['-vcodec'] == 'prores_ks':
            values['-profile'] = self.ui.prores_buttons.checkedButton()\
                .objectName().replace('pr_', '').replace('_', '-')
            if alpha and pixel_format == '422':
                message_box('Oops', "4:2:2 and including alpha isn't valid")
            values['-pix_fmt'] = f'yuv{alpha}{pixel_format}p10le'
        if values['-vcodec'] == 'libvpx':
            if self.ui.lossless.isChecked():
                values['-lossless'] = '1'
            values['-pix_fmt'] = f'yuv{alpha}{pixel_format}p'
            if colorspace == 'bt2020_cl':
                colorspace = 'bt2020_ncl'

        values['-colorspace'] = colorspace
        if (bitrate := self.ui.bitrate.text()) != '':
            values['-b'] = bitrate

        text = str(values).replace('{', '').replace("'", '').replace(', ', '\n').replace('}', '')
        self.ui.ffmpeg_inputs_edit.setPlainText(text)

    def process_sequence(self):
        if not self.validate_selections():
            return

        self.maybe_reset_misalignment_brightness()

        rectangle = (min(self.point1[0], self.point2[0]), min(self.point1[1], self.point2[1]),
                     max(self.point1[0], self.point2[0]), max(self.point1[1], self.point2[1]))
        rectangle = [rectangle[0] / self.image.width(), rectangle[1] / self.image.height(),
                     rectangle[2] / self.image.width(), rectangle[3] / self.image.height()]

        last_modified = files_last_updated(self.sequence.path)
        if last_modified > self.files_last_parsed:
            self.sequence.parse_sequence()
            self.files_last_parsed = time.time()

        ramp = self.ui.ramp_checkbox.isChecked()
        deflicker = self.ui.deflicker_checkbox.isChecked()
        stabilize = self.ui.stabilize_checkbox.isChecked()
        if ramp and not deflicker and not stabilize:
            self.sequence.ramp_minus_exmpsure()
        elif not ramp and deflicker and not stabilize:
            self.sequence.ramp_exposure(rectangle)
        elif not ramp and not deflicker and stabilize:
            self.sequence.stabilize(rectangle)
        elif ramp and deflicker and not stabilize:
            self.sequence.ramp(rectangle)
        elif not ramp and deflicker and stabilize:
            self.sequence.ramp_exposure_and_stabilize(rectangle)
        elif ramp and not deflicker and stabilize:
            self.sequence.ramp_minus_exposure_and_stabilize(rectangle)
        elif ramp and deflicker and stabilize:
            self.sequence.ramp_and_stabilize(rectangle)

        self.sequence.save()

        if deflicker:
            self.ui.reuse_brightness_checkbox.setChecked(True)
        if stabilize:
            self.ui.reuse_offsets_checkbox.setChecked(True)

        self.last_points = (self.point1, self.point2)

        if self.ui.notify_completion_checkbox.isChecked():
            message_box('Done', 'All Done!', 'Information')

        print('Done Processing!')

    def maybe_reset_misalignment_brightness(self):
        folder = Path(self.ui.ramp_folder_edit.text())
        files = [f.name.lower() for f in folder.iterdir() if
                 (folder / f).is_file() and f.suffix.lower() == '.dng']

        if (self.point1, self.point2) != self.last_points:
            self.sequence.set_misalignments({f: None for f in files})
            self.sequence.set_brightnesses({f: None for f in files})
        else:
            if not self.ui.reuse_offsets_checkbox.isChecked():
                self.sequence.set_misalignments({f: None for f in files})
            if not self.ui.reuse_brightness_checkbox.isChecked():
                self.sequence.set_brightnesses({f: None for f in files})

    def validate_selections(self):
        if self.point1 and self.point2:
            rectangle = True
        else:
            rectangle = False

        if not self.ui.ramp_folder_edit.text():
            message_box('Oops!', 'You need to specify a Sequence Folder.', 'Warning')
            return False

        ui = self.ui
        if rectangle and (ui.deflicker_checkbox.isChecked() or ui.stabilize_checkbox.isChecked()):
            return True
        elif ui.reuse_brightness_checkbox.isChecked() and ui.deflicker_checkbox.isChecked():
            return True
        elif ui.reuse_offsets_checkbox.isChecked() and ui.stabilize_checkbox.isChecked():
            return True
        elif ui.ramp_checkbox.isChecked() and not (ui.deflicker_checkbox.isChecked()
                                                   or ui.stabilize_checkbox.isChecked()):
            return True

        message_box('Oops!',
                    "You need to specify what to do (in the Operations to Perform box) "
                    "and what information to use (either highlight a rectangle or select "
                    "what info to reuse)",
                    'Warning')
        return False

    def open_folder(self, line_edit, default):
        folder = line_edit.text() if line_edit.text() else self.default_values.value(default)
        folder = QFileDialog.getExistingDirectory(self, "Open Directory", folder)
        if not folder:
            return
        line_edit.setText(folder)
        self.default_values.setValue(default, folder)
        return folder

    def open_sequence(self):
        folder = self.open_folder(self.ui.ramp_folder_edit, self.default_ramp_folder_name)
        self.load_sequence(folder)

    def load_sequence(self, folder):
        if not folder or not Path(folder).is_dir() or not has_dngs(folder):
            return
        if not self.sequence or folder != self.sequence.path:
            self.sequence = Sequence(folder)
            self.files_last_parsed = time.time()

        image = self.sequence.get_reference_image(index_order='yxc').astype(np.uint8)
        h, w, _ = image.shape
        self.image_data = np.reshape(image, (image.size,))
        self.image = QImage(self.image_data, w, h, QImage.Format_RGB888)

        self.draw_image()

    def mouseReleaseEvent(self, event: QMouseEvent):
        if not self.image or self.ui.tabs.currentIndex() != 0:
            return

        image_location = self.ui.ramp_image.mapToGlobal(QPoint(0, 0))
        image_x = image_location.x()
        image_y = image_location.y()
        image_width = self.image.width()
        image_height = self.image.height()
        x = event.globalX()
        y = event.globalY()

        if not (image_x <= x <= image_x + image_width and image_y <= y <= image_y + image_height):
            return

        if not self.point1:
            self.point1 = (x - image_x, y - image_y)
        elif not self.point2:
            self.point2 = (x - image_x, y - image_y)
        else:
            self.point1 = ()
            self.point2 = ()

        self.draw_image()

    def draw_image(self):
        canvas = QtGui.QPixmap(self.image)
        self.ui.ramp_image.setPixmap(canvas)

        if self.point1:
            painter = QtGui.QPainter(self.ui.ramp_image.pixmap())
            painter.setPen(MainWindow.COLOR)

            rect = get_cropped_qrect(self.point1, self.image, MainWindow.CORNER_RADIUS)
            painter.drawRect(rect)
            painter.fillRect(rect, MainWindow.COLOR)

            if self.point2:
                rect = get_cropped_qrect(self.point2, self.image, MainWindow.CORNER_RADIUS)
                painter.drawRect(rect)
                painter.fillRect(rect, MainWindow.COLOR)

                painter.drawRect(min(self.point1[0], self.point2[0]),
                                 min(self.point1[1], self.point2[1]),
                                 abs(self.point1[0] - self.point2[0]),
                                 abs(self.point1[1] - self.point2[1]))

            painter.end()

    def open_file(self, line_edit, default, extensions):
        file = line_edit.text() if line_edit.text() else self.default_values.value(default)
        file, _ = QFileDialog.getOpenFileName(self, "Open File", file, extensions)
        line_edit.setText(file)
        self.default_values.setValue(default, file)
        return file

    def save_render_output_file(self):
        extensions = 'All Files (*.*)'
        if self.ui.libx264.isChecked():
            extensions = 'MPEG-4/H264 (*.mp4);;All Files (*.*)'
        elif self.ui.libx265.isChecked():
            extensions = 'HEVC/H265 (*.mp4);;All Files (*.*)'
        elif self.ui.prores_ks.isChecked():
            extensions = 'ProRes (*.mov);;All Files (*.*)'
        elif self.ui.libvpx.isChecked():
            extensions = 'VP9/VPX (*.webm);;All Files (*.*)'
        self.save_file(self.ui.output_file_edit, self.default_rendered_video_name, extensions)

    def save_file(self, line_edit=None, default=None, extensions=None):
        if line_edit:
            if (file := line_edit.text()) != '':
                pass
            elif default:
                file = self.default_values.value(default)

        file = QFileDialog.getSaveFileName(self, 'Save File', file, extensions)[0]

        if default:
            self.default_values.setValue(default, file)

        if line_edit:
            line_edit.setText(file)

    def render_image_w_dialog(self):
        file = self.open_file(self.ui.image_render_edit,
                              self.default_rendered_images_folder_name, "(*.dng)")
        self.render_image(file)

    def render_image(self, file):
        if not file:
            return
        path = Path(file)
        if not path.is_file() or path.suffix.lower() != '.dng':
            return

        dng = DNG(file)
        image_array = dng.get_image() * 255
        _, w, h = image_array.shape
        # This has to be self... if the image is to be reloaded
        self._render_image_data = np.reshape(image_array, (image_array.size,), 'F').astype(np.uint8)

        image = QImage(self._render_image_data, w, h, QImage.Format_RGB888)
        image_label = QLabel()
        pixmap = QPixmap.fromImage(image)
        image_label.setPixmap(pixmap)

        self.ui.render_scroll_area.setWidget(image_label)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())

# to update gui_mainwindow.py with bash ($ bash)
# /mnt/c/Users/<user>/AppData/Local/pypoetry/Cache/virtualenvs/brilliantimagery-ui-ks1vM-kE-py3.8/Scripts/pyside2-uic.exe gui_mainwindow.ui | tr -d '\000' > gui_mainwindow.py
