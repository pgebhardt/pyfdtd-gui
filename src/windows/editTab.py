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
import dialogs
from plot import Plot


class EditTab(QtGui.QWidget):
    def __init__(self, mainwindow):
        # call base class constructor
        super(EditTab, self).__init__()

        # save mainwindow
        self.mainwindow = mainwindow

        # init gui
        self.init__gui()

    def init__gui(self):
        # create grid layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        # create plot
        self.plot = Plot(self.mainwindow)

        # create simulation buttons
        simulationButtonBox = QtGui.QHBoxLayout()

        self.durationEdit = QtGui.QLineEdit(
                '{}'.format(self.mainwindow.job.config['duration']))
        self.durationEdit.textChanged.connect(self.duration_update)

        durationLabel = QtGui.QLabel('Duration:')
        durationLabel.setBuddy(self.durationEdit)

        startSimButton = QtGui.QPushButton('Start Simulation')
        startSimButton.clicked.connect(self.mainwindow.run_simulation)

        simulationButtonBox.addWidget(durationLabel)
        simulationButtonBox.addWidget(self.durationEdit)
        simulationButtonBox.addWidget(startSimButton)

        # create button grid
        layerButtonGrid = QtGui.QGridLayout()

        # create new layer button
        newLayerButton = QtGui.QPushButton('New Layer')
        newLayerButton.clicked.connect(self.new_layer_clicked)

        # create delete layer buttons
        deleteLayerButton = QtGui.QPushButton('Delete Layer')
        deleteLayerButton.clicked.connect(self.deleate_layer)

        # add buttons to grid layout
        layerButtonGrid.addWidget(newLayerButton, 0, 0)
        layerButtonGrid.addWidget(deleteLayerButton, 0, 1)

        # create tree view
        treeGrid = QtGui.QGridLayout()
        treeLabel = QtGui.QLabel('Layer:')

        # init tree
        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderLabels(['Name', 'Mask', 'Function'])
        self.treeWidget.setColumnCount(3)
        treeLabel.setBuddy(self.treeWidget)
        self.init_tree()

        # layout
        treeGrid.addWidget(treeLabel, 0, 0)
        treeGrid.addWidget(self.treeWidget, 1, 0)

        grid.addWidget(self.plot, 0, 0)
        grid.addLayout(simulationButtonBox, 1, 0)
        grid.addLayout(layerButtonGrid, 1, 1)
        grid.addLayout(treeGrid, 0, 1)

    def init_tree(self):
        # clear tree
        self.treeWidget.clear()

        # init tree
        self.layerItems = []
        self.layerItems.append(QtGui.QTreeWidgetItem(None, ['Electric']))
        self.layerItems.append(QtGui.QTreeWidgetItem(None, ['Magnetic']))
        self.layerItems.append(QtGui.QTreeWidgetItem(None, ['Source']))
        self.layerItems.append(QtGui.QTreeWidgetItem(None, ['Listener']))
        self.treeWidget.addTopLevelItems(self.layerItems)

    # Button methods
    def duration_update(self):
        # update duration
        self.mainwindow.job.config['duration'] = \
        float(self.durationEdit.text())

    def new_layer_clicked(self):
        self.newLayerDialog = dialogs.NewLayer(mainwindow=self.mainwindow)
        self.newLayerDialog.okButton.clicked.connect(self.new_layer_create)
        self.newLayerDialog.show()

    def new_layer_create(self):
        # cloase dialog
        self.newLayerDialog.close()

        # get attributes
        name = self.newLayerDialog.nameEdit.text()
        type_ = self.newLayerDialog.typeComboBox.currentText()
        mask = self.newLayerDialog.maskEdit.text()
        function = self.newLayerDialog.functionEdit.text()
        x = float(self.newLayerDialog.xEdit.text())
        y = float(self.newLayerDialog.yEdit.text())

        # create new Layer
        self.new_layer(name, type_, mask, function=function, x=x, y=y)

        # add to job
        if type_ == 'Electric':
            self.mainwindow.job.material['electric'].append(
                    [name, mask, function])

        elif type_ == 'Magnetic':
            self.mainwindow.job.material['magnetic'].append(
                    [name, mask, function])

        elif type_ == 'Source':
            self.mainwindow.job.source.append([name, mask, function])

        elif type_ == 'Listener':
            self.mainwindow.job.listener.append([name, x, y])

        # update plot
        self.plot.update()
        self.mainwindow.playTab.update()

    def deleate_layer(self):
        # get current layer
        currentItem = self.treeWidget.currentItem()

        # get parent
        if not currentItem is None:
            parent = currentItem.parent()

        # delete layer from tree and job
        if not currentItem is None and not parent is None:
            # delete layer from job
            index = parent.indexOfChild(currentItem)
            type_ = parent.text(0)

            if type_ == 'Electric':
                self.mainwindow.job.material['electric'].remove(
                        self.mainwindow.job.material['electric'][index])
            elif type_ == 'Magnetic':
                self.mainwindow.job.material['magnetic'].remove(
                        self.mainwindow.job.material['magnetic'][index])
            elif type_ == 'Source':
                self.mainwindow.job.source.remove(
                        self.mainwindow.job.source[index])
            elif type_ == 'Listener':
                self.mainwindow.job.listener.remove(
                        self.mainwindow.job.listener[index])

            # delete layer from tree
            parent.removeChild(currentItem)

            # update plot
            self.plot.update()

    def update(self):
        # clear editTab tree
        self.init_tree()

        # update materials
        for name, mask, function in self.mainwindow.job.material['electric']:
            self.new_layer(name, 'Electric', mask, function)

        for name, mask, function in self.mainwindow.job.material['magnetic']:
            self.new_layer(name, 'Magnetic', mask, function)

        # update sources
        for name, mask, function in self.mainwindow.job.source:
            self.new_layer(name, 'Source', mask, function=function)

        # update listener
        for name, x, y in self.mainwindow.job.listener:
            self.new_layer(name, 'Listener', x=x, y=y)

        # update plot
        self.plot.update()
        self.mainwindow.playTab.update()

    def new_layer(self, name, type_, mask=None, function=None, x=0.0, y=0.0):
        # create layer
        try:
            if type_ == 'Electric':
                QtGui.QTreeWidgetItem(self.layerItems[0],
                        [name, mask, function])

            elif type_ == 'Magnetic':
                QtGui.QTreeWidgetItem(self.layerItems[1],
                        [name, mask, function])

            elif type_ == 'Source':
                QtGui.QTreeWidgetItem(self.layerItems[2],
                        [name, mask, function])

            elif type_ == 'Listener':
                QtGui.QTreeWidgetItem(self.layerItems[3],
                        [name, 'x={}, y={}'.format(x, y)])

        except SyntaxError:
            return

        except NameError:
            return

        except ValueError:
            return
