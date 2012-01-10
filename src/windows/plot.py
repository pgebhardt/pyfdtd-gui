import os
os.environ['QT_API'] = 'pyside'

import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from PySide import QtCore, QtGui
import numpy

class Plot(QtGui.QWidget):
    def __init__(self, size, parent):
        # call base class constructors
        super(Plot, self).__init__(parent)
        
        # grid layout
        self.grid = QtGui.QGridLayout()

        # create matplotlib canvas
        self.fig = Figure(figsize=size)
        self.canvas = FigureCanvas(self.fig)
        self.grid.addWidget(self.canvas, 0, 0)

        # set layout
        self.setLayout(self.grid)
