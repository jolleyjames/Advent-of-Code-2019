#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 16.

@author: James Jolley, james@jolley.co
"""

import numpy as np
from scipy.sparse import coo_matrix, vstack

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
    
def get_sparse_matrix(lensig, offset=0):
    '''Like get_matrix, but creates a sparse matrix.'''
    matrix = None
    temp_matrix = []
    for phase in range(offset+1, lensig+1):
        #DEBUG
        if phase%100 == 0: print('phase:', phase)
        temp_matrix.append(list(get_pattern(phase, offset+1, lensig+1)))
        if phase%10000 == 0 or phase == lensig:
            if matrix is None:
                matrix = coo_matrix(temp_matrix)
            else:
                matrix = vstack([matrix, coo_matrix(temp_matrix)])
            temp_matrix = []
    return matrix

def fft_with_large_offset(signal):
    '''Process the signal using the Flawed Frequency Transmission algorithm.
    Assumes the offset is more than half of the size of the signal, meaning
    all values in the sequence will be 0s and 1s.'''
    new_sig = np.zeros(len(signal),dtype=int)
    new_sig[-1] = signal[-1]
    for i in range(-2, -len(signal)-1, -1):
        new_sig[i] = signal[i] + new_sig[i+1]
    return new_sig % 10
    
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
    matrix = get_matrix(len(signal))
    signal = signal.reshape(len(signal), 1)
    for _ in range(100):
        signal = fft(matrix, signal)
    return ''.join(str(n[0]) for n in signal[:8])

def part2(path):
    with open(path, 'r') as fobj:
        signal = fobj.readline().strip()
    offset = int(signal[:7])
    if offset < len(signal)/2:
        raise ValueError('offset must be more than half the size of signal')
    signal = (signal * 10000)[offset:]
    signal = np.array([int(c) for c in signal])
    for _ in range(100):
        signal = fft_with_large_offset(signal)
    return ''.join(str(n) for n in signal[:8])
    

if __name__ == '__main__':
    print(part1('day16/input.txt'))
    print(part2('day16/input.txt'))
    