#!/usr/bin/env python3

import sys, getopt, os
from string import Template

sys.path.append(sys.path[0] + '/..')
from libs import get

def help():
  return Template('''
    Pre-processing an OpenFOAM case folder.

    Usage: ${app} [OPTIONS]

    OPTIONS:
      -h                  Show this message
      -f [FOLDER PATH]    Specify case folder as a string "FOLDER PATH"

    EXAMPLES:
      Run pre-processing on '/home/my_case':

        ${app} -f '/home/my_case'
  ''').substitute(app=sys.argv[0])

def read(case):
  zeroFolder = get.caseFolder(case, '0')
  if zeroFolder == -1: return
  print("TODO: Just template:", zeroFolder)

def main(argv):
  caseFolder = "../../cleanCase"
  try:
    opts, args = getopt.getopt(argv, "f:h")
  except getopt.GetoptError:
    print ("ERROR: Wrong option,", sys.argv[1], "for:", sys.argv[0])
    sys.exit(2)
  for opt, arg in opts:
    if opt == "-h":
      print (help())
      sys.exit(0)
    if opt == "-f":
      caseFolder = arg

  read(caseFolder)

if __name__ == "__main__":
  main(sys.argv[1:])
