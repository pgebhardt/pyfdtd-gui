import os
os.environ['QT_API'] = 'pyside'

import sys
from matplotlib.backends.backend_qt4agg \
        import NavigationToolbar2QTAgg as NavigationToolbar

from PySide import QtGui
from plot import matplotlibCanvas
from plugins import LogViewer
from numpy import *
from scipy import *
from scipy.signal import *
from scipy import constants


class EvalTab(QtGui.QWidget):
    def __init__(self, mainwindow):
        # call base class constructor
        super(EvalTab, self).__init__()

        # save mainwindow
        self.mainwindow = mainwindow

        # init gui
        self.init_gui()

    def init_gui(self):
        # create plot
        self.plot = matplotlibCanvas(None, 5.0, 5.0, dpi=72, title='Listener')

        # create toolbar
        self.toolbar = NavigationToolbar(self.plot, self)

        # create input
        self.inputEdit = QtGui.QTextEdit()

        # create button
        self.evalButton = QtGui.QPushButton('Evaluate')
        self.evalButton.clicked.connect(self.evaluate)

        # create LogViewer
        self.logviewer = LogViewer()
        self.logviewer.setMaximumHeight(100.0)
        sys.stderr = self.logviewer
        sys.stdout = self.logviewer

        # create layout
        box = QtGui.QVBoxLayout()

        root = QtGui.QGridLayout()
        root.addWidget(self.plot, 0, 0)
        root.addWidget(self.inputEdit, 0, 1)
        root.addWidget(self.toolbar, 1, 0)
        root.addWidget(self.evalButton, 1, 1)

        box.addLayout(root)
        box.addWidget(self.logviewer)

        self.setLayout(box)

    def evaluate(self):
        # get input
        inputText = self.inputEdit.toPlainText()

        # create propper environment
        plot = self.plot.axes
        listener = self.mainwindow.simulation.listener

        # clear axes
        plot.cla()

        # clear logviewer
        self.logviewer.setPlainText('')

        # evaluate
        exec(inputText)

        # draw plot
        self.plot.draw()
