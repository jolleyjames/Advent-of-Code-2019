#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 18:25:47 2019

@author: jim
"""

class Wire:
    def __init__(self, segments, min_x, min_y, max_x, max_y):
        self.segments = segments
        self.min_x = min_x
        self.min_y = min_y
        self.max_x = max_x
        self.max_y = max_y

def read_wires(path):
    '''Read the lines from the input path. Return a sequence of "wires", each
    "wire" being a sequence of "segments", each "segment" being a pair of (x,y)
    coordinates.'''
    wires = []
    with open(path, 'r') as fobj:
        for line in fobj:
            wires.append(str_to_wire(line.strip()))
    return wires

def str_to_wire(s):
    '''Read a string as directional movements into a "wire". The "wire" is a
    sequence of "segments", each "segment" being a pair of (x,y) coordinates.
    '''
    directions = s.split(',')
    segments = []
    start = [0,0]
    min_x, min_y, max_x, max_y = 0, 0, 0, 0
    for d in directions:
        dist = int(d[1:])
        if d[0] == 'U':
            end = [start[0],start[1]-dist]
            if end[1] < min_y:
                min_y = end[1]
        elif d[0] == 'D':
            end = [start[0],start[1]+dist]
            if end[1] > max_y:
                max_y = end[1]
        elif d[0] == 'L':
            end = [start[0]-dist,start[1]]
            if end[0] < min_x:
                min_x = end[0]
        elif d[0] == 'R':
            end = [start[0]+dist,start[1]]
            if end[0] > max_x:
                max_x = end[0]
        else:
            raise ValueError(f'unexpected direction {d[0]}')
        segment = sorted([start,end])
        segments.append(segment)
        start = end
    return Wire(segments, min_x, min_y, max_x, max_y)

def purge_segments(wire, min_x, min_y, max_x, max_y):
    '''Remove segments from the wire that fall outside of the range.'''
    keep_segments = []
    for seg in wire.segments:
        # vertical segment
        if seg[0][0] == seg[1][0]:            
            if min_x <= seg[0][0] <= max_x and \
               seg[0][1] <= max_y and \
               seg[1][1] >= min_y:
                keep_segments.append(seg)
        #horizonal segment
        elif seg[0][1] == seg[1][1]:
            if min_y <= seg[0][1] <= max_y and \
               seg[0][0] <= max_x and \
               seg[1][0] >= min_x:
                keep_segments.append(seg)
        else:
            raise ValueError(f'unexpected diagonal segment {seg}')
    wire.segments = keep_segments

def intersection(seg1, seg2):
    '''If segments intersect, returns the point of intersection [x,y], or the
    overlapping segment [[x,y1],[x,y2]] or [[x1,y],[x2,y]]. Returns None if
    segments do not intersect.'''
    # seg1 vertical, seg2 horizontal
    if seg1[0][0] == seg1[1][0] and seg2[0][1] == seg2[1][1]:
        if seg2[0][0] <= seg1[0][0] <= seg2[1][0] and \
           seg1[0][1] <= seg2[0][1] <= seg1[1][1]:
            return [seg1[0][0],seg2[0][1]]
    # seg1 horizontal, seg2 vertical
    elif seg1[0][1] == seg1[1][1] and seg2[0][0] == seg2[1][0]:
        if seg2[0][1] <= seg1[0][1] <= seg2[1][1] and \
           seg1[0][0] <= seg2[0][0] <= seg1[1][0]:
            return [seg2[0][0],seg1[0][1]]
    # both segments vertical
    elif seg1[0][0] == seg1[1][0] and seg2[0][0] == seg2[1][0]:
        if seg1[0][0] == seg2[0][0] and \
           seg1[0][1] <= seg2[1][1] and \
           seg1[1][1] >= seg2[0][1]:
            return [[seg1[0][0], max(seg1[0][1],seg2[0][1])], \
                    [seg1[0][0], min(seg1[1][1],seg2[1][1])]]
    # both segments horizontal
    elif seg1[0][1] == seg1[1][1] and seg2[0][1] == seg2[1][1]:
        if seg1[0][1] == seg2[0][1] and \
           seg1[0][0] <= seg2[1][0] and \
           seg1[1][0] >= seg2[0][0]:
            return [[max(seg1[0][0],seg2[0][0]), seg1[0][1]],
                    [min(seg1[1][0],seg2[1][0]), seg1[0][1]]]
            
    return None

def wire_intersections(wire1, wire2):
    '''Compare all segments from the wires for intersections, returning list'''
    intersections = []
    for w1seg in wire1.segments:
        for w2seg in wire2.segments:
            n = intersection(w1seg, w2seg)
            if n is not None and n != [0,0] and n != [[0,0],[0,0]]:
                if type(n[0]) == int:
                    intersections.append(n)
                else:
                    for x in range(n[0][0],n[1][0]+1):
                        for y in range(n[0][1],n[1][1]+1):
                            intersections.append([x,y])
    return intersections

def smallest_intersection_distance(intersections):
    '''Find the smallest Manhattan distance from [0,0] of all the intersections
    in the supplied list.'''
    distances = []
    for n in intersections:
        distances.append(abs(n[0])+abs(n[1]))
    return min(distances)

def smallest_intersection_distance_OLD(intersections):
    '''Find the smallest Manhattan distance from [0,0] of all the intersections
    in the supplied list.'''
    distances = []
    for n in intersections:
        if type(n[0]) == int:
            distances.append(abs(n[0])+abs(n[1]))
        elif n[0][0] == n[1][0]:
            # vertical
            # if both on same side of y-axis, get distance to closest end
            if n[0][1] * n[1][1] > 0:
                distances.append(abs(n[0][0]) + min(abs(n[0][1]),abs(n[1][1])))
            else:
                distances.append(abs(n[0][0]))
        elif n[0][1] == n[1][1]:
            # horizontal
            # if both on same side of x-axis, get distance to closest end
            if n[0][0] * n[1][0] > 0:
                distances.append(abs(n[0][1]) + min(abs(n[0][0]),abs(n[1][0])))
            else:
                distances.append(abs(n[0][1]))
        else:
            raise ValueError(f'unexpected intersection {n}')
    return min(distances)

def part1(path):
    wires = read_wires(path)
    purge_segments(wires[0], wires[1].min_x, wires[1].min_y, wires[1].max_x, wires[1].max_y)
    purge_segments(wires[1], wires[0].min_x, wires[0].min_y, wires[0].max_x, wires[0].max_y)
    intersections = wire_intersections(wires[0],wires[1])
    #DEBUG
    #print('intersections:')
    #sprint(intersections)
    return smallest_intersection_distance(intersections)

class Journey:
    def __init__(self, directions):
        self.loc = [0,0]
        self.directions = directions
        self.steps = 0
        
    def step(self):
        if self.directions and self.directions[0][1] == 0:
            del self.directions[0]
        if self.directions:
            if self.directions[0][0] == 'L':
                self.loc[0] -= 1
            elif self.directions[0][0] == 'R':
                self.loc[0] += 1
            elif self.directions[0][0] == 'U':
                self.loc[1] -= 1
            elif self.directions[0][0] == 'D':
                self.loc[1] += 1
            else:
                raise ValueError(f'unexpected direction {self.directions[0][0]}')
            self.steps += 1
            self.directions[0][1] -= 1

    
def read_journeys(path):
    '''Read the lines from the input path. Return a sequence of "journeys", 
    each "journey" representing a trip along a wire.'''
    journeys = []
    with open(path, 'r') as fobj:
        for line in fobj:
            journeys.append(str_to_journey(line.strip()))
    return journeys

def str_to_journey(s):
    '''Read a string of directions into a Journey object.'''
    directions = s.split(',')
    directions = [[d[0], int(d[1:])] for d in directions]
    return Journey(directions)


def part2(path):
    wires = read_wires(path)
    purge_segments(wires[0], wires[1].min_x, wires[1].min_y, wires[1].max_x, wires[1].max_y)
    purge_segments(wires[1], wires[0].min_x, wires[0].min_y, wires[0].max_x, wires[0].max_y)
    intersections = wire_intersections(wires[0],wires[1])
    wires = read_wires(path)
    journeys = read_journeys(path)
    j0_x_to_steps = {}
    j1_x_to_steps = {}
    intersections = set([tuple(n) for n in intersections])
    while journeys[0].directions:
        journeys[0].step()
        loc = tuple(journeys[0].loc)
        if loc in intersections and loc not in j0_x_to_steps:
            j0_x_to_steps[loc] = journeys[0].steps
    while journeys[1].directions:
        journeys[1].step()
        loc = tuple(journeys[1].loc)
        if loc in intersections and loc not in j1_x_to_steps:
            j1_x_to_steps[loc] = journeys[1].steps
    x_to_steps = []
    for n in intersections:
        x_to_steps.append(tuple([n, j0_x_to_steps[n] + j1_x_to_steps[n]]))
    x_to_steps.sort(key=lambda a: a[1])
    return x_to_steps[0][1]
    
    

if __name__ == '__main__':
    print(part1('day03/input.txt'))
    print(part2('day03/input.txt'))
    
