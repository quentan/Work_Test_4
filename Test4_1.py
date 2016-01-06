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
from lib import read_image
from lib import volume_rendering


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

        self.reader = read_image.ReadImage()

        self.ui.open_dicom_btn.clicked.connect(self.on_open_dicom_folder)
        self.ui.open_meta_btn.clicked.connect(self.on_open_metaimage)
        self.ui.test_btn.clicked.connect(self.on_test_btn)

        self.move(100, 100)
        self.show()

    def show_isosurface(vtk_source):

        actor = vtk.vtkActor()
        mapper = vtk.vtkPolyDataMapper()

        isosurface = volume_rendering.Isosurface(
            self.ren, actor, mapper, vtk_source, 500)

    # Event Response Function
    def on_open_dicom_folder(self):

        folder_name = QtGui.QFileDialog.getExistingDirectory(
            self, 'Open DICOM Folder', QtCore.QDir.currentPath(),
            QtGui.QFileDialog.ShowDirsOnly)
        folder_name = str(folder_name)  # QString --> Python String
        logging.info('No folder selected.')

        if folder_name:
            dicom_reader = read_image.ReadImage()
            dicom = dicom_reader.read_dicom(folder_name)
            # dicom = self.reader.read_dicom(folder_name)

            # isosurface = volume_rendering.Iso_test(
            #     self.ren, dicom, iso_value=500)

            contour = vtk.vtkContourFilter()
            normals = vtk.vtkPolyDataNormals()
            stripper = vtk.vtkStripper()
            mapper = vtk.vtkPolyDataMapper()
            actor = vtk.vtkActor()

            # contour.SetInputConnection(dicom.GetOutputPort())
            contour.SetInputData(dicom)
            contour.SetValue(0, 500)

            normals.SetInputConnection(contour.GetOutputPort())
            normals.SetFeatureAngle(60.0)
            normals.ReleaseDataFlagOn()

            stripper.SetInputConnection(normals.GetOutputPort())
            stripper.ReleaseDataFlagOn()

            mapper.SetInputConnection(stripper.GetOutputPort())

            actor.SetMapper(mapper)

            self.ren.AddActor(actor)

            self.ren.ResetCamera()
            self.ren_win.Render()

    def on_open_metaimage(self):

        file_name = QtGui.QFileDialog.getOpenFileName(
            self, 'Open Meta Image', QtCore.QDir.currentPath(),
            'Meta Image (*.mha *.mhd)')

        file_name = str(file_name)
        # assert file_name, 'No file selected.'  # Debug
        logging.info('No file selected.')

        if file_name:  # if file_name is not an empty string
            # meta = self.reader.read_metaimage(file_name)
            reader = vtk.vtkMetaImageReader()
            reader.SetFileName(file_name)

            cast = vtk.vtkImageCast()
            # cast.SetInputData(img_vtk)
            cast.SetInputConnection(reader.GetOutputPort())
            cast.SetOutputScalarType(5)
            cast.Update()
            meta = cast.GetOutput()  # The output of `cast` is a vtkImageData
            # meta = reader.GetOutput()

            # isosurface = volume_rendering.Iso_test(self.ren, meta, -500)
            contour = vtk.vtkContourFilter()
            normals = vtk.vtkPolyDataNormals()
            stripper = vtk.vtkStripper()
            mapper = vtk.vtkPolyDataMapper()
            actor = vtk.vtkActor()

            contour.SetInputData(meta)
            contour.SetValue(0, 500)

            normals.SetInputConnection(contour.GetOutputPort())
            normals.SetFeatureAngle(60.0)
            normals.ReleaseDataFlagOn()

            stripper.SetInputConnection(normals.GetOutputPort())
            stripper.ReleaseDataFlagOn()

            mapper.SetInputConnection(stripper.GetOutputPort())

            actor.SetMapper(mapper)

            self.ren.AddActor(actor)

            self.ren.ResetCamera()
            self.ren_win.Render()

    def on_test_btn(self):

        from vtk.util.misc import vtkGetDataRoot
        VTK_DATA_ROOT = vtkGetDataRoot()

        v16 = vtk.vtkVolume16Reader()
        v16.SetDataDimensions(64, 64)
        v16.SetDataByteOrderToLittleEndian()
        v16.SetFilePrefix(VTK_DATA_ROOT + "/Data/headsq/quarter")
        v16.SetImageRange(1, 93)
        v16.SetDataSpacing(3.2, 3.2, 1.5)

        skinExtractor = vtk.vtkContourFilter()
        skinExtractor.SetInputConnection(v16.GetOutputPort())
        skinExtractor.SetValue(0, 500)
        skinNormals = vtk.vtkPolyDataNormals()
        skinNormals.SetInputConnection(skinExtractor.GetOutputPort())
        skinNormals.SetFeatureAngle(60.0)
        skinMapper = vtk.vtkPolyDataMapper()
        skinMapper.SetInputConnection(skinNormals.GetOutputPort())
        skinMapper.ScalarVisibilityOff()
        skin = vtk.vtkActor()
        skin.SetMapper(skinMapper)

        self.ren.AddActor(skin)
        self.ren.ResetCamera()
        self.ren_win.Render()

    # Auxiliary Function
    def better_camera(self):

        self.ren.ResetCamera()

if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Basic()
    sys.exit(app.exec_())
