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

def process_script_list(path, deck_size):
    '''Apply all instructions in the file in the path to the supplied deck.
    Returns the deck shuffled by each instruction.'''
    deck = list(range(deck_size))
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


def process_script_psd(deck, lines):
    '''Apply all instructions in the file in the path to the supplied deck.
    Returns the deck shuffled by each instruction.'''
    for line in lines:
        line = line.split()
        if line[0] == 'cut':
            deck.cut(int(line[1]))
        elif line[:2] == ['deal','into']:
            deck.new_stack()
        elif line[:2] == ['deal','with']:
            deck.increment(int(line[3]))
        else:
            raise ValueError(f'invalid instruction {line}')
    return deck



class PrimeSizedDeck:
    '''A class to represent a deck of space cards. Works only if the number of
    space cards is prime.'''
    
    def __init__(self, size):
        '''Initialize the deck of space cards. Undefined behavior if size is
        not prime!'''
        self._size = size
        self._head = 0
        self._incr = 1
        #self._incr_to_hop_precalc = {1:1, size-1:size-1}
        
    @property
    def size(self):
        '''Return the size of the deck of space cards.'''
        return self._size
    
    @property
    def head(self):
        '''Return the value at the top of the deck of space cards.'''
        return self._head
    
    @property
    def incr(self):
        '''Return the increment magnitude of the deck of space cards.'''
        return self._incr

    @property
    def hop(self):
        '''Return the size of the hop. Based on the increment value, the hop
        will be the value s.t. increment*hop = 1 mod size. This is found by
        raising increment to (size-2), mod size.'''
        #if self._incr in self._incr_to_hop_precalc:
        #    return self._incr_to_hop_precalc[self._incr]
        #new_hop = (self._incr**(self._size-2))%self._size
        new_hop = pow(self._incr,self._size-2,self._size)
        #self._incr_to_hop_precalc[self._incr] = new_hop
        return new_hop
    
    def new_stack(self):
        '''Reverse the order of the cards in the deck.'''
        self._head = (self._head - self.hop) % self.size
        self._incr = (self._incr * (self._size-1)) % self.size
        
    def cut(self, n):
        '''Place the first n cards at the bottom of the deck.'''
        self._head = (self._head + (n*self.hop)) % self.size
        
    def increment(self, n):
        '''Shuffle the deck using the 'deal with increment N' method.
        Amplifies the value self._incr by n, which can be used to calculate
        the hop between values.'''
        self._incr = (self._incr * n) % self.size
        
    def __getitem__(self, key):
        '''Return card at position key.'''
        return (self._head + self.hop * key) % self._size
    
def part1(path, deck_size, card):
    deck = process_script_list(path, deck_size)
    return deck.index(card)

def part1_psd(path, deck_size, card):
    with open(path, 'r') as fobj:
        lines = fobj.readlines()
    deck = PrimeSizedDeck(deck_size)
    deck = process_script_psd(deck, lines)
    return [deck[i] for i in range(deck_size)].index(card)

def part2(path, size, iterations, pos):
    with open(path, 'r') as fobj:
        lines = fobj.readlines()
    deck = PrimeSizedDeck(size)
    deck = process_script_psd(deck, lines)
    # hop after n steps == ((hop after 1st step) ^ n) % size
    hop_n = pow(deck.hop, iterations, size)
    # head after n steps
    head_n = (1 - hop_n)%size
    head_n = (head_n * pow(1-deck.hop+size, size-2, size))%size
    head_n = (head_n*deck.head)%size
    # value at pos is head_n + hop_n * pos
    return (head_n + (hop_n*pos)%size)%size

if __name__ == '__main__':
    print(part1('day22/input.txt', 10007, 2019))
    print(part1_psd('day22/input.txt', 10007, 2019))
    print(part2('day22/input.txt', 119315717514047, 101741582076661, 2020))
    
