#!/usr/bin/env python3

import sys, getopt, os
from string import Template

sys.path.append(sys.path[0] + '/..')
from libs import run, get

thisFolder = os.path.dirname(os.path.realpath(__file__))

def help():
  return Template('''
    Turbulence and thermophysical models of an OpenFOAM case folder.

    Usage: ${app} [OPTIONS]

    OPTIONS:
      -h                  Show this message
      -f [FOLDER PATH]    Specify case folder as a string "FOLDER PATH"

    EXAMPLES:
      Collect data in '/home/my_case':

        ${app} -f '/home/my_case'
  ''').substitute(app=sys.argv[0])

def turbulence(case):
  tProps = run.openfoam('foamDictionary constant/turbulenceProperties', case)
  if tProps == -1: #return -1
    tPropsDict = os.path.join(thisFolder, '../tests/dicts/tModels')
    with open(tPropsDict, 'r') as f:
      tProps = f.read()

  type = get.keyword(tProps, 'simulationType')

  text = "==> Turbulence models:\n\n"
  if type != -1: text += "Type of turbulence modelling\t"
  if type == "RAS": text += "Reynolds-averaged stress (RAS)"
  return type

def transport(case):
  tProps = run.openfoam('foamDictionary constant/transportProperties', case)
  if tProps == -1: #return -1
    tPropsDict = os.path.join(thisFolder, '../tests/dicts/tModels')
    with open(tPropsDict, 'r') as f:
      tProps = f.read()
  return tProps

def read(case):
  print (turbulence(case))
  #print ('.............\n', transport(case))

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
