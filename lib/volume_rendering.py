# -*- coding: utf-8 -*-

# Class of normal Volume Rendering


import vtk
from scene_object import SceneObject
from medical_object import MedicalObject


class Rendering(SceneObject):

    '''
    Common properties of 3D rendering
    '''

    def __init__(self, renderer, actor, mapper):

        super(Rendering, self).__init__(renderer)

        self.vtk_actor = actor
        self.vtk_mapper = mapper

        self.vtk_actor.SetMapper(mapper)


class VolumeRendering(MedicalObject):

    def __init__(self, volume_renderer, volume_actor, volume_mapper):

        super(VolumeRendering, self).__init__(
            self, volume_renderer, volume_actor, volume_mapper)


class Isosurface(MedicalObject):

    def __init__(self, isosurf_renderer, isosurf_actor, isosurf_mapper,
                 vtk_source, iso_value=-500):

        super(Isosurface, self).__init__(
            isosurf_renderer, isosurf_actor, isosurf_mapper)

        contour = vtk.vtkContourFilter()
        contour.SetInputConnection(vtk_source.GetOutputPort())
        contour.SetValue(0, iso_value)

        normals = vtk.vtkPolyDataNormals()
        normals.SetInputConnection(contour.GetOutputPort())

        normals.SetFeatureAngle(60.0)
        normals.ReleaseDataFlagOn()

        stripper = vtk.vtkStripper()
        stripper.SetInputConnection(normals.GetOutputPort())
        stripper.ReleaseDataFlagOn()

        isosurf_mapper.SetInputConnection(stripper.GetOutputPort)


class Iso_test(object):

    def __init__(self, renderer, vtk_source, iso_value=500):

        contour = vtk.vtkContourFilter()
        normals = vtk.vtkPolyDataNormals()
        stripper = vtk.vtkStripper()
        mapper = vtk.vtkPolyDataMapper()
        actor = vtk.vtkActor()

        contour.SetInputConnection(vtk_source.GetOutputPort())
        contour.SetValue(0, iso_value)

        normals.SetInputConnection(contour.GetOutputPort())
        normals.SetFeatureAngle(60.0)
        normals.ReleaseDataFlagOn()

        stripper.SetInputConnection(normals.GetOutputPort())
        stripper.ReleaseDataFlagOn()

        mapper.SetInputConnection(stripper.GetOutputPort())

        actor.SetMapper(mapper)

        renderer.AddActor(actor)


class Iso_test_2(object):

    def __init__(self):

        self.contour = vtk.vtkContourFilter()
        self.normals = vtk.vtkPolyDataNormals()
        self.stripper = vtk.vtkStripper()
        self.mapper = vtk.vtkPolyDataMapper()
        self.actor = vtk.vtkActor()

    def render(self, renderer, vtk_source, iso_value=500):

        self.contour.SetInputConnection(vtk_source.GetOutputPort())
        self.contour.SetValue(0, iso_value)

        self.normals.SetInputConnection(self.contour.GetOutputPort())
        self.normals.SetFeatureAngle(60.0)
        self.normals.ReleaseDataFlagOn()

        self.stripper.SetInputConnection(self.normals.GetOutputPort())
        self.stripper.ReleaseDataFlagOn()

        self.mapper.SetInputConnection(self.stripper.GetOutputPort())

        self.actor.SetMapper(self.mapper)

        self.renderer.AddActor(self.actor)
