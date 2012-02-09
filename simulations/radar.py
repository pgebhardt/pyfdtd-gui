# create numpy array
signals = []
for l in listener:
    signals.append(array(l.Z))

# calc deltaT
deltaT = 1.0 / (constants.c * sqrt(1.0 / 0.001**2 + 1.0 / 0.001**2))

# get t
t = arange(0.0, len(signals[0])*deltaT, deltaT)

# calc baseband signal
signals = map(hilbert, signals)
signals = map(absolute, signals)

# cut everything too early

# init plot
plot.grid(True)
plot.hold(True)

# plot signals
for signal in signals:
    plot.plot(t, signal)

