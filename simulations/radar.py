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

def phaseshift(signal, phase=0):
    return signal*exp(phase*1j)

result = []
timerange = slice(2.5e-9/deltaT, 5e-9/deltaT)

phaserange = arange(-pi/2, 0.0, pi/128)
for phase in phaserange:
    result.append(add.reduce(convolve(phaseshift(signals[0][timerange], phase),
        signals[1][timerange])))

phaserange = arange(0.0, pi/2, pi/128)
for phase in phaserange:
    result.append(add.reduce(convolve(signals[0][timerange],
        phaseshift(signals[1][timerange], phase))))

# post process result
result = array(result)

# init plot
plot.grid(True)
plot.hold(True)

print linspace(-0.5, 0.5, len(result))[result.argmax()]*pi

# plot signals
for signal in signals:
    plot.plot(linspace(-0.5, 0.5, len(result)), result)