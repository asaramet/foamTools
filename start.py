#!/usr/bin/env python3

import sys, getopt, os
from string import Template

from preProcessing import *
from libs import *

def help():
  return Template('''
    Pre-processing an OpenFOAM case folder.

    Usage: ${app} [OPTIONS]

    OPTIONS:
      -h                  Show this message
      -f [FOLDER PATH]    Specify case folder as a string "FOLDER PATH"
      -c                  Pre-process 'controlDict'
      -i                  Pre-process initial conditions

    EXAMPLES:
      Run controlDict pre-processing on '/home/my_case':

        ${app} -c -f '/home/my_case'

      Scan initial conditions on '/home/my_case':

        ${app} -i -f '/home/my_case'
  ''').substitute(app=sys.argv[0])

def main(argv):
  caseFolder = "../cleanCase"
  try:
    opts, args = getopt.getopt(argv, "f:hci")
  except getopt.GetoptError:
    print ("ERROR: Wrong option,", sys.argv[1], "for:", sys.argv[0])
    sys.exit(2)
  for opt, arg in opts:
    if opt == "-h":
      print (help())
      sys.exit(0)
    if opt == "-f":
      caseFolder = arg

  for opt, arg in opts:
    if opt == "-c":
      controlDict.read(caseFolder)
    if opt == "-i":
      initials.read(caseFolder)

if __name__ == "__main__":
  main(sys.argv[1:])
