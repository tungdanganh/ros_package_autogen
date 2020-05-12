#from __future__ import print_function

import argparse
import os
import sys

import pkg_gen

def create_pkg():
  if len(sys.argv) != 2:
    pkg_gen.printError("Error: need to set a package name.")
    sys.exit(0)
  else:
    pkg_name = sys.argv[1]

  pt = pkg_gen.PackageTemplate(pkg_name)
  pt.create_folders()
  pt.create_xml()
  pt.create_cmakelist()
  pt.create_node()
  pt.create_src()
  pt.create_header()
  pt.create_launch()
  pt.create_config()
  pt.done()

if __name__ == "__main__":
  try:
    create_pkg()
  except KeyboardInterrupt:
    pkg_gen.printError('Interrupted by user!')