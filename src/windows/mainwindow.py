from PySide import QtCore, QtGui
import matplotlib.colors as colors
import pickle
from pyfdtd import *
from plugins import *
from plot import *
import dialogs
import jobs
from evalwindow import *


# Main window for pyfdtd-gui application
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # call base class constructor
        super(MainWindow, self).__init__()

        # init simulation
        self.simulation = solver(field(0.4, 0.4, 0.001))
        self.job = jobs.Job()

        # initialize gui elements
        self.create_actions()
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('Pyfdtd GUI')
        self.resize(1000, 600)

        # create menu bar
        fileMenu = self.menuBar().addMenu('&File')

        # add actions
        for action in self.actions:
            fileMenu.addAction(action)

        # create Container
        self.container = QtGui.QWidget(self)
        self.setCentralWidget(self.container)

        # create Plot
        self.plot = Plot(self.simulation)

        # create button
        startSimButton = QtGui.QPushButton('start simulation')
        startSimButton.resize(startSimButton.sizeHint())
        startSimButton.clicked.connect(self.run_simulation)

        # create treeview
        treeGrid = QtGui.QGridLayout()
        treeLabel = QtGui.QLabel('Layer:')

        # new Layer Button
        def new_layer_clicked():
            self.newLayerDialog = dialogs.NewLayer(mainWindow=self)
            self.newLayerDialog.okButton.clicked.connect(self.new_layer)
            self.newLayerDialog.show()

        newLayerButton = QtGui.QPushButton('New Layer')
        newLayerButton.clicked.connect(new_layer_clicked)

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setHeaderLabels(['Name', 'Mask', 'Function'])
        self.treeWidget.setColumnCount(3)
        treeLabel.setBuddy(self.treeWidget)

        # init tree
        self.init_tree()

        treeGrid.addWidget(treeLabel, 0, 0)
        treeGrid.addWidget(self.treeWidget, 1, 0)

        # layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.plot, 0, 0)
        grid.addWidget(startSimButton, 1, 0)
        grid.addWidget(newLayerButton, 1, 1)
        grid.addLayout(treeGrid, 0, 1)
        self.container.setLayout(grid)

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

    def create_actions(self):
        # create action list
        self.actions = []

        # new simulation action
        self.actions.append(QtGui.QAction('&New', self, shortcut='Ctrl+N',
            statusTip='New simulation', triggered=self.new_simulation))

        # open simulation action
        self.actions.append(QtGui.QAction('&Open', self, shortcut='Ctrl+O',
                statusTip='Open simulation', triggered=self.open_simulation))

        # save simulation action
        self.actions.append(QtGui.QAction('&Save', self, shortcut='Ctrl+S',
                statusTip='Save simulation', triggered=self.save_simulation))

        # exit action
        self.actions.append(QtGui.QAction('&Exit', self, shortcut='Ctrl+Q',
            statusTip='Exit application', triggered=self.close))

    def closeEvent(self, event):
        # close eval window
        if hasattr(self, 'evalWindow'):
            self.evalWindow.close()

    def new_simulation(self):
        # new simulation callback
        def new_simulation():
            # close dialog
            self.newSimDialog.close()

            # update simulation
            self.simulation = solver(field(
                float(self.newSimDialog.xSizeEdit.text()),
                float(self.newSimDialog.ySizeEdit.text()),
                float(self.newSimDialog.deltaYEdit.text()),
                float(self.newSimDialog.deltaYEdit.text())))

            # update job
            self.job = jobs.Job()
            self.job.config['size'] = (self.simulation.field.xSize,
                    self.simulation.field.ySize)
            self.job.config['delta'] = (self.simulation.field.deltaX,
                    self.simulation.field.deltaY)

            # update plot
            self.plot.simulation = self.simulation
            self.plot.simulationHistory = [
                    numpy.zeros(self.simulation.field.oddFieldX['field'].shape)
                    ]
            self.plot.update()

            # init tree
            self.init_tree()

        # create dialog
        self.newSimDialog = dialogs.NewSimulation()
        self.newSimDialog.okButton.clicked.connect(new_simulation)

        # set settings
        self.newSimDialog.xSizeEdit.setText(
                '{}'.format(self.simulation.field.xSize))
        self.newSimDialog.ySizeEdit.setText(
                '{}'.format(self.simulation.field.ySize))
        self.newSimDialog.deltaXEdit.setText(
                '{}'.format(self.simulation.field.deltaX))
        self.newSimDialog.deltaYEdit.setText(
                '{}'.format(self.simulation.field.deltaY))

        # show dialog
        self.newSimDialog.show()

    def open_simulation(self):
        # open dialog
        fname, _ = QtGui.QFileDialog.getOpenFileName(self, 'Open simulation')

        # load job
        self.job.load(fname)

        # create new simulation
        xSize, ySize = self.job.config['size']
        deltaX, deltaY = self.job.config['delta']
        self.simulation = solver(field(xSize, ySize, deltaX, deltaY))

        # update plot
        self.plot.simulation = self.simulation
        self.plot.simulationHistory = [
                numpy.zeros(self.simulation.field.oddFieldX['field'].shape)]

        # init tree
        self.init_tree()

        # update materials
        for name, mask, er, sigma in self.job.material['electric']:
            self.simulation.material['electric'][mask_from_string(mask)] = \
                material.epsilon(er=er, sigma=sigma)
            QtGui.QTreeWidgetItem(self.layerItems[0],
                    [name, mask, 'epsilon(er={}, sigma={})'.format(er, sigma)])

        for name, mask, mur, sigma in self.job.material['magnetic']:
            self.simulation.material['magnetic'][mask_from_string(mask)] = \
                material.mu(mur=mur, sigma=sigma)
            QtGui.QTreeWidgetItem(self.layerItems[1],
                    [name, mask, 'mu(mur={}, sigma={})'.format(mur, sigma)])

        # update sources
        for name, mask, function in self.job.source:
            self.simulation.source[mask_from_string(mask)] = \
                    source_from_string(function)
            QtGui.QTreeWidgetItem(self.layerItems[2],
                    [name, mask, function])

        # update listener
        for name, x, y in self.job.listener:
            self.simulation.listener.append(listener(x, y))
            QtGui.QTreeWidgetItem(self.layerItems[3],
                    [name, 'x={}, y={}'.format(x, y)])

        # update plot
        self.plot.update()

    def save_simulation(self):
        # open dialog
        fname, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save simulation')

        # save job
        self.job.save(fname)

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
                self.simulation.material['electric'][
                        mask_from_string(mask)] = \
                                material.epsilon(er=er, sigma=sigma)
                QtGui.QTreeWidgetItem(self.layerItems[0],
                        [name, mask,
                            'epsilon(er={}, sigma={})'.format(er, sigma)])
                self.job.material['electric'].append((name, mask, er, sigma))

            elif type_ == 'Magnetic':
                mur, sigma = (float(self.newLayerDialog.rEdit.text()),
                        float(self.newLayerDialog.sigmaEdit.text()))
                self.simulation.material['electric'][
                        mask_from_string(mask)] = \
                                material.mu(mur=mur, sigma=sigma)
                QtGui.QTreeWidgetItem(self.layerItems[1],
                        [name, mask,
                            'mu(mur={}, sigma={})'.format(mur, sigma)])
                self.job.material['magnetic'].append((name, mask, mur, sigma))

            elif type_ == 'Source':
                self.simulation.source[
                        mask_from_string(mask)] = source_from_string(function)
                QtGui.QTreeWidgetItem(self.layerItems[2],
                        [name, mask, function])
                self.job.source.append((name, mask, function))

            elif type_ == 'Listener':
                x, y = (float(self.newLayerDialog.xEdit.text()),
                        float(self.newLayerDialog.yEdit.text()))
                self.simulation.listener.append(listener(x, y))
                QtGui.QTreeWidgetItem(self.layerItems[3],
                        [name, 'x={}, y={}'.format(x, y)])
                self.job.listener.append((name, x, y))

        except SyntaxError:
            return
        except NameError:
            return
        except ValueError:
            return

        # update plot
        self.plot.update()

    def run_simulation(self):
        # progress function
        self.simulationHistory = []
        duration = 5.0e-9

        def progress(t, deltaT, field):
            xShape, yShape = field.oddFieldX['flux'].shape
            interval = xShape * yShape * duration / (256e6 / 4.0)

            # save history
            if t / deltaT % (interval / deltaT) < 1.0:
                self.simulationHistory.append(field.oddFieldX['field']
                        + field.oddFieldY['field'])

            # print progess
            if t / deltaT % 100 < 1.0:
                print '{}'.format(t * 100.0 / duration)

        # finish function
        def finish():
            # start timer
            self.plot.show_simulation(self.simulationHistory)

            # open eval window
            self.evalWindow = EvalWindow(self.simulation)
            self.evalWindow.show()

        # run simulation
        self.simulation.solve(duration,
                progressfunction=progress, finishfunction=finish)
