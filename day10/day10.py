#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 10.

@author: James Jolley, james@jolley.co
"""

import numpy as np
from itertools import groupby
import sys

def read_asteroids(path):
    '''Read the file and return a list of numpy arrays of the coordinates of
    the asteroids.'''
    with open(path, 'r') as fobj:
        lines = fobj.readlines()
    a = []
    for y in range(len(lines)):
        for x in range(len(lines[y])):
            if lines[y][x] == '#':
                a.append(np.array((x,y)))
    return a

def asteroids_by_direction(from_, to_list):
    '''For the asteroid in from_, return a dictionary of lists of the asteroids
    in to_list, indexed by the direction. The asteroids in each list are sorted
    by increasing distinace from from_.
    Example: from_ == [0,0], to_list = [[2,0],[6,4],[15,10],[0,8]]
    Returns {(1,0):[(2,0)],
             (3,2):[(6,4),(15,10)],
             (0,1):[(0,8)]}
    '''
    def get_direction(from_, to):
        distance = to - from_
        return tuple(distance//np.gcd(*distance))
    keylambda = lambda t: get_direction(from_, t)
    to_list.sort(key=keylambda)
    rval = {k:list(v) for k,v in groupby(to_list, key=keylambda)}
    for key in rval:
        rval[key].sort(key=lambda t: (from_[0]-t[0])**2 + (from_[1]-t[1])**2)
        rval[key] = list(map(tuple, rval[key]))
    return rval

def find_best_location(path):
    '''From the specified file, find the best location for the asteroid
    monitoring station. This is the asteroid that has the most other asteroids
    directly in the line of sight, which is the same as the number of unique
    directions to other asteroids.
    '''
    asteroids = read_asteroids(path)
    best_asteroid = None
    best_directions = None
    for n in range(len(asteroids)):
        directions = asteroids_by_direction(asteroids[n], asteroids[:n]+asteroids[n+1:])
        if best_asteroid is None or len(directions) > len(best_directions):
            best_asteroid, best_directions = tuple(asteroids[n]), directions
    return (best_asteroid, best_directions)

def order_of_destruction(directions):
    '''From the dictionary of direction to asteroids, return a list with the
    asteroids in order of when they will be destroyed.'''
    # The numpy.arctan2 function returns the angle in radians given x and y
    # coordinates, but the angles are in the range [-pi, pi]. To get them in
    # the range [-pi/2, +3pi/2], add 2pi to angles that are less than -pi/2.
    def get_angle(direction):
        x, y = direction
        angle = np.arctan2(y, x)
        return angle if angle >= -np.pi/2 else angle + 2*np.pi
    directions = [(get_angle(k),v) for k,v in directions.items()]
    directions.sort()
    directions = [d[1] for d in directions]
    order = []
    while directions:
        order += [d.pop(0) for d in directions]
        directions = [d for d in directions if len(d) > 0]
    return order
    
def part1(path):
    return partX(path, 1)

def part2(path):
    return partX(path, 2)
    
def partX(path, part):
    best_asteroid, best_directions = find_best_location(path)
    if part == 1:
        return (len(best_directions), best_asteroid)
    elif part == 2:
        return order_of_destruction(best_directions)
    else:
        raise ValueError('part argument must be 1 or 2')
        

if __name__ == '__main__':
    if sys.argv[1] == '1':
        print(part1('day10/input.txt'))
    elif sys.argv[1] == '2':
        a200 = part2('day10/input.txt')[199]
        print(a200[0]*100 + a200[1])
    else:
        raise ValueError('part argument must be 1 or 2')
    