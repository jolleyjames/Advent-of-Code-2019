#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 14

@author: James Jolley, james@jolley.co
"""

from math import ceil, floor

class Reaction:
    def __init__(self, in_, out):
        self.in_ = in_
        self.out = out
        
    def __str__(self):
        return f'Reaction(in_={self.in_}, out={self.out}'

    def __repr__(self):
        return self.__str__()


        
def str_to_unit_label(s):
    out = s.split(' ')
    out[0] = int(out[0])
    return out
        
def read_reactions(path):
    reactions = []
    with open(path, 'r') as fobj:
        for line in fobj:
            line = line.strip()
            in_, out = line.split(' => ')
            out = str_to_unit_label(out)
            in_ = in_.split(', ')
            in_ = [str_to_unit_label(s) for s in in_]
            reactions.append(Reaction(in_, out))
    return reactions

def get_levels(reactions):
    levels = {}
    for r in reactions:
        for n in r.in_:
            levels[n[1]] = None
        levels[r.out[1]] = None
    levels['ORE'] = 0
    reactions = reactions.copy()
    while reactions:
        r = reactions.pop(0)
        if levels[r.out[1]] is None:
            levels_in = [levels[n[1]] for n in r.in_]
            if None not in levels_in:
                levels[r.out[1]] = max(levels_in) + 1
            else:
                reactions.append(r)
    return levels

def reduce_reactions(reactions, part2=False):
    level = get_levels(reactions)
    # find reaction that produces FUEL
    fuel = [r for r in reactions if r.out[1] == 'FUEL'][0].in_
    while len(fuel) > 1 or fuel[0][1] != 'ORE':
        # replace the ingredient furthest from ORE
        max_ndx = 0
        for ndx in range(1,len(fuel)):
            if level[fuel[ndx][1]] > level[fuel[max_ndx][1]]:
                max_ndx = ndx
        rxn = None
        for r in reactions:
            if r.out[1] == fuel[max_ndx][1]:
                rxn = r
                break
        mult = fuel[max_ndx][0] / rxn.out[0]
        if not part2:
            mult = ceil(mult)
        new = rxn.in_.copy()
        for n in new:
            n[0] *= mult
        del fuel[max_ndx]
        fuel += new
        fuel.sort(key=lambda n: n[1])
        x = 0
        while x < len(fuel) - 1:
            if fuel[x][1] == fuel[x+1][1]:
                fuel[x][0] += fuel[x+1][0]
                del fuel[x+1]
            else:
                x += 1
    return fuel[0][0]
        
def part1(path):
    reactions = read_reactions(path)
    return reduce_reactions(reactions)

def part2(path):
    reactions = read_reactions(path)
    return floor(1000000000000 / reduce_reactions(reactions,part2=True))


if __name__ == '__main__':
    print(part1('day14/input.txt'))
    print(part2('day14/input.txt'))

