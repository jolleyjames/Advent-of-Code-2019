#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 16.

@author: James Jolley, james@jolley.co
"""

import numpy as np

def get_pattern(phase, limit=None):
    '''Generates values in the sequence 0, 1, 0, -1, repeating each value by
    the specified phase, always skipping the first element.'''
    n = 1
    values = (0,1,0,-1)
    while limit is None or n < limit+1:
        yield values[(n%(phase*4))//phase]
        n += 1

def fft(signal):
    '''Process the signal using the Flawed Frequency Transmission algorithm.
    signal is a numpy array of digits. Returns another string of digits.'''
    #TODO potentially improve performance by:
    # 1) factoring out string processing -- DONE
    # 2) using matrix multiplication for all signals at once
    out = []
    for phase in range(1, len(signal)+1):
        pattern = np.array(list(get_pattern(phase, len(signal))))
        d = np.sum(signal * pattern)
        d = d % 10 if d >= 0 else -d % 10
        out.append(d)
    return np.array(out)

def part1(path):
    with open(path, 'r') as fobj:
        signal = np.array([int(c) for c in fobj.readline().strip()])
    for _ in range(100):
        signal = fft(signal)
    return ''.join(str(n) for n in signal[:8])

if __name__ == '__main__':
    print(part1('day16/input.txt'))
    