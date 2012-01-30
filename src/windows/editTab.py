from PySide import QtGui
from dialogs import NewLayer
from plot import Plot


class EditTab(QtGui.QWidget):
    def __init__(self, simulation):
        # call base class constructor
        super(EditTab, self).__init__()

        # save simulation
        self.simulation = simulation

        # init gui
        self.init__gui()

    def init__gui(self):
        # create grid layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        # create plot
        self.plot = Plot(self.simulation)

        # create buttons
        startSimButton = QtGui.QPushButton('Start Simulation')
        startSimButton.clicked.connect(self.run_simulation)

        # new layer button
        def new_layer_clicked():
            self.newLayerDialog = dialogs.NewLayer(mainwindow=self)
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
