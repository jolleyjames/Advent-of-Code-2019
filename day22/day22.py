#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, Day 22.

@author: James Jolley, james@jolley.co
"""

def new_stack(deck):
    '''Reverse the order of the cards in the deck. Returns the newly reversed
    deck of cards.'''
    deck.reverse()
    return deck

def cut(deck, n):
    '''Return the deck with the first n cards placed at the bottom.'''
    return deck[n:] + deck[:n]

def increment(deck, n):
    '''Return the deck shuffled using the 'deal with increment N' method. This
    will only work correctly if n is coprime with len(deck).'''
    new_deck = [None]*len(deck)
    for i in range(len(deck)):
        new_deck[(i*n)%len(deck)] = deck[i]
    return new_deck

def process_script(path, deck):
    '''Apply all instructions in the file in the path to the supplied deck.
    Returns the deck shuffled by each instruction.'''
    with open(path, 'r') as fobj:
        lines = fobj.readlines()
    for line in lines:
        line = line.split()
        if line[0] == 'cut':
            deck = cut(deck, int(line[1]))
        elif line[:2] == ['deal','into']:
            deck = new_stack(deck)
        elif line[:2] == ['deal','with']:
            deck = increment(deck, int(line[3]))
        else:
            raise ValueError(f'invalid instruction {line}')
    return deck

def part1(path, deck_size, card):
    deck = list(range(deck_size))
    deck = process_script(path, deck)
    return deck.index(card)

if __name__ == '__main__':
    print(part1('day22/input.txt', 10007, 2019))
    