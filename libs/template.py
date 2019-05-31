#!/usr/bin/env python3

import sys, getopt, os
from string import Template

def help():
  return Template('''
    Pre-processing an OpenFOAM case folder.

    Usage: ${app} [OPTIONS]

    OPTIONS:
      -h                  Show this message
      -c [FOLDER PATH]    Specify case folder as a string "FOLDER PATH"


    EXAMPLES:
      Run pre-processing on '/home/my_case':

        ${app} -c '/home/my_case'
  ''').substitute(app=sys.argv[0])

def readCase(case):
  if not os.path.exists(case):
    print ("ERROR: Wrong case folder specified: ", case)
    return
  print (case)

def main(argv):
  caseFolder = "../cleanCase"
  try:
    opts, args = getopt.getopt(argv, "c:hp")
  except getopt.GetoptError:
    print ("ERROR: Wrong option,", sys.argv[1], "for:", sys.argv[0])
    sys.exit(2)
  for opt, arg in opts:
    if opt == "-h":
      print (help())
      sys.exit(0)
    if opt == "-c":
      caseFolder = arg

  readCase(caseFolder)

if __name__ == "__main__":
  main(sys.argv[1:])
