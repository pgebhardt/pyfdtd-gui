from PySide import QtCore, QtGui
from plot import *

# Main window for pyfdtd-gui application
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # call base class constructor
        super(MainWindow, self).__init__()

        # initialize gui elements
        self.create_actions()
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('pyfdtd gui')
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
        treeWidget = QtGui.QTreeWidget()
        treeWidget.setColumnCount(2)
        items = []
        for i in range(10):
            items.append(QtGui.QTreeWidgetItem(None, ['item: {}'.format(i), 'bla']))
        treeWidget.addTopLevelItems(items) 
        
        # layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.canvas, 0, 0)
        grid.addWidget(btn, 1, 0)
        grid.addWidget(treeWidget, 0, 1)
        self.container.setLayout(grid)

    def create_actions(self):
        # exit action
        self.exitAction = QtGui.QAction('&Extit', self)
        self.exitAction.setShortcut('Ctrl+Q')
        self.exitAction.setStatusTip('Exit application')
        self.exitAction.triggered.connect(self.close)
