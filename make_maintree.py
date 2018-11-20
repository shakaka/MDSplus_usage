#!/usr/bin/env python

import argparse
import MDSplus
import os

def new_shot(tree):
    MDSplus.Tree.setCurrent(tree, 1)
    MDSplus.Tree(tree, -1).createPulse(1)

def make_chan(tree, nchan, id):
    if nchan == 0:
        subdir = tree.addNode(".{}".format(id))
        subdir.addNode(":RAW", "SIGNAL")
    else:
        subdir = tree.addNode(".{}".format(id))
        chfmt = "CH{:0" + "{}".format('3' if nchan > 99 else '2') + "}"

        for ch in range(1, nchan+1):




            subdir.addNode(subtree_name, "SUBTREE")





def path_check(tname):
    root = os.getenv("MDS_TREE_ROOT", "{}/trees".format(os.environ['MAKE_TREE']))
    key = "{}_path".format(tname)
    tpath = "{}/{}".format(root, tname)
    mpath = os.getenv(key, "notfound")
    if mpath == "notfound":
        print("run as root:")
        print('echo "{} {}" >> {}'.
		format(key, tpath, "/usr/local/mdsplus/local/envsyms"))
        print("# for immediate use:")
        print("export {}={}".format(key, tpath))
	print("then run the command again please")
	exit(1)

    if not os.path.exists(root):
        print('mkdir {}'.format(root))
	exit(1)

    if os.path.exists(tpath):
        print('existing tree {} may already exist. Delete it'.format(tpath))
	exit(1)
    else:
        os.mkdir(tpath)


def make_acqtree(args):
    tname = args.tree[0]
    path_check(tname)
    tree = MDSplus.Tree(tname, -1, "NEW")

    if args.aichan >= 0:
	make_chan(tree, args.aichan, "AI")
    if args.aochan >= 0:
        make_chan(tree, args.aochan, "AO")
    if args.dio >= 0:
        make_chan(tree, args.dio, "DIO")
    if args.stat >= 0:
        make_chan(tree, args.stat, "ST")
    tree.write()
    new_shot(tname)

def int_or_raw(value):
    if value == 'RAW' or value == 'raw':
	return 0
    else:
        return int(value)

def run_main():
    parser = argparse.ArgumentParser(description="make_acqtree")
    parser.add_argument('--aichan', default=-1, type=int_or_raw, help='ai channel count')
    parser.add_argument('--aochan', default=-1, type=int_or_raw, help='ao channel count')
    parser.add_argument('--dio', default=-1, type=int, help='dio, words')
    parser.add_argument('--stat', default=-1, type=int, help='status, words')
    parser.add_argument('tree', nargs=1, help="tree name, ideally UUT name")
    parser.add_argument('subtrees', nargs='+', help="subtree list")
    make_acqtree(parser.parse_args())


if __name__ == '__main__':
    run_main()
