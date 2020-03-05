#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 18.

@author: James Jolley, james@jolley.co
"""

from collections import deque
from operator import add
from itertools import chain
from random import randrange

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

def find_dead_ends(neighbors):
    '''Find the dead ends. Dead ends have exactly one neighbor.'''
    return [k for k,v in neighbors.items() if len(v)==1]

def prune_dead_ends(map_, neighbors):
    '''Remove dead ends that do not affect the optimal path to collect keys.'''
    # What are the dead_ends?
    dead_ends = find_dead_ends(neighbors)
    # Evaluate all the dead ends, pruning if necessary.
    while dead_ends:
        dead_end = dead_ends.pop()
        # prune dead end if empty or if it contains a door
        dead_end_value = map_[dead_end]
        if dead_end_value == '.' or ('A' <= dead_end_value <= 'Z'):
            # who is this dead end's neighbor?
            neighbor = tuple(neighbors[dead_end])[0]
            # remove the dead_end from the map_
            del map_[dead_end]
            # remove the dead_end's set of neighbors
            del neighbors[dead_end]
            # remove the dead_end from its neighbor's set of neighbors
            neighbors[neighbor].remove(dead_end)
            # if the neighbor now only has one neighbor, then it is a dead end
            if len(neighbors[neighbor]) == 1:
                dead_ends.append(neighbor)


def get_distances_from_pos(map_, neighbors, startloc, stop_at_first_key=True):
    '''Find the shortest distance between the starting location and the keys.
    Record the doors that must be open to reach each key. If stop_at_first_key,
    do not proceed once picking up a key -- this will be used to limit the
    number of paths from the starting locations in part2.'''
    # Represents the state before traversing any locations.
    startstate = State(startloc)
    # Tracks the minimum distance from startloc to any location.
    state_to_steps = {}
    to_search = deque([(startstate, 0)])
    while to_search:
        state, steps = to_search.popleft()
        # Mark a door if there is one at this location
        if 'A' <= map_[state.pos] <= 'Z':
            # Use the add_key method to track doors instead of keys
            state.add_key(map_[state.pos].lower())
        # Mark the number of steps to this location given the doors traversed,
        # if this location/door-set hasn't yet been reached.
        if state.as_immutable() not in state_to_steps:
            state_to_steps[state.as_immutable()] = steps
            # Stop if there's a key here, if requested.
            if stop_at_first_key and ('a' <= map_[state.pos] <= 'z'):
                continue
            # Add neighboring states to the search queue
            to_search.extend(
                [(State(pos, state.key_bitmap), steps+1) \
                 for pos in neighbors[state.pos]])
    # Return only the states in state_to_steps if the state's position contains
    # a key, AND if that key is not where the search started
    return {k:v for k,v in state_to_steps.items() \
            if k[:2] != startloc and 'a' <= map_[k[:2]] <= 'z'}
    
def part2_initialize(path):
    '''Prepare the map, neighbors, and staring locations for Part 2.'''
    map_ = read_map(path)
    # Find the location with the character '@'
    startloc = [k for k,v in map_.items() if v == '@'][0]
    # Set the new starting locations
    offsets = [(a,b) for a in (-1,1) for b in (-1,1)]
    newstartlocs = [tuple(map(add, startloc, o)) for o in offsets]
    for newstartloc in newstartlocs:
        map_[newstartloc] = '@'
    # Set the new walls. This is done by removing the locations from the dict.
    offsets = [(a,b) for a in range(-1,2) for b in range(-1,2) if a == 0 or b == 0]
    newwalls = [tuple(map(add, startloc, o)) for o in offsets]
    for newwall in newwalls:
        del map_[newwall]
    # Find neighbors
    neighbors = get_neighbors(map_.keys())
    # prune dead ends
    prune_dead_ends(map_, neighbors)
    
    return (map_, neighbors, newstartlocs)

def part2(path, ignore_larger_than=None):
    map_, neighbors, locs = part2_initialize(path)
    # a cache of distances from each starting location
    dist_cache = {loc:get_distances_from_pos(map_, neighbors, loc) for loc in locs}
    # loop thru the map to create the bitmap of all keys and the origin
    stop_bitmap = 0
    for k,v in map_.items():
        if 'a' <= v <= 'z':
            stop_bitmap += (1 << ord(v)-ord('a'))
    # Represent the locations of the 4 robots as an 8-tuple of appended
    # (x,y) coordinates
    startloc = tuple(chain(*locs))
    startstate = State(startloc)
    # map the locations and set of collected keys to the distance from origin
    state_to_steps = {startstate.as_immutable() : 0}
    # evaluation queue
    to_search = deque([(startstate, 0)])
    # shortest complete path
    shortest = ignore_larger_than
    while to_search:
        state, steps = to_search.popleft()
        if shortest is not None and steps >= shortest:
            continue
        # Did we find all the keys?
        if state.key_bitmap == stop_bitmap:
            # Is this the shortest path?
            if shortest is None or steps < shortest:
                shortest = steps
            continue
        for i in range(0,len(state.pos), 2):
            pos = state.pos[i:i+2]
            if pos not in dist_cache:
                dist_cache[pos] = get_distances_from_pos(map_, neighbors, pos, False)
            # Evaluate only the distances where we can reach given the keys
            # currently collected.
            # This can be evaluated by taking a bitwise-AND of the bitmap of
            # collected keys with the bitmap of required keys to reach the
            # location. If this result is equal to the bitmap of required keys,
            # then this location can be reached.
            dist = {k:v for k,v in dist_cache[pos].items() \
                    if state.key_bitmap & k[2] == k[2]}
            for loc_keys, steps_from in dist.items():
                # create new State representing this location
                new_state = State(state.pos[:i] + loc_keys[:2] + state.pos[i+2:], state.key_bitmap)
                # pick up the key at this location
                new_state.add_key(map_[loc_keys[:2]])
                if new_state.as_immutable() not in state_to_steps or \
                   state_to_steps[new_state.as_immutable()] > steps + steps_from:
                    state_to_steps[new_state.as_immutable()] = steps + steps_from
                    #to_search.append((new_state, steps + steps_from))
                    to_search.appendleft((new_state, steps + steps_from))
    return shortest
    

def part2_abandoned(path):
    '''Implemented similarly as part1, except the State object contains an
    8-tuple as the locations of the 4 robots (x1, y1, x2, y2, x3, y3, x4, y4).
    ABANDONED: works for test cases, but input grows to 25GB memory with no
    solution.'''
    map_ = read_map(path)
    # Find the location with the character '@'
    startloc = [k for k,v in map_.items() if v == '@'][0]
    # Set the new starting locations
    offsets = [(a,b) for a in (-1,1) for b in (-1,1)]
    newstartlocs = [tuple(map(add, startloc, o)) for o in offsets]
    for newstartloc in newstartlocs:
        map_[newstartloc] = '@'
    # Set the new walls. This is done by removing the locations from the dict.
    offsets = [(a,b) for a in range(-1,2) for b in range(-1,2) if a == 0 or b == 0]
    newwalls = [tuple(map(add, startloc, o)) for o in offsets]
    for newwall in newwalls:
        del map_[newwall]
    # Find neighbors
    neighbors = get_neighbors(map_.keys())
    # prune dead ends
    prune_dead_ends(map_, neighbors)
    # loop thru the map to create the bitmap of all keys and the origin
    stop_bitmap = 0
    for k,v in map_.items():
        if 'a' <= v <= 'z':
            stop_bitmap += (1 << ord(v)-ord('a'))
    # Represent the locations of the 4 robots as an 8-tuple of appended
    # (x,y) coordinates
    startloc = tuple(chain(*newstartlocs))
    startstate = State(startloc)
    # map the locations and set of collected keys to the distance from origin
    state_to_steps = {startstate.as_immutable() : 0}
    # evaluation queue
    to_search = deque([(startstate, 0)])
    while to_search:
        state, steps = to_search.popleft()
        #DEBUG
        #if randrange(100000) == 0:
        #    print(f'state: {state}, steps: {steps}')
        #END DEBUG
        # Find the neighboring states of each robot.
        # Start with the robots locations.
        robots = [state.pos[i:i+2] for i in range(0,len(state.pos),2)]
        # Look at each robot's neighbors individually.
        for i in range(len(robots)):
            # Build the neighboring sequence. Keep 3 robots still, and move
            # just one robot.
            for neighbor in neighbors[robots[i]]:
                allpos = []
                for j in range(len(robots)):
                    allpos.append(neighbor if i==j else robots[j])
                pos = tuple(chain(*allpos))
                newstate = State(pos, state.key_bitmap)
                # Is there a key? Pick it up
                if 'a' <= map_[neighbor] <= 'z':
                    newstate.add_key(map_[neighbor])
                # Is there a locked door? Abandon this path
                elif 'A' <= map_[neighbor] <= 'Z':
                    if not newstate.door_open(map_[neighbor]):
                        continue
                # Have we reached the end? If so, return number of steps taken
                if newstate.key_bitmap == stop_bitmap:
                    return steps+1
                # Have we never been in this location with these exact keys?
                # If not, add to the search queue
                if newstate.as_immutable() not in state_to_steps:
                    state_to_steps[newstate.as_immutable()] = steps+1
                    to_search.append((newstate, steps+1))
