from PySide import QtCore, QtGui

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
