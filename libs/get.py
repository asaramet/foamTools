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

def systemDict(case, systemDict='controlDict'):
  systemFolder = caseFolder(case, "system")
  if systemFolder == -1: return -1
  dict = os.path.join(systemFolder, systemDict)
  if os.path.isfile(dict): return dict
  print ("ERROR:", dict, "doesn't exist!")
  return -1

def keyword(dict, key):
  if not os.path.exists(dict):
    print ("ERROR: ", dict, "not found")
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

def checkRunCompleted(case):
  # return 1 if endTime is defined and folder exists
  controlDict = systemDict(case, 'controlDict')
  if controlDict == -1: return [-1, "no controlDict"]
  endTime = keyword(controlDict, 'endTime')
  if endTime[0] == -1: return [-1, "no endTime"]
  if os.path.isdir(os.path.join(case, endTime[1])):
    return [1, endTime[1]]
  return [-1, "not completed"]
