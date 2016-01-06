# -*- coding: utf-8 -*-

import vtk
from lib import SceneObject


class Axes(SceneObject):

    def __init__(self, renderer):

        # Skip the parent constructor
        # super(Axes, self).__init__(renderer)

        self.vtk_actor = vtk.vtkAxesActor()
        self.vtk_actor.SetShaftTypeToCylinder()
        self.vtk_actor.SetCylinderRadius(0.05)
        self.vtk_actor.SetTotalLength(3 * [2.5])

        self.vtk_actor.GetXAxisCaptionActor2D().GetTextActor(
        ).SetTextScaleMode(vtk.vtkTextActor.TEXT_SCALE_MODE_NONE)
        self.vtk_actor.GetXAxisCaptionActor2D().GetTextActor(
        ).GetTextProperty().SetFontSize(25)

        self.vtk_actor.GetYAxisCaptionActor2D().GetTextActor(
        ).SetTextScaleMode(vtk.vtkTextActor.TEXT_SCALE_MODE_NONE)
        self.vtk_actor.GetYAxisCaptionActor2D().GetTextActor(
        ).GetTextProperty().SetFontSize(25)

        self.vtk_actor.GetZAxisCaptionActor2D().GetTextActor(
        ).SetTextScaleMode(vtk.vtkTextActor.TEXT_SCALE_MODE_NONE)
        self.vtk_actor.GetZAxisCaptionActor2D().GetTextActor(
        ).GetTextProperty().SetFontSize(25)

        # Add the actor
        # renderer.AddActor(self.vtk_actor)

    def add(self, renderer):

        renderer.AddActor(self.vtk_actor)

    def remove(self, renderer):

        renderer.RemoveActor(self.vtk_actor)


class AnnotationCube(SceneObject):

    def __init__(self, renderer):

        # super(AnnotationCube, self).__init__(renderer)

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


class Assembly(Axes, AnnotationCube):

    def __init__(self, renderer):

        super(Assembly, self).__init__(renderer)

        self.axes_actor = Axes(renderer)
        self.cube_actor = AnnotationCube(renderer)
        self.assembly = vtk.vtkAssembly()

    def add(self, _assembly):

        _assembly.AddPart(self.axes_actor)
        _assembly.AddPart(self.cube_actor)

    def remove(self, _assembly):

        _assembly.RemovePart(self.axes_actor)
        _assembly.RemovePart(self.cube_actor)
