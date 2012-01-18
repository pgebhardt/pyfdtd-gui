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

        cancelButton = QtGui.QPushButton('cancel')
        cancelButton.clicked.connect(self.close)
        buttonGrid.addWidget(cancelButton, 0, 1)

        # create edits
        self.nameEdit = QtGui.QLineEdit()
        self.typeComboBox = QtGui.QComboBox()
        self.typeComboBox.addItems(['Electric', 'Magnetic', 'Source'])
        self.typeComboBox.currentIndexChanged.connect(self.update_gui)
        self.maskEdit = QtGui.QLineEdit()
        self.rEdit = QtGui.QLineEdit()
        self.sigmaEdit = QtGui.QLineEdit()
        self.functionEdit = QtGui.QLineEdit()

        # create labels
        nameLabel = QtGui.QLabel('Name:')
        nameLabel.setBuddy(self.nameEdit)
        typeLabel = QtGui.QLabel('Type:')
        typeLabel.setBuddy(self.typeComboBox)
        maskLabel = QtGui.QLabel('Mask:')
        maskLabel.setBuddy(self.maskEdit)
        self.erLabel = QtGui.QLabel('Epsilon:')
        self.erLabel.setBuddy(self.rEdit)
        self.murLabel = QtGui.QLabel('Mu:')
        self.murLabel.setBuddy(self.rEdit)
        self.sigmaLabel = QtGui.QLabel('Sigma:')
        self.sigmaLabel.setBuddy(self.sigmaEdit)
        self.functionLabel = QtGui.QLabel('Function:')
        self.functionLabel.setBuddy(self.functionEdit)

        # set layout
        root.addWidget(nameLabel, 0, 0)
        root.addWidget(self.nameEdit, 0, 1)
        root.addWidget(typeLabel, 1, 0)
        root.addWidget(self.typeComboBox, 1, 1)
        root.addWidget(maskLabel, 2, 0)
        root.addWidget(self.maskEdit, 2, 1)
        root.addWidget(self.erLabel, 3, 0)
        root.addWidget(self.murLabel, 3, 0)
        root.addWidget(self.functionLabel, 3, 0)
        root.addWidget(self.rEdit, 3, 1)
        root.addWidget(self.functionEdit, 3, 1)
        root.addWidget(self.sigmaLabel, 4, 0)
        root.addWidget(self.sigmaEdit, 4, 1)
        root.addLayout(buttonGrid, 5, 1)

        # update gui
        self.update_gui()

    def update_gui(self):
        # show neccessary edits
        index = self.typeComboBox.currentText()

        if index == 'Electric':
            # hide
            self.murLabel.hide()
            self.functionLabel.hide()
            self.functionEdit.hide()

            # show
            self.erLabel.show()
            self.sigmaLabel.show()
            self.rEdit.show()
            self.sigmaEdit.show()
        elif index == 'Magnetic':
            # hide
            self.erLabel.hide()
            self.functionLabel.hide()
            self.functionEdit.hide()

            # show
            self.murLabel.show()
            self.sigmaLabel.show()
            self.rEdit.show()
            self.sigmaEdit.show()
        if index == 'Source':
            # hide
            self.erLabel.hide()
            self.murLabel.hide()
            self.sigmaLabel.hide()
            self.rEdit.hide()
            self.sigmaEdit.hide()

            # show
            self.functionLabel.show()
            self.functionEdit.show()
