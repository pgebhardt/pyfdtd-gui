from PySide import QtGui
from dialogs import NewLayer
from plot import Plot
import numpy


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
        self.plot = Plot(self.mainwindow.simulation)

        # create buttons
        startSimButton = QtGui.QPushButton('Start Simulation')
        startSimButton.clicked.connect(self.mainwindow.run_simulation)

        # new layer button
        def new_layer_clicked():
            self.newLayerDialog = dialogs.NewLayer(mainwindow=self.mainwindow)
            self.newLayerDialog.okButton.clicked.connect(self.new_layer)
            self.newLayerDialog.show()

        newLayerButton = QtGui.QPushButton('New Layer')
        newLayerButton.clicked.connect(new_layer_clicked)

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
        grid.addWidget(startSimButton, 1, 0)
        grid.addWidget(newLayerButton, 1, 1)
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

    def update(self):
        # update plot
        self.plot.simulation = self.mainwindow.simulation
        self.plot.simulationHistory = [numpy.zeros(
                    self.mainwindow.simulation.field.oddFieldX['field'].shape)]
        self.plot.update()

        # init tree
        self.init_tree()

    def new_layer(self):
        # close dialog
        self.newLayerDialog.close()

        # get attributes
        name = self.newLayerDialog.nameEdit.text()
        type_ = self.newLayerDialog.typeComboBox.currentText()
        mask = self.newLayerDialog.maskEdit.text()
        function = self.newLayerDialog.functionEdit.text()

        # create layer
        try:
            if type_ == 'Electric':
                er, sigma = (float(self.newLayerDialog.rEdit.text()),
                        float(self.newLayerDialog.sigmaEdit.text()))
                self.mainwindow.simulation.material['electric'][
                        mask_from_string(mask)] = \
                                material.epsilon(er=er, sigma=sigma)
                QtGui.QTreeWidgetItem(self.layerItems[0],
                        [name, mask,
                            'epsilon(er={}, sigma={})'.format(er, sigma)])
                self.mainwindow.job.material['electric'].append(
                        (name, mask, er, sigma))

            elif type_ == 'Magnetic':
                mur, sigma = (float(self.newLayerDialog.rEdit.text()),
                        float(self.newLayerDialog.sigmaEdit.text()))
                self.mainwindow.simulation.material['electric'][
                        mask_from_string(mask)] = \
                                material.mu(mur=mur, sigma=sigma)
                QtGui.QTreeWidgetItem(self.layerItems[1],
                        [name, mask,
                            'mu(mur={}, sigma={})'.format(mur, sigma)])
                self.mainwindow.job.material['magnetic'].append(
                        (name, mask, mur, sigma))

            elif type_ == 'Source':
                self.mainwindow.simulation.source[
                        mask_from_string(mask)] = source_from_string(function)
                QtGui.QTreeWidgetItem(self.layerItems[2],
                        [name, mask, function])
                self.mainwindow.job.source.append((name, mask, function))

            elif type_ == 'Listener':
                x, y = (float(self.newLayerDialog.xEdit.text()),
                        float(self.newLayerDialog.yEdit.text()))
                self.mainwindow.simulation.listener.append(listener(x, y))
                QtGui.QTreeWidgetItem(self.layerItems[3],
                        [name, 'x={}, y={}'.format(x, y)])
                self.mainwindow.job.listener.append((name, x, y))

        except SyntaxError:
            return
        except NameError:
            return
        except ValueError:
            return

        # update plot
        self.plot.update()
