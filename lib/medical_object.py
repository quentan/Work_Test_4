# -*- coding: utf-8 -*-

"""
Basic superclass
"""

import vtk


class MedicalObject(object):

    def __init__(self, vtk_renderer, vtk_actor, vtk_mapper):
        '''
        Basic elements for Medical Object rendering
        '''
        self.renderer = vtk_renderer
        self.actor = vtk_actor
        self.mapper = vtk_mapper

        self.actor.SetMapper(self.mapper)
        self.renderer.AddActor(self.actor)
