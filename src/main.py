import sys
from PySide import QtCore, QtGui
import windows
import dialogs

# create application
app = QtGui.QApplication(sys.argv)

mainWindow = windows.MainWindow()
mainWindow.show()

newLayer = dialogs.NewLayerDialog()
newLayer.show()

sys.exit(app.exec_())
