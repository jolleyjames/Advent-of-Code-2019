#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:37:42 2019

@author: jim
"""

import unittest
import day05.day05 as d
from collections import deque

class TestDay05(unittest.TestCase):
    
    def test_Computer_init(self):
        c = d.Computer([11002, 0, 100, -100, 99], 4, 2000, [7], [8,9])
        self.assertEqual(c.ram, {k:v for k,v in enumerate([11002, 0, 100, -100, 99])})
        self.assertEqual(c.ip, 4)
        self.assertEqual(c.rb, 2000)
        self.assertEqual(c.in_, deque([7]))
        self.assertEqual(c.out, deque([8,9]))
        
    def test_Computer_get_op_and_modes(self):
        c = d.Computer([11002, 0, 100, -100, 99])
        self.assertEqual(c.get_op_and_modes(), (2, 0, 1, 1))
        c = d.Computer([1101, 0, 100, -100, 99])
        self.assertEqual(c.get_op_and_modes(), (1, 1, 1, 0))
        c = d.Computer([103, 0, 99])
        self.assertEqual(c.get_op_and_modes(), (3, 1))
        c = d.Computer([4, 2, 99])
        self.assertEqual(c.get_op_and_modes(), (4, 0))
        c = d.Computer([99, 11002, 0, 100, -100])
        self.assertEqual(c.get_op_and_modes(), (99,))
        
    def test_Computer_step(self):
        program = [1, 22, 22, 0,     # add p[22] and p[22], store in p[0]]
                   1101, 22, 23, 4,  # add 22 and 23, store in p[4]
                   2, 22, 22, 8,      # mul p[22] and p[22], store in p[8]
                   1102, 22, 23, 12, # mul 22 and 23, store in p[12]
                   3, 16,            # save input to p[16]
                   4, 18,            # output p[18]
                   104, 20,          # output 20
                   99]               # halt
        exp_prg = [198, 22, 22, 0,   # add p[22] and p[22], store in p[0]]
                   45, 22, 23, 4,    # add 22 and 23, store in p[4]
                   9801, 22, 22, 8,   # mul p[22] and p[22], store in p[8]
                   506, 22, 23, 12,  # mul 22 and 23, store in p[12]
                   -1, 16,           # save input to p[16]
                   4, 18,            # output p[18]
                   104, 20,          # output 20
                   99]               # halt
        c = d.Computer(program)
        c.in_.append(-1)
        # expect to run 8 instructions without fail
        for _ in range(8):
            c.step()
        self.assertEqual(c.ram, {k:v for k,v in enumerate(exp_prg)})
        self.assertEqual(c.ip, 22)
        self.assertEqual(c.in_, deque())
        self.assertEqual(c.out, deque([4, 20]))
        
    def test_read_program(self):
        self.assertEqual(d.read_program('day05/test1.txt'),[1002,4,3,4,33])
        
    def test_run_program(self):
        program = d.read_program('day05/test1.txt')
        c = d.run_program(program)
        self.assertEqual(c.ip, 4)
        self.assertEqual(c.ram, {k:v for k,v in enumerate([1002,4,3,4,99])})
        program = d.read_program('day05/test2.txt')
        c = d.run_program(program)
        self.assertEqual(c.ip, 4)
        self.assertEqual(c.ram, {k:v for k,v in enumerate([1101,100,-1,4,99])})
        
    def test_compare(self):
        program = d.read_program('day05/test3.txt')
        c = d.run_program(program, 8)
        self.assertEqual(c.out[0], 1)
        program = d.read_program('day05/test3.txt')
        c = d.run_program(program, 80)
        self.assertEqual(c.out[0], 0)
        
        program = d.read_program('day05/test4.txt')
        c = d.run_program(program, 7)
        self.assertEqual(c.out[0], 1)
        program = d.read_program('day05/test4.txt')
        c = d.run_program(program, 8)
        self.assertEqual(c.out[0], 0)
        
        program = d.read_program('day05/test5.txt')
        c = d.run_program(program, 8)
        self.assertEqual(c.out[0], 1)
        program = d.read_program('day05/test5.txt')
        c = d.run_program(program, -8)
        self.assertEqual(c.out[0], 0)
        
        program = d.read_program('day05/test6.txt')
        c = d.run_program(program, 7)
        self.assertEqual(c.out[0], 1)
        program = d.read_program('day05/test6.txt')
        c = d.run_program(program, 8)
        self.assertEqual(c.out[0], 0)
        
    def test_jump(self):
        program = d.read_program('day05/test7.txt')
        c = d.run_program(program, 0)
        self.assertEqual(c.out[0], 0)
        program = d.read_program('day05/test7.txt')
        c = d.run_program(program, -1)
        self.assertEqual(c.out[0], 1)

        program = d.read_program('day05/test8.txt')
        c = d.run_program(program, 0)
        self.assertEqual(c.out[0], 0)
        program = d.read_program('day05/test8.txt')
        c = d.run_program(program, 1000)
        self.assertEqual(c.out[0], 1)

    def test_larger_example(self):
        program = d.read_program('day05/test9.txt')
        c = d.run_program(program, 6)
        self.assertEqual(c.out[0], 999)
        program = d.read_program('day05/test9.txt')
        c = d.run_program(program, 7)
        self.assertEqual(c.out[0], 999)
        program = d.read_program('day05/test9.txt')
        c = d.run_program(program, 8)
        self.assertEqual(c.out[0], 1000)
        program = d.read_program('day05/test9.txt')
        c = d.run_program(program, 9)
        self.assertEqual(c.out[0], 1001)
        program = d.read_program('day05/test9.txt')
        c = d.run_program(program, 10)
        self.assertEqual(c.out[0], 1001)
        
    def test_part1(self):
        '''Added for Day 9 extension of Intcode introducing relative mode.
        Verifying that the original graded output for Day 5 remains the same.
        '''
        self.assertEqual(d.part1('day05/input.txt'), 7259358)
        
    def test_part2(self):
        '''Added for Day 9 extension of Intcode introducing relative mode.
        Verifying that the original graded output for Day 5 remains the same.
        '''
        self.assertEqual(d.part2('day05/input.txt'), 11826654)
        
if __name__ == '__main__':
    unittest.main()
    