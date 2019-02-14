#!/usr/bin/env python

import MDSplus
import os
import argparse

def resample_show(args):
    resp_rate = args.resp[0]

    t = Tree("acq2106_test", 1176)
    ip = t.getNode("")


def run_main():
    parser = argparse.ArgumentParser(description="resampling")
    parser.add_argument('resp', nargs=1, help="resample rate")
    make_acqtree(parser.parse_args())


if __name__ == '__main__':
    run_main()
