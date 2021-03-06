#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from common.serialutils import Deserializer
from common.serialtalks import SHORT
from daughter_cards.arduino import SecureArduino
import time

# Instructions
GET_RANGE1_OPCODE = 0x10
GET_RANGE2_OPCODE = 0x11
CHECK_ERROR_OPCODE = 0x12
GET_BOTH_RANGE_OPCODE = 0x13


class FakeSensorsIR:
    def __init__(self):
        pass

    def get_range1(self):
        return SensorsIR.ERROR_DIST

    def get_range2(self):
        return SensorsIR.ERROR_DIST

    def is_ready(self):
        return True

    def check_errors(self):
        return 0, 0

    def get_both_range(self):
        return SensorsIR.ERROR_DIST, SensorsIR.ERROR_DIST


class SensorsIR(SecureArduino):
    MIN_TIMESTEP = 0.05
    ERROR_DIST = 1000
    DEFAULT = {GET_RANGE1_OPCODE: Deserializer(SHORT(ERROR_DIST)),
               GET_RANGE2_OPCODE: Deserializer(SHORT(ERROR_DIST))}

    # Default execute result

    def __init__(self, parent, uuid='sensors'):
        SecureArduino.__init__(
            self, parent, uuid, default_result=self.DEFAULT)
        self.last_time = None
        self.last_both = (SensorsIR.ERROR_DIST, SensorsIR.ERROR_DIST)

    def get_range1(self):
        return self.get_both_range()[0]

    def get_range2(self):
        return self.get_both_range()[1]

    def is_ready(self):
        try:
            return self.is_connected
        except:
            return False

    def check_errors(self):
        deser = self.execute(CHECK_ERROR_OPCODE)
        error1 = deser.read(SHORT)
        error2 = deser.read(SHORT)
        return error1, error2

    def get_both_range(self):
        current_time = time.time()
        if self.last_time is not None and current_time - self.last_time < SensorsIR.MIN_TIMESTEP:
            return self.last_both

        deser = self.execute(GET_BOTH_RANGE_OPCODE)

        try:
            dist1 = deser.read(SHORT)
        except AttributeError:
            dist1 = SensorsIR.ERROR_DIST
        try:
            dist2 = deser.read(SHORT)
        except AttributeError:
            dist2 = SensorsIR.ERROR_DIST

        if dist1 <= 0:
            dist1 = SensorsIR.ERROR_DIST
        if dist2 <= 0:
            dist2 = SensorsIR.ERROR_DIST

        self.last_both = (dist1, dist2)
        self.last_time = time.time()
        return self.last_both
