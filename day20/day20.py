#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, Day 20.

@author: James Jolley, james@jolley.co
"""

from collections import deque

def get_input(path):
    '''Read input from path as a list of strings.'''
    with open(path) as fobj:
        lines = fobj.readlines()
    return [line[:-1] for line in lines]

def add_to_portals(portals, portal, coord):
    ''' Add coord to the dictionary portals at the current portal.'''
    if portal not in portals:
        portals[portal] = [coord]
    else:
        portals[portal].append(coord)

def get_portals(lines):
    '''Return a dict of portal names to a 3-tuple containing the x coordinate,
    the y coordinate, and whether the portal is inside (+1) or outside (-1).'''
    portals = {}
    # top
    for x in range(len(lines[0])):
        if lines[0][x] != ' ':
            portal = lines[0][x] + lines[1][x]
            coord = (x, 2, -1)
            add_to_portals(portals, portal, coord)
    # bottom
    for x in range(len(lines[-1])):
        if lines[-1][x] != ' ':
            portal = lines[-2][x] + lines[-1][x]
            coord = (x, len(lines)-3, -1)
            add_to_portals(portals, portal, coord)
    # left and right
    for y in range(2, len(lines)-2):
        if lines[y][0] != ' ':
            portal = lines[y][:2]
            coord = (2, y, -1)
            add_to_portals(portals, portal, coord)
        if lines[y][-1] != ' ':
            portal = lines[y][-2:]
            coord = (len(lines[0])-3, y, -1)
            add_to_portals(portals, portal, coord)
    # inner portals
    for y in range(2, len(lines)-2):
        for x in range(2, len(lines[y])-2):
            # top
            if lines[y][x].isupper() and lines[y-1][x] == '.' and lines[y+1][x].isupper():
                portal = lines[y][x] + lines[y+1][x]
                coord = (x, y-1, 1)
                add_to_portals(portals, portal, coord)
            # bottom
            elif lines[y][x].isupper() and lines[y+1][x] == '.' and lines[y-1][x].isupper():
                portal = lines[y-1][x] + lines[y][x]
                coord = (x, y+1, 1)
                add_to_portals(portals, portal, coord)
            # left
            elif lines[y][x].isupper() and lines[y][x-1] == '.' and lines[y][x+1].isupper():
                portal = lines[y][x:x+2]
                coord = (x-1, y, 1)
                add_to_portals(portals, portal, coord)
            # right
            elif lines[y][x].isupper() and lines[y][x+1] == '.' and lines[y][x-1].isupper():
                portal = lines[y][x-1:x+1]
                coord = (x+1, y, 1)
                add_to_portals(portals, portal, coord)
    return portals

def get_passages(lines, z=0):
    '''Return a dict of coordinates of open passages, keyed to a list of 
    immediate neighbors. Neighbors will not include portal neighbors.'''
    passages = {}
    for y in range(2, len(lines)-2):
        for x in range(2, len(lines[y])-2):
            if lines[y][x] == '.':
                coord = (x,y,z)
                neighbors = [(nx,ny,z) \
                             for nx,ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)) \
                             if lines[ny][nx] == '.']
                passages[coord] = neighbors
    return passages

def add_portals_to_passages(passages, portals):
    '''Add neighbors to open passages using the listed portals.'''
    portals = [[tuple(p[:2])+(0,) for p in v] for v in portals.values() if len(v) == 2]
    for portal in portals:
        passages[portal[0]].append(portal[1])
        passages[portal[1]].append(portal[0])
    return passages

def add_new_floor_to_passages(passages, inner_portals, lines, z_new):
    '''Add a new floor of passages and portals to the existing set of passages.
    '''
    # Add the passages from the new floor to the dictionary of passages
    passages.update(get_passages(lines, z_new))
    for ip in inner_portals:
        ip, op = ip + (z_new-1,), inner_portals[ip] + (z_new,)
        passages[ip].append(op)
        passages[op].append(ip)
    return passages

def get_distances(passages, source, lines, dest=None, inner_portals=None):
    '''Find the minimum distances from the source to all passages in the
    supplied dict. Stop if dest is specified.'''
    dist = {source: 0}
    # queue contains tuples of (x,y,z,dist)
    to_search = deque([(x,y,z,1) for x,y,z in passages[source]])
    while to_search:
        x,y,z,this_dist = to_search.popleft()
        dist[(x,y,z)] = this_dist
        neighbors = passages[(x,y,z)]
        # is this an inner portal to a new floor we haven't seen?
        if inner_portals and len(neighbors) == 1 and tuple((x,y)) in inner_portals:
            passages = add_new_floor_to_passages(passages, inner_portals, lines, z+1)
            neighbors = passages[(x,y,z)]
        to_search.extend([(x_,y_,z_,this_dist+1) for x_,y_,z_ in neighbors if (x_,y_,z_) not in dist])
        if (x,y,z) == dest: break
    return dist

def get_inner_portals(portals):
    '''Create a dict of inner-portal (x,y) coordinates to corresponding
    outer-portal (x,y) coordinates'''
    inner_portals = {}
    for portal in portals.values():
        if len(portal) != 2: continue
        if portal[0][2] == 1:
            inner_portals[portal[0][:2]] = portal[1][:2]
        elif portal[0][2] == -1:
            inner_portals[portal[1][:2]] = portal[0][:2]
        else:
            raise ValueError(f'unexpected portal direction {portal[0][2]}, must be +1 or -1')
    return inner_portals

def part1(path):
    lines = get_input(path)
    portals = get_portals(lines)
    passages = get_passages(lines)
    passages = add_portals_to_passages(passages, portals)
    source=portals['AA'][0][:2] + (0,)
    dest=portals['ZZ'][0][:2] + (0,)
    distances = get_distances(passages, source, lines, dest)
    return distances[dest]

def part2(path):
    lines = get_input(path)
    portals = get_portals(lines)
    passages = get_passages(lines)
    source=portals['AA'][0][:2] + (0,)
    dest=portals['ZZ'][0][:2] + (0,)
    inner_portals = get_inner_portals(portals)
    distances = get_distances(passages, source, lines, dest, inner_portals)
    return distances[dest]
    

if __name__ == '__main__':
    print(part1('day20/input.txt'))
    print(part2('day20/input.txt'))

    