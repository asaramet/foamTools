#!/usr/bin/env python3

import os

__all__ = ['reportFile', 'caseFolder', 'keyword']

def reportFile(case):
  return "report_" + os.path.basename(case) + ".txt"

def caseFolder(case, subFolder=""):
  if not os.path.exists(case):
    print ("ERROR: Wrong case folder specified: ", case)
    return -1
  folder = os.path.join(case, subFolder)
  if not os.path.exists(folder):
    print ("No", subFolder,"folder in ", case)
    return -1
  return folder

def keyword(dict, key):
  if not os.path.exists(dict):
    print ("ERROR: ", controlDict, "not found")
    return -1
  with open(dict, 'r') as file:
    for line in file:
      if line.find(key + ' ') != -1:
        value = line.split()[1]
        valueSemiColumn = value.find(';')
        if valueSemiColumn != -1:
          value = value[:valueSemiColumn]
        return [key, value]
  return [-1, "not defined"]
