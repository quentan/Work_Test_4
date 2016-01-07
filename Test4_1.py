#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Code rule:
# http://zh-google-styleguide.readthedocs.org/en/latest/google-python-styleguide/python_style_rules/

import sys
import vtk
import logging
# logging.basicConfig(level=logging.INFO)

from PyQt4 import QtGui
from PyQt4 import QtCore

from inc import ui_main_window
from inc.medical_object import MedicalObject
from inc.annotation_cube import Marker


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

        self.ui.open_folder_btn.clicked[bool].connect(self.on_open_folder)
        self.ui.open_file_btn.clicked.connect(self.on_open_file)
        self.ui.test_btn.clicked.connect(self.on_test_btn)
        # self.ui.volume_btn.clicked.connect(self.on_volume_btn)
        self.ui.vol_cbox.stateChanged.connect(self.on_volume_cbox)

        self.marker = Marker(self.iren)  # Annotation Cube
        self.marker.show()
        # self.ui.annotationChk.toggle()

        self.path_name = None
        self.ui.vol_cbox.setCheckable(False)
        self.ui.iso_cbox.setCheckable(False)
        self.ui.plane_cbox.setCheckable(False)

        # TEST
        # self.ui.test_spin.value = 500
        self.ui.test_spin.valueChanged.connect(self.on_test_spin)

        self.move(100, 100)
        self.setWindowTitle('Prototype')
        self.show()

    # Event Response Function
    def on_open_folder(self):

        if self.ui.open_file_btn.isChecked():
            return

        folder_name = QtGui.QFileDialog.getExistingDirectory(
            self, 'Open DICOM Folder', QtCore.QDir.currentPath(),
            QtGui.QFileDialog.ShowDirsOnly)
        folder_name = str(folder_name)  # QString --> Python String
        logging.info('No folder selected.')

        self.path_name = folder_name

        if folder_name:

            self.ui.open_file_btn.setChecked(False)
            self.ui.open_folder_btn.setChecked(True)

            self.ui.vol_cbox.setCheckable(True)
            self.ui.iso_cbox.setCheckable(True)
            self.ui.plane_cbox.setCheckable(True)

            # self.reader = MedicalObject()
            # self.reader.read_dicom(folder_name)
            # self.reader.get_isosurface(500)
            # self.reader.render(self.ren)

            # Test
            # min, max = self.reader.get_value_range()
            # self.ui.test_spin.setMinimum(min)
            # self.ui.test_spin.setMaximum(max)
            # self.ui.test_spin.setSingleStep(50)
            # self.ui.test_spin.setValue(int(max - (max - min) * 0.618))

            # self.better_camera()
            # self.ren_win.Render()

    def on_open_file(self):

        file_name = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Meta Image', QtCore.QDir.currentPath(),
            'Meta Image (*.mha *.mhd)')

        file_name = str(file_name)
        # assert file_name, 'No file selected.'  # Debug
        logging.info('No file selected.')

        self.path_name = file_name

        if file_name:  # if file_name is not an empty string

            reader = MedicalObject()
            reader.read_metaimage(file_name)
            reader.get_isosurface(500)
            reader.render(self.ren)

            self.better_camera()
            self.ren_win.Render()

    def on_volume_cbox(self, state):

        if self.path_name:
            if state == QtCore.Qt.Checked:
                self.reader = MedicalObject()
                self.reader.read_dicom(self.path_name)
                self.reader.get_volume()
                self.reader.render(self.ren)

                self.better_camera()
                self.ren_win.Render()

            else:
                self.reader.clean(self.ren)
                self.ren_win.Render()

    def better_camera(self):

        self.ren.ResetCamera()
        cam = self.ren.GetActiveCamera()
        cam.Elevation(110)
        cam.SetViewUp(0, 0, -1)
        cam.Azimuth(45)
        self.ren.ResetCameraClippingRange()

    # TEST
    def on_test_btn(self):
        pass

    def on_test_spin(self):

        value = self.ui.test_spin.value()

        self.reader.clean(self.ren)
        self.reader.get_isosurface(value)
        self.reader.render(self.ren)

        # self.better_camera()
        self.ren.ResetCamera()
        self.ren_win.Render()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Basic()
    sys.exit(app.exec_())
