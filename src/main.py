"""Main execution file of PyFDTD-GUI."""

import sys
from PySide import QtGui
import matplotlib
matplotlib.use('Qt4Agg')

import windows


def main():
    # create application
    app = QtGui.QApplication(sys.argv)

    # create mainWindow
    mainWindow = windows.MainWindow()
    mainWindow.show()

    # run main loop
    sys.exit(app.exec_())

# call main function
if __name__ == '__main__':
    main()
