#!/usr/bin/env python

import argparse
from MDSplus import *

idnames = ("MAG_%d", "phi_%d", "PWR_%d" )
idunits = ("V", "rad", "W")
idcal   = ("7.109e-8", "1.8626e-9", "4.550e-6" )


def make_bolo_tree(args):
	tree = Tree(args.tree[0], -1, "NEW")
	
	for site in range(1, args.bolo8_count+1):
		bname = "BOLO%d" % (site)
		module = tree.addNode(".%s" % (bname))
		modpath = "\\%s::TOP.%s" % (args.tree[0], bname)

		for ch in range(1, 24+1):
			rawname = "CH%02d" % (ch)
			raw = module.addNode(rawname, "SIGNAL")
			bchan = 1 + (ch - 1)/3
			id = (ch - 1)%3
			cooked = module.addNode(idnames[id] % (bchan), "SIGNAL")
			expr = "%s.%s * %s" % (modpath, rawname, idcal[id])
			print(expr)
			cooked.putData(Data.compile(expr))
			cooked.setUnits(idunits[id])
	tree.write()

def run_main():
	parser = argparse.ArgumentParser(description="make_bolo_tree")
	parser.add_argument('--bolo8_count', default=1, help = "number of bolo8 modules" )
	parser.add_argument('tree', nargs=1, help = "tree name")
	make_bolo_tree(parser.parse_args())
# execution starts here

if __name__ == '__main__':
    run_main()

