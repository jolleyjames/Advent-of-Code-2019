#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Advent of Code 2019, Day 22.

@author: James Jolley, james@jolley.co
"""

import day22.day22 as d
import unittest

class TestDay22(unittest.TestCase):
    
    def test_new_stack(self):
        deck = [2**i for i in range(5)]
        self.assertEqual(d.new_stack(deck), [16, 8, 4, 2, 1])
        
    def test_cut(self):
        deck = list(range(10))
        self.assertEqual(d.cut(deck,3), [3,4,5,6,7,8,9,0,1,2])
        deck = list(range(10))
        self.assertEqual(d.cut(deck,-4), [6,7,8,9,0,1,2,3,4,5])
        
    def test_increment(self):
        deck = list(range(10))
        self.assertEqual(d.increment(deck,3), [0,7,4,1,8,5,2,9,6,3])
        
    def test_process_script(self):
        deck = list(range(10))
        self.assertEqual(d.process_script('day22/test1.txt',deck), [0,3,6,9,2,5,8,1,4,7])
        deck = list(range(10))
        self.assertEqual(d.process_script('day22/test2.txt',deck), [3,0,7,4,1,8,5,2,9,6])
        deck = list(range(10))
        self.assertEqual(d.process_script('day22/test3.txt',deck), [6,3,0,7,4,1,8,5,2,9])
        deck = list(range(10))
        self.assertEqual(d.process_script('day22/test4.txt',deck), [9,2,5,8,1,4,7,0,3,6])

if __name__ == '__main__':
    unittest.main()
    