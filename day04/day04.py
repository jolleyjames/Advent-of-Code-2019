#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 00:31:42 2019

@author: jim
"""

class Counter:
    _digits = tuple([10**x for x in range(5, -1, -1)])
    def __init__(self, start):
        if start > 999999:
            raise ValueError('max 6 digits')
        self._value = [(start // (10**x))%10 for x in range(5,-1,-1)]
        for i in range(1,len(self._value)):
            if self._value[i-1] > self._value[i]:
                raise ValueError('no declining digits')
    
    def get_value(self):
        return sum(z[0]*z[1] for z in zip(self._value, Counter._digits))
    
    def step(self):
        n = 5
        while n > -1:
            if self._value[n] < 9:
                self._value[n] += 1
                for m in range(n+1, 6):
                    self._value[m] = self._value[n]
                break
            else:
                n -= 1
    
    def repeats(self):
        for n in range(1,6):
            if self._value[n-1] == self._value[n]:
                return True
        return False
    
    def repeats2(self):
        for n in range(1,6):
            if self._value[n-1] == self._value[n] and \
               (n == 1 or self._value[n-2] != self._value[n]) and \
               (n == 5 or self._value[n] != self._value[n+1]):
                return True
        return False
        
    
def part1():
    start, end = 137777, 596253
    c = Counter(start)
    count = 0
    while c.get_value() <= end:
        if c.repeats():
            count += 1
        c.step()
    return count

def part2():
    start, end = 137777, 596253
    c = Counter(start)
    count = 0
    while c.get_value() <= end:
        if c.repeats2():
            count += 1
        c.step()
    return count
        
if __name__ == '__main__':
    print(part1())
    print(part2())