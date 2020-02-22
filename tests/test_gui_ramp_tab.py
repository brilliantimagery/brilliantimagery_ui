from pathlib import Path

from PySide2 import QtCore

from brilliantimagery_ui.gui import MainWindow
import pytest


@pytest.mark.skip(reason="Can't get editingFinished signal to fire")
def test_init_ramp_folder_edit_editingFinished(qtbot, path1):
    widget = MainWindow()
    qtbot.addWidget(widget)

    qtbot.keyClicks(widget.ui.ramp_folder_edit, f'{path1}\011')
    assert widget.ui.ramp_folder_edit.text() == path1


def test_open_sequence_no_path_present_in_edit(qtbot, mocker, path1, dng_folder, dng_preview):
    widget = MainWindow()
    qtbot.addWidget(widget)

    open_dir = mocker.patch('PySide2.QtWidgets.QFileDialog.getExistingDirectory',
                            return_value=dng_folder)
    mocker.patch('PySide2.QtCore.QSettings.value', return_value=path1)
    mocker.patch('PySide2.QtCore.QSettings.setValue')
    qtbot.mouseClick(widget.ui.ramp_folder_button, QtCore.Qt.LeftButton)

    open_dir.assert_called_once_with(widget, "Open Directory", path1)
    assert widget.ui.ramp_folder_edit.text() == dng_folder
    image = widget.ui.ramp_image.pixmap().toImage()
    for x in range(dng_preview.shape[1]):
        for y in range(dng_preview.shape[2]):
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()


def test_open_sequence_path_present_in_edit(qtbot, mocker, path1, dng_folder, dng_preview):
    widget = MainWindow()
    qtbot.addWidget(widget)

    widget.ui.ramp_folder_edit.setText(path1)

    open_dir = mocker.patch('PySide2.QtWidgets.QFileDialog.getExistingDirectory',
                            return_value=dng_folder)
    mocker.patch('PySide2.QtCore.QSettings.setValue')
    qtbot.mouseClick(widget.ui.ramp_folder_button, QtCore.Qt.LeftButton)

    open_dir.assert_called_once_with(widget, "Open Directory", path1)
    assert widget.ui.ramp_folder_edit.text() == dng_folder
    image = widget.ui.ramp_image.pixmap().toImage()
    for x in range(dng_preview.shape[1]):
        for y in range(dng_preview.shape[2]):
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()


def test_reload_image(qtbot, dng_folder, dng_preview):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.ui.ramp_folder_edit.setText(dng_folder)

    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)

    image = widget.ui.ramp_image.pixmap().toImage()
    for x in range(dng_preview.shape[1]):
        for y in range(dng_preview.shape[2]):
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview[0, x, y] == image.pixelColor(x, y).red()


def test_create_rectangle(qtbot, dng_folder, dng_preview_w_rectangle, image_click_locations):
    widget = MainWindow()
    qtbot.addWidget(widget)

    widget.ui.ramp_folder_edit.setText(dng_folder)
    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[0])
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[1])

    image = widget.ui.ramp_image.pixmap().toImage()
    for x in range(dng_preview_w_rectangle.shape[1]):
        for y in range(dng_preview_w_rectangle.shape[2]):
            assert dng_preview_w_rectangle[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview_w_rectangle[0, x, y] == image.pixelColor(x, y).red()
            assert dng_preview_w_rectangle[0, x, y] == image.pixelColor(x, y).red()


def test_ramp_button_ramp_success(qtbot, mocker, dng_folder_editable, image_click_locations):
    widget = MainWindow()
    qtbot.addWidget(widget)

    qtbot.keyClicks(widget.ui.ramp_folder_edit, dng_folder_editable)
    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[0])
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[1])
    qtbot.mouseClick(widget.ui.ramp_checkbox, QtCore.Qt.LeftButton)

    ramp = mocker.patch('brilliantimagery.sequence._sequence.Sequence.ramp_minus_exmpsure')
    save = mocker.patch('brilliantimagery.sequence._sequence.Sequence.save')
    qtbot.mouseClick(widget.ui.ramp_button, QtCore.Qt.LeftButton)

    assert not widget.ui.reuse_offsets_checkbox.isChecked()
    assert not widget.ui.reuse_brightness_checkbox.isChecked()
    assert widget.last_points == ((169, 60), (203, 80))
    ramp.assert_called_once_with()
    save.assert_called_once_with()


def test_ramp_button_deflicker_success(qtbot, mocker, dng_folder_editable, image_click_locations):
    widget = MainWindow()
    qtbot.addWidget(widget)

    qtbot.keyClicks(widget.ui.ramp_folder_edit, dng_folder_editable)
    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[0])
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[1])
    qtbot.mouseClick(widget.ui.deflicker_checkbox, QtCore.Qt.LeftButton)

    ramp = mocker.patch('brilliantimagery.sequence._sequence.Sequence.ramp_exposure')
    save = mocker.patch('brilliantimagery.sequence._sequence.Sequence.save')
    qtbot.mouseClick(widget.ui.ramp_button, QtCore.Qt.LeftButton)

    assert not widget.ui.reuse_offsets_checkbox.isChecked()
    assert widget.ui.reuse_brightness_checkbox.isChecked()
    assert widget.last_points == ((169, 60), (203, 80))
    ramp.assert_called_once_with([0.66015625, 0.4166666666666667, 0.79296875, 0.5555555555555556])
    save.assert_called_once_with()


def test_ramp_button_stabilize_success(qtbot, mocker, dng_folder_editable, image_click_locations):
    widget = MainWindow()
    qtbot.addWidget(widget)

    qtbot.keyClicks(widget.ui.ramp_folder_edit, dng_folder_editable)
    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[0])
    qtbot.mouseClick(widget.ui.tabs, QtCore.Qt.LeftButton, pos=image_click_locations[1])
    qtbot.mouseClick(widget.ui.stabilize_checkbox, QtCore.Qt.LeftButton)

    ramp = mocker.patch('brilliantimagery.sequence._sequence.Sequence.stabilize')
    save = mocker.patch('brilliantimagery.sequence._sequence.Sequence.save')
    qtbot.mouseClick(widget.ui.ramp_button, QtCore.Qt.LeftButton)

    assert widget.ui.reuse_offsets_checkbox.isChecked()
    assert not widget.ui.reuse_brightness_checkbox.isChecked()
    assert widget.last_points == ((169, 60), (203, 80))
    ramp.assert_called_once_with([0.66015625, 0.4166666666666667, 0.79296875, 0.5555555555555556])
    save.assert_called_once_with()


def test_maybe_reset_misalignment_brightness_reuse(qtbot, dng_folder):
    widget = MainWindow()
    qtbot.addWidget(widget)

    widget.point1 = (1, 2)
    widget.point2 = (3, 4)
    widget.last_points = ((1, 2), (3, 4))
    qtbot.keyClicks(widget.ui.ramp_folder_edit, dng_folder)
    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.reuse_offsets_checkbox, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.reuse_brightness_checkbox, QtCore.Qt.LeftButton)
    folder = Path(widget.ui.ramp_folder_edit.text())
    files = [f.name.lower() for f in folder.iterdir() if
             (folder / f).is_file() and f.suffix.lower() == '.dng']
    widget.sequence.set_misalignments({f: 3 for f in files})
    widget.sequence.set_brightnesses({f: 3 for f in files})

    widget.maybe_reset_misalignment_brightness()

    for image in list(widget.sequence._images.values()):
        assert image.misalignment == 3
        assert image.brightness == 3


def test_maybe_reset_misalignment_brightness_box_moved(qtbot, dng_folder):
    widget = MainWindow()
    qtbot.addWidget(widget)

    widget.point1 = ()
    widget.point2 = ()
    widget.last_points = ((1, 2), (3, 4))
    qtbot.keyClicks(widget.ui.ramp_folder_edit, dng_folder)
    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.reuse_offsets_checkbox, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.reuse_brightness_checkbox, QtCore.Qt.LeftButton)
    folder = Path(widget.ui.ramp_folder_edit.text())
    files = [f.name for f in folder.iterdir() if
             (folder / f).is_file() and f.suffix.lower() == '.dng']
    widget.sequence.set_misalignments({f: 3 for f in files})
    widget.sequence.set_brightnesses({f: 3 for f in files})

    widget.maybe_reset_misalignment_brightness()

    for image in list(widget.sequence._images.values()):
        assert image.misalignment == None
        assert image.brightness == None


def test_maybe_reset_misalignment_brightness_reuse_not_checked(qtbot, dng_folder):
    widget = MainWindow()
    qtbot.addWidget(widget)

    widget.point1 = (1, 2)
    widget.point2 = (3, 4)
    widget.last_points = ((1, 2), (3, 4))
    qtbot.keyClicks(widget.ui.ramp_folder_edit, dng_folder)
    qtbot.mouseClick(widget.ui.reload_image_button, QtCore.Qt.LeftButton)
    folder = Path(widget.ui.ramp_folder_edit.text())
    files = [f.name for f in folder.iterdir() if
             (folder / f).is_file() and f.suffix.lower() == '.dng']
    widget.sequence.set_misalignments({f: 3 for f in files})
    widget.sequence.set_brightnesses({f: 3 for f in files})

    widget.maybe_reset_misalignment_brightness()

    for image in list(widget.sequence._images.values()):
        assert image.misalignment == None
        assert image.brightness == None

