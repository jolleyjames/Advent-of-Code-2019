#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 12.

@author: James Jolley, james@jolley.co
"""

import re
from operator import mul
from copy import deepcopy

def read_positions(path):
    '''Return the positions of the moons described in the file at the path.'''
    pos = []
    with open(path, 'r') as fobj:
        for line in fobj:
            match = re.search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line)
            pos.append([int(s) for s in match.group(1,2,3)])
    return pos

def apply_gravity(pos, vel):
    for a in range(len(pos)-1):
        for b in range(a+1, len(pos)):
            for n in range(3):
                if pos[a][n] > pos[b][n]:
                    vel[a][n] -= 1
                    vel[b][n] += 1
                if pos[a][n] < pos[b][n]:
                    vel[a][n] += 1
                    vel[b][n] -= 1

def apply_velocity(pos, vel):
    for a in range(len(pos)):
        for n in range(3):
            pos[a][n] += vel[a][n]

def simulate(path, time):
    pos = read_positions(path)
    vel = [[0,0,0] for p in pos]
    for _ in range(time):
        apply_gravity(pos, vel)
        apply_velocity(pos, vel)
    return (pos, vel)

def total_energy(pos, vel):
    energy = lambda c: sum(map(abs, c))
    pot = [energy(p) for p in pos]
    kin = [energy(v) for v in vel]
    return sum(map(mul, pot, kin))
    
def part1(path, time):
    return total_energy(*simulate(path, time))

def part2(path):
    pos = read_positions(path)
    vel = [[0,0,0] for p in pos]
    pos_init = deepcopy(pos)
    vel_init = deepcopy(vel)
    steps = 0
    while True:
        apply_gravity(pos, vel)
        apply_velocity(pos, vel)
        steps += 1
        if pos == pos_init and vel == vel_init:
            break
    return steps

if __name__ == '__main__':
    print(part1('day12/input.txt', 1000))
    
