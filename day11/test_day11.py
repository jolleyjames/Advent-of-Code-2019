#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 11.

@author: James Jolley, james@jolley.co
"""

import unittest
import day11.day11 as d

class TestDay11(unittest.TestCase):
    def test_Robot(self):
        r = d.Robot()
        r.paint(1)
        r.move(0)
        r.paint(0)
        r.move(0)
        r.paint(1)
        r.move(0)
        r.paint(1)
        r.move(0)
        r.paint(0)
        r.move(1)
        r.paint(1)
        r.move(0)
        r.paint(1)
        r.move(0)
        self.assertEqual(len(r.painted), 6)
        
        
        
if __name__ == '__main__':
    unittest.main()
            

