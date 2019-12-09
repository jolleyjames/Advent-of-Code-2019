#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 9.

@author: James Jolley, james@jolley.co
"""

import unittest
from day05.day05 import read_program, run_program
#import day09.day09 as d

class TestDay09(unittest.TestCase):
    
    def test_examples(self):
        program = read_program('day09/test1.txt')
        self.assertEqual(list(run_program(program).out), program)
        program = read_program('day09/test2.txt')
        self.assertEqual(len(str(run_program(program).out[0])), 16)
        program = read_program('day09/test3.txt')
        self.assertEqual(run_program(program).out[0], 1125899906842624)
        

if __name__ == '__main__':
    unittest.main()
    