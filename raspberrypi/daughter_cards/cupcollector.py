#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import time
import math
from common.serialutils import Deserializer
from common.serialtalks import BYTE, INT, LONG, FLOAT, STRING
from daughter_cards.arduino import Arduino

# Instructions
_GET_CUP_OPCODE   = 0x10
_PUT_CUP_OPCODE   = 0x20
_GET_COLOR_CUP_OPCODE   = 0x30

GRIPPER_FRONT_LEFT = 1
GRIPPER_FRONT_CENTER = 2
GRIPPER_FRONT_RIGHT = 3

GRIPPER_BACK_LEFT = 4
GRIPPER_BACK_CENTER = 5
GRIPPER_BACK_RIGHT = 6

class CupCollector(Arduino):

    def __init__(self, parent, uuid='cupcollector'):
        Arduino.__init__(self, parent, uuid)

    def get(self, gripper_id):
        self.send(_GET_CUP_OPCODE, INT(gripper_id))

    def put(self, gripper_id):
        self.send(_PUT_CUP_OPCODE, INT(gripper_id))

    def get_color(self, gripper_id):
        ret = self.execute(_GET_COLOR_CUP_OPCODE, INT(gripper_id))

        return ret.read(STRING)
