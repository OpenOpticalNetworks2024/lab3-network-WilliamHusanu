import numpy as np
import math

def lin2db(x):
    return 10*np.log10(x)


def db2lin(x):
    return 10**(x/10)

def snr(noise):
    return 10*math.log(0.001/noise,10)