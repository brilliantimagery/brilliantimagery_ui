from PySide2 import QtCore

from brilliantimagery_ui.gui import MainWindow


def test_dng_sequence_folder(qtbot, mocker, dng_folder):
    widget = MainWindow()
    qtbot.addWidget(widget)

    mocker.patch('PySide2.QtWidgets.QFileDialog.getExistingDirectory', return_value=dng_folder)
    mocker.patch('PySide2.QtCore.QSettings.setValue')
    qtbot.mouseClick(widget.ui.export_tab, QtCore.Qt.LeftButton)
    qtbot.mouseClick(widget.ui.dng_folder_button, QtCore.Qt.LeftButton)

    assert widget.ui.dng_folder_edit.text() == dng_folder
    assert widget.ui.image_count_edit.text() == '3'


def test_calculate_ffmpeg_input(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)

    qtbot.mouseClick(widget.ui.export_tab, QtCore.Qt.LeftButton)

    assert widget.ui.ffmpeg_inputs_edit.toPlainText() == '-vcodec: libx265\n-r: 29.97\n' \
                                                         '-s: 3840x2160\n-colorspace: bt709'

    # widget.ui.prores_ks.setChecked(True)
    qtbot.mouseClick(widget.ui.prores_ks, QtCore.Qt.LeftButton)
    assert widget.ui.ffmpeg_inputs_edit.toPlainText() == '-vcodec: prores_ks\n-r: 29.97\n' \
                                                         '-s: 3840x2160\n-colorspace: bt709\n' \
                                                         '-profile: 4444xq'

    # qtbot.keyClicks(widget.ui.frame_rate, '60')
    # qtbot.keyClicks(widget.ui.bitrate, '600000')
    # qtbot.mouseClick(widget.ui.res_7680x4320, QtCore.Qt.LeftButton)
    widget.ui.frame_rate.setText('60')
    widget.ui.bitrate.setText('600000')
    widget.ui.res_7680x4320.setChecked(True)
    assert widget.ui.ffmpeg_inputs_edit.toPlainText() == '-vcodec: prores_ks\n-r: 60\n' \
                                                         '-s: 7680x4320\n-colorspace: bt709\n' \
                                                         '-b: 600000\n-profile: 4444xq'

    # qtbot.mouseClick(widget.ui.lossless, QtCore.Qt.LeftButton)
    widget.ui.lossless.setChecked(True)
    assert widget.ui.ffmpeg_inputs_edit.toPlainText() == '-vcodec: prores_ks\n-r: 60\n' \
                                                         '-s: 7680x4320\n-colorspace: bt709\n' \
                                                         '-b: 600000\n-profile: 4444xq'

    qtbot.mouseClick(widget.ui.bt2020_cl, QtCore.Qt.LeftButton)
    assert widget.ui.ffmpeg_inputs_edit.toPlainText() == '-vcodec: prores_ks\n-r: 60\n' \
                                                         '-s: 7680x4320\n-colorspace: bt2020_cl\n' \
                                                         '-b: 600000\n-profile: 4444xq'

    # qtbot.mouseClick(widget.ui.libvpx, QtCore.Qt.LeftButton)
    widget.ui.libvpx.setChecked(True)
    assert widget.ui.ffmpeg_inputs_edit.toPlainText() == '-vcodec: libvpx\n-r: 60\n' \
                                                         '-s: 7680x4320\n' \
                                                         '-colorspace: bt2020_ncl\n-b: 600000\n' \
                                                         '-lossless'


# def test_render_now_default_values():
