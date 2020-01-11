#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 19.

@author: James Jolley, james@jolley.co
"""

from day05.day05 import Computer, read_program

def get_drone_status(ram, x, y):
    '''Return the status of the drone at coordinates (x,y), calculated by an
    Intcode computer using the supplied program.'''
    comp = Computer(ram)
    comp.in_.append(x)
    comp.in_.append(y)
    while not comp.out:
        comp.step()
    return comp.out.popleft()

def find_first_in_row(ram, y, start_x=0, limit=100):
    '''Return the x-coord of the first spot with value 1 in row y. Returns None
    if no values of 1 found between start_x and start_x + limit.'''
    x = start_x
    while True:
        if x >= start_x + limit:
            return None
        status = get_drone_status(ram, x, y)
        if status == 0:
            x += 1
        else:
            break
    return x

def check_top_right(ram, x, y, length=100):
    '''Return True if the coordinate at (x+length-1,y) is 1, False otherwise.
    '''
    return get_drone_status(ram, x+length-1, y) == 1

def check_bottom_row(ram, x, y, length=100):
    '''Return True if the coordinates at (x,y+length-1) and 
    (x+length-1,y+length-1) are both 1, False otherwise.'''
    return get_drone_status(ram, x, y+length-1) == 1 and \
           get_drone_status(ram, x+length-1, y+length-1) == 1

def part1(path):
    ram = read_program(path)
    return sum(get_drone_status(ram, x, y) for x in range(50) for y in range(50))

def part2(path, debug=False):
    ram = read_program(path)
    x, y = 0, 0
    while True:
        if debug:
            print('part2', x, y)
        res_x = find_first_in_row(ram, y, x)
        if res_x is None:
            y += 1
        elif check_top_right(ram, x, y):
            if check_bottom_row(ram, x, y):
                return (x,y)
            else:
                x += 1
        else:
            y += 1
    

def print_part1(path):
    ram = read_program(path)
    for y in range(50):
        for x in range(50):
            print(get_drone_status(ram, x, y), end='')
        print()

if __name__ == '__main__':
    print(part1('day19/input.txt'))
    print(part2('day19/input.txt', True))
