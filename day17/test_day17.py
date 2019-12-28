#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 17.

@author: James Jolley, james@jolley.co
"""

import unittest
import day17.day17 as d

class TestDay17(unittest.TestCase):
    def setUp(self):
        self.ixns = [(2,2),(2,4),(6,4),(10,4)]
    
    def test_get_intersections(self):
        slist = ['..#..........',
                 '..#..........',
                 '#######...###',
                 '#.#...#...#.#',
                 '#############',
                 '..#...#...#..',
                 '..#####...^..']
        self.assertCountEqual(d.get_intersections(slist), self.ixns)
        
    def test_get_align_params(self):
        self.assertEqual(d.get_align_params(self.ixns), [4, 8, 24, 40])
        


if __name__ == '__main__':
    unittest.main()
    