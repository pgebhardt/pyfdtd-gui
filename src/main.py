import sys
from PySide import QtGui
from PySide import QtDeclarative
import windows

# create qt application
app = QtGui.QApplication(sys.argv)

# create view
view = QtDeclarative.QDeclarativeView()

# create url to qml file
url = QtDeclarative.QUrl('./windows/MainWindow.qml')

# register plot
QtDeclarative.qmlRegisterType(windows.Plot, 'MatplotLib', 1, 0, 'Plot')
# set qml file
view.setSource(url)

# connect engine quit to application quit
view.engine().quit.connect(app.quit)

# show view
view.show()

# enter qt main loop
sys.exit(app.exec_())
