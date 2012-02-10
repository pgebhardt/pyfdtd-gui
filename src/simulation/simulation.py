from PySide import QtCore


class SimulationThread(QtCore.QThread):
    def __init__(self, mainwindow):
        # call base class constructor
        super(SimulationThread, self).__init__()

        # save and mainwindow
        self.mainwindow = mainwindow
        self.progress = 0.0

    def run(self):
        # init simulation
        if hasattr(self, 'simulationHistory'):
            # clear simulation
            self.mainwindow.editTab.update()

        # progress function
        self.simulationHistory = []

        def progress(t, deltaT, field):
            xShape, yShape = field.oddFieldX['flux'].shape
            interval = xShape * yShape * \
                    self.mainwindow.job.config['duration'] / \
                    (256e6 / 4.0)

            # save history
            if t / deltaT % (interval / deltaT) < 1.0:
                self.simulationHistory.append(field.oddFieldX['field']
                        + field.oddFieldY['field'])

            # print progess
            self.progress = t * 100.0 / self.mainwindow.job.config['duration']

        # finish function
        def finish():
            # start timer
            self.mainwindow.playTab.simulationHistory = self.simulationHistory
            self.mainwindow.playTab.playButton.setEnabled(True)

        # deactivate play button
        self.mainwindow.playTab.playButton.setDisabled(True)

        # run simulation
        self.mainwindow.simulation.solve(
                self.mainwindow.job.config['duration'],
                progressfunction=progress, finishfunction=finish)
