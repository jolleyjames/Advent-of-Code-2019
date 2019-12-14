#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 12.

@author: James Jolley, james@jolley.co
"""

import re
from operator import mul
from copy import deepcopy
from numpy import lcm

def read_positions(path):
    '''Return the positions of the moons described in the file at the path.'''
    pos = []
    with open(path, 'r') as fobj:
        for line in fobj:
            match = re.search(r'<x=(-?\d+), y=(-?\d+), z=(-?\d+)>', line)
            pos.append([int(s) for s in match.group(1,2,3)])
    return pos

def positions_to_pv_coord_pairs(pos, init_vel=0):
    '''For the coordinate positions in the supplied list, create
    [position, velocity] pairs for each axis.'''
    return [ [[p[n], init_vel] for p in pos] for n in range(len(pos[0]))] 

def apply_gravity(pv):
    '''For each position/velocity pair in the list, calculate the new velocity.
    '''
    for a in range(len(pv)-1):
        for b in range(a+1, len(pv)):
            diff = pv[a][0] - pv[b][0]
            if diff > 0:
                pv[a][1] -= 1
                pv[b][1] += 1
            elif diff < 0:
                pv[a][1] += 1
                pv[b][1] -= 1

def apply_velocity(pv):
    '''For each position/velocity pair in the list, calculate the new position.
    '''
    for a in pv:
        a[0] += a[1]
    
def simulate(path, time):
    pos = read_positions(path)
    x,y,z = positions_to_pv_coord_pairs(pos)
    for _ in range(time):
        for a in (x,y,z):
            apply_gravity(a)
            apply_velocity(a)
    return (x,y,z)

def total_energy(pos, vel):
    energy = lambda c: sum(map(abs, c))
    pot = [energy(p) for p in pos]
    kin = [energy(v) for v in vel]
    return sum(map(mul, pot, kin))
    
def part1(path, time):
    x,y,z = simulate(path, time)
    pos = [ [x[n][0], y[n][0], z[n][0]] for n in range(len(x))]
    vel = [ [x[n][1], y[n][1], z[n][1]] for n in range(len(x))]
    return total_energy(pos, vel)

def steps_until_repeat(pv):
    '''Returns how many steps until the initial state is duplicated.'''
    steps = 0
    init = deepcopy(pv)
    while True:
        apply_gravity(pv)
        apply_velocity(pv)
        steps += 1
        if pv == init:
            break
    return steps

def part2(path):
    pos = read_positions(path)
    x,y,z = positions_to_pv_coord_pairs(pos)
    steps = [steps_until_repeat(pv) for pv in (x,y,z)]
    return lcm.reduce(steps)

if __name__ == '__main__':
    print(part1('day12/input.txt', 1000))
    print(part2('day12/input.txt'))
    
