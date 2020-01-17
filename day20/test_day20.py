#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, Day 20.

@author: James Jolley, james@jolley.co
"""

import unittest
import day20.day20 as d

class TestDay20(unittest.TestCase):

    def test_add_to_portals(self):
        portal, portals = 'test_portal', {}
        d.add_to_portals(portals, portal, (4,3))
        self.assertEqual(portals, {'test_portal':[(4,3)]})
        d.add_to_portals(portals, portal, (40,300))
        self.assertEqual(portals, {'test_portal':[(4,3),(40,300)]})
        
    def test_get_portals(self):
        portals = d.get_portals(d.get_input('day20/test2.txt'))
        exp_portals = {'AA': [(19, 2, -1)],
                       'BU': [(11, 34, -1), (26, 21, 1)],
                       'JP': [(15, 34, -1), (21, 28, 1)],
                       'CP': [(19, 34, -1), (21, 8, 1)],
                       'VT': [(32, 11, -1), (26, 23, 1)],
                       'DI': [(2, 15, -1), (8, 21, 1)],
                       'ZZ': [(2, 17, -1)],
                       'AS': [(32, 17, -1), (17, 8, 1)],
                       'JO': [(2, 19, -1), (13, 28, 1)],
                       'LF': [(32, 21, -1), (15, 28, 1)],
                       'YN': [(2, 23, -1), (26, 13, 1)],
                       'QG': [(32, 23, -1), (26, 17, 1)]}
        self.assertCountEqual(portals.keys(), exp_portals.keys())
        for key in portals.keys():
            self.assertCountEqual(portals[key], exp_portals[key])
            
    def test_part1(self):
        self.assertEqual(d.part1('day20/test1.txt'), 23)
        self.assertEqual(d.part1('day20/test2.txt'), 58)

    def test_part2(self):
        self.assertEqual(d.part2('day20/test1.txt'), 26)
        self.assertEqual(d.part2('day20/test3.txt'), 396)

if __name__ == '__main__':
    unittest.main()
    