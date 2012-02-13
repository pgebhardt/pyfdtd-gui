from PySide import QtGui


class NewSimulation(QtGui.QDialog):
    def __init__(self, mainwindow=None):
        # call base class constructor
        super(NewSimulation, self).__init__(mainwindow)

        # init gui
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('New Simulation')

        # layout
        root = QtGui.QGridLayout(self)

        # create buttons
        self.okButton = QtGui.QPushButton('OK')
        cancelButton = QtGui.QPushButton('cancel')
        cancelButton.clicked.connect(self.close)

        # create edits
        self.xSizeEdit = QtGui.QLineEdit()
        self.ySizeEdit = QtGui.QLineEdit()
        self.deltaXEdit = QtGui.QLineEdit()
        self.deltaYEdit = QtGui.QLineEdit()

        # create labels
        sizeLabel = QtGui.QLabel('Size:')
        sizeLabel.setBuddy(self.xSizeEdit)
        deltaLabel = QtGui.QLabel('Delta:')
        deltaLabel.setBuddy(self.deltaXEdit)
        x1Label = QtGui.QLabel('x')
        x2Label = QtGui.QLabel('x')

        # set layout
        root.addWidget(sizeLabel, 0, 0)
        root.addWidget(self.xSizeEdit, 0, 1)
        root.addWidget(x1Label, 0, 2)
        root.addWidget(self.ySizeEdit, 0, 3)
        root.addWidget(deltaLabel, 1, 0)
        root.addWidget(self.deltaXEdit, 1, 1)
        root.addWidget(x2Label, 1, 2)
        root.addWidget(self.deltaYEdit, 1, 3)
        root.addWidget(self.okButton, 2, 1)
        root.addWidget(cancelButton, 2, 3)
