#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 17.

@author: James Jolley, james@jolley.co
"""

from day05.day05 import Computer
from operator import mul

def get_intersections(slist):
    '''Get the list of (x,y) coordinates of all intersections.'''
    scaffchars = '#^>v<'
    ixns = []
    for y in range(len(slist)):
        for x in range(len(slist[y])):
            if slist[y][x] not in scaffchars:
                continue
            neighbors = 0
            if x!=0 and slist[y][x-1] in scaffchars:
                neighbors += 1
            if x!=len(slist[y])-1 and slist[y][x+1] in scaffchars:
                neighbors += 1
            if y!=0 and slist[y-1][x] in scaffchars:
                neighbors += 1
            if y!=len(slist)-1 and slist[y+1][x] in scaffchars:
                neighbors += 1
            if neighbors >= 3:
                ixns.append((x,y))
    return ixns

def get_program(path):
    '''Get the Intcode program from the specified path.'''
    with open(path, 'r') as fobj:
        ram = [int(s) for s in fobj.readline().strip().split(',')]
    return ram

def get_scaffold(ram):
    '''Run the Intcode program to get the scaffold output.'''
    c = Computer(ram)
    while c.ram[c.ip] != 99:
        c.step()
    return ''.join([chr(s) for s in c.out]).strip().split('\n')

def get_align_params(ixns):
    '''Get the alignment parameters for the intersections.'''
    return [mul(*coord) for coord in ixns]

def part1(path):
    return sum(get_align_params(get_intersections(get_scaffold(get_program(path)))))

def part2(progpath, routpath):
    ram = get_program(progpath)
    ram[0] = 2
    c = Computer(ram)
    with open(routpath, 'r') as fobj:
        routine = fobj.read()
    for char in routine:
        c.in_.append(ord(char))
    #disable video feed
    c.in_.extend((ord('n'),ord('\n')))
    while c.ram[c.ip] != 99:
        c.step()
    return c.out.pop()
    
if __name__ == '__main__':
    print(part1('day17/input.txt'))
    print(part2('day17/input.txt','day17/routine.txt'))
    