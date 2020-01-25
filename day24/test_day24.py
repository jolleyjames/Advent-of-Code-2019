#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Advent of Code 2019, Day 24.

@author: James Jolley, james@jolley.co
"""

import unittest
import day24.day24 as d

class TestDay05(unittest.TestCase):
    
    def test_Grid(self):
        with open('day24/test1.txt') as fobj:
            grid = d.Grid(fobj.readlines())
        grid.step()
        self.assertEqual(grid.rows, ['#..#.','####.','###.#','##.##','.##..'])
        grid.step()
        self.assertEqual(grid.rows, ['#####','....#','....#','...#.','#.###'])
        grid.step()
        self.assertEqual(grid.rows, ['#....','####.','...##','#.##.','.##.#'])
        grid.step()
        self.assertEqual(grid.rows, ['####.','....#','##..#','.....','##...'])
    
    def test_part1(self):
        self.assertEqual(d.part1('day24/test1.txt'), 2129920)
        
    def test_part2(self):
        self.assertEqual(d.part2('day24/test1.txt', 10), 99)

if __name__ == '__main__':
    unittest.main()
    