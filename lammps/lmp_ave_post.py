#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Takes the output file from some ave commands of LAMMPS
and returns average and sem.
'''

import argparse
import numpy as np
import sys
import os
import logging


def get_fields(infile, is_non_standard):
    '''
    Gets the fields of the file.
    If non-standard, returns empty string.
    '''
    fields = []
    if is_non_standard:
        fields = ['']
    else:
        with open(infile, 'r') as f:
            f.readline()
            f.readline()
            line = f.readline()
            fields = line[1:].split()
    logging.debug(fields)

    return fields


def compute_mean(fields, infile, stepmin, stepmax):
    '''
    Computes data ave and sem.
    '''
    # Skip through header
    nfields = len(fields)
    with open(infile, 'r') as f:
        line = f.readline()
        while line[0] == '#':
            line = f.readline()
        # Initialisation
        line = line.split()
        step, nentries = int(line[0]), int(line[1])
        nentries_ref = nentries
        ave = np.zeros((nentries, nfields))
        sem = np.zeros((nentries, nfields))
        # Computing the averages
        for i in range(nentries):
            line = list(map(float, f.readline().split()))
            for j, k in enumerate(fields):
                ave[i, j] += line[j]
        nrec = 1
        while True:
            try:
                line = f.readline().split()
                if not line:
                    break
                step, nentries = int(line[0]), int(line[1])
                keep = True
                if stepmin and step < stepmin:
                    keep = False
                if stepmax and step > stepmax:
                    break
                if nrec % 1000 == 0:
                    logging.info(
                            "Reading record number {:<10d}, step {:<10.2f}."
                            .format(nrec, step)
                            )
                if nentries != nentries_ref:
                    logging.error(
                            "Entries number changed between records. Check entry t={:10.2f}."
                            .format(step)
                            )
                    sys.exit(1)
                for i in range(nentries):
                    if keep:
                        line = list(map(float, f.readline().split()))
                        for j, k in enumerate(fields):
                            ave[i, j] += line[j]
                    else:
                        f.readline()
                nrec += keep
            except EOFError:
                break

        logging.debug("Computes average over {:<10d} records.".format(nrec))
        ave /= nrec
        logging.info("Computing sem. Rereading file.")
        # Computing sem
        nrec = 0
        f.seek(0)
        line = f.readline()
        while line[0] == '#':
            line = f.readline()
        while True:
            try:
                line = line.split()
                step, nentries = int(line[0]), int(line[1])
                keep = True
                if stepmin and step < stepmin:
                    keep = False
                if stepmax and step > stepmax:
                    break
                if nrec % 1000 == 0:
                    logging.info(
                            "Reading record number {:<10d}, step {:<10.2f}."
                            .format(nrec, step)
                            )
                if nentries != nentries_ref:
                    logging.error(
                            "Entries number changed between records. Check entry t={:10.2f}."
                            .format(step)
                            )
                    sys.exit(1)
                for i in range(nentries):
                    if keep:
                        line = list(map(float, f.readline().split()))
                        for j, k in enumerate(fields):
                            sem[i, j] += (line[j] - ave[i, j])**2
                    else:
                        f.readline()
                nrec += keep
                line = f.readline()
                if not line:
                    break
            except EOFError:
                break
    sem = np.sqrt(sem/nrec)
    return ave, sem


def write_output(outfile, fields, ave, sem):
    '''
    Self-explaining
    '''
    SPECIAL_CASES = [
            'Chunk',
            'OrigID',
            'Coord1',
            'Coord2',
            'Coord3'
            ]
    logging.info("About to write output file.")
    with open(outfile, 'w') as f:
        line = " ".join(('#', *["{:^17}"]*len(fields)))
        f.write(''.join([line.format(*fields).rstrip(), '\n']))
        for i, (a, s) in enumerate(zip(ave, sem)):
            # I found no nice way of doing this...
            elems = []
            for j, fi in enumerate(fields):
                if fi in SPECIAL_CASES:
                    if fi == 'Chunk':
                        elems.append("{:^17d}".format(i+1))
                    else:
                        elems.append("{:>12.6f} {:>12.6f}".format(a[j], 0.))
                else:
                    elems.append("{:>12.6f} {:>12.6f}".format(a[j], s[j]))
            line = " ".join((*elems, '\n'))
            f.write(line)
    logging.info("DONE!")
    return


def main():

    parser = argparse.ArgumentParser(
        description="Script to compute ave and standard error from lammps ave/* output"
    )
    parser.add_argument(
        "-f",
        "--file",
        dest="infile",
        default="",
        help="File to process",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="outfile",
        default="output.mean",
        help="Output file name.",
    )
    parser.add_argument(
        "--smin",
        dest="stepmin",
        default=0,
        type=int,
        help="Minimum step to consider [default %s]"
        )
    parser.add_argument(
        "--smax",
        dest="stepmax",
        default=0,
        type=int,
        help="Maximum step to consider, 0 for all [default %s]"
        )
    parser.add_argument(
        "-n",
        "--non-standard",
        dest="non_standard",
        action="store_true",
        help="Non standard LAMMPS headers.",
    )
    args = parser.parse_args()

    ##########
    # Manage arguments

    infile = args.infile
    outfile = args.outfile
    stepmin = args.stepmin
    stepmax = args.stepmax
    is_non_standard = args.non_standard

    if not os.path.isfile(infile):
        print("Could not find file {}.".format(infile))
        sys.exit()

    fields = get_fields(infile, is_non_standard)

    ave, sem = compute_mean(fields, infile, stepmin, stepmax)

    write_output(outfile, fields, ave, sem)

    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("User interruption.")
