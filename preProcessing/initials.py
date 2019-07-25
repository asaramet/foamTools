#!/usr/bin/env python3

import sys, getopt, os, re
from string import Template

thisFolder = os.path.dirname(os.path.realpath(__file__))

sys.path.append(sys.path[0] + '/..')
from libs import get, run
from random import randint

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

def getPatches(patchSummary):
  dict = {'patches':[], 'walls':[], 'groups':[]}
  for line in patchSummary.split('\n'):
    if (re.search("^patch", line)):
      dict['patches'].append(line.split()[2])
    if (re.search("^wall", line)):
      dict['walls'].append(line.split()[2])
    if (re.search("^group", line)):
      dict['groups'].append(line.split()[2])
  return dict

def getFields(patchSummary):
  fields = []
  for line in get.multipleStringSegment(patchSummary, '^Valid fields:', '').split('\n')[1:-1]:
    fields.append(line.split('\t')[1])
  return fields

def fieldData(field, case='.'):
  # TODO: set file to output run from 'foamDictionary 0/k'
  foamDictionary = run.openfoam('foamDictionary 0/' + field, case)
  if foamDictionary == -1: return -1

  return foamDictionary

def collectData(case):
  patchSummary = run.openfoam('patchSummary -time 0', case)
  if patchSummary == -1: return -1

  print (getPatches(patchSummary))
  print (getFields(patchSummary))

def read(case):
  patchSummary = '''Time = 0

Valid fields:
    volScalarField	nut
    volVectorField	U
    volScalarField	k
    volScalarField	p
    volScalarField	omega

patch	: frontAndBack
patch	: upperWall'''

  collectData(case)


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
