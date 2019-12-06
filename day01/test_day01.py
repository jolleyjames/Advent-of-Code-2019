#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 09:37:23 2019

@author: jim
"""

import unittest
import day01.day01 as d

class TestDay01(unittest.TestCase):

    def test_file_to_list(self):
        self.assertEqual(d.file_to_list('day01/test.txt'),
                         [12,14,1969,100756])
    
    def test_mass_to_fuel(self):
        self.assertEqual(d.mass_to_fuel(d.file_to_list('day01/test.txt')),
                         2+2+654+33583)
        
    def test_part1(self):
        self.assertEqual(d.part1('day01/test.txt'), 2+2+654+33583)
        
    def test_mass_to_fuel_with_mass(self):
        self.assertEqual(d.mass_to_fuel_with_mass(d.file_to_list('day01/test.txt')),
                         2+2+966+50346)
        
    def test_part2(self):
        self.assertEqual(d.part2('day01/test.txt'), 2+2+966+50346)

if __name__ == '__main__':
    unittest.main()