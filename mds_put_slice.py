#!/usr/bin/python

"""
mds_put_slice store slice[s] of a 2D array to mdsplu
example
./mds_put_slice.py --ncols 112 --dtype np.uint32 \      
        --store_cols 97,98,99 --node_name "CH%02d" \
        --default_node ST \
        acq2106_076 \
        PROJECTS/AFHBA404/LLCONTROL/afhba.0.log

eg:
    raw file is 112 cols uint32 wide 
    store cols 97.98.99 to node CH01 .. CH03
    under default node ST
    in tree acq2106_076
    raw data afhba.0.log
"""

#import acq400_hapi
import numpy as np
import argparse
import MDSplus

def do_tlatch_report(tla, verbose):
    t0 = 0;
    errors = 0
    errmax = 0
   
    if verbose:
        print("do_tlatch_report {}".format(tla)) 
    for tt in tla:
        if tt != t0+1:
            if verbose > 1:
                print("ERROR %d %d" % (t0, tt))
            errors += 1
            if tt - t0 > errmax:
                errmax = tt - t0
        t0 = tt
        
    if errors:
        print("SUMMARY: errors %d maxerr %d" % (errors, errmax))
    ll = len(tla)
    return np.concatenate((np.subtract(tla[1:ll], tla[0:ll-1]), [1]))
                
                
def mds_put_slice(args):
    if args.store_cols == ':':
	store_cols = range(0, args.ncols)
    else:
        store_cols = eval('('+args.store_cols+', )')
        try:
            n_store = len(store_cols)
        except TypeError:
            print "TypeError add brackets"
            store_cols = ( store_cols, )
        
    with open(args.file[0], 'r') as fp:
        raw = np.fromfile(fp, dtype=eval(args.dtype))
    nsam = len(raw)/args.ncols
    print("mds_put_slice len {} ncols {} nsam {} nsam*ncols {}".
		format(len(raw), args.ncols, nsam, nsam*args.ncols))

    cols = np.reshape(raw[0:nsam*args.ncols], (nsam, args.ncols))

    if args.shr != 0:
        cols = np.right_shift(cols, args.shr)


    
    tree = MDSplus.Tree(args.tree[0], 0)    
    iout = 1
    if args.tlatch_report:
        cols[:,1] = do_tlatch_report(cols[:,store_cols[0]], args.tlatch_report)

    for sc in store_cols:
        node_name = args.node_name % (iout)
        if args.default_node:
            node = tree.getNode("%s.%s" % (args.default_node, node_name))
        else:
            node = tree.getNode(node_name)
        node.putData(cols[:,sc])
	if args.tlatch_report and sc==1:
            print("Node {} is delta tlatch".format(node_name))
        iout += 1
    print("MDSplus.Event.setevent({}, 42)".format(args.tree[0]))
    MDSplus.Event.setevent(args.tree[0])



def run_main():
    parser = argparse.ArgumentParser(description='mds_put_slice slice a data file and submit to MDSplus')
    parser.add_argument('--ncols', type=int, default=64, help="number of columns in data")
    parser.add_argument('--dtype', type=str, default='np.uint32', help="data type np.uint32, np.int16 etc")
    parser.add_argument('--shr', type=int, default=0, help='right shift')
    parser.add_argument('--store_cols', default = ':', type=str, help="list of column indices to store")
    parser.add_argument('--node_name', type=str, help="node name %d format accepted")
    parser.add_argument('--default_node', type=str, help="default node")
    parser.add_argument('--tlatch_report', type=int, default=0, help="1: brief tlatch check, 2: detail tlatch check")
    parser.add_argument('tree', nargs=1, help="tree name")
    parser.add_argument('file', nargs=1, help="file ")
    mds_put_slice(parser.parse_args())

# execution starts here

if __name__ == '__main__':
    run_main()


