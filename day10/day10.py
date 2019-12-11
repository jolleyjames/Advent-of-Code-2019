#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 10.

@author: James Jolley, james@jolley.co
"""

import numpy as np

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

def unique_directions(from_, to_list):
    '''Find the number of unique directions from the position from_ to each of
    the positions in to_list.
    Example: from_ == [0,0], to_list = [[2,0],[6,4],[15,10],[0,8]]
    Returns [[1,0],[3,2],[0,1]]: [6,4] and [15,10] have the same direction,
    [3,2]
    '''
    distances = [to - from_ for to in to_list]
    directions = [d/np.gcd(*d) for d in distances]
    return set(tuple(d) for d in directions)

def part1(path):
    '''From the specified file, find the asteroid that can directly see the
    most other asteroids.'''
    asteroids = read_asteroids(path)
    # Will hold tuples where [0] is the number of unique directions to other
    # asteroids, which is the same as the number of asteroids directly in the
    # line of sight; [1] is the coordinates of the asteroid
    seen_by = []
    for n in range(len(asteroids)):
        directions = unique_directions(asteroids[n], asteroids[:n]+asteroids[n+1:])
        seen_by.append((len(directions), tuple(asteroids[n])))
    seen_by.sort(key=lambda a:-a[0])
    return seen_by[0]

if __name__ == '__main__':
    print(part1('day10/input.txt'))
    