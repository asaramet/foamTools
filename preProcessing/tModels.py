#!/usr/bin/env python3

import sys, getopt, os, re, typing
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
    ras = get.dictionary(tProps, "RAS")
    modelName = get.keyword(ras, 'RASModel')
    text += "\tType:\t\t\t" + modelName + " Reynolds-averaged stress (RAS)\n"

    rasCoeffs = get.dictionary(ras, modelName + 'Coeffs')
    if rasCoeffs != "":
      text += "\t" + modelName + " coefficients:\n"
      for line in rasCoeffs.split('\n')[1:-1]:
        line = run.ignoreComments(line)
        coeffData = line.split()
        if len(coeffData) > 1:
          text += "\t\t" + coeffData[0] + run.tabs(coeffData[0]) + coeffData[1] + '\n'

  if type == "LES":
    les = get.dictionary(tProps, 'LES')
    modelName = get.keyword(les, 'LESModel')
    text += "\tType:\t\t" + modelName + " large-eddy simulation (LES) or detached-eddy simulation (DES)\n"
    delta = get.keyword(les, 'delta')
    if delta != -1: text += "\tDelta model:\t" + delta + '\n'

    ignoreKeys = ['delta', 'printCoeffs', 'turbulence', 'LESModel']
    coeffs, values = [], {}
    for line in les.split('\n'):
      line = run.ignoreComments(line)
      if re.search('Coeff', line):
        coeff = line.split()[0]
        if coeff not in ignoreKeys and coeff not in coeffs: coeffs.append(coeff)
      splt = line.split()
      if len(splt) >= 2:
        key = splt[0]
        if re.search(';', splt[1]) and key not in ignoreKeys:
          value = get.keyword(line, splt[0])
          if key in values.keys() and value != values[key]:
            if isinstance(values[key], typing.List):
              if value not in values[key]: values[key].append(value)
            else: values[key] = [value, values[key]]
          else:
            values[key] = value
    if coeffs != []:
      text += "\tDefined coefficients:\n"
      for cf in coeffs:
        text += "\t\t" + cf + '\n'
    if values != {}:
      text += "\tDefined options:\n"
      for key in values.keys():
        text += "\t\t" + key + run.tabs(key) + str(values[key]) + '\n'

  if get.keyword(tProps, 'turbulence') != -1:
    text += "\tTurbulence modelling:\t" + get.keyword(tProps, 'turbulence') + "\n"

  if get.keyword(tProps, 'printCoeffs') == 'on':
    text += "\tPrint model coeffs to terminal at simulation startup!\n"

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
