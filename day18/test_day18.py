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
        
    def test_get_neighbors(self):
        check = {}
        check[(1,1)] = set([(2,1)])
        check[(2,1)] = set([(1,1),(3,1)])
        check[(3,1)] = set([(2,1),(4,1)])
        check[(4,1)] = set([(3,1),(5,1)])
        check[(5,1)] = set([(4,1),(6,1)])
        check[(6,1)] = set([(5,1),(7,1)])
        check[(7,1)] = set([(6,1)])
        self.assertEqual(d.get_neighbors(d.read_map('day18/test1.txt')), check)
        
    def test_reverse_coord_dict(self):
        check = {'b':(1,1), 'A':(3,1), '@':(5,1), 'a':(7,1)}
        self.assertEqual(d.reverse_coord_dict(d.read_map('day18/test1.txt')), check)
        
    def test_next_keys(self):
        coord_to_loc = d.read_map('day18/test1.txt')
        loc_to_coord = d.reverse_coord_dict(coord_to_loc)
        neighbors = d.get_neighbors(coord_to_loc)
        self.assertEqual(d.next_keys(coord_to_loc,loc_to_coord,neighbors,loc_to_coord['@']),{'a':2})
        self.assertEqual(d.next_keys(coord_to_loc,loc_to_coord,neighbors,loc_to_coord['a'],2,'a'),{'b':8})
        self.assertEqual(d.next_keys(coord_to_loc,loc_to_coord,neighbors,(2,1)),{'b':1})
        self.assertEqual(d.next_keys(coord_to_loc,loc_to_coord,neighbors,loc_to_coord['b'],1,'b'),{})
        
        coord_to_loc = d.read_map('day18/test2.txt')
        loc_to_coord = d.reverse_coord_dict(coord_to_loc)
        neighbors = d.get_neighbors(coord_to_loc)
        self.assertEqual(d.next_keys(coord_to_loc,loc_to_coord,neighbors,loc_to_coord['c'],1000,'abc'),{'e':1014, 'd':1024})
        
        

if __name__ == '__main__':
    unittest.main()
    