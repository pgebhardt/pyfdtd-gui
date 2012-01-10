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
    def __init__(self, size, parent=None):
        # call base class constructors
        super(Plot, self).__init__(parent)

        # grid layout
        self.grid = QtGui.QGridLayout()

        # create matplotlib canvas
        self.fig = Figure(figsize=size, dpi=72)
        self.canvas = FigureCanvas(self.fig)
        self.grid.addWidget(self.canvas, 0, 0)

        # set layout
        self.setLayout(self.grid)
        
        x, y = size
        self.resize(x, y)

class matplotlibCanvas(FigureCanvas):       
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=8, height=4, dpi=100, title=None):
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes_top = fig.add_subplot(211)
        self.axes_bottom = fig.add_subplot(212)
            
        # We want the axes cleared every time plot() is called
        self.axes_top.hold(False)
        self.axes_bottom.hold(False)
                   
        if title != None:
            fig.suptitle(title, fontsize=12)
           
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
           
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
