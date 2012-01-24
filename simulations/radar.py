# create numpy array
signals = []
for l in listener:
    signals.append(array(l.Z))

# init plot
plot.grid(True)
plot.hold(True)

# plot signals
for signal in signals:
    plot.plot(signal[750:1100])

