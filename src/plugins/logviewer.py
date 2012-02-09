import sys
from PySide import QtGui


class OutputWindow(QtGui.QPlainTextEdit):
    def write(self, txt):
        self.appendPlainText(str(txt))

app = QtGui.QApplication(sys.argv)
out = OutputWindow()
sys.stdout = out
sys.stderr = out
out.show()

print 'Hallo Welt'

sys.exit(app.exec_())
