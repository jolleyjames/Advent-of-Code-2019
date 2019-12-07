#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Source for Advent of Code 2019, day 6

@author: James Jolley, james@jolley.co
"""

class Orb:
    '''Astronomical object which may directly orbit another object.'''
    
    def __init__(self, name):
        '''
        name: name of object. 
        d_orbit: object directly orbited by this object.
        '''
        self.name = name
        self.orbits = None
        self.level = None
        
    def __str__(self):
        '''Return the name of the object orbited by this object, and the name
        of this object.'''
        return f'{self.orbits.name if self.orbits else ""}){self.name}'
    
    def __repr__(self):
        return self.__str__()
        

def read_orbs(path):
    '''Load the orbits from the input file. Return as dict of Orbs indexed by
    their names.'''
    orbs = {}
    with open(path, 'r') as fobj:
        for line in fobj.readlines():
            orbited_name, orbiter_name = line.strip().split(')')
            orbited = orbs.get(orbited_name, None)
            if orbited is None:
                orbited = Orb(orbited_name)
                orbs[orbited_name] = orbited
            orbiter = orbs.get(orbiter_name, None)
            if orbiter is None:
                orbiter = Orb(orbiter_name)
                orbs[orbiter_name] = orbiter
            orbiter.orbits = orbited
            
    return orbs

def set_level(orb):
    '''Set the level for the object. The level is the total number of objects
    this object orbits.'''
    if orb.orbits is None:
        orb.level = 0
    else:
        if orb.orbits.level is None:
            set_level(orb.orbits)
        orb.level = orb.orbits.level + 1
        
def set_levels(orbs):
    '''Set the level for all the objects.'''
    for orb in orbs:
        if orb.level is None:
            set_level(orb)
            
def part1(path):
    orbs = read_orbs(path)
    set_levels(orbs.values())
    return sum(orb.level for orb in orbs.values())

def part2(path):
    orbs = read_orbs(path)
    set_levels(orbs.values())
    you = orbs['YOU']
    san = orbs['SAN']
    t = 0
    if you.level > san.level:
        t = you.level - san.level
        for _ in range(t):
            you.orbits = you.orbits.orbits
    if san.level > you.level:
        t = san.level - you.level
        for _ in range(t):
            san.orbits = san.orbits.orbits
    while you.orbits.name != san.orbits.name:
        you.orbits = you.orbits.orbits
        san.orbits = san.orbits.orbits
        t += 2
    return t
    
    

if __name__ == '__main__':
    print(part1('day06/input.txt'))
    print(part2('day06/input.txt'))
            
            