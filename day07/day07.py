#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 7.

@author: James Jolley, james@jolley.co
"""

from itertools import permutations
from day05.day05 import Computer

def read_program(path):
    '''Read the Intcode program located at the path into a list of integers.'''
    with open(path, 'r') as fobj:
        program = list(map(int, fobj.readline().strip().split(',')))
    return program

def amplify_signal(program, phase, input_=0, debug=False):
    '''Run the input through a sequence of Intcode Computers, using input as
    input to the first in the sequence. All Computers run the same program.
    Each Computer is initialized with its phase number and the output of the
    previous Computer in the sequence, or the input parameter if it is the 
    first Computer. Returns output of the last Computer.'''
    computers = [Computer(program.copy()) for _ in range(len(phase))]
    for n in range(len(phase)):
        computers[n].in_.append(phase[n])
        computers[n].in_.append(input_)
        # process until the Computer produces output
        while not computers[n].out:
            computers[n].step(debug)
        # save output to be used as the next input
        input_ = computers[n].out.popleft()
    # Return output of the final Computer in the sequence
    return input_

def part1(path, debug=False):
    return partX(amplify_signal, range(5), path, debug)
    
def part2(path, debug=False):
    return partX(amplify_signal_with_feedback, range(5,10), path, debug)

def partX(f, phases, path, debug=False):
    '''Run the program saved at the path through the provided function,
    using every permutation of the provided phases. Return the
    maximum signal value and the phase that produced it.'''
    program = read_program(path)
    max_sig = None
    max_phase = None
    for phase in permutations(phases):
        sig = f(program, phase)
        if max_sig is None or sig > max_sig:
            max_sig = sig
            max_phase = phase
    return (max_sig, max_phase)

def amplify_signal_with_feedback(program, phase, input_=0, debug=False):
    '''After final Computer outputs, feed signal back to first Computer. 
    Continue until all Computers halt. Return final output of last Computer.
    '''
    output = None
    computers = [Computer(program.copy()) for _ in range(len(phase))]
    # apply phases as first inputs to each Computer
    for n in range(len(phase)):
        computers[n].in_.append(phase[n])
    # apply initial input to first Computer
    computers[0].in_.append(input_)
    c_ndx = 0
    # while the final computer has not yet halted
    while computers[-1].ram[computers[-1].ip] != 99:
        c = computers[c_ndx]
        next_c = computers[(c_ndx+1)%len(computers)]
        # process until the Computer halts or needs input
        while c.ram[c.ip] != 99 and (c.ram[c.ip] != 3 or c.in_):
            c.step(debug)
            # apply output to the next computer
            if c.out:
                c_out = c.out.popleft()
                next_c.in_.append(c_out)
                # if it's the last computer, save to the thruster output
                if c_ndx == len(computers)-1:
                    output = c_out
        # move on to next computer
        c_ndx = (c_ndx+1) % len(computers)
    # return thruster output
    return output


    


if __name__ == '__main__':
    print(part1('day07/input.txt'))
    print(part2('day07/input.txt'))

        