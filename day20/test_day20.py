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
        exp_portals = {'AA': [(19, 2)],
                       'BU': [(11, 34), (26, 21)],
                       'JP': [(15, 34), (21, 28)],
                       'CP': [(19, 34), (21, 8)],
                       'VT': [(32, 11), (26, 23)],
                       'DI': [(2, 15), (8, 21)],
                       'ZZ': [(2, 17)],
                       'AS': [(32, 17), (17, 8)],
                       'JO': [(2, 19), (13, 28)],
                       'LF': [(32, 21), (15, 28)],
                       'YN': [(2, 23), (26, 13)],
                       'QG': [(32, 23), (26, 17)]}
        self.assertCountEqual(portals.keys(), exp_portals.keys())
        for key in portals.keys():
            self.assertCountEqual(portals[key], exp_portals[key])
            
    def test_part1(self):
        self.assertEqual(d.part1('day20/test1.txt'), 23)
        self.assertEqual(d.part1('day20/test2.txt'), 58)

if __name__ == '__main__':
    unittest.main()
    