#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 12:37:36 2019

@author: jim
"""

from operator import add, mul, lt, eq
from collections import deque

class Computer:
    '''Emulates the Intcode computer from Advent of Code 2019 day 5.'''
    
    def __init__(self, ram, ip=0, rb=0, in_=[], out=[]):
        # Save ram as a dict. Unused non-negative addresses are assumed to be 0
        self.ram = {k:v for k,v in enumerate(ram)}
        self.ip = ip
        self.rb = rb
        self.in_ = deque(in_)
        self.out = deque(out)
        
    def get_op_and_modes(self):
        '''Return an iterable of the current opcode and the parameter modes.'''
        op = self.ram.get(self.ip,0) % 100
        param = self.ram.get(self.ip,0) // 100
        p = ()
        if op in (1,2,3,4,5,6,7,8,9):
            if op in (1,2,7,8):
                p_count = 3
            elif op in (3,4,9):
                p_count = 1
            elif op in (5,6):
                p_count = 2
            p = tuple((param // (10**x))%10 for x in range(p_count) )
        return (op,) + p
    
    def step(self, debug=False):
        '''Perform the action at the current instruction pointer value.'''
        op, *modes = self.get_op_and_modes()
        if op in (1,2):
            if modes[0] == 0:
                arg0 = self.ram.get(self.ram.get(self.ip+1,0),0)
            elif modes[0] == 1:
                arg0 = self.ram.get(self.ip+1,0)
            elif modes[0] == 2:
                arg0 = self.ram.get(self.ram.get(self.ip+1,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[0]}')
            if modes[1] == 0:
                arg1 = self.ram.get(self.ram.get(self.ip+2,0),0)
            elif modes[1] == 1:
                arg1 = self.ram.get(self.ip+2,0)
            elif modes[1] == 2:
                arg1 = self.ram.get(self.ram.get(self.ip+2,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[1]}')
            # add or multiply?
            f = add if op == 1 else mul
            # "Parameters that an instruction writes to will **never be in
            # immediate mode.**"
            if modes[2] == 0:
                self.ram[self.ram.get(self.ip+3,0)] = f(arg0,arg1)
            elif modes[2] == 2:
                self.ram[self.ram.get(self.ip+3,0)+self.rb] = f(arg0,arg1)
            else:
                raise ValueError(f'illegal paramter mode {modes[2]}')
            # next instruction
            self.ip += 4
        elif op == 3:
            # no-op if self.in_ is empty
            if self.in_:
                # "Parameters that an instruction writes to will **never be in
                # immediate mode.**"
                if modes[0] == 0:
                    self.ram[self.ram.get(self.ip+1,0)] = self.in_.popleft()
                elif modes[0] == 2:
                    self.ram[self.ram.get(self.ip+1,0)+self.rb] = self.in_.popleft()
                else:
                    raise ValueError(f'illegal paramter mode {modes[0]}')    
                self.ip += 2
        elif op == 4:
            if modes[0] == 0:
                arg0 = self.ram.get(self.ram.get(self.ip+1,0),0)
            elif modes[0] == 1:
                arg0 = self.ram.get(self.ip+1,0)
            elif modes[0] == 2:
                arg0 = self.ram.get(self.ram.get(self.ip+1,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[0]}')
            self.out.append(arg0)
            self.ip += 2
        elif op in (5,6):
            # op == 5 => jump-if-true: if p1 != 0, set ip to p2
            # op == 6 => jump-if-false: if p1 == 0, set ip to p2
            if modes[0] == 0:
                check = self.ram.get(self.ram.get(self.ip+1,0),0)
            elif modes[0] == 1:
                check = self.ram.get(self.ip+1,0)
            elif modes[0] == 2:
                check = self.ram.get(self.ram.get(self.ip+1,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[0]}')
            if modes[1] == 0:
                new_ip = self.ram.get(self.ram.get(self.ip+2,0),0)
            elif modes[1] == 1:
                new_ip = self.ram.get(self.ip+2,0)
            elif modes[1] == 2:
                new_ip = self.ram.get(self.ram.get(self.ip+2,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[1]}')
            self.ip = new_ip if ((op == 5 and check != 0) or (op == 6 and check == 0)) \
                             else self.ip + 3
        elif op in (7,8):
            # op == 7 ==> less than: p3 = 1 if p1 < p2 else 0
            # op == 8 ==> equals: p3 = 1 if p1 == p2 else 0
            if modes[0] == 0:
                arg0 = self.ram.get(self.ram.get(self.ip+1,0),0)
            elif modes[0] == 1:
                arg0 = self.ram.get(self.ip+1,0)
            elif modes[0] == 2:
                arg0 = self.ram.get(self.ram.get(self.ip+1,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[0]}')
            if modes[1] == 0:
                arg1 = self.ram.get(self.ram.get(self.ip+2,0),0)
            elif modes[1] == 1:
                arg1 = self.ram.get(self.ip+2,0)
            elif modes[1] == 2:
                arg1 = self.ram.get(self.ram.get(self.ip+2,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[1]}')
            f = lt if op == 7 else eq
            # "Parameters that an instruction writes to will **never be in
            # immediate mode.**"
            if modes[2] == 0:
                self.ram[self.ram.get(self.ip + 3,0)] = 1 if f(arg0,arg1) else 0
            elif modes[2] == 2:
                self.ram[self.ram.get(self.ip + 3,0)+self.rb] = 1 if f(arg0,arg1) else 0
            else:
                raise ValueError(f'illegal paramter mode {modes[2]}')
            self.ip += 4
        elif op == 9:
            if modes[0] == 0:
                self.rb += self.ram.get(self.ram.get(self.ip+1,0),0)
            elif modes[0] == 1:
                self.rb += self.ram.get(self.ip+1,0)
            elif modes[0] == 2:
                self.rb += self.ram.get(self.ram.get(self.ip+1,0)+self.rb,0)
            else:
                raise ValueError(f'illegal paramter mode {modes[1]}')
            self.ip += 2
        elif op == 99:
            pass
        else:
            raise ValueError(f'illegal operation code {op}')
            
        if debug:
            print(self)
    
    def __repr__(self):
        return f'Computer({self.ram}, ip={self.ip}, rb={self.rb}, in_={self.in_}, out={self.out})'
    
    def __str__(self):
        return self.__repr__()
    
def read_program(path):
    '''Read the program from a text file to a list of integers.'''
    with open(path, 'r') as fobj:
        program = list(map(int, fobj.readline().strip().split(',')))
    return program

def run_program(program, in_=0, debug=False):
    '''Create a Computer from the provided program, and run until it halts.'''
    c = Computer(program)
    c.in_.append(in_)
    while c.ram[c.ip] != 99:
        c.step(debug)
    return c

def part1(path):
    '''Load the program, supply the input value 1, ensure the output is all
    zeroes until the final diagnostic value, then return the diagnostic
    value.'''
    program = read_program(path)
    c = run_program(program, 1)
    if len(c.out) < 1:
        raise ValueError('no output')
    exp_zeroes = list(c.out)[:-1]
    if len(exp_zeroes) != exp_zeroes.count(0):
        raise ValueError('not all values are 0')
    return c.out[-1]

def part2(path):
    '''Load the program, supply the input value 5, then return the one and
    only diagnostic value.'''
    program = read_program(path)
    c = run_program(program, 5)
    if len(c.out) != 1:
        raise ValueError(f'expected one output, received {c.out}')
    return c.out[0]
    

if __name__ == '__main__':
    print(part1('day05/input.txt'))
    print(part2('day05/input.txt'))
    

    


        
