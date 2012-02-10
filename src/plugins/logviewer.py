from PySide import QtGui


class LogViewer(QtGui.QTextEdit):
    def __init__(self):
        # call base class constructor
        super(LogViewer, self).__init__()

        # set to read only
        self.setReadOnly(True)

    def write(self, txt):
        # default write method for streaming compatibility
        self.setPlainText(self.toPlainText() + txt)

        # scroll to bottom
        self.moveCursor(QtGui.QTextCursor.End)
        self.ensureCursorVisible()
