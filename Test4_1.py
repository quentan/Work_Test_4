#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Code rule:
# http://zh-google-styleguide.readthedocs.org/en/latest/google-python-styleguide/python_style_rules/

import sys
import vtk

from PyQt4 import QtGui

from lib import ui_main_window


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

        self.move(100, 100)
        self.show()


if __name__ == '__main__':

    app = QtGui.QApplication(sys.argv)
    window = Basic()
    sys.exit(app.exec_())
