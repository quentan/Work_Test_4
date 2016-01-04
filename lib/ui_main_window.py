# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from vtk.qt4.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


class Ui_MainWindow(object):

    def setup_ui(self, main_window):

        main_window.setObjectName('Main Window')
        main_window.resize(640, 480)

        self.central_widget = QtGui.QWidget(main_window)
        self.gridlayout = QtGui.QGridLayout(self.central_widget)

        # Widgets
        self.vtk_widget = QVTKRenderWindowInteractor(self.central_widget)

        # Layout of widgets
        self.gridlayout.addWidget(self.vtk_widget, 2, 0, 10, 1)

        main_window.setCentralWidget(self.central_widget)
