import os
os.environ['QT_API'] = 'pyside'

import numpy
import matplotlib
matplotlib.use('Qt4Agg')
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.colors as colors

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

class Plot(QtGui.QWidget):
    def __init__(self, simulation, parent=None):
        # call base class constructor
        super(Plot, self).__init__()

        # save simulation
        self.simulation = simulation
        self.step = 0
        self.simulationHistory = [numpy.zeros(self.simulation.field.oddFieldX['field'].shape)]

        # create timer 
        self.init_timer()

        # create canvas
        self.canvas = matplotlibCanvas(None, 5.0, 5.0, dpi=72, title='Domain')

        # create layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.canvas)
        self.setLayout(grid)

        # plot once
        self.update()

    def update(self):
        # redraw im
        self.im = self.canvas.axes.imshow(numpy.fabs(self.simulation.field.oddFieldX['field']), norm=colors.Normalize(0.0, 10.0), extent=[0.0, self.simulation.field.ySize, self.simulation.field.xSize, 0.0])
        self.canvas.axes.grid(True)

        # cummulate all layer masks
        self.masks = numpy.zeros(self.simulation.field.oddFieldX['field'].shape)

        # get electric layer
        for fX, fY, dX, dY, mask in self.simulation.material['electric'].layer[1:]:
            self.masks += mask
        
        self.masks *= 1.0/numpy.max(self.masks)

        # plot
        self.plot()

    def plot(self):
        # plot
        self.im.set_array(self.masks + self.simulationHistory[self.step])

        # update canvas
        self.canvas.draw()

    def init_timer(self):
        # timer function
        def timeout():
            # increment step
            self.step += 1
            if self.step >= len(self.simulationHistory):
                self.step = 0

        # create timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot)
        self.timer.timeout.connect(timeout)
            
    def show_simulation(self, simulationHistory):
        # save history
        self.simulationHistory = simulationHistory

        # start timer
        self.timer.start(50)
