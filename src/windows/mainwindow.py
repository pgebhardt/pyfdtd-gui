from PySide import QtCore, QtGui
from plot import *

# Main window for pyfdtd-gui application
class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        # call base class constructor
        super(MainWindow, self).__init__()

        # initialize gui elements
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('pyfdtd gui')
        self.resize(600, 600)        
        
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
        treeWidget.setText(0, 'bla')
        cities =  QtGui.QTreeWidgetItem(treeWidget)
        cities.setText(0, 'Cities')
        osloItem =  QtGui.QTreeWidgetItem(cities)
        osloItem.setText(0, 'Oslo')
        osloItem.setText(1, 'Yes') 
        planets = QtGui.QTreeWidgetItem(treeWidget, cities)
        planets.setText(0, 'Planets')

        # layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.canvas, 0, 0)
        grid.addWidget(btn, 1, 0)
        grid.addWidget(treeWidget, 0, 1)
        self.container.setLayout(grid)
