#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Takes the output file from some ave commands of LAMMPS
and returns average and sem.
'''

import argparse
import numpy as np
import sys
import logging
import utilsscript


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


def compute_mean(fields, infile):
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
                    line = list(map(float, f.readline().split()))
                    for j, k in enumerate(fields):
                        ave[i, j] += line[j]
                nrec += 1
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
                    line = list(map(float, f.readline().split()))
                    for j, k in enumerate(fields):
                        sem[i, j] += (line[j] - ave[i, j])**2
                nrec += 1
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
        line = " ".join(('#', *["{:^17}"]*len(fields), '\n'))
        f.write(line.format(*fields))
        for i, (a, s) in enumerate(zip(ave, sem)):
            # I found no nice way of doing this...
            elems = []
            for j, fi in enumerate(fields):
                if fi in SPECIAL_CASES:
                    if fi == 'Chunk':
                        elems.append("{:^17d}".format(i+1))
                    else:
                        elems.append("{:>8.3f} {:>8.3f}".format(a[j], 0.))
                else:
                    elems.append("{:>8.3f} {:>8.3f}".format(a[j], s[j]))
            line = " ".join((*elems, '\n'))
            f.write(line)
    logging.info("DONE!")
    return


def main():

    parser = argparse.ArgumentParser(
        description="Script to compute lifetime of tubes of symmetric star polymers."
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
        "-n",
        "--non-standard",
        dest="non_standard",
        action="store_true",
        help="Non standard LAMMPS headers.",
    )
    args = parser.parse_args()

    ##########
    # Manage arguments

    # -v/--verbose
    utilsscript.init_logging(args.verbosity)

    infile = args.infile
    outfile = args.outfile
    is_non_standard = args.non_standard

    fields = get_fields(infile, is_non_standard)

    ave, sem = compute_mean(fields, infile)

    write_output(outfile, fields, ave, sem)

    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("User interruption.")
