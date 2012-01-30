from PySide import QtGui, QtCore
from plot import Plot
import numpy


class PlayTab(QtGui.QWidget):
    def __init__(self, mainwindow):
        # call base class constructor
        super(PlayTab, self).__init__()

        # save mainwindow
        self.mainwindow = mainwindow

        # create timer
        self.timer = QtCore.QTimer(self)

        # init gui
        self.init_gui()

        # init timer
        self.step = 0
        self.simulationHistory = [numpy.zeros(
            self.mainwindow.simulation.field.oddFieldX['field'].shape)]
        self.init_timer()

    def init_gui(self):
        # create grid
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        # create plot
        self.plot = Plot(self.mainwindow.simulation)

        # create buttons
        buttonGrid = QtGui.QGridLayout()

        def play_simulation():
            self.timer.start(50)

        self.playButton = QtGui.QPushButton('Play')
        self.playButton.clicked.connect(play_simulation)
        self.playButton.setDisabled(True)

        stopButton = QtGui.QPushButton('Stop')
        stopButton.clicked.connect(self.timer.stop)

        buttonGrid.addWidget(self.playButton, 0, 0)
        buttonGrid.addWidget(stopButton, 0, 1)

        # set layout
        grid.addWidget(self.plot, 0, 0)
        grid.addLayout(buttonGrid, 1, 0)

    def init_timer(self):
        # timer function
        def timeout():
            # increment step
            self.step += 1
            if self.step >= len(self.simulationHistory):
                self.step = 0

        # plot function
        def p():
            self.plot.plot(self.simulationHistory[self.step])

        # create timer
        self.timer.timeout.connect(p)
        self.timer.timeout.connect(timeout)

    def update(self):
        # upate plot
        self.plot.simulation = self.mainwindow.simulation
        self.plot.update()
