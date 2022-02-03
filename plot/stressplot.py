#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
This script plots 3d volume of LAMMPS output of
ave/chunk for 3d bins chunk.
'''

import matplotlib
import argparse
from matplotlib import cm
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import numpy as np
import os

def read_file(file):
    nentries = 0
    try:
        with open(file, 'r') as f:
            f.readline() # Junk
            f.readline() # Kind of junk too
            fields = f.readline().split()[1:]
            data = {}
            for field in fields:
                data[field] = []

            while True:
                # Looking for the first line of a new entry, else break.
                line = f.readline().split()
                if not line:
                    break
                # These values can be exported as float
                # by LAMMPS to save space on big numbers
                timestep, nline, natoms = list(map(float, line))
                nline = int(nline)

                for _ in range(nline):
                    line = list(map(float, f.readline().split()))
                    for l, (field, value) in enumerate(zip(fields, line)):
                        if nentries:
                            data[field][l] += value
                        else:
                            data[field].append(value)
                if nentries == 0:
                    for field in data.keys():
                        data[field] = np.array(data[field])
                nentries += 1
            for field in data.keys():
                data[field] /= nentries
            return data
    except IOError:
        if os.path.isfile(file):
            raise SystemExit("Something went wrong when reading file")
        else:
            raise SystemExit("File {} does not exists.".format(file))

def main():
    parser = argparse.ArgumentParser(
        description="3d plot from LAMMPS averaged bin output from ave/bin."
    )
    parser.add_argument(
        "-v",
        "--verbose",
        dest="verbosity",
        default=0,
        action="count",
        help="display more information",
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="filename",
        default='bin.ave',
        help="The file to be read.",
    )
    parser.add_argument(
        "-c",
        "--cm",
        dest="cmap_name",
        default="coolwarm",
        help="The name of the colormap to use."
        )
    parser.add_argument(
        "-t",
        "--atom-threshold",
        dest="threshold",
        default="1.",
        help="Average of atoms (Ncount) below which bins are not ploted."
        )
    args = parser.parse_args()

    data = read_file(args.filename)

    # Get the number of coordinates for binned plot
    dim = []
    cmap_name = args.cmap_name
    for Coord in ["Coord1", "Coord2", "Coord3"]:
        if Coord in data.keys():
            dim.append(len(np.unique(data[Coord])))
    x, y, z = np.indices(dim)
    natoms = data['Ncount']
    voxels = (x >= 0) & (y >= 0) & (z >= 0)

    # number of interesting columns
    to_skip = len(dim)+2
    mykeys = list(data)[to_skip:]
    for k in mykeys:
        xbin = ybin = zbin = 0
        colors = np.zeros(voxels.shape)

        norm = matplotlib.colors.Normalize(vmin=min(data[k]), vmax=max(data[k]))
        for d in data[k]:
            colors[xbin, ybin, zbin] = d
            zbin += 1
            if zbin == voxels.shape[2]:
                zbin = 0
                ybin += 1
                if ybin == voxels.shape[1]:
                    ybin = 0
                    xbin += 1

        facecolors = plt.get_cmap(cmap_name)(norm(colors))
        xbin = ybin = zbin = 0
        for nat in natoms:
            if nat < 1.:
                voxels[xbin, ybin, zbin] = False
            zbin += 1
            if zbin == voxels.shape[2]:
                zbin = 0
                ybin += 1
                if ybin == voxels.shape[1]:
                    ybin = 0
                    xbin += 1

        ax = plt.figure().add_subplot(projection='3d')
        # ax.set_title(k+" Ave: {:6.4f} pm {:6.4f}".format(np.mean(data[k]), np.std(data[k])))
        ax.voxels(voxels, facecolors=facecolors, edgecolor='k')
        # m = cm.ScalarMappable(cmap=cmap_name, norm=norm)
        # m.set_array([])
        # plt.colorbar(m)

    # plt.show()
    plt.savefig('crap.png', dpi=300)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("User interruption")
