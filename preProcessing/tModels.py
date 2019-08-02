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
    #tPropsDict = os.path.join(thisFolder, '../tests/dicts/lesModel')
    with open(tPropsDict, 'r') as f:
      tProps = f.read()

  type = get.keyword(tProps, 'simulationType')

  text = "==> Turbulence model:\n"
  if type == 'laminar': text += "\tno turbulence models are used."
  if type == "RAS":
    modelName = get.keyword(tProps, 'RASModel')
    text += "\tType:\t\t\t" + modelName + " Reynolds-averaged stress (RAS)\n"
    text += "\tTurbulence modelling:\t" + get.keyword(tProps, 'turbulence') + "\n"

    rasCoeffs = get.dictionary(tProps, modelName + 'Coeffs')
    if rasCoeffs != -1:
      text += "\t" + modelName + " coefficients:\n"
      for line in rasCoeffs.split('\n')[1:-2]:
        data = line.split()
        text += "\t\t" + data[0] + '\t\t' + data[1] + '\n'

    if get.keyword(tProps, 'printCoeffs') == 'on':
      text += "\tPrint model coeffs to terminal at simulation startup!\n"

  if type == "LES":
    modelName = get.keyword(tProps, 'LESModel')
    print (modelName)
    text += "\tType:\t" + modelName + " large-eddy simulation (LES) or detached-eddy simulation (DES)\n"
  return text

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
