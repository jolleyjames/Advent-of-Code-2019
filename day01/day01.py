#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  1 09:36:42 2019

@author: jim
"""

import numpy as np

mass_to_fuel_calc = lambda fuel:(fuel//3)-2

def file_to_list(path):
    '''Return a list of integer values of the values in the file.'''
    with open(path,'r') as fobj:
        m = map(int, fobj.readlines())
    return list(m)

def mass_to_fuel(masslist):
    '''Return fuel required for all mass values in the list.'''
    return sum(map(mass_to_fuel_calc, masslist))

def part1(path):
    '''Return fuel requrired for mass value in the file.'''
    return mass_to_fuel(file_to_list(path))

def mass_to_fuel_with_mass(masslist):
    '''Return fuel required for all mass values in the list, taking additional
    fuel requirements from the fuel added.'''
    masslist = np.array(masslist)
    fuellist = masslist
    fuellist_total = np.zeros(len(fuellist))
    fuelsum = 1
    while fuelsum > 0:
        fuellist = mass_to_fuel_calc(fuellist)
        fuellist = np.maximum(fuellist, 0)
        fuellist_total += fuellist        
        fuelsum = np.sum(fuellist)
    return np.sum(fuellist_total)

def part2(path):
    '''Return fuel required for mass values in the file, taking additional 
    fuel requirements from the fuel added.'''
    return mass_to_fuel_with_mass(file_to_list(path))
    
    

if __name__ == '__main__':
    print(part1('day01/input.txt'))
    print(part2('day01/input.txt'))
    


