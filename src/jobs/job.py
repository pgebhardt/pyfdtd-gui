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


import pickle


class Job:
    def __init__(self):
        # create standart values
        self.config = {'size': (0.4, 0.4), 'delta': (0.001, 0.001), 'duration':
                5e-9}
        self.listener = []
        self.source = []
        self.material = {'electric': [], 'magnetic': []}

    def load(self, fname):
        # open file
        f = open(fname, 'rb')

        # unpickle
        self.config = pickle.load(f)
        self.listener = pickle.load(f)
        self.source = pickle.load(f)
        self.material = pickle.load(f)

        # close file
        f.close()

    def save(self, fname):
        # open file
        f = open(fname, 'wb')

        # pickle
        pickle.dump(self.config, f)
        pickle.dump(self.listener, f)
        pickle.dump(self.source, f)
        pickle.dump(self.material, f)

        # close file
        f.close()

# test
if __name__ == '__main__':
    # create job
    job = Job()

    # save job
    job.save('temp.sim')

    # change job
    job.config['size'] = (0.2, 0.4)
    print job.config['size']

    # load job
    job.load('temp.sim')
    print job.config['size']
