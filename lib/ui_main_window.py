# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Ui_MainWindow(object):

    def setup_ui(self, main_window):

        exitAction = QtGui.QAction(
            QtGui.QIcon('exit.png'), 'E&xit', main_window)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit Application')
        exitAction.triggered.connect(main_window.close)

        # Menu
        self.menubar = QtGui.QMenuBar(main_window)
        self.menubar.setNativeMenuBar(False)
        self.file_menu = self.menubar.addMenu('&File')
        self.file_menu.addAction(exitAction)
        main_window.setMenuBar(self.menubar)

        # Status Bar
        self.statusbar = QtGui.QStatusBar(main_window)
        self.statusbar.showMessage('Ready')
        main_window.setStatusBar(self.statusbar)

        main_window.setObjectName('Main Window')
        main_window.resize(640, 480)

        self.central_widget = QtGui.QWidget(main_window)
        self.gridlayout = QtGui.QGridLayout(self.central_widget)

        # Widgets
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        self.vtk_widget.setStatusTip('VTK Rendering Pane')

        self.open_dicom_btn = QtGui.QPushButton('&Open DICOM folder')
        self.open_meta_btn = QtGui.QPushButton('Open Meta Image')

        self.test_btn = QtGui.QPushButton('Test Image Loading')

        # Layout of widgets
        self.gridlayout.addWidget(self.vtk_widget, 2, 0, 10, 1)
        self.gridlayout.addWidget(self.open_dicom_btn, 2, 1)
        self.gridlayout.addWidget(self.open_meta_btn, 3, 1)

        self.gridlayout.addWidget(self.test_btn, 10, 1)

        main_window.setCentralWidget(self.central_widget)
