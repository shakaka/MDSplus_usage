#!/usr/bin/env python

import argparse
import MDSplus
import os

def new_shot(tree):
    MDSplus.Tree.setCurrent(tree, 1)
    MDSplus.Tree(tree, -1).createPulse(1)

def make_tree(tree, nchan, id):
    for subtrees in args.subtrees:
        tree.addNode(subtrees, "SUBTREE")

def path_check(tname):
    root = os.getenv("MDS_TREE_ROOT", "{}/trees".format(os.environ['HOME']))
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


def make_acqtree(args):
    tname = args.tree[0]
    path_check(tname)
    tree = MDSplus.Tree(tname, -1, "NEW")

    if not args.subtrees is None:
        make_tree(tree, args.subtrees)
    else:
        new_shot(tname)




def int_or_raw(value):
    if value == 'RAW' or value == 'raw':
	return 0
    else:
        return int(value)

def run_main():
    parser = argparse.ArgumentParser(description="make_acqtree")
    parser.add_argument('tree', nargs=1, help="tree name, ideally UUT name")
    parser.add_argument('--subtrees', nargs='+', help="subtree list")
    make_acqtree(parser.parse_args())


if __name__ == '__main__':
    run_main()
