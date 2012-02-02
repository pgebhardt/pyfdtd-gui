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


class matplotlibCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""
    def __init__(self, parent=None, width=8, height=4, dpi=100, title=None):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        # We want the axes cleared every time plot() is called
        self.axes.hold(False)

        if title != None:
            fig.suptitle(title, fontsize=12)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self, QtGui.QSizePolicy.Expanding,
                QtGui.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class Plot(QtGui.QWidget):
    def __init__(self, simulation, parent=None):
        # call base class constructor
        super(Plot, self).__init__()

        # save simulation
        self.simulation = simulation

        # create canvas
        self.canvas = matplotlibCanvas(None, 5.0, 5.0, dpi=72, title='Domain')

        # create toolbar
        self.toolbar = NavigationToolbar(self.canvas, self)

        # create layout
        grid = QtGui.QGridLayout()
        grid.addWidget(self.canvas, 0, 0)
        grid.addWidget(self.toolbar, 1, 0)
        self.setLayout(grid)

        # plot once
        self.update()

    def update(self):
        # redraw im
        self.im = self.canvas.axes.imshow(
                numpy.fabs(numpy.transpose(
                    self.simulation.field.oddFieldX['field'])),
                norm=colors.Normalize(0.0, 10.0),
                extent=[0.0, self.simulation.field.xSize,
                    self.simulation.field.ySize, 0.0])
        self.canvas.axes.grid(True)

        # cummulate all layer masks
        self.masks = numpy.zeros(
                self.simulation.field.oddFieldX['field'].shape)
        self.sources = numpy.zeros(
                self.simulation.field.oddFieldX['field'].shape)
        self.listener = numpy.zeros(
                self.simulation.field.oddFieldX['field'].shape)

        # get electric layer
        layer = self.simulation.material['electric'].layer[2:]
        for fX, fY, dX, dY, mask in layer:
            self.masks += mask

        # get magnetic layer
        layer = self.simulation.material['magnetic'].layer[2:]
        for fX, fY, dX, dY, mask in layer:
            self.masks += mask

        # get sources
        for fX, fY, dX, dY, mask in self.simulation.source.layer:
            self.sources += mask

        # get listener
        for listener in self.simulation.listener:
            x, y = listener.pos
            self.listener[x / self.simulation.field.deltaX,
                    y / self.simulation.field.deltaY] = 5.0

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
