# -*- coding: utf-8 -*-

"""
Basic superclass
"""

import sys
import vtk
import SimpleITK as sitk

from vtk.util import numpy_support


class MedicalObject(object):

    def __init__(self):
        '''
        Basic elements for Medical Object rendering
        '''
        self.reader = vtk.vtkImageData()

        self.dims = self.reader.GetDimensions()
        self.bounds = self.reader.GetBounds()
        self.spacing = self.reader.GetSpacing()
        self.origin = self.reader.GetOrigin()
        self.value_range = self.reader.GetScalarRange()

        self.flag_read = False

    def read_dicom(self, path_dicom, cast_type=11):

        reader_dicom = sitk.ImageSeriesReader()
        filename_dicom = reader_dicom.GetGDCMSeriesFileNames(path_dicom)

        reader_dicom.SetFileNames(filename_dicom)

        img_sitk = reader_dicom.Execute()
        spacing = img_sitk.GetSpacing()

        # Convert SimpleITK image to numpy image
        # array_np is a numpy array
        array_np = sitk.GetArrayFromImage(img_sitk)

        # Convert numpy array to VTK array (vtkDoubleArray)
        array_vtk = numpy_support.numpy_to_vtk(
            num_array=array_np.transpose(2, 1, 0).ravel(),
            deep=True,
            array_type=vtk.VTK_DOUBLE)

        # Convert VTK array to VTK image (vtkImageData)
        img_vtk = vtk.vtkImageData()
        img_vtk.SetDimensions(array_np.shape)
        img_vtk.SetSpacing(spacing[::-1])  # Reverse the order
        img_vtk.GetPointData().SetScalars(array_vtk)  # is a vtkImageData

        # VTK image cast
        img_cast = vtk.vtkImageCast()
        if cast_type == 0:
            self.reader = img_vtk

        elif cast_type in [i for i in range(2, 12)]:
            img_cast.SetInputData(img_vtk)
            img_cast.SetOutputScalarType(cast_type)
            img_cast.Update()

            self.reader = img_cast.GetOutput()

        else:
            sys.stderr.write(
                ('Wrong Cast Type! It should be 2, 3, ..., 11\n')
                ('No Image Cast Applied')
            )
            self.reader = img_vtk

        self.flag_read = True

        return self.reader

    def read_metaimage(self, fname_meta, cast_type=5):

        reader = vtk.vtkMetaImageReader()
        reader.SetFileName(fname_meta)

        # VTK image cast
        img_cast = vtk.vtkImageCast()
        if cast_type == 0:
            # return a vtkImageData with wrong dims and bounds value
            self.reader = reader.GetOutput()
            # return reader.GetOutput()

        elif cast_type in [i for i in range(2, 12)]:
            img_cast.SetInputConnection(reader.GetOutputPort())
            img_cast.SetOutputScalarType(cast_type)
            img_cast.Update()
            self.reader = img_cast.GetOutput()
            # return img_cast.GetOutput()  # a vtkImageData

        else:
            sys.stderr.write(
                ('Wrong Cast Type! It should be 2, 3, ..., 11\n')
                ('No Image Cast Applied')
            )
            self.reader = img_cast.GetOutput()
            # return reader.GetOutput()

        self.flag_read = True

        return self.reader

    def get_isosurface(self, iso_value=500):

        if not self.flag_read:

            sys.stderr.write('No Image Loaded.')
            return

        contour = vtk.vtkContourFilter()
        normals = vtk.vtkPolyDataNormals()
        stripper = vtk.vtkStripper()
        mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

        contour.SetInputData(self.reader)
        contour.SetValue(0, iso_value)

        normals.SetInputConnection(contour.GetOutputPort())
        normals.SetFeatureAngle(60.0)
        normals.ReleaseDataFlagOn()

        stripper.SetInputConnection(normals.GetOutputPort())
        stripper.ReleaseDataFlagOn()

        mapper.SetInputConnection(stripper.GetOutputPort())
        mapper.SetScalarVisibility(False)

        self.actor.SetMapper(mapper)

        # Default colour, should be changed.
        self.actor.GetProperty().SetDiffuseColor(
            [247.0 / 255.0, 150.0 / 255.0, 155.0 / 255.0])  # Look like red
        self.actor.GetProperty().SetSpecular(0.3)
        self.actor.GetProperty().SetSpecularPower(20)

    def render(self, renderer):

        renderer.AddActor(self.actor)

    def clean(self, renderer):

        renderer.RemoveActor(self.actor)

    def get_value_range(self):

        value_range = self.reader.GetScalarRange()
        return value_range
