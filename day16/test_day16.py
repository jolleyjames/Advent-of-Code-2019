#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 16.

@author: James Jolley, james@jolley.co
"""

import unittest
import numpy as np
import day16.day16 as d

class TestDay16(unittest.TestCase):
    def test_get_pattern(self):
        self.assertEqual(list(d.get_pattern(1,end=8+1)), [1, 0, -1, 0, 1, 0, -1, 0])
        self.assertEqual(list(d.get_pattern(2,end=8+1)), [0, 1, 1, 0, 0, -1, -1, 0])
        self.assertEqual(list(d.get_pattern(3,end=9+1)), [0, 0, 1, 1, 1, 0, 0, 0, -1])

        self.assertEqual(list(d.get_pattern(1,4+1,12+1)), [ 1, 0, -1, 0, 1, 0, -1, 0])
        self.assertEqual(list(d.get_pattern(2,4+1,12+1)), [ 0, -1, -1, 0, 0, 1, 1, 0])
        self.assertEqual(list(d.get_pattern(3,4+1,12+1)), [ 1, 0, 0, 0, -1, -1, -1, 0])
    
    @unittest.skip('skipping until get_pattern verified correct')
    def test_fft(self):
        signal = np.array([int(c) for c in '12345678'])
        signal = d.fft(signal)
        self.assertEqual(''.join(str(n) for n in signal), '48226158')
        signal = d.fft(signal)
        self.assertEqual(''.join(str(n) for n in signal), '34040438')
        signal = d.fft(signal)
        self.assertEqual(''.join(str(n) for n in signal), '03415518')
        signal = d.fft(signal)
        self.assertEqual(''.join(str(n) for n in signal), '01029498')
        
    @unittest.skip('skipping until get_pattern verified correct')
    def test_part1(self):
        self.assertEqual(d.part1('day16/test1.txt'), '24176176')
        self.assertEqual(d.part1('day16/test2.txt'), '73745418')
        self.assertEqual(d.part1('day16/test3.txt'), '52432133')
        
        
if __name__ == '__main__':
    unittest.main()
    