#!/usr/bin/env python3

import sys, getopt, os, re
from string import Template

thisFolder = os.path.dirname(os.path.realpath(__file__))

sys.path.append(sys.path[0] + '/..')
from libs import get, run

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

def getPatches(case):
  # TODO: set file to output run from 'patchSummary -time 0'
  file = os.path.join(thisFolder, '../tests/dicts/patchSummary')
  dict = {'patches':[], 'walls':[], 'groups':[]}
  with open(file, 'r') as patchSummary:
    for line in patchSummary:
      if (re.search("^patch", line)):
        dict['patches'].append(line.split()[2])
      if (re.search("^wall", line)):
        dict['walls'].append(line.split()[2])
      if (re.search("^group", line)):
        dict['groups'].append(line.split()[2])
  return dict

def getFields(case):
  # TODO: set file to output run from 'patchSummary -time 0'
  file = os.path.join(thisFolder, '../tests/dicts/patchSummary')
  fields = []
  for line in get.fileSegment(file, '^Valid fields:', '^\n'):
    fields.append(line.split('\t')[1])
  return fields

def fieldData(case):
  # TODO: set file to output run from 'foamDictionary 0/k'
  file = os.path.join(thisFolder, '../tests/dicts/foamDictionary_0_k')
  print (getPatches(case))
  print (getFields(case))

def read(case):
  fieldData(case)
  print(run.openfoam('ls', case))

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
