#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 15.

@author: James Jolley, james@jolley.co
"""

from collections import deque
from day05.day05 import Computer, read_program

def next_output(comp, in_):
    '''Apply the input to the Computer, and return the next output value.
    Assumes there is no input or output currently in the Computer.'''
    comp.in_.append(in_)
    while not comp.out:
        if comp.ram[comp.ip] == 99:
            raise ValueError('computer halted')
        comp.step()
    return comp.out.popleft()

def check_origin(path):
    '''Check if the origin contains the oxygen system. True if it does, False
    if it does not.'''
    robot = Computer(read_program(path))
    # try each direction; if wall, try other direction
    if next_output(robot, 1) != 0:
        return next_output(robot, 2) == 2
    elif next_output(robot, 2) != 0:
        return next_output(robot, 1) == 2
    elif next_output(robot, 3) != 0:
        return next_output(robot, 4) == 2
    elif next_output(robot, 4) != 0:
        return next_output(robot, 3) == 2
    else:
        raise ValueError('surrounded by walls')
    
def get_neighbors(loc):
    x,y = loc
    return [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]

def get_map(path):
    '''Get a full map of the oxygen system layout. Assumes origin is
    traversable and is NOT and oxygen location.
    
    Returns tuple: element 0 is a dictionary of (x,y) coordinates mapped to
    traversable neighbors; element 1 is a set of oxygen locations.
    '''
    map_ = {}
    oxygen = set()
    orig = (0,0)
    orig_robot = Computer(read_program(path))
    to_search = deque([(orig,orig_robot)])
    while to_search:
        loc, robot = to_search.popleft()
        neighbors = []
        for nb in get_neighbors(loc):
            if nb[1] == loc[1]-1:
                dir_ = 1 # north
            elif nb[1] == loc[1]+1:
                dir_ = 2 # south
            elif nb[0] == loc[0]-1:
                dir_ = 3 # west
            elif nb[0] == loc[0]+1:
                dir_ = 4 # east
            else:
                raise ValueError(f'illegal neighbor {nb} to location {loc}')
            out = next_output(robot, dir_)
            if out != 0:
                neighbors.append(nb)
                if nb not in map_:
                    to_search.append((nb,robot.clone()))
                if out == 2:
                    oxygen.add(nb)
                # move back
                dir_ = {1:2, 2:1, 3:4, 4:3}[dir_]
                next_output(robot, dir_)
        map_[loc] = neighbors
    return (map_, oxygen)
    
def get_distances(orig, map_):
    '''Return distances of every location in the map from the origin.'''
    dist = {orig: 0}
    # queue contains tuples of (x,y,dist)
    to_search = deque([(x,y,1) for x,y in map_[orig]])
    while to_search:
        x,y,this_dist = to_search.popleft()
        dist[(x,y)] = this_dist
        neighbors = map_[(x,y)]
        to_search.extend([(x_,y_,this_dist+1) for x_,y_ in neighbors if (x_,y_) not in dist])
    return dist

def part_1_and_2(path):
    map_, oxygen = get_map(path)
    if len(oxygen) != 1:
        raise ValueError('expected only 1 oxygen source')
    oxygen = oxygen.pop()
    dist = get_distances((0,0), map_)
    part1 = dist[oxygen]
    dist = get_distances(oxygen, map_)
    part2 = max(dist.values())
    return (part1,part2)
        
if __name__ == '__main__':
    part1, part2 = part_1_and_2('day15/input.txt')
    print(part1)
    print(part2)