#!/usr/bin/env python3

import os, re

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

def checkRunCompleted(case):
  # return 1 if endTime is defined and folder exists
  controlDict = systemDict(case, 'controlDict')
  if controlDict == -1: return [-1, "no controlDict"]
  endTime = keyword(controlDict, 'endTime')
  if endTime[0] == -1: return [-1, "no endTime"]
  if os.path.isdir(os.path.join(case, endTime[1])):
    return [1, endTime[1]]
  return [-1, "not completed"]

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

def powerof(x, power):
  if power == 0: return 1
  return x + "^" + str(power)

def dimensions(text):
  units = ["kg", "m", "s", "K", "mol", "A", "cd"]
  for line in text.split('\n'):
    if line.find('dimensions' + ' ') != -1:
      values = re.sub('[;\[\]]','', line[len('dimensions'):].strip()).split()
      mesure, index = "", 0
      while index < len(values):
        power_str = powerof(units[index], int(values[index]))
        if power_str != 1: mesure += power_str + ' '
        index += 1
      return mesure
  print("ERROR: no 'dimensions' found in", text)
  return -1

def fileSegment(file, start, end):
  snippet, flag = '', -1
  with open(file, 'r') as f:
    for line in f:
      snippet += line
      if (re.search(start, line)):
        snippet = line
        flag = 1
      if flag != -1 and re.search(end, line):
          break
  return snippet.split('\n')[1:-2]

def multipleStringSegment(multistring, start, end):
  snippet, flag = '', -1
  for line in multistring.split('\n'):
    if re.search(start, line) and flag == -1:
      snippet, flag = '', 1
    if flag != -1:
      if end == '':
        if line == end: break
      elif re.search(end, line): break
    snippet += line + '\n'
  return snippet
