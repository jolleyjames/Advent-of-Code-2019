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
        self.assertTrue(d.part1('day18/test4.txt'), 136)
        self.assertTrue(d.part1('day18/test5.txt'), 81)
        
    def test_part2_abandoned(self):
        self.assertTrue(d.part2_abandoned('day18/test6.txt'), 8)
        self.assertTrue(d.part2_abandoned('day18/test7.txt'), 24)
        self.assertTrue(d.part2_abandoned('day18/test8.txt'), 32)
        self.assertTrue(d.part2_abandoned('day18/test9.txt'), 72)
        
    def test_get_distances_from_pos(self):
        map_, neighbors, startlocs = d.part2_initialize('day18/test8.txt')
        exp = {(4, 1, 0): 2, (2, 1, 2): 4, (1, 3, 10): 7}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (5,2), False).items())
        exp = {(9, 1, 64): 3, (9, 3, 64+256): 5, (11, 1, 64+1024): 5}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (7,2), False).items())
        exp = {(3, 5, 1): 3, (3, 3, 5): 5, (1, 5, 17): 5}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (5,4), False).items())
        exp = {(9, 5, 32): 3, (11, 5, 32+128): 5, (11, 3, 32+128+512): 7}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (7,4), False).items())
        
        map_, neighbors, startlocs = d.part2_initialize('day18/test9.txt')
        exp = {(4, 3, 0): 1, (3, 3, 0): 2, (1, 3, 4): 4, (1, 1, 4+32): 6, 
               (5, 2, 0): 1, (3, 1, 8): 4}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (5,3), False).items())
        exp = {(9, 1, 16): 4, (9, 3, 2): 2, (11, 1, 2+256+512): 6}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (7,3), False).items())
        exp = {(1, 5, 1024+2048): 4, (1, 7, 1024+2048+4096): 6, (3, 7, 8192): 4}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (5,5), False).items())
        exp = {(10, 7, 64): 7, (9, 7, 64): 8, (7, 7, 128): 2}
        self.assertTrue(exp.items() <= d.get_distances_from_pos(map_, neighbors, (7,5), False).items())
        
    def test_part2(self):
        self.assertTrue(d.part2('day18/test6.txt'), 8)
        self.assertTrue(d.part2('day18/test7.txt'), 24)
        self.assertTrue(d.part2('day18/test8.txt'), 32)
        self.assertTrue(d.part2('day18/test9.txt'), 72)
        
    

if __name__ == '__main__':
    unittest.main()
