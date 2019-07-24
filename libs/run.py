#!/usr/bin/env python3

import subprocess, re

def openfoam(command, case='.'):
  # check if OpenFOAM is installed on the system
  if (not re.search('OpenFOAM', subprocess.getoutput('foamVersion'))): return -1

  return subprocess.getoutput(command)


def main():
  print (openfoam('patchSummary'))

if __name__ == '__main__':
  main()
