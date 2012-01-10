import sys
from PySide import QtCore, QtGui
import windows

# create application
app = QtGui.QApplication(sys.argv)

mainWindow = windows.MainWindow()
mainWindow.show()

sys.exit(app.exec_())
