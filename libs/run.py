#!/usr/bin/env python3

import subprocess, re

def openfoam(command, case='.'):
  # check if OpenFOAM is installed on the system
  if (subprocess.getoutput('echo ${FOAM_VERSION}') == ''):
    print ('ERROR: OpenFOAM is not initiated')
    return -1

  return subprocess.getoutput('cd ' + case + ' && ' + command)


def main():
  print (openfoam('ls', '$HOME'))

if __name__ == '__main__':
  main()
