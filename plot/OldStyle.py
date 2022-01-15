#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
An old journal style plotting configuration file
'''

import numpy as np
import re
from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import sys

plt.rc('axes', linewidth=2)
label_fontsize = 20
ticks_fontsize = 20
linewidth = 3
axes_linewidth = 1
major_tick_length = 15
minor_tick_length = major_tick_length//2
no_tick = 0

# print(plt.rcParams.keys())
# sys.exit()
plt.rcParams['font.family'] = 'Latin Modern Math'
plt.rcParams['font.weight'] = 'normal'
plt.rcParams['font.variant'] = 'small-caps' # Unfortunately, this does not work yet with matplotlib
plt.rcParams['axes.linewidth'] = axes_linewidth
plt.rcParams['lines.linewidth'] = linewidth
plt.rcParams['axes.labelsize'] = label_fontsize
plt.rcParams['legend.fontsize'] = label_fontsize
plt.rcParams['xtick.major.size'] = major_tick_length
plt.rcParams['xtick.minor.visible'] = True
plt.rcParams['xtick.minor.size'] = minor_tick_length
plt.rcParams['xtick.labelsize'] = ticks_fontsize
plt.rcParams['ytick.labelsize'] = ticks_fontsize
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['ytick.right'] = True
plt.rcParams['ytick.major.size'] = major_tick_length
plt.rcParams['ytick.minor.visible'] = True
plt.rcParams['ytick.minor.size'] = minor_tick_length
plt.rcParams['xtick.major.width'] = axes_linewidth
plt.rcParams['ytick.major.width'] = axes_linewidth
plt.rcParams['xtick.minor.width'] = axes_linewidth
plt.rcParams['ytick.minor.width'] = axes_linewidth
plt.rcParams['lines.markerfacecolor'] = 'white'
plt.rcParams['lines.markeredgecolor'] = 'black'
nlinestyle = 4
linestyle_list = ['-', '--', '-.', ':']
color_list = ['#000000', '#888888', '#CCCCCC']
marker_list = ['o', 's', 'v', '^']
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list) * (plt.cycler(linestyle=linestyle_list) + plt.cycler(marker=marker_list))

##### SOME EXAMPLES FOR TESTING PURPOSE ####
##### WITH SOME PERSONAL ADVICES

# 1) Better to set font and stuff for each axes
# 2) The bigger the better

##### Plotting linear data
npoints = 10
for i in range(12):
    data = np.linspace(0, 1, 10)
    plt.plot((i+1)*data, label=" ".join(['data', str(i+1)]))
ax = plt.gca()  # Get current axes to set properties
ax.legend(frameon=False)  # Fat font, no frame
ax.set_xlabel(r"PIF ($\int_{-\infty}^{3} \frac{x}{l_0}$)")
ax.set_ylabel("POUET")

##### Plotting heatmap
# data = np.random.rand(20, 20)
# plt.pcolormesh(data, cmap=GCcmap, rasterized=True)  # Data is output from ListedColormap
# plt.colorbar(ax = plt.gca())  # Puts the colorbar on the side

##### Show result
plt.show()
