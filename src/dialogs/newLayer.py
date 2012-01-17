from PySide import QtGui, QtCore

class NewLayer(QtGui.QWidget):
    def __init__(self, mainWindow=None):
        # call base class constructor
        super(NewLayer, self).__init__()

        # init gui
        self.init_gui()

        # save parameter
        self.mainWindow = mainWindow

    def init_gui(self):
        # set window title
        self.setWindowTitle('New Layer')

        # layout
        root = QtGui.QGridLayout(self)

        # create buttons
        buttonGrid = QtGui.QGridLayout()

        self.okButton = QtGui.QPushButton('OK')
        buttonGrid.addWidget(self.okButton, 0, 0)

        cancleButton = QtGui.QPushButton('cancle')
        cancleButton.clicked.connect(self.close)
        buttonGrid.addWidget(cancleButton, 0, 1)

        # create edits
        self.nameEdit = QtGui.QLineEdit()
        self.typeComboBox = QtGui.QComboBox()
        self.typeComboBox.addItems(['Electric', 'Magnetic', 'Source'])
        self.maskEdit = QtGui.QLineEdit()
        self.functionEdit = QtGui.QLineEdit()

        # create labels
        nameLabel = QtGui.QLabel('Name:')
        nameLabel.setBuddy(self.nameEdit)
        typeLabel = QtGui.QLabel('Type:')
        typeLabel.setBuddy(self.typeComboBox)
        maskLabel = QtGui.QLabel('Mask:')
        maskLabel.setBuddy(self.maskEdit)
        functionLabel = QtGui.QLabel('Function:')
        functionLabel.setBuddy(self.functionEdit)

        # set layout
        root.addWidget(nameLabel, 0, 0)
        root.addWidget(self.nameEdit, 0, 1)
        root.addWidget(typeLabel, 1, 0)
        root.addWidget(self.typeComboBox, 1, 1)
        root.addWidget(maskLabel, 2, 0)
        root.addWidget(self.maskEdit, 2, 1)
        root.addWidget(functionLabel, 3, 0)
        root.addWidget(self.functionEdit, 3, 1)
        root.addLayout(buttonGrid, 4, 1)
