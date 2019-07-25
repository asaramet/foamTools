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

  def test_keyword(self):
    self.assertEqual(get.keyword(self.testDict, 'application'), ['application', 'simpleFoam'])
    self.assertEqual(get.keyword(self.testDict, 'startTime'), ['startTime', '0'])
    self.assertEqual(get.keyword(self.testDict, 'app'), [-1, 'not defined'])
    self.assertEqual(get.keyword('testNonFile', 'application'), -1)

  def test_dimensions(self):
    self.assertEqual(get.dimensions('testNonFile'), -1)
    self.assertEqual(get.dimensions(self.testDict), "kg^1 m^2 s^-2 K^-3 mol^3 A^4 cd^-4 " )

  def test_fileSegment(self):
    self.assertEqual(get.fileSegment(self.testDict, 'lowerWall', '}'),[ '    {',
      '        type            kqRWallFunction;',
      '        value           $internalField;'])

class InitialsTest(unittest.TestCase):
  patchSummaryDict = os.path.join(testsFolder, 'dicts/patchSummary')

  def test_getPatches(self):
    self.assertEqual(initials.getPatches(self.patchSummaryDict), {
      'patches': ['frontAndBack', 'upperWall', 'inlet', 'outlet'],
      'walls': ['lowerWall'],
      'groups': ['motorBikeGroup']
    })

  def test_getFields(self):
    self.assertEqual(initials.getFields(
'''Valid fields:
    volScalarField	nut
    volVectorField	U
    volScalarField	k
    volScalarField	p
    volScalarField	omega

patch	: frontAndBack'''), ['nut', 'U', 'k', 'p', 'omega'])


if __name__ == '__main__':
  unittest.main()
