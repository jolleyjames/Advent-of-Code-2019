#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 9.

@author: James Jolley, james@jolley.co
"""

from day05.day05 import Computer

def read_program(path):
    with open(path, 'r') as fobj:
        program = list(map(int, fobj.readline().strip().split(',')))
    return program

def part1(path, debug=False):
    return partX(path, 1, debug)

def part2(path, debug=False):
    return partX(path, 2, debug)

def partX(path, in_, debug=False):    
    program = read_program(path)
    c = Computer(program)
    c.in_.append(in_)
    while c.ram[c.ip] != 99:
        c.step(debug)
    if len(c.out) != 1:
        print(f'WARNING: expected 1 output, received {len(c.out)} instead')
        print(f'c.out == {c.out}')
    return c.out[-1]

if __name__ == '__main__':
    print(part1('day09/input.txt'))
    print(part2('day09/input.txt'))


