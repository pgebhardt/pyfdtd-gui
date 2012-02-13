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


from PySide import QtGui


class NewSimulation(QtGui.QDialog):
    def __init__(self, mainwindow=None):
        # call base class constructor
        super(NewSimulation, self).__init__(mainwindow)

        # init gui
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('New Simulation')

        # layout
        root = QtGui.QGridLayout(self)

        # create buttons
        self.okButton = QtGui.QPushButton('OK')
        cancelButton = QtGui.QPushButton('cancel')
        cancelButton.clicked.connect(self.close)

        # create edits
        self.xSizeEdit = QtGui.QLineEdit()
        self.ySizeEdit = QtGui.QLineEdit()
        self.deltaXEdit = QtGui.QLineEdit()
        self.deltaYEdit = QtGui.QLineEdit()

        # create labels
        sizeLabel = QtGui.QLabel('Size:')
        sizeLabel.setBuddy(self.xSizeEdit)
        deltaLabel = QtGui.QLabel('Delta:')
        deltaLabel.setBuddy(self.deltaXEdit)
        x1Label = QtGui.QLabel('x')
        x2Label = QtGui.QLabel('x')

        # set layout
        root.addWidget(sizeLabel, 0, 0)
        root.addWidget(self.xSizeEdit, 0, 1)
        root.addWidget(x1Label, 0, 2)
        root.addWidget(self.ySizeEdit, 0, 3)
        root.addWidget(deltaLabel, 1, 0)
        root.addWidget(self.deltaXEdit, 1, 1)
        root.addWidget(x2Label, 1, 2)
        root.addWidget(self.deltaYEdit, 1, 3)
        root.addWidget(self.okButton, 2, 1)
        root.addWidget(cancelButton, 2, 3)
