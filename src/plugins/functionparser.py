from lib import pyfdtd
from types import FunctionType
from numpy import *
from math import *


def source_from_string(expression):
    # standart pulse function
    def pulse(amplitude=1e3, width=200e-12, freq=20e9, offset=1e-9):
        def res(flux, deltaT, t, mem):
            value = amplitude * exp(-(t - offset) ** 2 / (2 * width ** 2)) * \
                    cos(2 * pi * freq * (t - offset))

            return -0.5 * deltaT * value
        return res

    # try parse standart function
    function = eval(expression, {'pulse': pulse})

    # check for function type
    if isinstance(function, FunctionType):
        return function

    # if not a source function, create one
    def res(flux, deltaT, t, mem):
        return -0.5 * deltaT * eval(expression)

    return source(res)


def material_from_string(expression):
    # try parse standart functions
    function = eval(expression, {'epsilon': pyfdtd.material.epsilon, 'mu':
        pyfdtd.material.mu})

    # check for function type
    if isinstance(function, FunctionType):
        return function

    # if not a material function, create one
    def res(flux, deltaT, t, mem):
        return eval(expression)

    return res
