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
    
    def test_get_matrix(self):
        m1 = [[1, 0, -1, 0, 1],
              [0, 1, 1, 0, 0],
              [0, 0, 1, 1, 1],
              [0, 0, 0, 1, 1],
              [0, 0, 0, 0, 1]]
        m1 = np.array(m1)
        self.assertTrue(np.array_equal(d.get_matrix(5), m1))
        m2 = [[1, 0, -1, 0, 1,  0, -1, 0,  1,  0, -1,  0],
              [0, 1,  1, 0, 0, -1, -1, 0,  0,  1,  1,  0],
              [0, 0,  1, 1, 1,  0,  0, 0, -1, -1, -1,  0],
              [0, 0,  0, 1, 1,  1,  1, 0,  0,  0,  0, -1],
              [0, 0,  0, 0, 1,  1,  1, 1,  1,  0,  0,  0],
              [0, 0,  0, 0, 0,  1,  1, 1,  1,  1,  1,  0],
              [0, 0,  0, 0, 0,  0,  1, 1,  1,  1,  1,  1],
              [0, 0,  0, 0, 0,  0,  0, 1,  1,  1,  1,  1],
              [0, 0,  0, 0, 0,  0,  0, 0,  1,  1,  1,  1],
              [0, 0,  0, 0, 0,  0,  0, 0,  0,  1,  1,  1],
              [0, 0,  0, 0, 0,  0,  0, 0,  0,  0,  1,  1],
              [0, 0,  0, 0, 0,  0,  0, 0,  0,  0,  0,  1]]
        m2 = np.array(m2)[5:,5:]
        self.assertTrue(np.array_equal(d.get_matrix(12, 5), m2))
        
    
    def test_fft(self):
        signal = np.array([int(c) for c in '12345678']).reshape(8,1)
        matrix = d.get_matrix(8)
        signal = d.fft(matrix,signal)
        self.assertEqual(''.join(str(n[0]) for n in signal), '48226158')
        signal = d.fft(matrix,signal)
        self.assertEqual(''.join(str(n[0]) for n in signal), '34040438')
        signal = d.fft(matrix,signal)
        self.assertEqual(''.join(str(n[0]) for n in signal), '03415518')
        signal = d.fft(matrix,signal)
        self.assertEqual(''.join(str(n[0]) for n in signal), '01029498')
        
    def test_part1(self):
        self.assertEqual(d.part1('day16/test1.txt'), '24176176')
        self.assertEqual(d.part1('day16/test2.txt'), '73745418')
        self.assertEqual(d.part1('day16/test3.txt'), '52432133')
        
    def test_part2(self):
        self.assertEqual(d.part2('day16/test4.txt'), '84462026')
        self.assertEqual(d.part2('day16/test5.txt'), '78725270')
        self.assertEqual(d.part2('day16/test6.txt'), '53553731')
        
        
if __name__ == '__main__':
    unittest.main()
    