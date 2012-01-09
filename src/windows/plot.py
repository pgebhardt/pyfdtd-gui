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
        
        # resize
        x, y = size
        self.resize(x, y)

        # set figure
        self.fig = Figure(figsize=size, dpi=72)
        ax = self.fig.add_subplot(111)
        
        x = numpy.linspace(0.0, 5.0, 100)
        ax.plot(x, x**2)

        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self)
