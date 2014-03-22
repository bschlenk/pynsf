#!/usr/bin/env python

import math
from pynes.corestatus import CoreStatus
from pynes.stack import Stack
from pynes.instructions import instruction_map


class Core6502(object):
    
    def __init__(self):
        self._acc = 0;
        self._x = 0;
        self._y = 0;
        self.status = CoreStatus()
        self.pc = 0
        self.stack = Stack()
        self.memory = []

    def load(self, nes_file):
        with open(nes_file) as f:
            data = f.read()
        
        # the first 16 bytes are the NES file header - ignore it for now
        data = data[16:]
        self.__init__()
        self.memory_str = data
        self.memory = [ord(d) for d in data]


    def run(self):
        while True:
            inst = instruction_map[self.memory[self.pc]](self)
            inst()
            if not inst.is_branch:
                self.pc += inst.num_bytes


    @property
    def acc(self):
        return self._acc


    @acc.setter
    def acc(self, value):
        self._acc = value
        self.update_zero_neg(value)


    @property
    def x(self):
        return self._x


    @x.setter
    def x(self, value):
        self._x = value
        self.update_zero_neg(value)


    @property
    def y(self):
        return self._y


    @y.setter
    def y(self, value):
        self._y = value
        self.update_zero_neg(value)

    
    def update_zero_neg(self, value):
        self.status.z = not value
        self.status.n = bool((value >> 6) & 0x01)


    def add(self, arg1, arg2, update_overflow=True):
        val = arg1 + arg2 + int(self.status.c)
        if update_overflow:
            self.status.v = val > 127
        if val > 255:
            val -= 255
            self.status.c = True
        else:
            self.status.c = False
        return val


    def sub(self, arg1, arg2, update_overflow=True):
        val = arg1 - arg2 - int(not self.status.c)
        if update_overflow:
            self.status.v = val < -128
        if val < 0:
            val += 255
            self.status.c = False
        else:
            self.status.c = True
        return val

    
    def set_status_from_value(self, valNew, valOrig, update_overflow=True):
        max_num = 0xFF
        self.status.s = False

        # subtraction performed
        if valNew < valOrig:
            if valNew < 0: # borrow required
                self.status.c = False
                self.status.s = True
                valNew += max_num
            else:
                self.status.c = True
        else:
            if valNew > max_num: # overflow occurred
                valNew = valNew - max_num
                self.status.c = True
                if update_overflow:
                    self.status.v = True
            else:
                self.status.c = False
                if update_overflow:
                    self.status.v = False

        self.status.z = not value
        return valNew


if __name__ == '__main__':
    import sys
    core = Core6502()
    core.load(sys.argv[1])
    core.run()
