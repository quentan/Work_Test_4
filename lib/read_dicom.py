# -*- coding: utf-8 -*-

# Class of reading DICOMs, from folder

import sys
import vtk
import SimpleITK as sitk

from vtk.util import numpy_support

from read_image import read_image


class read_dicom(read_image):

    def __init__(self, path_dicom, cast_type=11):

        super(read_dicom, self).__init__()

        reader = sitk.ImageSeriesReader()
        filename_dicom = reader.GetGDCMSeriesFileNames(path_dicom)

        reader.SetFileNames(filename_dicom)

        img_sitk = reader.Execute()
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
        if cast_type == 0:
            return img_vtk

        elif cast_type in [i for i in range(2, 12)]:
            self.cast.SetInputData(img_vtk)
            self.cast.SetOutputScalarType(cast_type)
            self.cast.Update()

            return self.cast.GetOutput()  # is a vtkImageData

        else:
            sys.stderr.write(
                'Wrong Cast Type! It should be 2, 3, ..., 11\nNo Image Cast Applied')
            return img_vtk
