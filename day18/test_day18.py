#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 18.

@author: James Jolley, james@jolley.co
"""

import unittest
import day18.day18 as d

class TestDay18(unittest.TestCase):
    def test_read_map(self):
        check = {(1,1):'b', (2,1):'.', (3,1):'A', (4,1):'.', (5,1):'@', (6,1):'.', (7,1):'a'}
        self.assertEqual(d.read_map('day18/test1.txt'), check)
    
    def test_neighbor_coords(self):
        self.assertCountEqual(d.neighbor_coords((-4,8)), [(-4,7),(-4,9),(-3,8),(-5,8)])
        
    def test_neighbors(self):
        check = {}
        check[(1,1)] = set([(2,1)])
        check[(2,1)] = set([(1,1),(3,1)])
        check[(3,1)] = set([(2,1),(4,1)])
        check[(4,1)] = set([(3,1),(5,1)])
        check[(5,1)] = set([(4,1),(6,1)])
        check[(6,1)] = set([(5,1),(7,1)])
        check[(7,1)] = set([(6,1)])
        self.assertEqual(d.neighbors(d.read_map('day18/test1.txt')), check)
        
    def test_reverse_coord_dict(self):
        check = {'b':(1,1), 'A':(3,1), '@':(5,1), 'a':(7,1)}
        self.assertEqual(d.reverse_coord_dict(d.read_map('day18/test1.txt')), check)

if __name__ == '__main__':
    unittest.main()
    