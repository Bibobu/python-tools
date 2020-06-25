#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Your docstring here
'''

import numpy as np
import re
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap

# Found in a comment on Toward data science
# Tweaked my way
def colourGradient(fromRGB, toRGB, steps=50):
    '''
    colourGradient(fromRGB, toRGB, steps=50)
    Returns a list of <steps> html-style colour codes forming a gradient between the two supplied colours
    steps is an optional parameter with a default of 50
    If fromRGB or toRGB is not a valid colour code (omitting the initial hash sign is permitted),
    an exception is raised.
    '''
    # hexRgbRe = re.compile('#?[0–9A-F]{6}')  # So we can check format of input html-style colour codes
    # The code will handle upper and lower case hex characters, with or without a # at the front
    # if not hexRgbRe.match(fromRGB) or not hexRgbRe.match(toRGB):
        # raise Exception('Invalid parameter format')
 
    # Tidy up the parameters
    RGBA = np.ones((steps, 4))
    rgbFrom = fromRGB.split('#')[-1]
    rgbTo = toRGB.split('#')[-1]

    # Extract the three RGB fields as integers from each (from and to) parameter
    rFrom, gFrom, bFrom = [(int(rgbFrom[n:n+2], 16)) for n in range(0, len(rgbFrom), 2)]
    rTo, gTo, bTo = [(int(rgbTo[n:n+2], 16)) for n in range(0, len(rgbTo), 2)]

    # For each colour component, generate the intermediate steps
    rSteps = ['{0:02x}'.format(round(rFrom + n * (rTo - rFrom) / (steps - 1))) for n in range(steps)]
    gSteps = ['{0:02x}'.format(round(gFrom + n * (gTo - gFrom) / (steps - 1))) for n in range(steps)]
    bSteps = ['{0:02x}'.format(round(bFrom + n * (bTo - bFrom) / (steps - 1))) for n in range(steps)]

    # Values in 0, 1 format
    Rcol = np.array([round(rFrom + n * (rTo - rFrom) / (steps - 1))/256 for n in range(steps)])
    Gcol = np.array([round(gFrom + n * (gTo - gFrom) / (steps - 1))/256 for n in range(steps)])
    Bcol = np.array([round(bFrom + n * (bTo - bFrom) / (steps - 1))/256 for n in range(steps)])
    # Reassemble the components into a list of html-style #rrggbb codes
    RGBA[:, 0] = Rcol
    RGBA[:, 1] = Gcol
    RGBA[:, 2] = Bcol
    return RGBA, ["".join(['#',r,g,b]) for r, g, b in zip(rSteps, gSteps, bSteps)]

# My set of colors from colormind.io
GC_pink = "#FF01C0"
GC_dblue = "#122070"
# GC_blue = "#0013FF"
GC_blue = "#2CBDFE"
GC_green = "#558D3A"
GC_orange = "#FF8C00"
RGBA, GC_grad = colourGradient(GC_blue, GC_orange)
GCcmap = ListedColormap(RGBA)

color_list = [GC_pink, GC_dblue, GC_blue, GC_green, GC_orange]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
plt.rc('axes', linewidth=2)

##### SOME EXAMPLES FOR TESTING PURPOSE ####
##### WITH SOME PERSONAL ADVICES

# 1) Better to set font and stuff for each axes
# 2) The bigger the better

##### Plotting linear data
# npoints = 10
# data = np.random.rand(npoints)  # Random datas
# for i, _ in enumerate(color_list):
#     plt.plot((i+1)*data, label=" ".join(['data', str(i+1)]))
# ax = plt.gca()  # Get current axes to set properties
# ax.legend(frameon=False, fontsize=30)  # Fat font, no frame
# ax.set_ylabel("Pouet", fontname="Hack", fontsize=30)  # ylabel name, font is Hack, size 30pts
# ax.tick_params(axis='both', which='major', labelsize=30)  # Biggers ticks, bigger ticks label!

##### Plotting heatmap
# data = np.random.rand(20, 20)
# plt.pcolormesh(data, cmap=GCcmap, rasterized=True)  # Data is output from ListedColormap
# plt.colorbar(ax = plt.gca())  # Puts the colorbar on the side

##### Show result
# plt.show()
