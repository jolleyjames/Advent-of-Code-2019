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
        vel = [[0,0,0] for p in pos]
        exp = [[3, -1, -1],
               [1, 3, 3],
               [-3, 1, -3],
               [-1, -3, 1]]
        d.apply_gravity(pos, vel)
        self.assertEqual(vel, exp)
    
    def test_apply_velocity(self):
        pos = d.read_positions('day12/test1.txt')
        vel = [[0,0,0] for p in pos]
        exp = [[2, -1, 1],
               [3, -7, -4],
               [1, -7, 5],
               [2, 2, 0]]
        d.apply_gravity(pos, vel)
        d.apply_velocity(pos, vel)
        self.assertEqual(pos, exp)

    def test_simulate(self):
        exp_pos = [[2, 1, -3],
                   [1, -8, 0],
                   [3, -6, 1],
                   [2, 0, 4]]
        exp_vel = [[-3, -2, 1],
                   [-1, 1, 3],
                   [3, 2, -3],
                   [1, -1, -1]]
        pos, vel = d.simulate('day12/test1.txt', 10)
        self.assertEqual(pos, exp_pos)
        self.assertEqual(vel, exp_vel)
        
    def test_total_energy(self):
        pos, vel = d.simulate('day12/test1.txt', 10)
        self.assertEqual(d.total_energy(pos, vel), 179)
        
    def test_total_energy2(self):
         pos, vel = d.simulate('day12/test2.txt', 100)
         self.assertEqual(d.total_energy(pos, vel), 1940)
         
         
        

if __name__ == '__main__':
    unittest.main()
