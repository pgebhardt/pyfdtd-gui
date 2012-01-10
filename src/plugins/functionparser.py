from numpy import *

def mask_from_string(expression):
    def res(x, y):
        if eval(expression):
            return 1.0
        return 0.0
    return res

def source_from_string(expression):
    def res(t):
        return eval(expression)
    return res
