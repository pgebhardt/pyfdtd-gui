from PySide import QtGui, QtCore
from plot import *
from numpy import *
from scipy import *
from scipy.signal import *
from math import *

class EvalWindow(QtGui.QMainWindow):
    def __init__(self, simulation):
        # call base class constructor
        super(EvalWindow, self).__init__()

        # save simulation
        self.simulation = simulation

        # initialize gui
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('PyFDTD GUI - Eval')
        self.resize(1000, 600)

        # create container
        self.container = QtGui.QWidget(self)
        self.setCentralWidget(self.container)
        
        # create plot
        self.plot = matplotlibCanvas(None, 5.0, 5.0, dpi=72, title='Listener')
        
        # create input
        self.inputEdit = QtGui.QTextEdit()

        # create button
        self.evalButton = QtGui.QPushButton('Eval')
        self.evalButton.clicked.connect(self.evaluate)

        # create layout
        root = QtGui.QGridLayout()
        root.addWidget(self.plot, 0, 0)
        root.addWidget(self.inputEdit, 0, 1)
        root.addWidget(self.evalButton, 1, 1)
        self.container.setLayout(root)

    def evaluate(self):
        # get input
        inputText = self.inputEdit.toPlainText()
        
        # create propper environment
        plot = self.plot.axes
        canvas = self.plot
        listener = self.simulation.listener

        # evaluate
        exec(inputText)

        # draw plot
        self.plot.draw()
