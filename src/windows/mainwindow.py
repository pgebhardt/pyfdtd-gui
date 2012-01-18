from PySide import QtCore, QtGui
import matplotlib.colors as colors
from pyfdtd import *
from plugins import *
from plot import *
import dialogs

# Main window for pyfdtd-gui application
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # call base class constructor
        super(MainWindow, self).__init__()

        # init simulation
        self.simulation = solver(field(0.4, 0.4, 0.001))

        # initialize gui elements
        self.create_actions()
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('Pyfdtd GUI')
        self.resize(1000, 600)        
        
        # create menu bar
        fileMenu = self.menuBar().addMenu('&File')
        fileMenu.addAction(self.settingsAction)
        fileMenu.addAction(self.exitAction)

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
        treeLabel.setBuddy(self.treeWidget)

        # update tree
        self.layerItems = []
        self.layerItems.append(QtGui.QTreeWidgetItem(None, ['Electric']))
        self.layerItems.append(QtGui.QTreeWidgetItem(None, ['Magnetic']))
        self.layerItems.append(QtGui.QTreeWidgetItem(None, ['Source']))
        self.treeWidget.addTopLevelItems(self.layerItems)

        # add PML layer
        QtGui.QTreeWidgetItem(self.layerItems[0], ['PML', '', ''])
        QtGui.QTreeWidgetItem(self.layerItems[1], ['PML', '', ''])

        treeGrid.addWidget(treeLabel, 0, 0)
        treeGrid.addWidget(self.treeWidget, 1, 0)

        # layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.plot, 0, 0)
        grid.addWidget(startSimButton, 1, 0)
        grid.addWidget(newLayerButton, 1, 1)
        grid.addLayout(treeGrid, 0, 1)
        self.container.setLayout(grid)

    def create_actions(self):
        # settings action
        self.settingsAction = QtGui.QAction('&Settings', self, statusTip='Set domain size', triggered=self.update_settings)

        # exit action
        self.exitAction = QtGui.QAction('&Exit', self, shortcut='Ctrl+Q', statusTip='Exit application', triggered=self.close)

    def update_settings(self):
        # new settings callback
        def new_settings(xSize, ySize, deltaX, deltaY):
            self.simulation = solver(field(xSize, ySize, deltaX, seltaY))
            self.plot.simulation = self.simulation
            self.plot.update()

        # create dialog
        self.settingsDialog = dialogs.Settings()
        self.settingsDialog.show()

    def new_layer(self):
        # close dialog
        self.newLayerDialog.close()

        # get attributes
        name = self.newLayerDialog.nameEdit.text()
        type_ = self.newLayerDialog.typeComboBox.currentText()
        mask = self.newLayerDialog.maskEdit.text()
        function = self.newLayerDialog.functionEdit.text()

        # create layer
        if type_ == 'Electric':
            er, sigma = float(self.newLayerDialog.rEdit.text()), float(self.newLayerDialog.sigmaEdit.text())
            QtGui.QTreeWidgetItem(self.layerItems[0], [name, mask, 'epsilon(er={}, sigma={})'.format(er, sigma)])
            self.simulation.material['electric'][mask_from_string(mask)] = material.epsilon(er=er, sigma=sigma)
        elif type_ == 'Magnetic':
            mur, sigma = float(self.newLayerDialog.rEdit.text()), float(self.newLayerDialog.sigmaEdit.text())
            QtGui.QTreeWidgetItem(self.layerItems[0], [name, mask, 'mu(mur={}, sigma={})'.format(mur, sigma)])
            self.simulation.material['electric'][mask_from_string(mask)] = material.mu(mur=mur, sigma=sigma)
        elif type_ == 'Source':
            QtGui.QTreeWidgetItem(self.layerItems[2], [name, mask, function])
            self.simulation.source[mask_from_string(mask)] = source_from_string(function)

        # update plot
        self.plot.update()

    def run_simulation(self):
        # progress function
        self.simulationHistory = []
        duration = 1.0e-9
        def progress(t, deltaT, field):
            xShape, yShape = field.oddFieldX['flux'].shape
            interval = xShape*yShape*duration/(256e6/4.0)

            # save history
            if t/deltaT % (interval/deltaT) < 1.0:
                self.simulationHistory.append(field.oddFieldX['field'] + field.oddFieldY['field'])
            
            # print progess
            if t/deltaT % 100 < 1.0:
                print '{}'.format(t*100.0/duration)

        # finish function
        def finish():
            # start timer
            self.plot.show_simulation(self.simulationHistory)
            print 'finish'

        # run simulation
        self.simulation.solve(duration, progressfunction=progress, finishfunction=finish) 
