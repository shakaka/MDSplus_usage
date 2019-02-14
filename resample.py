#!/usr/bin/env python

import MDSplus
import os
import argparse
import matplotlib.pyplot as plt

def resample_show(args):
    resp_rate = args.resp[0]

    t = Tree("acq2106_test", 1176)
    mp1Node = t.getNode("")
    mp1Data = mp1Node.record.data()

    mp1Data_re = []

    if resp_rate < len(mp1Data):
        i = 0
        while i < len(mp1Data):
            mp1Data_re.append(mp1Data[i])
            i += resp_rate



    plt.figure(1)
    plt.subplot(211)
    plt.plot(mp1Data)

    plt.subplot(212)
    plt.plot(mp1Data_re)
    plt.show()

def run_main():
    parser = argparse.ArgumentParser(description="resampling")
    parser.add_argument('resp', nargs=1, help="resample rate")
    make_acqtree(parser.parse_args())


if __name__ == '__main__':
    run_main()
