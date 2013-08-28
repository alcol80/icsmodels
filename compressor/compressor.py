### Author: Alessio Coletta <alcol80@gmail.com>
###
### Copyright © 2013 Alessio Coletta - All Rights Reserved

from scipy.integrate import odeint
from numpy import arange
import matplotlib.pyplot as plt
import numpy as np

a = 3
b = 1
y0 = [0,0]

def desired(t):
    return 10

def ipressure(t):
    w = 2 * np.pi / 10
    if t < 10:
        r = 5
    elif t < 15:
        r = 2 * np.cos(w * t) + 3
    elif t < 25:
        r = 1
    elif t < 30:
        r = 3 * np.cos(w * t) + 4
    else:
        r = 7
    return r

def func(y,t):
    d = desired(t)
    p = ipressure(t)
    o = y[0]
    w = y[1]
    return [a*(w+p-o), b*(d-p-w)]

t = arange(0, 50.0, 0.05)

y = odeint(func, [0, 0], t)

### Plotting and export to file
output_file = 'out/fig.pdf'

# plot input and output pressure values
fig = plt.figure()
ax = fig.add_subplot(111)
ax.plot(t,y[:,0], label = "output pressure")
ax.plot(t,[ipressure(s) for s in t], 'r', label = "input pressure")

# plot light blue dots at the *back to regime* times
regime = 100
ax.plot(t[regime], y[regime,0], 'co', label = "regime")
regime = 370
ax.plot(t[regime], y[regime,0], 'co')
regime = 690
ax.plot(t[regime], y[regime,0], 'co')

# export the output
ax.legend(loc=4)
fig.savefig(output_file)
