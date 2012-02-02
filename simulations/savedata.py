# create numpy array
signals = []
for l in listener:
    signals.append(array(l.Z))

for i in range(len(signals)):
    numpy.savetxt("signal-{}.txt".format(i), signals[i])