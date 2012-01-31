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
