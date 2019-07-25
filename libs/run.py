#!/usr/bin/env python3

import subprocess, re

def openfoam(command, case='.'):
  # check if OpenFOAM is installed on the system
  if (subprocess.getoutput('echo ${FOAM_VERSION}') == ''):
    print ('ERROR: OpenFOAM not found on the system')
    return -1

  stdout = subprocess.getoutput('cd ' + case + ' && ' + command)
  if re.search('FOAM FATAL ERROR', stdout):
    print ("ERROR:", command, "failed in", case)
    return -1
  if re.search('command not found', stdout):
    print ("ERROR: OpenFOAM not initialized, '", command, "' not found")
    return -1
  return stdout

def main():
  print (openfoam('ls', '$HOME'))

if __name__ == '__main__':
  main()
