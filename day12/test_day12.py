#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 12.

@author: James Jolley, james@jolley.co
"""

import unittest
import day12.day12 as d

class TestDay12(unittest.TestCase):
    def test_read_positions(self):
        exp = [[-1, 0, 2],
               [2, -10, -7],
               [4, -8, 8],
               [3, 5, -1]]
        self.assertEqual(d.read_positions('day12/test1.txt'), exp)
        
    def test_apply_gravity(self):
        pos = d.read_positions('day12/test1.txt')
        x,y,z = d.positions_to_pv_coord_pairs(pos)
        exp = [[-1,3],[2,1],[4,-3],[3,-1]]
        d.apply_gravity(x)
        self.assertEqual(x, exp)
    
    def test_apply_velocity(self):
        pos = d.read_positions('day12/test1.txt')
        x,y,z = d.positions_to_pv_coord_pairs(pos)
        exp = [[2,3],[3,1],[1,-3],[2,-1]]
        d.apply_gravity(x)
        d.apply_velocity(x)
        self.assertEqual(x, exp)

    def test_simulate(self):
        exp_x = [[2,-3],[1,-1],[3,3],[2,1]]
        exp_y = [[1,-2],[-8,1],[-6,2],[0,-1]]
        exp_z = [[-3,1],[0,3],[1,-3],[4,-1]]
        x,y,z = d.simulate('day12/test1.txt', 10)
        self.assertEqual(x, exp_x)
        self.assertEqual(y, exp_y)
        self.assertEqual(z, exp_z)
        
    def test_part1(self):
        self.assertEqual(d.part1('day12/test1.txt',10), 179)
        
    def test_part1_2(self):
        self.assertEqual(d.part1('day12/test2.txt',100), 1940)
        
    def test_part2(self):
        self.assertEqual(d.part2('day12/test1.txt'), 2772)
         
    def test_part2_2(self):
        self.assertEqual(d.part2('day12/test2.txt'), 4686774924)
         
         
        

if __name__ == '__main__':
    unittest.main()
