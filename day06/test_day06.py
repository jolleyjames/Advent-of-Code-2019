#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 6

@author: James Jolley, james@jolley.co
"""

import unittest
import day06.day06 as d

class TestDay06(unittest.TestCase):
    
    def test_read_orbits(self):
        orbs = d.read_orbs('day06/test1.txt')
        exp = [')COM',
               'COM)B',
               'B)C',
               'C)D',
               'D)E',
               'E)F',
               'B)G',
               'G)H',
               'D)I',
               'E)J',
               'J)K',
               'K)L']
        self.assertCountEqual([o.__str__() for o in orbs.values()], exp)
        
    def test_set_levels(self):
        a = d.Orb('a')
        b = d.Orb('b')
        b.orbits = a
        c = d.Orb('c')
        c.orbits = b
        D = d.Orb('D')
        D.orbits = a
        d.set_levels([c, a, D, b])
        self.assertEqual(a.level, 0)
        self.assertEqual(b.level, 1)
        self.assertEqual(c.level, 2)
        self.assertEqual(D.level, 1)
        
    def test_part1(self):
        self.assertEqual(d.part1('day06/test1.txt'), 42)
        
    def test_part2(self):
        self.assertEqual(d.part2('day06/test2.txt'), 4)
        
    
if __name__ == '__main__':
    unittest.main()
    