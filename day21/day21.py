#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 21.

@author: James Jolley, james@jolley.co
"""

from day05.day05 import Computer, read_program

def add_statement(cmp, stmt):
    '''Adds a springscript statement to a computer loaded with the springdroid
    program. cmp is a Computer; stmt is a string with a springscript
    statement.'''
    stmt += '\n'
    cmp.in_.extend([ord(c) for c in stmt])
    
def run(cmp):
    '''Runs the Computer until it halts or until it awaits input.'''
    while cmp.ram[cmp.ip] not in (3,99) or (cmp.ram[cmp.ip] == 3 and cmp.in_):
        cmp.step()
    if cmp.out[-1]>127:
        end = -1
    else:
        end = len(cmp.out)
    out = ''.join([chr(c) for c in list(cmp.out)[:end]])
    if end == -1:
        out += str(cmp.out[-1])
    cmp.out.clear()
    return out

def shell(path):
    '''Runs an interactive springdroid shell, using the Intcode program stored
    at the specified path.'''
    cmp = Computer(read_program(path))
    while cmp.ram[cmp.ip] != 99:
        out = run(cmp)
        print(out, end='' if type(out)==str else '\n')
        while True:
            instr = input()
            add_statement(cmp, instr)
            if instr in ('WALK','RUN'): break
    print('exiting shell')
        
