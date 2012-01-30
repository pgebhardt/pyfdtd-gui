from PySide import QtCore, QtGui
import matplotlib.colors as colors
import pickle
import pyfdtd
from plot import Plot
import dialogs
import jobs
from evalTab import EvalTab
from editTab import EditTab
from playTab import PlayTab


# Main window for pyfdtd-gui application
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # call base class constructor
        super(MainWindow, self).__init__()

        # init simulation
        self.simulation = pyfdtd.solver(pyfdtd.field(0.4, 0.4, 0.001))
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

        # init tab view
        tabView = QtGui.QTabWidget()
        self.setCentralWidget(tabView)

        # create edit tab
        self.editTab = EditTab(self)
        tabView.addTab(self.editTab, 'Edit')

        # create play tab
        self.playTab = PlayTab(self)
        tabView.addTab(self.playTab, 'Play')

        # create edit tab
        self.evalTab = EvalTab(self)
        tabView.addTab(self.evalTab, 'Evaluate')

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
            self.simulation = pyfdtd.solver(pyfdtd.field(
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

            # update edit tab
            self.editTab.init_tree()
            self.editTab.update()

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

        # clear editTab tree
        self.editTab.init_tree()

        # update materials
        for name, mask, er, sigma in self.job.material['electric']:
            self.simulation.material['electric'][mask_from_string(mask)] = \
                pyfdtd.material.epsilon(er=er, sigma=sigma)
            QtGui.QTreeWidgetItem(self.editTab.layerItems[0],
                    [name, mask, 'epsilon(er={}, sigma={})'.format(er, sigma)])

        for name, mask, mur, sigma in self.job.material['magnetic']:
            self.simulation.material['magnetic'][mask_from_string(mask)] = \
                pyfdtd.material.mu(mur=mur, sigma=sigma)
            QtGui.QTreeWidgetItem(self.editTab.layerItems[1],
                    [name, mask, 'mu(mur={}, sigma={})'.format(mur, sigma)])

        # update sources
        for name, mask, function in self.job.source:
            self.simulation.source[mask_from_string(mask)] = \
                    source_from_string(function)
            QtGui.QTreeWidgetItem(self.editTab.layerItems[2],
                    [name, mask, function])

        # update listener
        for name, x, y in self.job.listener:
            self.simulation.listener.append(pyfdtd.listener(x, y))
            QtGui.QTreeWidgetItem(self.editTab.layerItems[3],
                    [name, 'x={}, y={}'.format(x, y)])

        # update edit tab
        self.editTab.update()

    def save_simulation(self):
        # open dialog
        fname, _ = QtGui.QFileDialog.getSaveFileName(self, 'Save simulation')

        # save job
        self.job.save(fname)

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
