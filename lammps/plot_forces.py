#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Plot LAMMPS forces.
'''

import argparse
import numpy as np
import os
import logging
import sys
from matplotlib import pyplot as plt


def compute_energy(tp):
    r = tp[0]
    fo = tp[2]
    e = np.zeros(r.shape)
    for i, (ri, fi) in enumerate(zip(r, fo)):
        if i == 0:
            continue
        dr = ri - r[i-1]
        e[i] = e[i-1]-dr*fo[i-1]
    e -= e[-1]
    return e


def main():

    parser = argparse.ArgumentParser(
        description="Plots Lammps tabulated forces."
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
        dest="infile",
        default="",
        help="File to read",
    )
    parser.add_argument(
        "-x",
        dest="xrange",
        default="",
        help="xrange : separated (for negative values: -x=-3:10)",
    )
    parser.add_argument(
        "-y",
        dest="yrange",
        default="",
        help="yrange : separated",
    )
    parser.add_argument(
        "-t",
        dest="temp",
        default=-1, type=float,
        help="temperature for kbT plot [default none]",
    )
    parser.add_argument(
        "-e",
        dest="extract",
        action="store_true",
        help="Extract the forces in separate files",
    )
    args = parser.parse_args()

    ##########
    # Manage arguments

    # -v/--verbose

    kb = 0.001985875  # kcal/K/mol

    try:
        utilsscript.init_logging(args.verbosity)
    except NameError:
        logging.basicConfig(level=logging.WARNING)
        logging.warning("utilsscript lib not found, using default logging at warning level.")

    infile = args.infile
    if not os.path.isfile(infile):
        logging.error("Input file not found")
        sys.exit(1)

    toplot = []
    with open(infile, 'r') as f:
        lines = iter(f.readlines())
        while True:
            try:
                r = []
                force = []
                ener = []
                tok = []
                while not tok:
                    tok = next(lines).partition('#')[0].rstrip()
                logging.info("Found {} token".format(tok))
                infos = next(lines).split()
                npoints = int(infos[1])
                next(lines)
                for i in range(npoints):
                    line = next(lines).split()
                    r.append(float(line[1]))
                    ener.append(float(line[2]))
                    force.append(float(line[3]))
                r = np.array(r)
                ener = np.array(ener)
                force = np.array(force)
                toplot.append([r, ener, force, tok])
                tok = []
                next(lines)
            except StopIteration:
                break
    for tp in toplot:
        tp[1] = compute_energy(tp)

    fig, axes = plt.subplots(1, 2)

    for tp in toplot:
        axes[0].plot(tp[0], tp[1], label=tp[3], linewidth=3)
        axes[1].plot(tp[0], tp[2], label=tp[3], linewidth=3)
        hmin, hmax = axes[1].get_xlim()
        axes[1].hlines(0, hmin, hmax, color="black", linewidth=3, linestyles="dashdot")

    if args.temp > 0:
        hmin, hmax = axes[0].get_xlim()
        axes[0].hlines(kb*args.temp, hmin, hmax, color="orange", label=r'$k_BT$', linewidth=3, linestyles="dashdot")

    if args.xrange:
        xmin, xmax = list(map(float, args.xrange.split(":")))
        axes[0].set_xlim(xmin, xmax)
        axes[1].set_xlim(xmin, xmax)
    if args.yrange:
        ymin, ymax = list(map(float, args.yrange.split(":")))
        axes[0].set_ylim(ymin, ymax)
        axes[1].set_ylim(ymin, ymax)

    font = "Hack"
    fontsize = 30

    # Setting axes 0
    axes[0].set_title("Estimated energy", fontsize=fontsize)
    # axes[0].legend(frameon=False, fontsize=fontsize)  # Fat font, no frame
    axes[0].set_xlabel("r [A]", fontname=font, fontsize=fontsize)  # ylabel name, font is Hack, size 30pts
    axes[0].set_ylabel("E [kcal/mol]", fontname=font, fontsize=fontsize)  # ylabel name, font is Hack, size 30pts
    axes[0].tick_params(axis='both', which='major', labelsize=fontsize)  # Biggers ticks, bigger ticks label!

    # Setting axes 1
    axes[1].set_title("Tabulated force", fontsize=fontsize)
    axes[1].legend(frameon=False, fontsize=fontsize)  # Fat font, no frame
    axes[1].set_xlabel("r [A]", fontname=font, fontsize=fontsize)  # ylabel name, font is Hack, size 30pts
    axes[1].set_ylabel("F [kcal/mol/A]", fontname=font, fontsize=fontsize)  # ylabel name, font is Hack, size 30pts
    axes[1].tick_params(axis='both', which='major', labelsize=fontsize)  # Biggers ticks, bigger ticks label!

    plt.subplots_adjust(wspace=0.3)
    plt.show()

    if args.extract:
        for tp in toplot:
            outfile = "".join([tp[3], '.plot'])
            logging.info("Writing file {}".format(outfile))
            with open(outfile, 'w') as f:
                f.write("# {} force extracted from {}\n".format(tp[3], infile))
                f.write("# {:^20} {:^20} {:^20}\n".format('r', 'energy', 'force'))
                for a, b, c in zip(tp[0], tp[1], tp[2]):
                    f.write("{:>18.16e} {:>18.16e} {:>18.16e}\n".format(a, b, c))
    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("User interruption.")
