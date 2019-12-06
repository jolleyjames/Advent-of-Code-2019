#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  3 18:45:17 2019

@author: jim
"""

import unittest
import day03.day03 as d

class TestDay03(unittest.TestCase):
    
    def test_str_to_wire(self):
        s = 'R8,U5,L5,D3'
        wire = d.str_to_wire(s)
        exp_seg = [[[0,0],[8,0]],[[8,0],[8,-5]],[[8,-5],[3,-5]],[[3,-5],[3,-2]]]
        exp_seg = [sorted(seg) for seg in exp_seg]
        self.assertCountEqual(wire.segments, exp_seg)
        self.assertEqual(wire.min_x, 0)
        self.assertEqual(wire.max_x, 8)
        self.assertEqual(wire.min_y, -5)
        self.assertEqual(wire.max_y, 0)
        
    def test_purge_segments(self):
        wires = d.read_wires('day03/test1.txt')
        d.purge_segments(wires[0], wires[1].min_x, wires[1].min_y, wires[1].max_x, wires[1].max_y)
        # the segment from [8,0], [8,-5] should be purged
        exp_seg = [[[0,0],[8,0]],[[3,-5],[8,-5]],[[3,-5],[3,-2]]]
        self.assertCountEqual(wires[0].segments, exp_seg)
        
        d.purge_segments(wires[1], wires[0].min_x, wires[0].min_y, wires[0].max_x, wires[0].max_y)
        # the segment from [0,-7], [6,-7] should be purged
        exp_seg = [[[0,-7],[0,0]],[[6,-7],[6,-3]],[[2,-3],[6,-3]]]
        self.assertCountEqual(wires[1].segments, exp_seg)
        
    def test_intersection(self):
        # s1 horz, s2 vert
        s1 = [[-4,-3],[4,-3]]
        s2 = [[-1,-5],[-1,7]]
        self.assertEqual(d.intersection(s1,s2), [-1,-3])
        s2 = [[-10,-6],[-10,-4]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[0,-6],[0,-4]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[10,-6],[10,-4]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[-10,-4],[-10,4]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[10,-4],[10,4]]
        self.assertIsNone(d.intersection(s1,s2))        
        s2 = [[-10,-1],[-10,7]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[0,-1],[0,7]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[10,-1],[10,7]]
        self.assertIsNone(d.intersection(s1,s2))
        # s1 vert, s2 horz
        s1 = [[-1,-5],[-1,7]]
        s2 = [[-4,-3],[4,-3]]
        self.assertEqual(d.intersection(s1,s2), [-1,-3])
        s2 = [[-10,-9],[-4,-9]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[-4,-9],[4,-9]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[4,-9],[10,-9]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[-10,2],[-4,2]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[4,2],[10,2]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[-10,12],[-4,12]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[-4,12],[4,12]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[4,12],[10,12]]
        self.assertIsNone(d.intersection(s1,s2))
        # s1, s2 vert
        s1 = [[0,-5],[0,5]]
        s2 = [[0,-2],[0,4]]
        self.assertEqual(d.intersection(s1,s2),[[0,-2],[0,4]])
        s2 = [[0,-10],[0,10]]
        self.assertEqual(d.intersection(s1,s2),[[0,-5],[0,5]])
        s2 = [[0,-10],[0,1]]
        self.assertEqual(d.intersection(s1,s2),[[0,-5],[0,1]])
        s2 = [[0,-1],[0,10]]
        self.assertEqual(d.intersection(s1,s2),[[0,-1],[0,5]])
        s2 = [[0,-100],[0,-7]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[0,7],[0,100]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[1,-5],[1,5]]
        self.assertIsNone(d.intersection(s1,s2))
        # s1, s2 horz
        s1 = [[3,-8],[8,-8]]
        s2 = [[4,-8],[6,-8]]
        self.assertEqual(d.intersection(s1,s2),[[4,-8],[6,-8]])
        s2 = [[-20,-8],[800,-8]]
        self.assertEqual(d.intersection(s1,s2),[[3,-8],[8,-8]])
        s2 = [[-3,-8],[5,-8]]
        self.assertEqual(d.intersection(s1,s2),[[3,-8],[5,-8]])
        s2 = [[4,-8],[9000,-8]]
        self.assertEqual(d.intersection(s1,s2),[[4,-8],[8,-8]])
        s2 = [[-10,-8],[-1,-8]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[9,-8],[29,-8]]
        self.assertIsNone(d.intersection(s1,s2))
        s2 = [[3,8],[8,8]]
        self.assertIsNone(d.intersection(s1,s2))
        
    def test_wire_intersections(self):
        wires = d.read_wires('day03/test1.txt')
        d.purge_segments(wires[0], wires[1].min_x, wires[1].min_y, wires[1].max_x, wires[1].max_y)
        d.purge_segments(wires[1], wires[0].min_x, wires[0].min_y, wires[0].max_x, wires[0].max_y)
        intersections = d.wire_intersections(wires[0],wires[1])
        exp_intersections = [[3,-3],[6,-5]]
        self.assertCountEqual(intersections, exp_intersections)
        
    def test_smallest_intersection_distance(self):
        wires = d.read_wires('day03/test1.txt')
        d.purge_segments(wires[0], wires[1].min_x, wires[1].min_y, wires[1].max_x, wires[1].max_y)
        d.purge_segments(wires[1], wires[0].min_x, wires[0].min_y, wires[0].max_x, wires[0].max_y)
        intersections = d.wire_intersections(wires[0],wires[1])
        self.assertEqual(d.smallest_intersection_distance(intersections),6)
        wires = d.read_wires('day03/test2.txt')
        d.purge_segments(wires[0], wires[1].min_x, wires[1].min_y, wires[1].max_x, wires[1].max_y)
        d.purge_segments(wires[1], wires[0].min_x, wires[0].min_y, wires[0].max_x, wires[0].max_y)
        intersections = d.wire_intersections(wires[0],wires[1])
        self.assertEqual(d.smallest_intersection_distance(intersections),159)
        wires = d.read_wires('day03/test3.txt')
        d.purge_segments(wires[0], wires[1].min_x, wires[1].min_y, wires[1].max_x, wires[1].max_y)
        d.purge_segments(wires[1], wires[0].min_x, wires[0].min_y, wires[0].max_x, wires[0].max_y)
        intersections = d.wire_intersections(wires[0],wires[1])
        self.assertEqual(d.smallest_intersection_distance(intersections),135)
        
    def test_part2(self):
        self.assertEqual(d.part2('day03/test1.txt'), 30)
        self.assertEqual(d.part2('day03/test2.txt'), 610)
        self.assertEqual(d.part2('day03/test3.txt'), 410)


if __name__ == '__main__':
    unittest.main()