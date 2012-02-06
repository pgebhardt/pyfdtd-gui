from PySide import QtGui
import pyfdtd
from plugins import mask_from_string, source_from_string
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
        self.plot = Plot(self.mainwindow.simulation)

        # create buttons
        startSimButton = QtGui.QPushButton('Start Simulation')
        startSimButton.clicked.connect(self.mainwindow.run_simulation)

        # button functions
        def new_layer_clicked():
            self.newLayerDialog = dialogs.NewLayer(mainwindow=self.mainwindow)
            self.newLayerDialog.okButton.clicked.connect(new_layer_create)
            self.newLayerDialog.show()

        def new_layer_create():
            # cloase dialof
            self.newLayerDialog.close()

            # get attributes
            name = self.newLayerDialog.nameEdit.text()
            type_ = self.newLayerDialog.typeComboBox.currentText()
            mask = self.newLayerDialog.maskEdit.text()
            function = self.newLayerDialog.functionEdit.text()
            er = float(self.newLayerDialog.rEdit.text())
            mur = float(self.newLayerDialog.rEdit.text())
            sigma = float(self.newLayerDialog.sigmaEdit.text())
            x = float(self.newLayerDialog.xEdit.text())
            y = float(self.newLayerDialog.yEdit.text())

            # create new Layer
            self.new_layer(name, type_, mask, function=function, er=er,
                    mur=mur, sigma=sigma, x=x, y=y)

            # add to job
            if type_ == 'Electric':
                self.mainwindow.job.material['electric'].append(
                        [name, mask, er, sigma])

            elif type_ == 'Magnetic':
                self.mainwindow.job.material['magnetic'].append(
                        [name, mask, mur, sigma])

            elif type_ == 'Source':
                self.mainwindow.job.source.append([name, mask, function])

            elif type_ == 'Listener':
                self.mainwindow.job.listener.append([name, x, y])

            # update plot
            self.plot.update()
            self.mainwindow.playTab.update()

        # create new layer button
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

    def update_job(self):
        # clear editTab tree
        self.init_tree()

        # create new simulation
        self.mainwindow.simulation = pyfdtd.solver(
                pyfdtd.field(self.mainwindow.job.config['size'],
                    self.mainwindow.job.config['delta']))

        # update materials
        for name, mask, er, sigma in self.mainwindow.job.material['electric']:
            self.new_layer(name, 'Electric', mask, er=er, sigma=sigma)

        for name, mask, mur, sigma in self.mainwindow.job.material['magnetic']:
            self.new_layer(name, 'Magnetic', mask, mur=mur, sigma=sigma)

        # update sources
        for name, mask, function in self.mainwindow.job.source:
            self.new_layer(name, 'Source', mask, function=function)

        # update listener
        for name, x, y in self.mainwindow.job.listener:
            self.new_layer(name, 'Listener', x=x, y=y)

        # update plot
        self.plot.update()
        self.mainwindow.playTab.update()

    def update_plot(self):
        # update plot
        self.plot.simulation = self.mainwindow.simulation
        self.plot.update()

    def new_layer(self, name, type_, mask=None, function=None, er=1.0, mur=1.0,
            sigma=0.0, x=0.0, y=0.0):
        # create layer
        try:
            if type_ == 'Electric':
                self.mainwindow.simulation.material['electric'][
                        mask_from_string(mask)] = \
                                pyfdtd.material.epsilon(er=er, sigma=sigma)
                QtGui.QTreeWidgetItem(self.layerItems[0],
                        [name, mask,
                            'epsilon(er={}, sigma={})'.format(er, sigma)])

            elif type_ == 'Magnetic':
                self.mainwindow.simulation.material['electric'][
                        mask_from_string(mask)] = \
                               pyfdtd.material.mu(mur=mur, sigma=sigma)
                QtGui.QTreeWidgetItem(self.layerItems[1],
                        [name, mask,
                            'mu(mur={}, sigma={})'.format(mur, sigma)])

            elif type_ == 'Source':
                self.mainwindow.simulation.source[
                        mask_from_string(mask)] = source_from_string(function)
                QtGui.QTreeWidgetItem(self.layerItems[2],
                        [name, mask, function])

            elif type_ == 'Listener':
                self.mainwindow.simulation.listener.append(
                        pyfdtd.listener(x, y))
                QtGui.QTreeWidgetItem(self.layerItems[3],
                        [name, 'x={}, y={}'.format(x, y)])

        except SyntaxError:
            return

        except NameError:
            return

        except ValueError:
            return
