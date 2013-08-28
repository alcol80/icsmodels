#!/usr/bin/python

# Author: Alessio Coletta <alcol80@gmail.com>
#
# Copyright (C) 2013 Alessio Coletta - All Rights Reserved

from scipy.integrate import odeint
from numpy import arange
import matplotlib.pyplot as plt
import numpy as np

def plot_steady_point(p, steady):
    rx, ry = t[steady], y[steady,0]
    p.plot([rx,rx], [ry,0], 'g:')
    p.plot(rx, ry, 'co')
    return rx

def annotate_multiple(p, text, points, **kwargs):
    p.annotate(text, xy=points[0], **kwargs)
    kwargs['alpha'] = 0.0
    for point in points[1:]:
        p.annotate(text, xy=point, **kwargs)

### Math definitions: parameters and functions
a, b = 3, 1

def desired(t):
    return 10

def ipressure(t):
    w = 2 * np.pi / 10          # just a useful radians conversion constant
    if   t < 10: r = 5
    elif t < 15: r = 2 * np.cos(w * t) + 3
    elif t < 25: r = 1
    elif t < 30: r = 3 * np.cos(w * t) + 4
    else:        r = 7
    return r

def func(y,t):
    d, p = desired(t), ipressure(t)
    o, w = y[0], y[1]
    return [a*(w+p-o), b*(d-p-w)]


### Numeric evaluation of the model
t_max = 45
t, step = np.linspace(0, t_max, num=900, retstep=True)

y0 = [ipressure(0), 0]
y = odeint(func, y0, t)

### Plotting the results
output_file = 'out/fig.pdf'

fig = plt.figure()
ax = fig.add_subplot(111)
ds = desired(t)

ax.plot([0, t_max], [10.0, 10.0], 'y--')
ax.plot(t,y[:,0], label = "output pressure")
ax.plot(t,[ipressure(s) for s in t], 'r', label = "input pressure")

ax.annotate('input\npressure\ndrop', xy = (11, 3), xytext=(8, 2),
            arrowprops=dict(arrowstyle='->'), horizontalalignment='right')
ax.annotate('input pressure\nincrease', xy = (26, 4), xytext=(17, 5),
            arrowprops=dict(arrowstyle='->'))

xticks = [plot_steady_point(ax, np.around(rp / step)) for rp in [6.5, 19.3, 35]]
ax.set_xticks(xticks)
ax.set_xticklabels([r'$t_1$', r'$t_2$', r'$t_3$'])

ax.set_yticks([desired(0)])
ax.set_yticklabels(['set\npoint'])

steady_points = [ (x, desired(x)) for x in xticks ]
annotate_multiple(ax, 'steady state\nreached', steady_points, xytext=(13, 7),
                  arrowprops=dict(arrowstyle='->', shrinkB = 10),
                  horizontalalignment='center')

ax.set_xlabel('Time')
ax.set_ylabel('Input and Output Pressure')
ax.legend(loc=4)

fig.savefig(output_file)
