#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 18.

@author: James Jolley, james@jolley.co
"""

from collections import deque

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

def get_neighbors(coords):
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

def next_keys(coord_to_loc, loc_to_coord, neighbors, from_, steps=0, keys=''):
    '''Find the keys that are reachable from the starting coordinate, given
    the set of keys already collected. Returns only keys that are not blocked
    by unopened doors or other keys. Returns a dict of the key name (lowercase
    letter) keyed to the minimum number of steps to reach it.'''
    dist = {from_:steps}
    keys_found = {}
    to_search = deque([(*n,steps+1) for n in neighbors[from_]])
    while to_search:
        x,y,this_dist = to_search.popleft()
        # Do not continue evaluating this path if the door is locked.
        # Locked door is indicated by an uppercase letter whose corresponding
        # lowercase letter is not in the pre-supplied set of keys.
        loc = coord_to_loc[(x,y)]
        if (ord('A') <= ord(loc) <= ord('Z')) and loc.lower() not in keys:
            continue
        # If this location is a key that hasn't yet been found, add it to the
        # found keys dict, with the number of steps to this key as the value.
        # Then stop evaluating this path.
        if (ord('a') <= ord(loc) <= ord('z')) and \
           loc not in keys and loc not in keys_found:
            keys_found[loc] = this_dist
            continue
        # Add this location to the dict of minimum distances
        dist[(x,y)] = this_dist
        # Add the un-evaluated neighbors to the queue
        to_search.extend([(x_,y_,this_dist+1) for x_,y_ in neighbors[(x,y)] if (x_,y_) not in dist])
    # Return the keys found and the minimum distances to each
    return keys_found
    
