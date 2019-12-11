#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code, day 10.

@author: James Jolley, james@jolley.co
"""

import unittest
import day10.day10 as d
import numpy as np

class TestDay10(unittest.TestCase):
    
    def test_read_asteroids(self):
        exp = [(1,0),(4,0),(0,2),(1,2),(2,2),(3,2),(4,2),(4,3),(3,4),(4,4)]
        actual = [tuple(a) for a in d.read_asteroids('day10/test1.txt')]
        self.assertCountEqual(exp, actual)
        
    def test_asteroids_by_direction(self):
        from_ = np.array([3,0])
        to_list = list(map(np.array, [[18,10],[5,0],[3,8],[9,4]]))
        exp = {(1,0):[(5,0)],
               (3,2):[(9,4),(18,10)],
               (0,1):[(3,8)]}
        self.assertEqual(d.asteroids_by_direction(from_, to_list), exp)        

    def test_part1(self):
        self.assertEqual(d.part1('day10/test1.txt'), (8,(3,4)))
        self.assertEqual(d.part1('day10/test2.txt'), (33,(5,8)))
        self.assertEqual(d.part1('day10/test3.txt'), (35,(1,2)))
        self.assertEqual(d.part1('day10/test4.txt'), (41,(6,3)))
        self.assertEqual(d.part1('day10/test5.txt'), (210,(11,13)))
        
    def test_order_of_destruction(self):
        order = d.part2('day10/test5.txt')
        self.assertEqual(order[0], (11,12))
        self.assertEqual(order[1], (12,1))
        self.assertEqual(order[2], (12,2))
        self.assertEqual(order[9], (12,8))
        self.assertEqual(order[19], (16,0))
        self.assertEqual(order[49], (16,9))
        self.assertEqual(order[99], (10,16))
        self.assertEqual(order[198], (9,6))
        self.assertEqual(order[199], (8,2))
        self.assertEqual(order[200], (10,9))
        self.assertEqual(order[298], (11,1))
        
if __name__ == '__main__':
    unittest.main()
    