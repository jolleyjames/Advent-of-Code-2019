#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 16.

@author: James Jolley, james@jolley.co
"""

import unittest
import day16.day16 as d

class TestDay16(unittest.TestCase):
    def test_get_pattern(self):
        self.assertEqual(list(d.get_pattern(1,8)), [1, 0, -1, 0, 1, 0, -1, 0])
        self.assertEqual(list(d.get_pattern(2,8)), [0, 1, 1, 0, 0, -1, -1, 0])
        self.assertEqual(list(d.get_pattern(3,9)), [0, 0, 1, 1, 1, 0, 0, 0, -1])
        
    def test_fft(self):
        signal = d.fft('12345678')
        self.assertEqual(signal, '48226158')
        signal = d.fft(signal)
        self.assertEqual(signal, '34040438')
        signal = d.fft(signal)
        self.assertEqual(signal, '03415518')
        signal = d.fft(signal)
        self.assertEqual(signal, '01029498')
        
    def test_part1(self):
        self.assertEqual(d.part1('day16/test1.txt'), '24176176')
        self.assertEqual(d.part1('day16/test2.txt'), '73745418')
        self.assertEqual(d.part1('day16/test3.txt'), '52432133')
        
        
if __name__ == '__main__':
    unittest.main()
    