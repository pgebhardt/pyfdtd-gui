import sys
from PySide.QtGui import *
from PySide.QtCore import *
from PySide.QtDeclarative import *
import windows

# create qt application
app = QApplication(sys.argv)

# create view
view = QDeclarativeView()

# create url to qml file
url = QUrl('./windows/MainWindow.qml')

# register plot
qmlRegisterType(windows.Plot, 'MatplotLib', 1, 0, 'Plot')
# set qml file
view.setSource(url)

# connect engine quit to application quit
view.engine().quit.connect(app.quit)

# show view
view.show()

# enter qt main loop
sys.exit(app.exec_())
