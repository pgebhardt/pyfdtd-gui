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


from lib import pyfdtd
from types import FunctionType
from scipy import constants
import numpy


def source_from_string(expression):
    # standart pulse function
    def pulse(amplitude=1e3, width=200e-12, freq=20e9, offset=1e-9):
        def res(flux, deltaT, t, mem):
            value = amplitude * \
                    numpy.exp(-(t - offset) ** 2 / (2 * width ** 2)) * \
                    numpy.cos(2 * numpy.pi * freq * (t - offset))

            return -0.5 * deltaT * value
        return res

    # try parse standart function
    function = eval(expression, {'pulse': pulse, 'sin': numpy.sin, 'cos':
        numpy.cos, 'exp': numpy.exp, 'pi': numpy.pi})

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
        pyfdtd.material.mu, 'sin': numpy.sin, 'cos': numpy.cos,
        'exp': numpy.exp, 'pi': numpy.pi, 'c': constants.c,
        'epsilon_0': constants.epsilon_0, 'mu_0': constants.mu_0})

    # check for function type
    if isinstance(function, FunctionType):
        return function

    # if not a material function, create one
    def res(flux, deltaT, t, mem):
        return eval(expression)

    return res
