from PySide import QtGui, QtCore

class NewLayerDialog(QtGui.QWidget):
    def __init__(self):
        # call base class constructor
        super(NewLayerDialog, self).__init__()

        # init gui
        self.init_gui()

    def init_gui(self):
        # set window title
        self.setWindowTitle('New Layer')
        self.resize(400, 400)

        # layout
        root = QtGui.QGridLayout(self)

        # create buttons
        buttonGrid = QtGui.QGridLayout()

        okButton = QtGui.QPushButton('OK')
        okButton.clicked.connect(self.get_layer)
        buttonGrid.addWidget(okButton, 0, 0)

        cancleButton = QtGui.QPushButton('cancle')
        cancleButton.clicked.connect(self.close)
        buttonGrid.addWidget(cancleButton, 0, 1)

        # create edits
        nameEdit = QtGui.QLineEdit()
        maskFunctionEdit = QtGui.QTextEdit()

        # create labels
        nameLabel = QtGui.QLabel('&Name:')
        nameLabel.setBuddy(nameEdit)

        # set layout
        root.addWidget(nameLabel, 0, 0)
        root.addWidget(nameEdit, 0, 1)
        root.addWidget(maskFunctionEdit, 1, 1)
        root.addLayout(buttonGrid, 2, 1)

    def get_layer(self):
        pass
