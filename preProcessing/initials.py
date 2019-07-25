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

def fieldData(fieldDict):
  data = get.multipleStringSegment(fieldDict, 'boundaryField', '^}')
  patches, patch = [], ''
  for line in data.split('\n')[2:-1]:
    if re.search('{', line):
      patches.append(patch.strip())
    patch = line

  patch_data = []
  for patch in patches:
    dict = {patch:{}}
    for item in get.multipleStringSegment(data, patch, '}').split('\n')[2:-1]:
      dict[patch][item.split()[0]] = item.split()[1:]
    patch_data.append(dict)
  return patch_data

def collectData(case):
  patchSummary = run.openfoam('patchSummary -time 0', case)
  if patchSummary == -1: return -1

  print (getPatches(patchSummary))
  print (getFields(patchSummary))

def read(case):
  #collectData(case)
  foamDictionary = run.openfoam('foamDictionary 0/k', case)
  if foamDictionary == -1:
    foamDict = os.path.join(thisFolder, '../tests/dicts/foamDictionary_0_k')
    with open(foamDict, 'r') as f:
      foamDictionary = f.read()
  print(fieldData(foamDictionary))


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
