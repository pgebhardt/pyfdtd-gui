# GUI for pyfdtd using PySide
# Copyright (C) 2012  Patrik Gebhardt
# Contact: grosser.knuff@googlemail.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
                    (512e6 / 4.0)

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
