#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, Day 24.

@author: James Jolley, james@jolley.co
"""

from collections import deque
from itertools import chain

class Grid:
    '''A representation of the grid of cells containing bugs.'''
    
    def __init__(self, rows):
        '''Initialize the Grid using the list of strings.'''
        self._bugs = []
        for row in rows:
            for c in row.strip():
                self._bugs.append(c == '#')
    
    @property
    def rows(self):
        '''A representation of the spaces in the grid with whether or not they
        contain a bug.'''
        rows = []
        for i in range(0,25,5):
            rows.append(''.join('#' if b else '.' for b in self._bugs[i:i+5]))
        return rows
    
    @property
    def biodiversity(self):
        '''The biodiversity rating of the grid of bugs.'''
        return sum(2**i if self._bugs[i] else 0 for i in range(len(self._bugs)))
    
    def neighboring_bugs(self, i):
        '''The number of bugs neighboring the cell at position i. i is the
        0-indexed column number plus 5 times the 0-indexed row number.'''
        count = 0
        # upper neighbor?
        if i > 4:
            count += (1 if self._bugs[i-5] else 0)
        # lower neighbor?
        if i < 20:
            count += (1 if self._bugs[i+5] else 0)
        # left neighbor?
        if i%5 != 0:
            count += (1 if self._bugs[i-1] else 0)
        # right neighbor?
        if i%5 != 4:
            count += (1 if self._bugs[i+1] else 0)
        return count
        
    def next_state(self, i):
        '''The next state of the cell at position i, according to if it has a
        bug and how many neighboring bugs there are.'''
        neighbors = self.neighboring_bugs(i)
        return neighbors == 1 or (neighbors == 2 and not self._bugs[i])
    
    def step(self):
        '''Set all cells to whether or not there will be a bug in a minute.'''
        self._bugs = [self.next_state(i) for i in range(len(self._bugs))]

class InfiniteGrid:
    '''A representation of an infinite grid of cells containing bugs.'''
    
    def __init__(self, rows):
        '''Initialize the InfiniteGrid using the list of strings.'''
        self._levels = deque()
        self._min_level = 0
        grid = []
        for row in rows:
            for c in row.strip():
                grid.append(c == '#')
        self._levels.append(grid)
        
    def get_rows(self, level):
        '''A representation of the spaces in the grid with whether or not they
        contain a bug. The middle cell will be represented with a ? character.
        '''
        bugs = self._levels[self._min_level + level]
        rows = []
        for i in range(0,25,5):
            rows.append(''.join('?' if i+j==12 else '#' if bugs[i+j] else '.' for j in range(5)))
        return rows
    
    @property
    def bug_count(self):
        '''How many bugs are in this InfiniteGrid?'''
        return len([b for b in chain(*self._levels) if b])
    
    def neighboring_bugs(self, level, i):
        '''The number of bugs neighboring the cell at the level and position.
        i is the 0-indexed column number plus 5 times the 0-indexed row number.
        '''
        count = 0
        index = level - self._min_level
        if i == 12:
            return 0
        # count bugs above
        if 0 <= i < 5 and index > 0:
            count += 1 if self._levels[index-1][7] else 0
        elif i == 17 and index < len(self._levels)-1:
            count += len([b for b in self._levels[index+1][20:25] if b])
        elif 5 <= i < 25 and i != 17:
            count += 1 if self._levels[index][i-5] else 0
        # count bugs below
        if 20 <= i < 25 and index > 0:
            count += 1 if self._levels[index-1][17] else 0
        elif i == 7 and index < len(self._levels)-1:
            count += len([b for b in self._levels[index+1][0:5] if b])
        elif 0 <= i < 20 and i != 7:
            count += 1 if self._levels[index][i+5] else 0
        # count bugs left
        if i%5 == 0 and index > 0:
            count += 1 if self._levels[index-1][11] else 0
        elif i == 13 and index < len(self._levels)-1:
            count += len([v for x,v in enumerate(self._levels[index+1]) if x%5==4 and v])
        elif i%5 != 0 and i != 13:
            count += 1 if self._levels[index][i-1] else 0
        # count bugs right
        if i%5 == 4 and index > 0:
            count += 1 if self._levels[index-1][13] else 0
        elif i == 11 and index < len(self._levels)-1:
            count += len([v for x,v in enumerate(self._levels[index+1]) if x%5==0 and v])
        elif i%5 != 4 and i != 11:
            count += 1 if self._levels[index][i+1] else 0
        return count
        
    def next_state(self, level, i):
        '''The next state of the cell at the level and position i, according to
        if it has a bug and how many neighboring bugs there are.'''
        neighbors = self.neighboring_bugs(level, i)
        index = level - self._min_level
        return neighbors == 1 or (neighbors == 2 and not self._levels[index][i])
    
    def step(self):
        '''Set all cells to whether or not there will be a bug in a minute.'''
        # Add a level below if a bug will infest there in one minute.
        if len([b for b in self._levels[0][0:5] if b]) in (1,2) or \
           len([b for b in self._levels[0][20:25] if b]) in (1,2) or \
           len([b for x,b in enumerate(self._levels[0]) if b and x%5==0]) or \
           len([b for x,b in enumerate(self._levels[0]) if b and x%5==4]):
            self._levels.appendleft([False]*25)
            self._min_level -= 1
        # Add a level above if a bug will infest there in one minute
        if len([b for x,b in enumerate(self._levels[-1]) if b and x in (7,17,11,13)]):
            self._levels.append([False]*25)
        
        self._levels = deque([[self.next_state(level,i) for i in range(25)] for level in range(self._min_level, self._min_level+len(self._levels))])




def part1(path):
    with open(path) as fobj:
        grid = Grid(fobj.readlines())
    biodiversities = set()
    while grid.biodiversity not in biodiversities:
        biodiversities.add(grid.biodiversity)
        grid.step()
    return grid.biodiversity

def part2(path, time):
    with open(path) as fobj:
        grid = InfiniteGrid(fobj.readlines())
    for _ in range(time):
        grid.step()
    return grid.bug_count

if __name__ == '__main__':
    print(part1('day24/input.txt'))
    print(part2('day24/input.txt',200))
    