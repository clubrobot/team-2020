#!/usr/bin/python3
# -*- coding: utf-8 -*-

from common.serialtopics import *


class CounterTopic(Topic):
    TIMESTEP = 500
    OPCODE = TOPIC_2_OPCODE

    def __init__(self):
        Topic.__init__(self, self.OPCODE, self.TIMESTEP)
        self.ressource = 0

    def _handler(self, args):
        self.ressource = args.read(INT)

    def getRessource(self):
        return self.ressource
