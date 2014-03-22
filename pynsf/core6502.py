#!/usr/bin/env python

import math
from pynes.corestatus import CoreStatus
from pynes.stack import Stack


class Core6502(object):
    
    def __init__(self):
        self._acc = 0;
        self.x = 0;
        self.y = 0;
        self.status = CoreStatus()
        self.pc = 0
        self.stack = Stack()
        self.memory = []

    @property
    def acc(self):
        return self._acc

    @acc.setter
    def acc(self, value):
        self._acc = set_status_from_value(value, self._acc)

    
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


