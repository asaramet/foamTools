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
  endTime = keywordInFile(controlDict, 'endTime')
  if endTime == -1: return [-1, "no endTime"]
  if os.path.isdir(os.path.join(case, endTime)):
    return [1, endTime]
  return [-1, "not completed"]

def keywordInFile(dict, key):
  if not os.path.exists(dict):
    print ("ERROR: ", dict, "not found")
    return -1
  with open(dict, 'r') as file:
    text = file.read()
  return keyword(text, key)

def keyword(text, key):
  for line in text.split('\n'):
    if line.find(key + ' ') != -1:
      value = line.split()[1]
      valueSemiColumn = value.find(';')
      if valueSemiColumn != -1:
        value = value[:valueSemiColumn]
      return value
  print (key, 'not defined in')
  return -1

def powerof(x, power):
  if power == 0: return 1
  return x + "^" + str(power)

def dimensions(text):
  dimmLine = line(text, 'dimensions')
  if dimmLine == -1:
    print("ERROR: no 'dimensions' found in", text)
    return -1
  return convertDimensions(dimmLine)

def convertDimensions(of_dim_line):
  units = ["kg", "m", "s", "K", "mol", "A", "cd"]
  dimms, flag = [], -1
  for elem in of_dim_line.split():
    if elem == '[': flag = 0
    if flag == 0: dimms.append(elem)
    if elem == ']': flag = 1
  values = dimms[1:-1]
  mesure, index = "", 0
  while index < len(values):
    power_str = powerof(units[index], int(values[index]))
    if power_str != 1: mesure += power_str + ' '
    index += 1
  return mesure

def line(text, keyword):
  for line in text.split('\n'):
    if line.find(keyword) != -1: return line
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

def dictionary(text, name):
  dict, flag = "", -1
  for line in text.split('\n'):
    if re.search(name, line) and flag == -1: flag = 0
    if re.search('{', line) and flag == 0: dict, flag = '', 1
    if re.search('{', line) and flag > 0: flag += 1
    if re.search('}', line) and flag > 0: flag -= 1
    if re.search('}', line) and flag == 1:
      dict += line.strip()
      break
    dict += line.strip() + '\n'
    if flag == -1: dict = ""
  return dict
