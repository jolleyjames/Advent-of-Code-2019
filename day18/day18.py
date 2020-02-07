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

class State:
    '''Represents the state of the search for keys: the current (x,y) position,
    and the set of keys retrieved.'''
    
    def __init__(self, pos, keys=None):
        '''Initialize a state object with its current position and set of keys.
        '''
        self._pos = pos
        if keys is None:
            keys = 0
        if type(keys) is int:
            self._key_bitmap = keys
        elif type(keys) is set:
            self._key_bitmap = 0
            for key in keys:
                self._key_bitmap |= (1 << (ord(key) - ord('a')))
        
    @property
    def pos(self):
        '''The position represented by this State.'''
        return self._pos
        
    @property
    def key_bitmap(self):
        '''The bitmap of keys retrieved.'''
        return self._key_bitmap
    
    @property
    def key_set(self):
        '''The keys retrieved, expressed as a set.'''
        return set([chr(k) for k in range(ord('a'),ord('z')+1) if self.key_bitmap & (1 << (k-ord('a'))) > 0])
        
    def as_immutable(self):
        '''Returns the state as an immutable 3-tuple: x and y coordinates are
        the first 2 members, and the integer bitmap of keys is the last
        member.'''
        return (*self.pos, self.key_bitmap)
    
    def add_key(self, key):
        '''Updates this State to include the specified key.'''
        self._key_bitmap |= (1 << (ord(key) - ord('a')))
        
    def contains_key(self, key):
        '''Returns True if this State has collected the specified key, False
        otherwise.'''
        return self.key_bitmap & (1 << ord(key)-ord('a')) > 0
    
    def door_open(self, door):
        '''Returns True if this door is open -- that is, if this State contains
        the key that opens this door -- and False otherwise.'''
        return self.contains_key(door.lower())
    
    def __str__(self):
        return f'State({self.pos}, {self.key_set})'
    
    def __repr__(self):
        return self.__str__()
    
def part1(path):
    '''A breadth-first search of a complete path from the start to the first
    state where all keys are collected.'''
    map_ = read_map(path)
    neighbors = get_neighbors(map_.keys())
    # loop thru the map to create the bitmap of all keys and the origin
    orig, stop_bitmap = None, 0
    for k,v in map_.items():
        if v == '@':
            orig = State(k)
        elif 'a' <= v <= 'z':
            stop_bitmap += (1 << ord(v)-ord('a'))
    # map the location and set of collected keys to the distance from origin
    state_to_steps = {orig.as_immutable() : 0}
    # evaluation queue
    to_search = deque([(orig, 0)])
    while to_search:
        state, steps = to_search.popleft()
        # neighboring states
        nstates = [State(pos, state.key_bitmap) for pos in neighbors[state.pos]]
        for nstate in nstates:
            # Is there a key? Pick it up
            if 'a' <= map_[nstate.pos] <= 'z':
                nstate.add_key(map_[nstate.pos])
            # Is there a locked door? Abandon this path
            elif 'A' <= map_[nstate.pos] <= 'Z':
                if not nstate.door_open(map_[nstate.pos]):
                    continue
            # Have we reached the end? If so, return number of steps taken
            if nstate.key_bitmap == stop_bitmap:
                return steps+1
            # Have we never been in this location with these exact keys?
            # If not, add to the search queue
            if nstate.as_immutable() not in state_to_steps:
                state_to_steps[nstate.as_immutable()] = steps+1
                to_search.append((nstate, steps+1))
