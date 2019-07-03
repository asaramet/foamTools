#!/usr/bin/env python3

import sys, getopt, os, re
from string import Template

__all__ = ['read']

sys.path.append(sys.path[0] + '/..')
from libs import get

def help():
  return Template('''
    Pre-processing initial conditions in an OpenFOAM case folder.

    Usage: ${app} [OPTIONS]

    OPTIONS:
      -h                  Show this message
      -f [FOLDER PATH]    Specify case folder as a string "FOLDER PATH"

    EXAMPLES:
      Run pre-processing on '/home/my_case':

        ${app} -f '/home/my_case'
  ''').substitute(app=sys.argv[0])

def getField(file):
  with open(file, 'r') as zeroFile:
    for line in zeroFile:
      if (re.search("boundaryField*", line)):
        print(line)


def read(case):
  zeroFolder = get.caseFolder(case, '0')
  if zeroFolder == -1: return
  print("=== Initial conditions ===")
  for item in os.listdir(zeroFolder):
    zeroFile = os.path.join(zeroFolder, item)
    if os.path.isfile(zeroFile):
      print(item, ':', get.dimensions(zeroFile))
      print(getField(zeroFile))
      #print(get.keyword(zeroFile, 'type'))

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
