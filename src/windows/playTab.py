from PySide import QtGui, QtCore


class PlayTab(QtGui.QWidget):
    def __init__(self, mainwindow):
        # call base class constructor
        super(PlayTab, self).__init__()

        # save mainwindow
        self.mainwindow = mainwindow
