from PySide import QtCore, QtGui
from plot import *
import numpy

from plugins import *
from pyfdtd import *

import matplotlib.colors as colors

# Main window for pyfdtd-gui application
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # call base class constructor
        super(MainWindow, self).__init__()

        # initialize gui elements
        self.init_gui()
        self.init_fdtd()
        self.init_timer()

        # run fdtd
        self.run_fdtd()
        self.timer.start(50)

    def init_gui(self):
        # set window title
        self.setWindowTitle('pyfdtd gui')
        self.resize(600, 600)        
        
        # create matplotlib plot
        self.figure = Plot((600, 600), self)
        self.ax = self.figure.fig.add_subplot(111)
        self.ax.imshow(numpy.zeros((200, 400)))

        # create button
        btn = QtGui.QPushButton('run')

        # create layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.figure)
        #grid.addWidget(btn)

        self.setCentralWidget(self.figure) 

    def init_timer(self):
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.plot)

    def init_fdtd(self):
        # create solver
        self.solver = solver(field(0.2, 0.4, deltaX=0.001))

        # add material
        self.solver.material['electric'][mask_from_string('x - 0.02*sin(2.0*pi*8.0*y) - 0.11 > 0.0')] = material.epsilon(sigma=59.1e6)
        self.solver.material['electric'][mask_from_string('x - 0.02*sin(2.0*pi*8.0*y) - 0.09 < 0.0')] = material.epsilon(sigma=59.1e6)

        # add source
        f = source_from_string('40.0*math.exp(-(t-1e-9)**2/(2.0*50.0e-12**2))*math.cos(2.0*math.pi*20e9*(t-1e-9))')
        self.solver.source[masks.ellipse(0.1, 0.05, 5, 0.001)] = source(f)
    def run_fdtd(self):
        # iterate
        self.history = self.solver.solve(1e-9, saveHistory=True)

    def plot(self):
        if not hasattr(self, 'step'):
            self.step = 0
        
        # plot current image
        if not hasattr(self, 'im'):
            self.im = self.ax.imshow(numpy.fabs(self.history[self.step]), norm=colors.Normalize(0.0, 10.0))
        else:
            self.im.set_array(self.history[self.step])

        # increment step
        self.step += 1
        if self.step >= len(self.history):
            self.step = 0

        self.figure.canvas.draw()
    
