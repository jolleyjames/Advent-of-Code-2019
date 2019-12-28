#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 16.

@author: James Jolley, james@jolley.co
"""

import numpy as np

def get_pattern(phase, start=1, end=None):
    '''Generates values in the sequence 0, 1, 0, -1, repeating each value by
    the specified phase, always skipping the first element.'''
    n = start
    values = (0,1,0,-1)
    while end is None or n < end:
        yield values[(n%(phase*4))//phase]
        n += 1

def get_matrix(lensig, offset=0):
    '''Generates the matrix used by the Flawed Frequency Transmission
    algorithm. lensig is the length of the signal; offset is the number of
    characters until the message appears.'''
    matrix = [np.array(list(get_pattern(phase, offset+1, lensig+1))) for phase in range(offset+1, lensig+1)]
    return np.array(matrix)
    
def fft(matrix, signal):
    '''Process the signal using the Flawed Frequency Transmission algorithm.
    matrix is a square matrix containing the signal codes needed for the FFT
    calculation. signal is an n-by-1 matrix containing the signal digits to be
    processed. Returns an n-by-1 matrix of digits.'''
    out = matrix @ signal
    return np.vectorize(lambda d: abs(d)%10)(out)

def part1(path):
    with open(path, 'r') as fobj:
        signal = np.array([int(c) for c in fobj.readline().strip()])
    for _ in range(100):
        signal = fft(signal)
    return ''.join(str(n) for n in signal[:8])

if __name__ == '__main__':
    print(part1('day16/input.txt'))
    