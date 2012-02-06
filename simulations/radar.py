# create numpy array
signals = []
for l in listener:
    signals.append(array(l.Z))

# init plot
plot.grid(True)
plot.hold(True)

signals = map(hilbert, signals)
signals = map(absolute, signals)

# plot signals
for signal in signals:
    plot.plot(signal)

