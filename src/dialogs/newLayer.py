from PySide import QtGui


class NewLayer(QtGui.QWidget):
    def __init__(self, mainwindow=None):
        # call base class constructor
        super(NewLayer, self).__init__()

        # init gui
        self.init_gui()

        # save parameter
        self.mainwindow = mainwindow

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
        self.typeComboBox.addItems(['Electric', 'Magnetic',
                                    'Source', 'Listener'])
        self.typeComboBox.currentIndexChanged.connect(self.update_gui)
        self.maskEdit = QtGui.QLineEdit()
        self.functionEdit = QtGui.QLineEdit('epsilon()')
        self.xEdit = QtGui.QLineEdit('0.0')
        self.yEdit = QtGui.QLineEdit('0.0')

        # create labels
        nameLabel = QtGui.QLabel('Name:')
        nameLabel.setBuddy(self.nameEdit)
        typeLabel = QtGui.QLabel('Type:')
        typeLabel.setBuddy(self.typeComboBox)
        self.maskLabel = QtGui.QLabel('Mask:')
        self.maskLabel.setBuddy(self.maskEdit)
        self.functionLabel = QtGui.QLabel('Function:')
        self.functionLabel.setBuddy(self.functionEdit)
        self.xLabel = QtGui.QLabel('X:')
        self.xLabel.setBuddy(self.xEdit)
        self.yLabel = QtGui.QLabel('Y:')
        self.yLabel.setBuddy(self.yEdit)

        # set layout
        root.addWidget(nameLabel, 0, 0)
        root.addWidget(self.nameEdit, 0, 1)
        root.addWidget(typeLabel, 1, 0)
        root.addWidget(self.typeComboBox, 1, 1)
        root.addWidget(self.maskLabel, 2, 0)
        root.addWidget(self.maskEdit, 2, 1)
        root.addWidget(self.functionLabel, 3, 0)
        root.addWidget(self.xLabel, 3, 0)
        root.addWidget(self.functionEdit, 3, 1)
        root.addWidget(self.xEdit, 3, 1)
        root.addWidget(self.yLabel, 4, 0)
        root.addWidget(self.yEdit, 4, 1)
        root.addLayout(buttonGrid, 5, 1)

        # update gui
        self.update_gui()

    def update_gui(self):
        # show neccessary edits
        index = self.typeComboBox.currentText()

        if index == 'Electric' or index == 'Magnetic' or index == 'Source':
            # hide
            self.xLabel.hide()
            self.yLabel.hide()
            self.xEdit.hide()
            self.yEdit.hide()

            # show
            self.maskLabel.show()
            self.maskEdit.show()
            self.functionLabel.show()
            self.functionEdit.show()

            # set standart value fro function
            if index == 'Electric':
                self.functionEdit.setText('epsilon()')
            elif index == 'Magnetic':
                self.functionEdit.setText('mu()')
            else:
                self.functionEdit.setText('pulse()')

        elif index == 'Listener':
            # hide
            self.maskLabel.hide()
            self.functionLabel.hide()
            self.maskEdit.hide()
            self.functionEdit.hide()

            # show
            self.xLabel.show()
            self.yLabel.show()
            self.xEdit.show()
            self.yEdit.show()
