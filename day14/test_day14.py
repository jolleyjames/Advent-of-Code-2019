#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 14.

@author: James Jolley, james@jolley.co
"""

import unittest
import day14.day14 as d

class TestDay14(unittest.TestCase):
    def test_part1(self):
        self.assertEqual(d.part1('day14/test1.txt'), 31)
        self.assertEqual(d.part1('day14/test2.txt'), 165)
        self.assertEqual(d.part1('day14/test3.txt'), 13312)
        self.assertEqual(d.part1('day14/test4.txt'), 180697)
        self.assertEqual(d.part1('day14/test5.txt'), 2210736)
        
    def test_part2(self):
        self.assertEqual(d.part2('day14/test3.txt'), 82892753)
        self.assertEqual(d.part2('day14/test4.txt'), 5586022)
        self.assertEqual(d.part2('day14/test5.txt'), 460664)

    
    
if __name__ == '__main__':
    unittest.main()


