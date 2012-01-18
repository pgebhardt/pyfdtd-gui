from pyfdtd import *
from numpy import *
from math import *

def mask_from_string(expression):
    def res(x, y):
        if eval(expression):
            return 1.0
        return 0.0
    return res

def source_from_string(expression):
    def res(flux, deltaT, t, mem):
        return -0.5*deltaT*eval(expression)
    return res
