import pyfdtd.material as material
from types import FunctionType
from numpy import *
from math import *


epsilon = material.epsilon
mu = material.mu


def pulse(amplitude, width, freq, offset=0.0):
    def res(t):
        return amplitude * exp(-(t - offset) ** 2 / (2 * width ** 2)) * \
                cos(2 * pi * freq * (t - offset))

    return res


def source_from_string(expression):
    def res(flux, deltaT, t, mem):
        # eval expression
        value = eval(expression)

        # check value type
        if isinstance(value, FunctionType):
            value = value(t)

        return -0.5 * deltaT * value
    return res
