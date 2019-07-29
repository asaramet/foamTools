#!/usr/bin/env python3

import sys, getopt, os
from string import Template

thisFolder = os.path.dirname(os.path.realpath(__file__))

sys.path.append(sys.path[0] + '/..')
from libs import get, run

def help():
  return Template('''
    Mesh info of an OpenFOAM case folder.

    Usage: ${app} [OPTIONS]

    OPTIONS:
      -h                  Show this message
      -f [FOLDER PATH]    Specify case folder as a string "FOLDER PATH"

    EXAMPLES:
      Collect mesh data on '/home/my_case':

        ${app} -f '/home/my_case'
  ''').substitute(app=sys.argv[0])

def stats(case):
  checkMesh = run.openfoam('checkMesh', case)
  if checkMesh == -1: #return -1
    checkMeshDict = os.path.join(thisFolder, '../tests/dicts/checkMesh')
    with open(checkMeshDict, 'r') as f:
      checkMesh = f.read()
  stats = get.multipleStringSegment(checkMesh, 'Mesh stats', '')
  cells = get.multipleStringSegment(checkMesh, 'Overall number of cells', '')
  return (stats, cells)

def read(case):
  print (stats(case)[0])

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
