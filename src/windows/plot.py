import os
os.environ['QT_API'] = 'pyside'

import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import matplotlib.pyplot as plt
from PySide import QtCore, QtGui

class matplotlibCanvas(FigureCanvas):       
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=8, height=4, dpi=100, title=None):
        
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
                    
        # We want the axes cleared every time plot() is called
        self.axes.hold(False)
                   
        if title != None:
            fig.suptitle(title, fontsize=12)
           
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
           
        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
