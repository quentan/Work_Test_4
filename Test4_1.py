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
        """
        In practial application, a rendering scene should have only ONE volume actor,
        ONE or TWO isosurface actors, FOUR to FIVE image planes.
        """

        super(Basic, self).__init__()

        self.reader = None
        self.path_name = None

        self.actor_iso = None
        self.actor_iso_2 = None  # Not used now
        self.actor_vol = None

        self.plane_x = None
        self.plane_y = None
        self.plane_z = None

        self.plane = None  # For single vtkImagePlaneWidget

        self.info = None

        self.init_ui()

    def init_ui(self):

        self.ui = ui_main_window.Ui_MainWindow()
        self.ui.setup_ui(self)

        self.ren = vtk.vtkRenderer()

        self.ren_win = self.ui.vtk_widget.GetRenderWindow()
        self.ren_win.AddRenderer(self.ren)

        self.iren = self.ren_win.GetInteractor()
        self.iren.Initialize()

        self.ui.open_folder_radio.clicked[bool].connect(self.on_open_folder)
        self.ui.open_file_radio.clicked[bool].connect(self.on_open_file)
        self.ui.test_btn.clicked.connect(self.on_test_btn)
        # self.ui.volume_btn.clicked.connect(self.on_volume_btn)
        self.ui.vol_cbox.stateChanged.connect(self.on_volume_cbox)
        self.ui.iso_cbox.stateChanged.connect(self.on_iso_cbox)
        self.ui.plane_cbox.stateChanged.connect(self.on_plane_cbox)
        self.ui.reset_camera_btn.clicked.connect(self.on_reset_camera_btn)

        self.marker = Marker(self.iren)  # Annotation Cube
        self.marker.show()
        # self.ui.annotationChk.toggle()

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

        path = QtGui.QFileDialog.getExistingDirectory(
            self, 'Open DICOM Folder', QtCore.QDir.currentPath(),
            QtGui.QFileDialog.ShowDirsOnly)

        self._read(path)

        # Test
        # min, max = self.reader.get_value_range()
        # self.ui.test_spin.setMinimum(min)
        # self.ui.test_spin.setMaximum(max)
        # self.ui.test_spin.setSingleStep(50)
        # self.ui.test_spin.setValue(int(max - (max - min) * 0.618))

        # self.better_camera()
        # self.ren_win.Render()

    def on_open_file(self):

        path = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Meta Image', QtCore.QDir.currentPath(),
            'Meta Image (*.mha *.mhd)')

        self._read(path)

    def _read(self, path):
        """
        Common thing of reading image(s)
        """
        path = str(path)
        # assert path, 'No file selected.'  # Debug
        logging.info('No file or folder selected.')

        try:
            not path
        except IOError, e:
            print IOError, e

        # For the first time file reading
        if not self.path_name and path:
            self.path_name = path

        # After the first file reading
        elif self.is_path_changed(path) and path:

            if self.actor_vol:
                self.reader.remove_actor(self.ren, self.actor_vol)
                self.actor_vol = None  # Don't forget this!

            if self.actor_iso:
                self.reader.remove_actor(self.ren, self.actor_iso)
                self.actor_iso = None

            if self.plane_x:
                self.plane_x.Off()
                self.plane_x = None

            if self.plane_y:
                self.plane_y.Off()
                self.plane_y = None

            if self.plane_z:
                self.plane_z.Off()
                self.plane_z = None

            if self.reader:  # If there was a reader, delete it
                del self.reader

        self.path_name = path

        self.reader = MedicalObject()
        self.reader.read(self.path_name)

        self.info = self.reader.get_info()

        self.ui.vol_cbox.setCheckable(True)
        self.ui.iso_cbox.setCheckable(True)
        self.ui.plane_cbox.setCheckable(True)

        self.ui.vol_cbox.setChecked(False)
        self.ui.iso_cbox.setChecked(False)
        self.ui.plane_cbox.setChecked(False)

    def on_volume_cbox(self, state):

        if self.reader is not None:
            logging.info('"self.reader" exists.')

            if self.actor_vol is None:
                self.actor_vol = self.reader.get_volume()
                self.reader.add_actor(self.ren, self.actor_vol)

            if state == QtCore.Qt.Checked:
                self.actor_vol.VisibilityOn()

            else:
                self.actor_vol.VisibilityOff()

            self.ren.ResetCamera()
            self.ren_win.Render()

    def on_iso_cbox(self, state):

        # if self.path_name:
        if self.reader is not None:
            logging.info('"self.reader" exists.')

            if self.actor_iso is None:
                self.actor_iso = self.reader.get_isosurface(500)
                self.reader.add_actor(self.ren, self.actor_iso)

            if state == QtCore.Qt.Checked:
                self.actor_iso.VisibilityOn()

            else:
                self.actor_iso.VisibilityOff()

            self.ren.ResetCamera()
            self.ren_win.Render()

    def on_plane_cbox(self, state):

        if self.reader is not None:
            logging.info('"self.reader" exists.')

            dims = self.info['dims']

            if self.plane_x is None:
                self.plane_x = self.reader.get_plane(
                    axis=0, slice_idx=dims[0] / 2, color=[1, 0, 0], key='x')
                self.plane_x.SetInteractor(self.iren)

            if self.plane_y is None:
                self.plane_y = self.reader.get_plane(
                    axis=1, slice_idx=dims[1] / 2, color=[1, 1, 0], key='y')
                self.plane_y.SetInteractor(self.iren)

            if self.plane_z is None:
                self.plane_z = self.reader.get_plane(
                    axis=2, slice_idx=dims[2] / 2, color=[0, 0, 1], key='z')
                self.plane_z.SetInteractor(self.iren)

            if state == QtCore.Qt.Checked:
                self.plane_x.On()
                self.plane_y.On()
                self.plane_z.On()

            else:
                self.plane_x.Off()
                self.plane_y.Off()
                self.plane_z.Off()

            self.ren.ResetCamera()
            self.ren_win.Render()

    def on_reset_camera_btn(self):

        self.ren.ResetCamera()

    def better_camera(self):

        self.ren.ResetCamera()
        cam = self.ren.GetActiveCamera()
        cam.Elevation(110)
        cam.SetViewUp(0, 0, -1)
        cam.Azimuth(45)
        self.ren.ResetCameraClippingRange()

    def is_path_changed(self, path):

        # import os.path

        # try:
        #     os.path.exist(path)
        # except IOError, e:
        #     print 'IOError:', e

        if self.path_name == path:
            return False

        else:
            return True

    def close_image(self):

        del self.reader
        self.reader = None

    def is_changed(self, obj):
        pass

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
