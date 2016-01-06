# -*- coding: utf-8 -*-

"""
Basic superclass
"""

import vtk


class SceneObject(object):

    def __init__(self, renderer):
        '''
        Constructor with the renderer passed in
        '''
        self.vtk_actor = vtk.vtkActor()
        renderer.AddActor(self.vtk_actor)

    def setPosition(self, p):  # p: position
        self.vtk_actor.SetPosition(p[0], p[1], p[2])

    def getPosition(self):
        return self.vtk_actor.GetPosition()

    def setOrientation(self, o):  # o: orientation
        self.vtk_actor.SetOrientation(o[0], o[1], o[2])

    def getOrientation(self):
        return self.vtk_actor.GetOrientation()
