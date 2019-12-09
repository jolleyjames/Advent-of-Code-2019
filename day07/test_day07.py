#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for Advent of Code 2019, day 7.

@author: James Jolley, james@jolley.co
"""

import unittest
import day07.day07 as d

test_result = True

class TestDay07(unittest.TestCase):
    def test_amplify_signal(self):
        '''Runs an input 1 through a sequence of 4 Computers to calculate
        the factorial of 5. Each Computer takes the output of the last 
        Computer (or 1 for the first Computer), and multiplies it by the
        provided phase. The final output should be 5!, or 120.'''
        program = d.read_program('day07/test1.txt')
        self.assertEqual(d.amplify_signal(program, (2,3,4,5), 1), 120)

    def test_part1(self):
        self.assertEqual(d.part1('day07/test2.txt'), (43210, (4,3,2,1,0)))
        self.assertEqual(d.part1('day07/test3.txt'), (54321, (0,1,2,3,4)))
        self.assertEqual(d.part1('day07/test4.txt'), (65210, (1,0,4,3,2)))
        if test_result:
            self.assertEqual(d.part1('day07/input.txt')[0], 398674)
        
    def test_amplify_signal_with_feedback(self):
        '''Should produce same output as test_amplify_signal using 
        "day07/test.txt".
        '''
        program = d.read_program('day07/test1.txt')
        self.assertEqual(d.amplify_signal_with_feedback(program, (2,3,4,5), 1),
                         120)

    def test_part2(self):
        self.assertEqual(d.part2('day07/test5.txt'), (139629729, (9,8,7,6,5)))
        self.assertEqual(d.part2('day07/test6.txt'), (18216, (9,7,8,5,6)))
        if test_result:
            self.assertEqual(d.part2('day07/input.txt')[0], 39431233)
        
if __name__ == '__main__':
    unittest.main()
    
