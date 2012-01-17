from PySide import QtCore, QtGui
from pyfdtd import *
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
        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(self.exitAction)

        # create Container
        self.container = QtGui.QWidget(self)
        self.setCentralWidget(self.container)

        # create matplotlib plot
        self.canvas = matplotlibCanvas(None, 5.0, 5.0, dpi=72, title='bla')

        # create button
        btn = QtGui.QPushButton('start simulation')
        btn.resize(btn.sizeHint())

        # create treeview
        treeGrid = QtGui.QGridLayout()
        treeLabel = QtGui.QLabel('Layer:')
        newLayerButton = QtGui.QPushButton('New Layer')
        newLayerButton.clicked.connect(lambda : dialogs.NewLayerDialog(show=True, mainWindow=self))

        self.treeWidget = QtGui.QTreeWidget()
        self.treeWidget.setColumnCount(2)
        treeLabel.setBuddy(self.treeWidget)

        # update tree
        self.update_tree()

        treeGrid.addWidget(treeLabel, 0, 0)
        treeGrid.addWidget(self.treeWidget, 1, 0)

        # layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.canvas, 0, 0)
        grid.addWidget(btn, 1, 0)
        grid.addWidget(newLayerButton, 1, 1)
        grid.addLayout(treeGrid, 0, 1)
        self.container.setLayout(grid)

    def create_actions(self):
        # exit action
        self.exitAction = QtGui.QAction('&Exit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)

    def update_tree(self):
        topItems = []
        topItems.append(QtGui.QTreeWidgetItem(None, ['Electric']))
        topItems.append(QtGui.QTreeWidgetItem(None, ['Magnetic']))
        topItems.append(QtGui.QTreeWidgetItem(None, ['Source']))
        self.treeWidget.addTopLevelItems(topItems)
        
        QtGui.QTreeWidgetItem(topItems[-1], ['Radar 1', 'sin(2.0*pi*x)'])
        QtGui.QTreeWidgetItem(topItems[0], ['Kupfer 1', 'blupp'])
        QtGui.QTreeWidgetItem(topItems[0], ['Kupfer 2', 'bla'])
        QtGui.QTreeWidgetItem(topItems[1], ['Magnet', 'kreis'])
