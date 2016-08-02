#!/usr/bin/env python

'''
assert: base assert allowing you to write your own assertions
assertEqual(a, b): check a and b are equal
assertNotEqual(a, b): check a and b are not equal
assertIn(a, b): check that a is in the item b
assertNotIn(a, b): check that a is not in the item b
assertFalse(a): check that the value of a is False
assertTrue(a): check the value of a is True
assertIsInstance(a, TYPE): check that a is of type "TYPE"
assertRaises(ERROR, a, args): check that when a is called with args that it raises ERROR



'''

import unittest
from big_data import find_dor 

class TestBing_data(unittest.TestCase):
	
	def test_find_dor(self):
		self.assertEqual(find_dor(25),True)
		self.assertEqual(find_dor(-25),True)


if __name__ == '__main__':
	unittest.main()