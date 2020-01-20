#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit Tests for Advent of Code 2019, Day 22.

@author: James Jolley, james@jolley.co
"""

import day22.day22 as d
import unittest

class TestDay22(unittest.TestCase):
    
    def test_new_stack(self):
        deck = [2**i for i in range(5)]
        self.assertEqual(d.new_stack(deck), [16, 8, 4, 2, 1])
        
    def test_cut(self):
        deck = list(range(10))
        self.assertEqual(d.cut(deck,3), [3,4,5,6,7,8,9,0,1,2])
        deck = list(range(10))
        self.assertEqual(d.cut(deck,-4), [6,7,8,9,0,1,2,3,4,5])
        
    def test_increment(self):
        deck = list(range(10))
        self.assertEqual(d.increment(deck,3), [0,7,4,1,8,5,2,9,6,3])
        
    def test_process_script_list(self):
        deck = d.process_script_list('day22/test1.txt', 10)
        self.assertEqual(deck, [0,3,6,9,2,5,8,1,4,7])
        deck = d.process_script_list('day22/test2.txt', 10)
        self.assertEqual(deck, [3,0,7,4,1,8,5,2,9,6])
        deck = d.process_script_list('day22/test3.txt', 10)
        self.assertEqual(deck, [6,3,0,7,4,1,8,5,2,9])
        deck = d.process_script_list('day22/test4.txt', 10)
        self.assertEqual(deck, [9,2,5,8,1,4,7,0,3,6])
        
    def test_PSD_new_stack(self):
        deck = d.PrimeSizedDeck(11)
        deck.new_stack()
        self.assertEqual([deck[i] for i in range(11)], list(range(10,-1,-1)))
        
    def test_PSD_cut(self):
        deck = d.PrimeSizedDeck(11)
        deck.cut(3)
        self.assertEqual([deck[i] for i in range(11)], [3,4,5,6,7,8,9,10,0,1,2])
        deck = d.PrimeSizedDeck(11)
        deck.cut(-4)
        self.assertEqual([deck[i] for i in range(11)], [7,8,9,10,0,1,2,3,4,5,6])
        
    def test_PSD_increment(self):
        deck = d.PrimeSizedDeck(11)
        deck.increment(3)
        self.assertEqual([deck[i] for i in range(11)], [0,4,8,1,5,9,2,6,10,3,7])
        
    def test_process_script_psd(self):
        deck = d.PrimeSizedDeck(11)
        with open('day22/test1.txt') as fobj:
            lines = fobj.readlines()
        deck = d.process_script_psd(deck, lines)
        self.assertEqual([deck[i] for i in range(11)], [0, 8, 5, 2, 10, 7, 4, 1, 9, 6, 3])
        deck = d.PrimeSizedDeck(11)
        with open('day22/test2.txt') as fobj:
            lines = fobj.readlines()
        deck = d.process_script_psd(deck, lines)
        self.assertEqual([deck[i] for i in range(11)], [9, 1, 4, 7, 10, 2, 5, 8, 0, 3, 6])
        deck = d.PrimeSizedDeck(11)
        with open('day22/test3.txt') as fobj:
            lines = fobj.readlines()
        deck = d.process_script_psd(deck, lines)
        self.assertEqual([deck[i] for i in range(11)], [8, 4, 0, 7, 3, 10, 6, 2, 9, 5, 1])
        deck = d.PrimeSizedDeck(11)
        with open('day22/test4.txt') as fobj:
            lines = fobj.readlines()
        deck = d.process_script_psd(deck, lines)
        self.assertEqual([deck[i] for i in range(11)], [1, 8, 4, 0, 7, 3, 10, 6, 2, 9, 5])
        

if __name__ == '__main__':
    unittest.main()
    