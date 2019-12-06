#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:53:01 2019

@author: jim
"""

import unittest
import day02.day02 as d

class TestDay02(unittest.TestCase):
    def test_read_program(self):
        self.assertEqual(d.read_program('day02/test1.txt'),[1,0,0,0,99])
        
    def test_run(self):
        p = d.read_program('day02/test1.txt')
        d.run(p)
        self.assertEqual(p, [2,0,0,0,99])
        p = d.read_program('day02/test2.txt')
        d.run(p)
        self.assertEqual(p, [2,3,0,6,99])
        p = d.read_program('day02/test3.txt')
        d.run(p)
        self.assertEqual(p, [2,4,4,5,99,9801])
        p = d.read_program('day02/test4.txt')
        d.run(p)
        self.assertEqual(p, [30,1,1,4,2,5,6,0,99])
        
    
if __name__ == '__main__':
    unittest.main()