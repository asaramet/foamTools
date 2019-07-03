#!/usr/bin/env python3

import unittest, os, sys

sys.path.append(sys.path[0] + '/..')
from libs import get

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
  testDict = os.path.join(testsFolder, 'testDict')

  def test_keyword(self):
    self.assertEqual(get.keyword(self.testDict, 'application'), ['application', 'simpleFoam'])
    self.assertEqual(get.keyword(self.testDict, 'startTime'), ['startTime', '0'])
    self.assertEqual(get.keyword(self.testDict, 'app'), [-1, 'not defined'])
    self.assertEqual(get.keyword('testNonFile', 'application'), -1)

  def test_dimensions(self):
    self.assertEqual(get.dimensions('testNonFile'), -1)
    self.assertEqual(get.dimensions(self.testDict), "kg^1 m^2 s^-2 K^-3 mol^3 A^4 cd^-4 " )

  def test_dictionaries(self):
    self.assertEqual(get.dictionaries('testNonFile'), -1)
    self.assertEqual(get.dictionaries(self.testDict), [
      {"name": "outlet", 'data': [['type', 'inletOutlet'], ['inletValue', '$internalField'], ['value', '$internalField']]},
      {"name": "outlet", 'data': [['type', 'inletOutlet'], ['value', 'internalField']]}
    ])


if __name__ == '__main__':
  unittest.main()