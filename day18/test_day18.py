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
        
    def test_State_init(self):
        s1 = d.State((10,99))
        self.assertEqual(s1.pos, (10,99))
        self.assertEqual(s1.key_bitmap, 0)
        self.assertEqual(s1.key_set, set())
        s2 = d.State((99,10), set('az'))
        self.assertEqual(s2.pos, (99,10))
        self.assertEqual(s2.key_bitmap, 33554433)
        s3 = d.State((50,50), 56)
        self.assertEqual(s3.pos, (50,50))
        self.assertEqual(s3.key_set, set('def'))
        
    def test_State_as_immutable(self):
        s1 = d.State((17,42), set('abcdefghijklmnopqrstvwxyz'))
        self.assertEqual(s1.as_immutable(), (17, 42, 66060287))
        
    def test_State_add_key(self):
        s1 = d.State((0,0))
        s1.add_key('a')
        self.assertEqual(s1.key_bitmap, 1)
        s1.add_key('x')
        self.assertEqual(s1.key_bitmap, 8388609)
        
    def test_State_contains_key(self):
        s1 = d.State((0,0), set('gnu'))
        self.assertTrue(s1.contains_key('n'))
        self.assertFalse(s1.contains_key('o'))
    
    def test_State_door_open(self):
        s1 = d.State((0,0), set('unlock'))
        self.assertTrue(s1.door_open('U'))
        self.assertFalse(s1.door_open('V'))
    
    def test_part1(self):
        self.assertTrue(d.part1('day18/test1.txt'), 8)
        self.assertTrue(d.part1('day18/test2.txt'), 86)
        self.assertTrue(d.part1('day18/test3.txt'), 132)
        #self.assertTrue(d.part1('day18/test4.txt'), 136)
        self.assertTrue(d.part1('day18/test5.txt'), 81)
        


if __name__ == '__main__':
    unittest.main()
