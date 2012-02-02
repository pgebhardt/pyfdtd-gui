# load from file
signals = []
for i in range(0, 3):
    signals.append(numpy.genfromtxt("signal-{}.txt".format(i)))

# calc time step
deltaT = 1.0 / (constants.c * sqrt(1.0 / 0.001**2 + 1.0 / 0.001**2))

# generate x
x = arange(0.0, len(signals[0])*deltaT, deltaT)

# post processing
signals = map(hilbert, signals)
signals = map(absolute, signals)

# plotting range
range = slice(int(4e-9/deltaT), int(5e-9/deltaT))

# plot
plot.grid(True)
plot.hold(True)

for signal in signals:
    plot.plot(x[range], signal[range])
