#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

class Smallbox:
    def __init__(self):
        self.x = 0.
        self.y = 0.
        self.vx = 0.
        self.vy = 0.
        self.atoms = 0.
        self.temp = 0.
    def __repr__(self):
        return "{} {} {} {} {}".format(self.x, self.y, self.vx, self.vy, self.atoms)

def read_file(filename):
    with open(filename, 'r') as f:
        for _ in range(3): f.readline()
        head = f.readline().split()
        nentries = int(head[1])
        boxes = []
        for _ in range(nentries):
            boxes.append(Smallbox())
        minrec = 0
        maxrec = 0
        nrec = 0
        while True:
            for i in range(nentries):
                line = f.readline().strip()
                if not line:
                    break
                line = line.split()
                nbox = int(line[0])-1
                xbox = float(line[1])
                ybox = float(line[2])
                atbox = float(line[3])
                vxbox = float(line[4])
                vybox = float(line[5])
                tbox = float(line[6])
                boxes[nbox].vx += vxbox
                boxes[nbox].vy += vybox
                boxes[nbox].atoms += atbox
                boxes[nbox].temp += tbox
                if boxes[nbox].x == 0.:
                    boxes[nbox].x = xbox
                if boxes[nbox].y == 0.:
                    boxes[nbox].y = ybox
            nrec += 1
            line = f.readline().strip()
            if not line:
                break
            print(nrec, end='\r')
        for b in boxes:
            b.vx /= nrec
            b.vy /= nrec
            b.atoms /= nrec
            b.temp /= nrec
        return boxes


def main():

    boxes = read_file("vel.bin.ave")
    lx = 456.4354645876385
    ly = 54.772255750516614
    ratio = lx/ly
    circle_coord = (lx/2., ly/2.)
    circle = plt.Circle(circle_coord, 10, color='#FF000030')
    fig1, ax1 = plt.subplots(figsize=(16,16/ratio))
    x  = np.array([b.x*lx for b in boxes if b.atoms > 0.])
    y  =  np.array([b.y*ly for b in boxes if b.atoms > 0.])
    vx = np.array([b.vx for b in boxes if b.atoms > 0.])
    vy = np.array([b.vy for b in boxes if b.atoms > 0.])
    t  = np.array([b.temp for b in boxes if b.atoms > 0.])
    ax1.quiver(x, y, vx, vy, t, cmap='jet') # , scale=1., scale_units='xy')
    # ax1.add_patch(circle)
    plt.savefig('toto.pdf', format='pdf', dpi=600)

    return


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        raise SystemExit("User interruption.")

