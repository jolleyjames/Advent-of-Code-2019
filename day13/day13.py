#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 13.

@author: James Jolley, james@jolley.co
"""

from day05.day05 import Computer, read_program

def part1(path):
    c = Computer(read_program(path))
    tiles = {id:set() for id in range(5)}
    while c.ram[c.ip] != 99:
        c.step()
        if len(c.out) == 3:
            x,y,tile_id = (c.out.popleft() for _ in range(3))
            tiles[tile_id].add((x,y))
    return len(tiles[2])

def part2(path):
    program = read_program(path)
    program[0] = 2
    c = Computer(program)
    score = None
    paddle = None
    ball = None
    blocks = None
    while c.ram[c.ip] != 99:
        # when prompted for controller input, have the paddle move toward the
        # ball, if their x coordinates are different
        if c.ram[c.ip]%100 == 3:
            if paddle is None or ball is None:
                c.in_.append(0)
            elif paddle[0] < ball[0]:
                c.in_.append(1)
            elif paddle[0] > ball[0]:
                c.in_.append(-1)
            else:
                c.in_.append(0)
        c.step()
        if len(c.out) == 3:
            x,y,tile_id = (c.out.popleft() for _ in range(3))
            if (x,y) == (-1,0):
                score = tile_id
            elif tile_id == 0 and blocks is not None:
                blocks.discard((x,y))
            elif tile_id == 2:
                if blocks is None:
                    blocks = set()
                blocks.add((x,y))
            elif tile_id == 3:
                paddle=(x,y)
            elif tile_id == 4:
                ball=(x,y)
    return score


if __name__ == '__main__':
    print(part1('day13/input.txt'))
    print(part2('day13/input.txt'))


