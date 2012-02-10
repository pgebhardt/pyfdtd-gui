import os
os.environ['QT_API'] = 'pyside'

import numpy
from matplotlib.backends.backend_qt4agg \
        import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg \
        import NavigationToolbar2QTAgg as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.colors as colors

from PySide import QtGui
import plugins


class matplotlibCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=8, height=4, dpi=100, title=None):
        # create palette object
        palette = QtGui.QPalette()

        # get background color
        r, g, b, a = palette.color(QtGui.QPalette.Window.Background).toTuple()
        r, g, b, a = map(lambda x: x / 255.0, (r, g, b, a))

        # create figure
        fig = Figure(figsize=(width, height), dpi=dpi, facecolor=(r, g, b))

        # create single plot
        self.axes = fig.add_subplot(111)

        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        # set title
        if title != None:
            fig.suptitle(title, fontsize=12)

        # call base class constructor
        super(matplotlibCanvas, self).__init__(fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class Plot(QtGui.QWidget):
    def __init__(self, mainwindow, parent=None):
        # call base class constructor
        super(Plot, self).__init__()

        # save mainwindw
        self.mainwindow = mainwindow

        # create canvas
        self.canvas = matplotlibCanvas(None, 5.0, 5.0, dpi=72)

        # create toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # create layout
        grid = QtGui.QGridLayout()
        self.setLayout(grid)

        # set content margin
        grid.setContentsMargins(0, 0, 0, 0)

        # add widgets
        grid.addWidget(self.canvas, 0, 0)
        grid.addWidget(self.toolbar, 1, 0)

        # plot once
        self.update()

    def update(self):
        # get parameter
        sizeX, sizeY = self.mainwindow.job.config['size']
        deltaX, deltaY = self.mainwindow.job.config['delta']

        # create parser
        parser = plugins.NumpyParser()

        # get meshgrid
        x, y = numpy.meshgrid(numpy.arange(0.0, sizeX, deltaX),
                numpy.arange(0.0, sizeY, deltaY))
        x = x.transpose()
        y = y.transpose()

        # redraw im
        self.im = self.canvas.axes.imshow(
                numpy.fabs(numpy.transpose(
                    numpy.zeros((sizeX / deltaX, sizeY / deltaY)))),
                norm=colors.Normalize(0.0, 10.0),
                extent=[0.0, sizeX, sizeY, 0.0])

        # set label
        self.canvas.axes.set_xlabel('X')
        self.canvas.axes.set_ylabel('Y')

        # set grid
        self.canvas.axes.grid(True)

        # cummulate all layer masks
        self.masks = numpy.zeros((sizeX / deltaX, sizeY / deltaY))
        self.sources = numpy.zeros(self.masks.shape)
        self.listener = numpy.zeros(self.masks.shape)

        # get electric layer
        for name, mask, function in self.mainwindow.job.material['electric']:
            self.masks += numpy.where(parser.parse(str(mask), x=x, y=y),
                    1.0, 0.0)

        # get magnetic layer
        for name, mask, function in self.mainwindow.job.material['magnetic']:
            self.masks += numpy.where(parser.parse(str(mask), x=x, y=y),
                    1.0, 0.0)

        # get sources
        for name, mask, function in self.mainwindow.job.source:
            self.sources += numpy.where(parser.parse(str(mask), x=x, y=y),
                    1.0, 0.0)

        # get listener
        for name, x, y in self.mainwindow.job.listener:
            self.listener[x / deltaX, y / deltaY] = 5.0

        # norm masks
        if numpy.max(self.masks) != 0.0:
            self.masks *= 1.0 / numpy.max(self.masks)
        if numpy.max(self.sources) != 0.0:
            self.sources *= 10.0 / numpy.max(self.sources)

        # plot
        self.plot()

    def plot(self, field=None):
        # plot
        if field == None:
            self.im.set_array(numpy.transpose(
                self.masks + self.sources + self.listener))
        else:
            self.im.set_array(numpy.transpose(
                self.masks + self. sources + self.listener + field))

        # update canvas
        self.canvas.draw()
