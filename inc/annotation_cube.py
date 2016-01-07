# -*- coding: utf-8 -*-

import vtk
from scene_object import SceneObject


class Axes(SceneObject):

    def __init__(self):

        # Skip the parent constructor
        # super(Axes, self).__init__(renderer)

        text_property_x = vtk.vtkTextProperty()
        text_property_x.ItalicOn()
        text_property_x.ShadowOn()
        text_property_x.BoldOn()
        text_property_x.SetFontFamilyToTimes()
        text_property_x.SetColor(1, 0, 0)

        text_property_y = vtk.vtkTextProperty()
        text_property_y.ShallowCopy(text_property_x)
        text_property_y.SetColor(0, 1, 0)

        text_property_z = vtk.vtkTextProperty()
        text_property_z.ShallowCopy(text_property_x)
        text_property_z.SetColor(0, 0, 1)

        self.axes = vtk.vtkAxesActor()
        self.axes.SetShaftTypeToCylinder()
        self.axes.SetCylinderRadius(0.05)
        self.axes.SetTotalLength(3 * [1.5])

        self.axes.GetXAxisCaptionActor2D().SetCaptionTextProperty(
            text_property_x)
        self.axes.GetYAxisCaptionActor2D().SetCaptionTextProperty(
            text_property_y)
        self.axes.GetZAxisCaptionActor2D().SetCaptionTextProperty(
            text_property_z)

        # self.axes.GetXAxisCaptionActor2D().GetTextActor(
        # ).SetTextScaleMode(vtk.vtkTextActor.TEXT_SCALE_MODE_NONE)
        # self.axes.GetXAxisCaptionActor2D().GetTextActor(
        # ).GetTextProperty().SetFontSize(25)

        # self.axes.GetYAxisCaptionActor2D().GetTextActor(
        # ).SetTextScaleMode(vtk.vtkTextActor.TEXT_SCALE_MODE_NONE)
        # self.axes.GetYAxisCaptionActor2D().GetTextActor(
        # ).GetTextProperty().SetFontSize(25)

        # self.axes.GetZAxisCaptionActor2D().GetTextActor(
        # ).SetTextScaleMode(vtk.vtkTextActor.TEXT_SCALE_MODE_NONE)
        # self.axes.GetZAxisCaptionActor2D().GetTextActor(
        # ).GetTextProperty().SetFontSize(25)

        # Add the actor
        # renderer.AddActor(self.axes)

    def add(self, renderer):

        renderer.AddActor(self.axes)

    def remove(self, renderer):

        renderer.RemoveActor(self.axes)


class Cube(SceneObject):

    def __init__(self):

        # super(Cube, self).__init__(renderer)

        self.cube = vtk.vtkAnnotatedCubeActor()
        self.cube.SetXPlusFaceText('R')
        self.cube.SetXMinusFaceText('L')
        self.cube.SetYPlusFaceText('A')
        self.cube.SetYMinusFaceText('P')
        self.cube.SetZPlusFaceText('I')
        self.cube.SetZMinusFaceText('S')
        self.cube.SetXFaceTextRotation(180)
        self.cube.SetYFaceTextRotation(180)
        self.cube.SetZFaceTextRotation(-90)
        self.cube.SetFaceTextScale(0.65)
        self.cube.GetCubeProperty().SetColor(0.5, 1.0, 1.0)
        self.cube.GetTextEdgesProperty().SetLineWidth(1)
        self.cube.GetTextEdgesProperty().SetColor(0.18, 0.28, 0.23)
        self.cube.GetTextEdgesProperty().SetDiffuse(0)
        self.cube.GetTextEdgesProperty().SetAmbient(1)

        self.cube.GetXPlusFaceProperty().SetColor(1, 0, 0)
        self.cube.GetXPlusFaceProperty().SetInterpolationToFlat()
        self.cube.GetXMinusFaceProperty().SetColor(1, 0, 0)
        self.cube.GetXMinusFaceProperty().SetInterpolationToFlat()

        self.cube.GetYPlusFaceProperty().SetColor(0, 1, 0)
        self.cube.GetYPlusFaceProperty().SetInterpolationToFlat()
        self.cube.GetYMinusFaceProperty().SetColor(0, 1, 0)
        self.cube.GetYMinusFaceProperty().SetInterpolationToFlat()

        self.cube.GetZPlusFaceProperty().SetColor(0, 0, 1)
        self.cube.GetZPlusFaceProperty().SetInterpolationToFlat()
        self.cube.GetZMinusFaceProperty().SetColor(0, 0, 1)
        self.cube.GetZMinusFaceProperty().SetInterpolationToFlat()

        # renderer.AddActor(self.cube)

    def add(self, renderer):

        renderer.AddActor(self.cube)

    def remove(self, renderer):

        renderer.RemoveActor(self.cube)


class Marker(SceneObject):

    def __init__(self, iren):

        # super(Marker, self).__init__()

        self.axes_actor = Axes().axes
        self.cube_actor = Cube().cube

        self.assembly = vtk.vtkPropAssembly()
        self.assembly.AddPart(self.axes_actor)
        self.assembly.AddPart(self.cube_actor)

        self.marker = vtk.vtkOrientationMarkerWidget()
        self.marker.SetOutlineColor(0.93, 0.57, 0.13)
        self.marker.SetOrientationMarker(self.assembly)
        # self.marker.SetViewport(0.0, 0.0, 0.15, 0.3)
        self.marker.SetInteractor(iren)
        # self.marker.EnabledOn()
        # self.marker.InteractiveOn()

    def show(self):

        self.marker.EnabledOn()
        self.marker.InteractiveOn()

    def hide(self):

        self.marker.InteractiveOff()
        self.marker.EnabledOff()
