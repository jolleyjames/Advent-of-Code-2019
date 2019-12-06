#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  2 19:52:55 2019

@author: jim
"""

def read_program(path):
    '''Read the text file of comma-separated integer values at path, and
    return as a list of integers.'''
    with open(path,'r') as fobj:
        p = list(map(int, fobj.readline().split(',')))
    return p

def run(program):
    '''Run the program. The program is a list of integers.'''
    ip = 0
    try:
        while program[ip] != 99:
            if program[ip] == 1:
                program[program[ip+3]] = program[program[ip+1]] + program[program[ip+2]]
            elif program[ip] == 2:
                program[program[ip+3]] = program[program[ip+1]] * program[program[ip+2]]
            else:
                raise ValueError(f'illegal value {program[ip]} at index {ip}')
            ip += 4
    except Exception as e:
        print(f'{e}')
        print(f'ip: {ip}')
        print(f'program: {program}')
        
def part1(noun, verb):
    program = read_program('day02/input.txt')
    program[1:3] = [noun, verb]
    run(program)
    return program[0]
    
def part2():
    break_outer = False
    for noun in range(100):
        for verb in range(100):
            r = part1(noun, verb)
            print(f'n|v {(noun,verb)} ==> {r}')
            if r == 19690720:
                break_outer = True
                break
        if break_outer:
            break
    print(f'100 * noun + verb == {100 * noun + verb}')
            
    
if __name__ == '__main__':
    #print('part1 UPDATE UPDATE')
    #print(part1(12, 2))
    part2()
    
    
        