# GUI for pyfdtd using PySide
# Copyright (C) 2012  Patrik Gebhardt
# Contact: grosser.knuff@googlemail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
os.environ['QT_API'] = 'pyside'

from matplotlib.backends.backend_qt4agg \
        import NavigationToolbar2QTAgg as NavigationToolbar

from PySide import QtGui
from widgets import matplotlibCanvas


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

        # create layout
        root = QtGui.QGridLayout()
        root.addWidget(self.plot, 0, 0)
        root.addWidget(self.inputEdit, 0, 1)
        root.addWidget(self.toolbar, 1, 0)
        root.addWidget(self.evalButton, 1, 1)
        self.setLayout(root)

    def evaluate(self):
        # get input
        inputText = self.inputEdit.toPlainText()

        # clear axes
        self.plot.axes.cla()

        # add std imports to inputText
        inputText = """
from numpy import *
from scipy import *
from scipy.signal import *
from scipy import constants
        """ + inputText

        # evaluate
        exec(inputText, {'plot': self.plot.axes, 'listener':
            self.mainwindow.simulation.listener})

        # draw plot
        self.plot.draw()
