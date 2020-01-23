#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advent of Code 2019, Day 23.

@author: James Jolley, james@jolley.co
"""

from day05.day05 import Computer, read_program
from collections import deque

class Nic:
    '''The Network Interface Controller.'''
    
    def __init__(self, path, addr):
        '''Creates a new Network Interface Controller using the Intcode program
        at the specified path and the specified address.'''
        self._comp = Computer(read_program(path))
        self._addr = addr
        self._comp.in_.append(addr)
        self.run()
        
    @property
    def addr(self):
        '''Property for addr value of this Network Interface Controller.'''
        return self._addr
    
    @property
    def comp(self):
        '''The underlying Intcode computer of this Network Interface
        Controller.'''
        return self._comp
    
    @property
    def out(self):
        '''The output queue of this Network Interface Controller.'''
        return self.comp.out
    
    @property
    def in_(self):
        '''The input queue of this Network Interface Controller.'''
        return self.comp.in_
    
    @property
    def waiting(self):
        '''Returns True if this Network Interface Controller is waiting for
        input to continue. False otherwise.'''
        return self.comp.ram[self.comp.ip] == 3 and not self.in_
    
    def run(self):
        '''Process the input. Runs until the program halts or until the Network
        Interface Controller waits for more input.'''
        while self.comp.ram[self.comp.ip] != 99 and not self.waiting:
            self.comp.step()
            
class Hub:
    '''A networked hub of Network Interface Controllers.'''
    
    def __init__(self, path, addrs):
        '''Creates a new hub of new Network Interface Controllers using the
        Intcode program at the specified path and the addresses in the 
        supplied iterable.'''
        self._addrs = tuple(addrs)
        self._nics = {}
        for addr in self.addrs:
            self._nics[addr] = Nic(path, addr)
        self._nic_index = 0
        self._queue = {}
        
    @property
    def addrs(self):
        '''Returns the tuple of addresses of the Network Interface Controllers
        in this hub.'''
        return self._addrs
    
    @property
    def nics(self):
        '''Returns the address-keyed Network Interface Controllers in this
        hub.'''
        return self._nics
    
    @property
    def queue(self):
        '''Returns queues of values waiting to be input into the Network
        Interface Controllers in this hub.'''
        return self._queue
    
    @property
    def idle(self):
        '''Returns True if all computers are waiting for input, AND there is
        a packet at address 255.'''
        if 255 not in self.queue:
            return False
        for pktq in [v for k,v in self.queue.items() if k != 255]:
            if pktq:
                return False
        return True
    
    def run_next_nic(self):
        '''Get the input for the next Network Interface Controller. Apply that
        input and run it until it waits for additional input. Take the output
        and apply it to the queue.'''
        if self.idle:
            if 0 not in self.queue:
                self.queue[0] = deque()
            self.queue[0].extend(self.queue[255])
            self.queue[255].clear()
        addr = self.addrs[self._nic_index]
        nic = self.nics[addr]
        if addr not in self.queue:
            self._queue[addr] = deque()
        queue = self.queue[addr]
        if queue:
            in_ = (queue.popleft(), queue.popleft())
        else:
            in_ = (-1,)
        nic.in_.extend(in_)
        nic.run()
        while nic.out:
            addr = nic.out.popleft()
            x = nic.out.popleft()
            y = nic.out.popleft()
            if addr == 255:
                self.queue[255] = deque((x,y))
            else:
                if addr not in self.queue:
                    self.queue[addr] = deque()
                queue = self.queue[addr]
                queue.extend((x,y))
        self._nic_index += 1
        self._nic_index %= len(self._addrs)
        
def part1(path, size):
    hub = Hub(path, range(size))
    while 255 not in hub.queue:
        hub.run_next_nic()
    return hub.queue[255][1]

def part2(path, size):
    hub = Hub(path, range(size))
    last_y_to_0 = None
    while True:
        while not hub.idle:
            hub.run_next_nic()
        if hub.queue[255][1] == last_y_to_0:
            return last_y_to_0
        else:
            last_y_to_0 = hub.queue[255][1]
            hub.run_next_nic()
    

if __name__ == '__main__':
    print(part1('day23/input.txt', 50))
    print(part2('day23/input.txt', 50))
    