#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, day 8

@author: James Jolley, james@jolley.co
"""

def read_layers(path, width, height):
    with open(path, 'r') as fobj:
        s = fobj.readline().strip()
    layers = []
    for n in range(0,len(s),width*height):
        layers.append(s[n:n+width*height])
    return layers

def part1(path):
    layers = read_layers(path, 25, 6)
    # get counts of 0s, 1s, and 2s per layer
    counts = []
    for n in range(len(layers)):
        # (0 count, 1 count, 2 count, layer number)
        counts.append(tuple(layers[n].count(x) for x in '012') + (n,))
    # sort counts to get the layer with the fewest 0s as first element
    counts.sort()
    # return number of 1s times number of 2s in layer with fewest 0s
    return counts[0][1] * counts[0][2]

def part2(path):
    width, height = 25, 6
    layers = read_layers(path, width, height)
    # start with first layer
    image = list(layers[0])
    # continue until no transparent pixels in image:
    n = 1
    while image.count('2') > 0 or n < len(layers):
        for m in range(len(layers[n])):
            if image[m] == '2':
                image[m] = layers[n][m]
        n += 1
    # replace 0s with space characters
    for n in range(len(image)):
        if image[n] == '0':
            image[n] = ' '
    for x in range(0, len(image), width):
        print(''.join(image[x:x+width]))

if __name__ == '__main__':
    print(part1('day08/input.txt'))
    print(part2('day08/input.txt'))
    

