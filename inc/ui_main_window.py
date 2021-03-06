#!/usr/bin/env python
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
        self.gridlayout.setSpacing(5)

        # Widgets
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)
        self.vtk_widget.setStatusTip('VTK Rendering Pane')

        # QGroupBox with 2 Buttons. For file/folder open
        self.open_gbox = QtGui.QGroupBox('Open Image')
        self.open_folder_radio = QtGui.QRadioButton('Folder')
        self.open_folder_radio.setCheckable(True)
        self.open_folder_radio.setStatusTip('Open DICOM folder')
        self.open_file_radio = QtGui.QRadioButton('File')
        self.open_file_radio.setCheckable(True)
        self.open_file_radio.setStatusTip('Open single medical image')
        # hbox: Horizontal Box
        self.open_hboxlayout = QtGui.QHBoxLayout(self.open_gbox)
        self.open_hboxlayout.setSpacing(3)
        self.open_hboxlayout.addWidget(self.open_folder_radio)
        self.open_hboxlayout.addWidget(self.open_file_radio)

        # For 3 vtkImagePlaneWidget
        self.plane_gbox = QtGui.QGroupBox()
        # self.plane_gbox.setStyleSheet("QGroupBox {border: 0, solid;\
        #                                           }")
        self.plane_x_cbox = QtGui.QCheckBox('X')  # x-plane
        self.plane_y_cbox = QtGui.QCheckBox('Y')
        self.plane_z_cbox = QtGui.QCheckBox('Z')
        self.plane_hboxlayout = QtGui.QHBoxLayout(self.plane_gbox)
        # self.plane_hboxlayout.setSpacing(3)
        # self.plane_hboxlayout.addStretch(1)
        self.plane_hboxlayout.addWidget(self.plane_x_cbox)
        self.plane_hboxlayout.addWidget(self.plane_y_cbox)
        self.plane_hboxlayout.addWidget(self.plane_z_cbox)

        # QGroupBox with 3 QCheckBox. For rendering
        self.render_gbox = QtGui.QGroupBox('Rendering')  # gbox: Group Box
        self.vol_cbox = QtGui.QCheckBox('Volume')  # cbox: Check Box
        self.iso_cbox = QtGui.QCheckBox('Isosurface')
        self.plane_cbox = QtGui.QCheckBox('Planes')
        # vbox: Vertical Box
        self.render_vboxlayout = QtGui.QVBoxLayout(self.render_gbox)
        self.render_vboxlayout.addWidget(self.vol_cbox)
        self.render_vboxlayout.addWidget(self.iso_cbox)
        self.render_vboxlayout.addWidget(self.plane_cbox)
        # self.render_vboxlayout.addWidget(self.plane_gbox)

        # Reset Camera Button
        self.reset_camera_btn = QtGui.QPushButton('Reset Camera')

        # Layout of widgets
        self.gridlayout.addWidget(self.vtk_widget, 2, 0, 10, 1)
        self.gridlayout.addWidget(self.open_gbox, 2, 1)
        self.gridlayout.addWidget(self.render_gbox, 3, 1)

        self.gridlayout.addWidget(self.reset_camera_btn, 9, 1)

        # TEST
        self.test_btn = QtGui.QPushButton('Test Button')
        self.gridlayout.addWidget(self.test_btn, 10, 1)
        self.test_spin = QtGui.QSpinBox()
        self.gridlayout.addWidget(self.test_spin, 11, 1)

        main_window.setCentralWidget(self.central_widget)

if __name__ == '__main__':
    '''
    Make the UI executable to debug it.
    '''
    import sys
    app = QtGui.QApplication(sys.argv)
    w = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(w)
    w.show()
    sys.exit(app.exec_())
