# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'gui_mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 5.14.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import (QCoreApplication, QMetaObject, QObject, QPoint,
    QRect, QSize, QUrl, Qt)
from PySide2.QtGui import (QBrush, QColor, QConicalGradient, QCursor, QFont,
    QFontDatabase, QIcon, QLinearGradient, QPalette, QPainter, QPixmap,
    QRadialGradient)
from PySide2.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(702, 463)
        self.action_open_project = QAction(MainWindow)
        self.action_open_project.setObjectName(u"action_open_project")
        self.action_save_project = QAction(MainWindow)
        self.action_save_project.setObjectName(u"action_save_project")
        self.action_exit = QAction(MainWindow)
        self.action_exit.setObjectName(u"action_exit")
        self.action_about = QAction(MainWindow)
        self.action_about.setObjectName(u"action_about")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.tabs = QTabWidget(self.centralwidget)
        self.tabs.setObjectName(u"tabs")
        self.tabs.setGeometry(QRect(0, 0, 701, 431))
        self.tabs.setMinimumSize(QSize(0, 0))
        self.tabs.setMaximumSize(QSize(20000, 20000))
        self.tabs.setAutoFillBackground(False)
        self.tabs.setMovable(False)
        self.ramp_tab = QWidget()
        self.ramp_tab.setObjectName(u"ramp_tab")
        self.ramp_image = QLabel(self.ramp_tab)
        self.ramp_image.setObjectName(u"ramp_image")
        self.ramp_image.setGeometry(QRect(10, 50, 256, 256))
        self.ramp_image.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.ramp_opperations_box = QGroupBox(self.ramp_tab)
        self.ramp_opperations_box.setObjectName(u"ramp_opperations_box")
        self.ramp_opperations_box.setGeometry(QRect(275, 50, 150, 90))
        self.ramp_checkbox = QCheckBox(self.ramp_opperations_box)
        self.ramp_checkbox.setObjectName(u"ramp_checkbox")
        self.ramp_checkbox.setGeometry(QRect(10, 20, 131, 17))
        self.deflicker_checkbox = QCheckBox(self.ramp_opperations_box)
        self.deflicker_checkbox.setObjectName(u"deflicker_checkbox")
        self.deflicker_checkbox.setGeometry(QRect(10, 40, 70, 17))
        self.stabilize_checkbox = QCheckBox(self.ramp_opperations_box)
        self.stabilize_checkbox.setObjectName(u"stabilize_checkbox")
        self.stabilize_checkbox.setGeometry(QRect(10, 60, 70, 17))
        self.data_resue_box = QGroupBox(self.ramp_tab)
        self.data_resue_box.setObjectName(u"data_resue_box")
        self.data_resue_box.setGeometry(QRect(275, 150, 231, 101))
        self.reuse_offsets_checkbox = QCheckBox(self.data_resue_box)
        self.reuse_offsets_checkbox.setObjectName(u"reuse_offsets_checkbox")
        self.reuse_offsets_checkbox.setGeometry(QRect(10, 20, 191, 17))
        self.reuse_brightness_checkbox = QCheckBox(self.data_resue_box)
        self.reuse_brightness_checkbox.setObjectName(u"reuse_brightness_checkbox")
        self.reuse_brightness_checkbox.setGeometry(QRect(10, 40, 211, 17))
        self.reload_image_button = QPushButton(self.data_resue_box)
        self.reload_image_button.setObjectName(u"reload_image_button")
        self.reload_image_button.setGeometry(QRect(10, 65, 75, 23))
        self.horizontalLayoutWidget = QWidget(self.ramp_tab)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(280, 260, 223, 31))
        self.horizontalLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.ramp_button = QPushButton(self.horizontalLayoutWidget)
        self.ramp_button.setObjectName(u"ramp_button")

        self.horizontalLayout.addWidget(self.ramp_button)

        self.notify_completion_checkbox = QCheckBox(self.horizontalLayoutWidget)
        self.notify_completion_checkbox.setObjectName(u"notify_completion_checkbox")

        self.horizontalLayout.addWidget(self.notify_completion_checkbox)

        self.horizontalLayoutWidget_2 = QWidget(self.ramp_tab)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 10, 641, 31))
        self.horizontalLayout_3 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_3.addWidget(self.label)

        self.ramp_folder_edit = QLineEdit(self.horizontalLayoutWidget_2)
        self.ramp_folder_edit.setObjectName(u"ramp_folder_edit")

        self.horizontalLayout_3.addWidget(self.ramp_folder_edit)

        self.ramp_folder_button = QPushButton(self.horizontalLayoutWidget_2)
        self.ramp_folder_button.setObjectName(u"ramp_folder_button")

        self.horizontalLayout_3.addWidget(self.ramp_folder_button)

        self.tabs.addTab(self.ramp_tab, "")
        self.export_tab = QWidget()
        self.export_tab.setObjectName(u"export_tab")
        self.gridLayoutWidget = QWidget(self.export_tab)
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QRect(10, 10, 641, 111))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(10)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.dng_folder_edit = QLineEdit(self.gridLayoutWidget)
        self.dng_folder_edit.setObjectName(u"dng_folder_edit")

        self.gridLayout.addWidget(self.dng_folder_edit, 0, 1, 1, 1)

        self.label_5 = QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName(u"label_5")

        self.gridLayout.addWidget(self.label_5, 0, 0, 1, 1)

        self.label_3 = QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName(u"label_3")

        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)

        self.rendered_image_folder_edit = QLineEdit(self.gridLayoutWidget)
        self.rendered_image_folder_edit.setObjectName(u"rendered_image_folder_edit")

        self.gridLayout.addWidget(self.rendered_image_folder_edit, 2, 1, 1, 1)

        self.label_4 = QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName(u"label_4")

        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)

        self.dng_folder_button = QPushButton(self.gridLayoutWidget)
        self.dng_folder_button.setObjectName(u"dng_folder_button")

        self.gridLayout.addWidget(self.dng_folder_button, 0, 2, 1, 1)

        self.output_file_edit = QLineEdit(self.gridLayoutWidget)
        self.output_file_edit.setObjectName(u"output_file_edit")

        self.gridLayout.addWidget(self.output_file_edit, 3, 1, 1, 1)

        self.output_file_button = QPushButton(self.gridLayoutWidget)
        self.output_file_button.setObjectName(u"output_file_button")

        self.gridLayout.addWidget(self.output_file_button, 3, 2, 1, 1)

        self.renderd_image_folder_button = QPushButton(self.gridLayoutWidget)
        self.renderd_image_folder_button.setObjectName(u"renderd_image_folder_button")

        self.gridLayout.addWidget(self.renderd_image_folder_button, 2, 2, 1, 1)

        self.label_6 = QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName(u"label_6")

        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)

        self.horizontalLayout_4 = QHBoxLayout()
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.label_8 = QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName(u"label_8")
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setMinimumSize(QSize(20, 0))

        self.horizontalLayout_4.addWidget(self.label_8)

        self.image_count_edit = QLineEdit(self.gridLayoutWidget)
        self.image_count_edit.setObjectName(u"image_count_edit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.image_count_edit.sizePolicy().hasHeightForWidth())
        self.image_count_edit.setSizePolicy(sizePolicy1)
        self.image_count_edit.setMinimumSize(QSize(0, 0))
        self.image_count_edit.setMaximumSize(QSize(50, 16777215))

        self.horizontalLayout_4.addWidget(self.image_count_edit)

        self.label_7 = QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setMinimumSize(QSize(250, 0))

        self.horizontalLayout_4.addWidget(self.label_7)


        self.gridLayout.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)

        self.groupBox = QGroupBox(self.export_tab)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 140, 211, 71))
        self.gridLayoutWidget_2 = QWidget(self.groupBox)
        self.gridLayoutWidget_2.setObjectName(u"gridLayoutWidget_2")
        self.gridLayoutWidget_2.setGeometry(QRect(10, 10, 201, 61))
        self.gridLayout_3 = QGridLayout(self.gridLayoutWidget_2)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.prores = QRadioButton(self.gridLayoutWidget_2)
        self.prores.setObjectName(u"prores")

        self.gridLayout_3.addWidget(self.prores, 0, 1, 1, 1)

        self.vp9 = QRadioButton(self.gridLayoutWidget_2)
        self.vp9.setObjectName(u"vp9")

        self.gridLayout_3.addWidget(self.vp9, 1, 1, 1, 1)

        self.h264 = QRadioButton(self.gridLayoutWidget_2)
        self.h264.setObjectName(u"h264")
        self.h264.setChecked(False)

        self.gridLayout_3.addWidget(self.h264, 0, 0, 1, 1)

        self.h265 = QRadioButton(self.gridLayoutWidget_2)
        self.h265.setObjectName(u"h265")
        self.h265.setChecked(True)

        self.gridLayout_3.addWidget(self.h265, 1, 0, 1, 1)

        self.groupBox_2 = QGroupBox(self.export_tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(230, 140, 221, 41))
        self.gridLayoutWidget_4 = QWidget(self.groupBox_2)
        self.gridLayoutWidget_4.setObjectName(u"gridLayoutWidget_4")
        self.gridLayoutWidget_4.setGeometry(QRect(10, 10, 211, 31))
        self.gridLayout_5 = QGridLayout(self.gridLayoutWidget_4)
        self.gridLayout_5.setObjectName(u"gridLayout_5")
        self.gridLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_11 = QLabel(self.gridLayoutWidget_4)
        self.label_11.setObjectName(u"label_11")

        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 1)

        self.frame_rate = QLineEdit(self.gridLayoutWidget_4)
        self.frame_rate.setObjectName(u"frame_rate")

        self.gridLayout_5.addWidget(self.frame_rate, 0, 1, 1, 1)

        self.groupBox_3 = QGroupBox(self.export_tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 220, 211, 101))
        self.gridLayoutWidget_3 = QWidget(self.groupBox_3)
        self.gridLayoutWidget_3.setObjectName(u"gridLayoutWidget_3")
        self.gridLayoutWidget_3.setGeometry(QRect(10, 10, 201, 91))
        self.gridLayout_4 = QGridLayout(self.gridLayoutWidget_3)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.gridLayout_4.setContentsMargins(0, 0, 0, 0)
        self.p720 = QRadioButton(self.gridLayoutWidget_3)
        self.p720.setObjectName(u"p720")

        self.gridLayout_4.addWidget(self.p720, 0, 0, 1, 1)

        self.k2 = QRadioButton(self.gridLayoutWidget_3)
        self.k2.setObjectName(u"k2")

        self.gridLayout_4.addWidget(self.k2, 0, 2, 1, 1)

        self.k4 = QRadioButton(self.gridLayoutWidget_3)
        self.k4.setObjectName(u"k4")

        self.gridLayout_4.addWidget(self.k4, 1, 0, 1, 1)

        self.k4_uhd = QRadioButton(self.gridLayoutWidget_3)
        self.k4_uhd.setObjectName(u"k4_uhd")
        self.k4_uhd.setChecked(True)

        self.gridLayout_4.addWidget(self.k4_uhd, 1, 1, 1, 1)

        self.dci_4k = QRadioButton(self.gridLayoutWidget_3)
        self.dci_4k.setObjectName(u"dci_4k")

        self.gridLayout_4.addWidget(self.dci_4k, 1, 2, 1, 1)

        self.p1080 = QRadioButton(self.gridLayoutWidget_3)
        self.p1080.setObjectName(u"p1080")

        self.gridLayout_4.addWidget(self.p1080, 0, 1, 1, 1)

        self.k6 = QRadioButton(self.gridLayoutWidget_3)
        self.k6.setObjectName(u"k6")

        self.gridLayout_4.addWidget(self.k6, 2, 0, 1, 1)

        self.k8 = QRadioButton(self.gridLayoutWidget_3)
        self.k8.setObjectName(u"k8")

        self.gridLayout_4.addWidget(self.k8, 2, 1, 1, 1)

        self.source_res = QRadioButton(self.gridLayoutWidget_3)
        self.source_res.setObjectName(u"source_res")

        self.gridLayout_4.addWidget(self.source_res, 2, 2, 1, 1)

        self.groupBox_5 = QGroupBox(self.export_tab)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(230, 190, 221, 41))
        self.horizontalLayoutWidget_5 = QWidget(self.groupBox_5)
        self.horizontalLayoutWidget_5.setObjectName(u"horizontalLayoutWidget_5")
        self.horizontalLayoutWidget_5.setGeometry(QRect(10, 10, 211, 31))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget_5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.color411 = QRadioButton(self.horizontalLayoutWidget_5)
        self.color411.setObjectName(u"color411")

        self.horizontalLayout_6.addWidget(self.color411)

        self.color422 = QRadioButton(self.horizontalLayoutWidget_5)
        self.color422.setObjectName(u"color422")
        self.color422.setChecked(True)

        self.horizontalLayout_6.addWidget(self.color422)

        self.color444 = QRadioButton(self.horizontalLayoutWidget_5)
        self.color444.setObjectName(u"color444")

        self.horizontalLayout_6.addWidget(self.color444)

        self.groupBox_6 = QGroupBox(self.export_tab)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.groupBox_6.setGeometry(QRect(10, 330, 211, 61))
        self.horizontalLayoutWidget_4 = QWidget(self.groupBox_6)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(10, 0, 201, 61))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.label_9 = QLabel(self.horizontalLayoutWidget_4)
        self.label_9.setObjectName(u"label_9")

        self.horizontalLayout_5.addWidget(self.label_9)

        self.quality_slider = QSlider(self.horizontalLayoutWidget_4)
        self.quality_slider.setObjectName(u"quality_slider")
        self.quality_slider.setMaximum(4)
        self.quality_slider.setValue(2)
        self.quality_slider.setOrientation(Qt.Horizontal)
        self.quality_slider.setInvertedAppearance(False)
        self.quality_slider.setInvertedControls(False)
        self.quality_slider.setTickPosition(QSlider.TicksAbove)

        self.horizontalLayout_5.addWidget(self.quality_slider)

        self.label_10 = QLabel(self.horizontalLayoutWidget_4)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setMinimumSize(QSize(10, 0))

        self.horizontalLayout_5.addWidget(self.label_10)

        self.groupBox_4 = QGroupBox(self.export_tab)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(230, 240, 221, 151))
        self.ffmpeg_inputs_edit = QPlainTextEdit(self.groupBox_4)
        self.ffmpeg_inputs_edit.setObjectName(u"ffmpeg_inputs_edit")
        self.ffmpeg_inputs_edit.setGeometry(QRect(13, 20, 201, 121))
        self.ffmpeg_inputs_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.watch_render_button = QPushButton(self.export_tab)
        self.watch_render_button.setObjectName(u"watch_render_button")
        self.watch_render_button.setGeometry(QRect(540, 280, 111, 31))
        self.tabs.addTab(self.export_tab, "")
        self.image_render = QWidget()
        self.image_render.setObjectName(u"image_render")
        self.horizontalLayoutWidget_6 = QWidget(self.image_render)
        self.horizontalLayoutWidget_6.setObjectName(u"horizontalLayoutWidget_6")
        self.horizontalLayoutWidget_6.setGeometry(QRect(10, 10, 641, 31))
        self.horizontalLayout_7 = QHBoxLayout(self.horizontalLayoutWidget_6)
        self.horizontalLayout_7.setSpacing(10)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.label_12 = QLabel(self.horizontalLayoutWidget_6)
        self.label_12.setObjectName(u"label_12")

        self.horizontalLayout_7.addWidget(self.label_12)

        self.image_render_edit = QLineEdit(self.horizontalLayoutWidget_6)
        self.image_render_edit.setObjectName(u"image_render_edit")

        self.horizontalLayout_7.addWidget(self.image_render_edit)

        self.image_render_button = QPushButton(self.horizontalLayoutWidget_6)
        self.image_render_button.setObjectName(u"image_render_button")

        self.horizontalLayout_7.addWidget(self.image_render_button)

        self.scale_to_fit_checkbox = QCheckBox(self.horizontalLayoutWidget_6)
        self.scale_to_fit_checkbox.setObjectName(u"scale_to_fit_checkbox")

        self.horizontalLayout_7.addWidget(self.scale_to_fit_checkbox)

        self.rendered_image_view = QGraphicsView(self.image_render)
        self.rendered_image_view.setObjectName(u"rendered_image_view")
        self.rendered_image_view.setGeometry(QRect(10, 50, 691, 351))
        self.image_horizontal_scrollbar = QScrollBar(self.image_render)
        self.image_horizontal_scrollbar.setObjectName(u"image_horizontal_scrollbar")
        self.image_horizontal_scrollbar.setGeometry(QRect(9, 380, 691, 20))
        self.image_horizontal_scrollbar.setOrientation(Qt.Horizontal)
        self.image_vertical_scrollbar = QScrollBar(self.image_render)
        self.image_vertical_scrollbar.setObjectName(u"image_vertical_scrollbar")
        self.image_vertical_scrollbar.setGeometry(QRect(680, 49, 20, 331))
        self.image_vertical_scrollbar.setOrientation(Qt.Vertical)
        self.tabs.addTab(self.image_render, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 702, 21))
        self.file_menu = QMenu(self.menubar)
        self.file_menu.setObjectName(u"file_menu")
        self.help_menu = QMenu(self.menubar)
        self.help_menu.setObjectName(u"help_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.file_menu.menuAction())
        self.menubar.addAction(self.help_menu.menuAction())
        self.file_menu.addAction(self.action_open_project)
        self.file_menu.addAction(self.action_save_project)
        self.file_menu.addSeparator()
        self.file_menu.addAction(self.action_exit)
        self.help_menu.addAction(self.action_about)

        self.retranslateUi(MainWindow)

        self.tabs.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"BrilliantImagery", None))
        self.action_open_project.setText(QCoreApplication.translate("MainWindow", u"Open Project", None))
        self.action_save_project.setText(QCoreApplication.translate("MainWindow", u"Save Project", None))
        self.action_exit.setText(QCoreApplication.translate("MainWindow", u"Exit", None))
        self.action_about.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.ramp_image.setText("")
        self.ramp_opperations_box.setTitle(QCoreApplication.translate("MainWindow", u"Opperations To Perform", None))
        self.ramp_checkbox.setText(QCoreApplication.translate("MainWindow", u"Ramp Linear Properties", None))
        self.deflicker_checkbox.setText(QCoreApplication.translate("MainWindow", u"Deflicker", None))
        self.stabilize_checkbox.setText(QCoreApplication.translate("MainWindow", u"Stabilize", None))
        self.data_resue_box.setTitle(QCoreApplication.translate("MainWindow", u"Data Reuse", None))
        self.reuse_offsets_checkbox.setText(QCoreApplication.translate("MainWindow", u"Use Previously Calculated Offsets", None))
        self.reuse_brightness_checkbox.setText(QCoreApplication.translate("MainWindow", u"Use Previously Caluclated Brightnesses", None))
        self.reload_image_button.setText(QCoreApplication.translate("MainWindow", u"Reload Image", None))
        self.ramp_button.setText(QCoreApplication.translate("MainWindow", u"Process", None))
        self.notify_completion_checkbox.setText(QCoreApplication.translate("MainWindow", u"Notify Upon Completion", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sequence Folder:", None))
        self.ramp_folder_button.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.tabs.setTabText(self.tabs.indexOf(self.ramp_tab), QCoreApplication.translate("MainWindow", u"Ramp & Stabilize", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"DNG Sequence Folder:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Output File:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Rendered Image Folder:", None))
        self.dng_folder_button.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.output_file_button.setText(QCoreApplication.translate("MainWindow", u"File", None))
        self.renderd_image_folder_button.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Sequence Stats:", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Image Count:", None))
        self.label_7.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Codec", None))
        self.prores.setText(QCoreApplication.translate("MainWindow", u"ProRes", None))
        self.vp9.setText(QCoreApplication.translate("MainWindow", u"VP9", None))
        self.h264.setText(QCoreApplication.translate("MainWindow", u"H.264 (MPEG-4)", None))
        self.h265.setText(QCoreApplication.translate("MainWindow", u"H.265 (MPEG-H, HEVC)", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Playback", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Frame Rate (fps)", None))
        self.frame_rate.setText(QCoreApplication.translate("MainWindow", u"29.97", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MainWindow", u"Resolution", None))
        self.p720.setText(QCoreApplication.translate("MainWindow", u"720p", None))
        self.k2.setText(QCoreApplication.translate("MainWindow", u"2K", None))
        self.k4.setText(QCoreApplication.translate("MainWindow", u"3K", None))
        self.k4_uhd.setText(QCoreApplication.translate("MainWindow", u"4K UHD", None))
        self.dci_4k.setText(QCoreApplication.translate("MainWindow", u"DCI 4K", None))
        self.p1080.setText(QCoreApplication.translate("MainWindow", u"1080p", None))
        self.k6.setText(QCoreApplication.translate("MainWindow", u"6K", None))
        self.k8.setText(QCoreApplication.translate("MainWindow", u"8K", None))
        self.source_res.setText(QCoreApplication.translate("MainWindow", u"Source", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Color Sampling", None))
        self.color411.setText(QCoreApplication.translate("MainWindow", u"4:1:1", None))
        self.color422.setText(QCoreApplication.translate("MainWindow", u"4:2:2", None))
        self.color444.setText(QCoreApplication.translate("MainWindow", u"4:4:4", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"Compression Quality", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Lo", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Hi", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MainWindow", u"FFmpeg Inputs", None))
        self.watch_render_button.setText(QCoreApplication.translate("MainWindow", u"Watch / Render", None))
        self.tabs.setTabText(self.tabs.indexOf(self.export_tab), QCoreApplication.translate("MainWindow", u"Video Export", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Imate:", None))
        self.image_render_button.setText(QCoreApplication.translate("MainWindow", u"Image", None))
        self.scale_to_fit_checkbox.setText(QCoreApplication.translate("MainWindow", u"Scale to Fit", None))
        self.tabs.setTabText(self.tabs.indexOf(self.image_render), QCoreApplication.translate("MainWindow", u"Image Render", None))
        self.file_menu.setTitle(QCoreApplication.translate("MainWindow", u"File", None))
        self.help_menu.setTitle(QCoreApplication.translate("MainWindow", u"Help", None))
    # retranslateUi

