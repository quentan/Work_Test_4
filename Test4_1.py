#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Code rule:
# http://zh-google-styleguide.readthedocs.org/en/latest/google-python-styleguide/python_style_rules/

import sys
import vtk
import logging
logging.basicConfig(level=logging.INFO)

from PyQt4 import QtGui
from PyQt4 import QtCore

from lib import ui_main_window
from lib.medical_object import MedicalObject
from lib.annotation_cube import Marker


class Basic(QtGui.QMainWindow):

    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self):

        super(Basic, self).__init__()

        self.init_ui()

    def init_ui(self):

        self.ui = ui_main_window.Ui_MainWindow()
        self.ui.setup_ui(self)

        self.ren = vtk.vtkRenderer()

        self.ren_win = self.ui.vtk_widget.GetRenderWindow()
        self.ren_win.AddRenderer(self.ren)

        self.iren = self.ren_win.GetInteractor()
        self.iren.Initialize()

        self.ui.open_dicom_btn.clicked.connect(self.on_open_dicom_folder)
        self.ui.open_meta_btn.clicked.connect(self.on_open_metaimage)
        self.ui.test_btn.clicked.connect(self.on_test_btn)

        self.marker = Marker(self.iren)  # Annotation Cube
        self.marker.show()
        # self.ui.annotationChk.toggle()

        self.move(100, 100)
        self.show()

    # Event Response Function
    def on_open_dicom_folder(self):

        folder_name = QtGui.QFileDialog.getExistingDirectory(
            self, 'Open DICOM Folder', QtCore.QDir.currentPath(),
            QtGui.QFileDialog.ShowDirsOnly)
        folder_name = str(folder_name)  # QString --> Python String
        logging.info('No folder selected.')

        if folder_name:

            reader = MedicalObject()
            reader.read_dicom(folder_name)
            reader.get_isosurface(500)
            reader.render(self.ren)

            self.better_camera()
            self.ren_win.Render()

    def on_open_metaimage(self):

        file_name = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Meta Image', QtCore.QDir.currentPath(),
            'Meta Image (*.mha *.mhd)')

        file_name = str(file_name)
        # assert file_name, 'No file selected.'  # Debug
        logging.info('No file selected.')

        if file_name:  # if file_name is not an empty string

            reader = MedicalObject()
            reader.read_metaimage(file_name)
            reader.get_isosurface(500)
            reader.render(self.ren)

            self.better_camera()
            self.ren_win.Render()

    def on_test_btn(self):

        pass

    def better_camera(self):

        self.ren.ResetCamera()
        cam = self.ren.GetActiveCamera()
        cam.Elevation(110)
        cam.SetViewUp(0, 0, -1)
        cam.Azimuth(45)
        self.ren.ResetCameraClippingRange()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Basic()
    sys.exit(app.exec_())
