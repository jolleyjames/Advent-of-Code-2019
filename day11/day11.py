#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 11.

@author: James Jolley, james@jolley.co
"""

from day05.day05 import Computer, read_program

class Robot:
    '''Represents the current direction of the robot. Includes methods to
    retrieve the robots current location, and to move the robot.'''
    
    directions = ['U','R','D','L']
    def __init__(self):
        self.coord = [0,0]
        self.dir_index = 0
        self.painted = {}
        
    def get_coord(self):
        return self.coord
    
    def move(self, next_dir):
        '''0 to move left, 1 to move right.'''
        if next_dir == 0:
            self.dir_index -= 1
        elif next_dir == 1:
            self.dir_index += 1
        else:
            raise ValueError(f'illegal direction {next_dir}, must be 0 or 1')
        self.dir_index %= len(Robot.directions)
        
        if Robot.directions[self.dir_index] == 'U':
            self.coord[1] -= 1
        elif Robot.directions[self.dir_index] == 'D':
            self.coord[1] += 1
        elif Robot.directions[self.dir_index] == 'L':
            self.coord[0] -= 1
        elif Robot.directions[self.dir_index] == 'R':
            self.coord[0] += 1
        else:
            raise ValueError(f'unexpected direction {Robot.directions[self.dir_index]}')
            
    def paint(self, color):
        '''0 black, 1 white'''
        self.painted[tuple(self.coord)] = color
        
    def get_color(self):
        return self.painted.get(tuple(self.coord), 0)
            
def run_program(path, start_white=False):
    '''Returns the Robot that runs the program loaded from path.'''
    program = read_program(path)
    c = Computer(program)
    r = Robot()
    paint_next = True
    
    if start_white:
        r.painted[(0,0)] = 1
    
    while c.ram[c.ip] != 99:
        if c.ram[c.ip]== 3: #waiting for input
            c.in_.append(r.get_color())
        c.step()
        if c.out:
            out = c.out.popleft()
            if paint_next:
                r.paint(out)
            else:
                r.move(out)
            paint_next = not paint_next
    return r

def part1(path):
    r = run_program(path)
    # how many panels were painted at least once?
    return len(r.painted)

def part2(path):
    r = run_program(path, True)
    # which panels were painted white?
    panels = [coord for coord in r.painted if r.painted[coord] == 1]
    x,y = zip(*panels)
    min_x, max_x, min_y, max_y = min(x), max(x), min(y), max(y)
    for y in range(min_y, max_y+1):
        row = []
        for x in range(min_x, max_x+1):
            if (x,y) in panels:
                row.append('*')
            else:
                row.append(' ')
        print(''.join(row))
    
        
        

if __name__ == '__main__':
    print(part1('day11/input.txt'))
    print(part2('day11/input.txt'))
    
        
    
        