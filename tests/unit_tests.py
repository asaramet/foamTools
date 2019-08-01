#!/usr/bin/env python3

import unittest, os, sys

sys.path.append(sys.path[0] + '/..')
from libs import get
from preProcessing import initials

testsFolder=os.path.dirname(os.path.realpath(__file__))

class TestStringMethods(unittest.TestCase):
  def test_upper(self):
    self.assertEqual('foo'.upper(), 'FOO')

  def test_isupper(self):
    self.assertTrue('FOO'.isupper())
    self.assertFalse('Foo'.isupper())

  def test_split(self):
    s = 'hello world'
    self.assertEqual(s.split(), ['hello', 'world'])
    # check that s.split fails when a separator is not a string
    with self.assertRaises(TypeError):
      s.split(2)

class GetMethods(unittest.TestCase):
  testDict = os.path.join(testsFolder, 'dicts/testDict')
  with open(testDict, 'r') as f:
    testData = f.read()

  def test_keywordInFile(self):
    self.assertEqual(get.keywordInFile(self.testDict, 'application'), 'simpleFoam')
    self.assertEqual(get.keywordInFile(self.testDict, 'startTime'), '0')
    self.assertEqual(get.keywordInFile(self.testDict, 'app'), -1)
    self.assertEqual(get.keywordInFile('testNonFile', 'application'), -1)

  def test_dimensions(self):
    self.assertEqual(get.dimensions('testNonFile'), -1)
    self.assertEqual(get.dimensions(self.testData), "kg^1 m^2 s^-2 K^-3 mol^3 A^4 cd^-4 " )

  def test_fileSegment(self):
    self.assertEqual(get.fileSegment(self.testDict, 'lowerWall', '}'),[ '    {',
      '        type            kqRWallFunction;',
      '        value           $internalField;'])

class InitialsTest(unittest.TestCase):
  patchSummaryDict = os.path.join(testsFolder, 'dicts/patchSummary')
  with open(patchSummaryDict, 'r') as f:
    patchSummary = f.read()

  foamDict = os.path.join(testsFolder, 'dicts/foamDictionary_0_k')
  with open(foamDict, 'r') as f:
    foamDictionary = f.read()

  def test_getPatches(self):
    self.assertEqual(initials.getPatches(self.patchSummary), {
      'patches': ['frontAndBack', 'upperWall', 'inlet', 'outlet'],
      'walls': ['lowerWall'],
      'groups': ['motorBikeGroup']
    })

  def test_getFields(self):
    self.assertEqual(initials.getFields(self.patchSummary), ['nut', 'U', 'k', 'p', 'omega'])

  def test_fieldData(self):
    self.assertEqual(initials.fieldData(self.foamDictionary),
    {'cyclic': {'type': ['cyclic;']}, 'cyclicAMI': {'type': ['cyclicAMI;']},
    'cyclicACMI': {'type': ['cyclicACMI;'], 'value': ['uniform', '0.24;']},
    'cyclicSlip': {'type': ['cyclicSlip;']}, 'empty': {'type': ['empty;']},
    'nonuniformTransformCyclic': {'type': ['nonuniformTransformCyclic;']},
    'processor': {'type': ['processor;'], 'value': ['uniform', '0.24;']},
    'processorCyclic': {'type': ['processorCyclic;'], 'value': ['uniform', '0.24;']},
    'symmetryPlane': {'type': ['symmetryPlane;']}, 'symmetry': {'type': ['symmetryPlane;']},
    'wedge': {'type': ['wedge;']}, 'overset': {'type': ['overset;']},
    'inlet': {'type': ['fixedValue;'], 'value': ['uniform', '0.24;']},
    'outlet': {'type': ['inletOutlet;'], 'inletValue': ['uniform', '0.24;'],
    'value': ['uniform', '0.24;']}, 'lowerWall': {'type': ['kqRWallFunction;'],
    'value': ['uniform', '0.24;']}, 'motorBikeGroup': {'type': ['kqRWallFunction;'],
    'value': ['uniform', '0.24;']}, 'upperWall': {'type': ['slip;']},
    'frontAndBack': {'type': ['slip;']}})

if __name__ == '__main__':
  unittest.main()
