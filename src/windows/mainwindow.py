from PySide import QtCore, QtGui
from plot import *
import numpy

# Main window for pyfdtd-gui application
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # call base class constructor
        super(MainWindow, self).__init__()

        # initialize gui elements
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('pyfdtd gui')
        
        self.resize(600, 600)        
        self.figure = Plot((600, 600), self)

        self.setCentralWidget(self.figure)
        ax = self.figure.fig.add_subplot(111)
        
        x = numpy.linspace(0.0, 10.0, 100)
        ax.plot(x, x**2)
