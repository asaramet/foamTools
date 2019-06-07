#!/usr/bin/env python3

import sys, getopt, os
from string import Template

__all__ = ['read']

sys.path.append(sys.path[0] + '/..')
from libs import get

def help():
  return Template('''
    Pre-processing controlDict an OpenFOAM case folder.

    Usage: ${app} [OPTIONS]

    OPTIONS:
      -h                  Show this message
      -f [FOLDER PATH]    Specify case folder as a string "FOLDER PATH"


    EXAMPLES:
      Run pre-processing controlDict on '/home/my_case':

        ${app} -f '/home/my_case'
  ''').substitute(app=sys.argv[0])

def report(controlDict):
  return Template('''=== controlDict options:
    Application name [application]: ${application}
    Simulation starting from [startFrom]: ${startFrom}\n''').substitute(
    application = get.keyword(controlDict, 'application')[1],
    startFrom = get.keyword(controlDict, 'startFrom')[1]
  )

def read(case):
  controlDict = get.systemDict(case, 'controlDict')
  if controlDict == -1: return

  with open(get.reportFile(case), 'w') as file:
    file.write(report(controlDict))
    completeRun = get.checkRunCompleted(case)
    if completeRun[0] == 1:
      file.write("\nSimulation successfuly completed at: t - " + completeRun[1] + "!\n")
  print (get.reportFile(case), "updated!")

def main(argv):
  caseFolder = "../../cleanCase"
  try:
    opts, args = getopt.getopt(argv, "f:hc")
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
