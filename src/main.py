import sys
from PySide import QtCore, QtGui
import windows
import dialogs

# create application
app = QtGui.QApplication(sys.argv)

mainWindow = windows.MainWindow()
mainWindow.show()

evalWindow = windows.EvalWindow(None)
evalWindow.show()

sys.exit(app.exec_())

# TODO
