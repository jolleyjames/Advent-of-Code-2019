#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 18.

@author: James Jolley, james@jolley.co
"""

def read_map(path):
    '''Read the map at the specified path. Returns as a dict with (x,y)
    coordinates as a 2-tuple key, linked to a character of what exists at
    that location -- '.' == open space, lowercase == key, uppercase == door.
    '''
    with open(path, 'r') as fobj:
        lines = fobj.readlines()
    coord_dict = {}
    for y in range(len(lines)):
        line = lines[y].strip()
        for x in range(len(line)):
            if lines[y][x] != '#':
                coord_dict[(x,y)] = lines[y][x]
    return coord_dict

def neighbor_coords(coord):
    '''Return the coordinates that could potentially be a neighbor to the
    supplied coordinate. Neighbors must be directly left, right, up, or down
    from the coordinate.'''
    x,y = coord
    return ((x-1,y),(x+1,y),(x,y-1),(x,y+1))

def neighbors(coords):
    '''Return a dict of each (x,y) coordinate in coords, keyed to a set of all
    of its neighbors.'''
    neighbor_dict = {}
    for coord in coords:
        neighbor_dict[coord] = set(n for n in neighbor_coords(coord) if n in coords)
    return neighbor_dict

def reverse_coord_dict(coords):
    '''Take the coord-to-location dict, and return a location-to-coord dict,
    using only the starting location (indicated by '@') and the key and door
    locations (indicated by lowercase and uppercase letters respecitvely).'''
    return {v:k for k,v in coords.items() if v != '.'}
