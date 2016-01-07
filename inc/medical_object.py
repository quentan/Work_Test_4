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
        self.actor_iso = vtk.vtkActor()

        contour.SetInputData(self.reader)
        contour.SetValue(0, iso_value)

        normals.SetInputConnection(contour.GetOutputPort())
        normals.SetFeatureAngle(60.0)
        normals.ReleaseDataFlagOn()

        stripper.SetInputConnection(normals.GetOutputPort())
        stripper.ReleaseDataFlagOn()

        mapper.SetInputConnection(stripper.GetOutputPort())
        mapper.SetScalarVisibility(False)

        self.actor_iso.SetMapper(mapper)

        # Default colour, should be changed.
        self.actor_iso.GetProperty().SetDiffuseColor(
            [247.0 / 255.0, 150.0 / 255.0, 155.0 / 255.0])  # Look like red
        self.actor_iso.GetProperty().SetSpecular(0.3)
        self.actor_iso.GetProperty().SetSpecularPower(20)

    def get_volume(self, color_file=None, volume_opacity=0.25):
        '''
        Default Volume Rendering
        '''
        transfer_func = self.get_transfer_functioin(color_file, volume_opacity)
        prop_volume = vtk.vtkVolumeProperty()
        prop_volume.ShadeOff()
        prop_volume.SetColor(transfer_func[0])
        prop_volume.SetScalarOpacity(transfer_func[1])
        prop_volume.SetGradientOpacity(transfer_func[2])
        prop_volume.SetInterpolationTypeToLinear()
        prop_volume.SetAmbient(0.4)
        prop_volume.SetDiffuse(0.6)
        prop_volume.SetSpecular(0.2)

        mapper = vtk.vtkSmartVolumeMapper()
        mapper.SetRequestedRenderMode(0)
        # mapper = vtk.vtkGPUVolumeRayCastMapper()
        mapper.SetInputData(self.reader)

        self.actor = vtk.vtkVolume()
        self.actor.SetMapper(mapper)

        self.actor.SetProperty(prop_volume)

    def render(self, renderer):

        renderer.AddActor(self.actor)

    def clean(self, renderer):

        renderer.RemoveActor(self.actor)

    def get_value_range(self):

        return self.reader.GetScalarRange()

    def get_transfer_functioin(self, color_file=None, volume_opacity=0.25):
        '''
        It is for volume rendering.
        Calculate transfer function from color file.
        Generate default transfer functions if no color file given.
        '''
        if color_file:  # Color file is given

            import csv
            fid = open(color_file, "r")
            reader_color = csv.reader(fid)

            dict_RGB = {}
            for line in reader_color:
                dict_RGB[int(line[0])] = [float(line[2]) / 255.0,
                                          float(line[3]) / 255.0,
                                          float(line[4]) / 255.0]
            fid.close()

            # Define colour transfer function
            color_transfor = vtk.vtkColorTransferFunction()

            for idx in dict_RGB.keys():
                color_transfor.AddRGBPoint(idx,
                                           dict_RGB[idx][0],
                                           dict_RGB[idx][1],
                                           dict_RGB[idx][2])

            # Opacity transfer function
            opacity_scalar = vtk.vtkPiecewiseFunction()

            for idx in dict_RGB.keys():
                opacity_scalar.AddPoint(
                    idx, volume_opacity if idx != 0 else 0.0)

            # Opacity Gradient Transfer function
            opacity_gradient = vtk.vtkPiecewiseFunction()
            opacity_gradient.AddPoint(1, 0.0)
            opacity_gradient.AddPoint(5, 0.1)
            opacity_gradient.AddPoint(100, 1.0)

            return color_transfor, opacity_scalar, opacity_gradient

        else:  # Default color transfer functions

            # min, max = self.get_value_range()
            color_transfor = vtk.vtkColorTransferFunction()
            color_transfor.AddRGBPoint(0,    0.0, 0.0, 0.0)
            color_transfor.AddRGBPoint(500,  1.0, 0.5, 0.3)
            color_transfor.AddRGBPoint(1000, 1.0, 0.5, 0.3)
            color_transfor.AddRGBPoint(1150, 1.0, 1.0, 0.9)

            # The opacity transfer function is used to control the opacity
            # of different tissue types.
            opacity_scalar = vtk.vtkPiecewiseFunction()
            opacity_scalar.AddPoint(0,    0.00)
            opacity_scalar.AddPoint(500,  0.15)
            opacity_scalar.AddPoint(1000, 0.15)
            opacity_scalar.AddPoint(1150, 0.85)

            # The gradient opacity function is used to decrease the opacity
            # in the "flat" regions of the volume while maintaining the opacity
            # at the boundaries between tissue types.  The gradient is measured
            # as the amount by which the intensity changes over unit distance.
            # For most medical data, the unit distance is 1mm.
            opacity_gradient = vtk.vtkPiecewiseFunction()
            opacity_gradient.AddPoint(0,   0.0)
            opacity_gradient.AddPoint(90,  0.5)
            opacity_gradient.AddPoint(100, 1.0)

            return color_transfor, opacity_scalar, opacity_gradient
