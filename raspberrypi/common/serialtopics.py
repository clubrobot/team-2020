#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This library is free software from Club robot Insa Rennes sources; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.
"""

from common.serialtalks import *
from collections import namedtuple

SubscriptionContext = namedtuple('SubscriptionContext', ['timestep', 'state'])

MANAGE_OPCODE = 0X07

TOPIC_MAX_OPCODE = 0X05

TOPIC_1_OPCODE = 0X00
TOPIC_2_OPCODE = 0X01
TOPIC_3_OPCODE = 0X02
TOPIC_4_OPCODE = 0X03
TOPIC_5_OPCODE = 0X04

TOPIC_DEFAULT_TIMESTEP = 100  # ms


class Topic:
    def __init__(self, id, timestep=TOPIC_DEFAULT_TIMESTEP):
        self.id = id
        self.timestep = timestep

    def _handler(self, args):
        raise NotImplementedError("Not implemented")

    def getRessource(self, args):
        raise NotImplementedError("Not implemented")

    def getID(self):
        return self.id

    def getTimestep(self):
        return self.timestep

    def getHandler(self):
        return self._handler


class SerialTopics:
    SUBSCRIBE = 0X0
    UNSUBSCRIBE = 0X1

    def __init__(self, parent):
        self.parent = parent

    def subscribe(self, topic):
        output = self.parent.execute(
            MANAGE_OPCODE, BYTE(self.SUBSCRIBE), BYTE(topic.getID()), LONG(topic.getTimestep()))

        return bool(output.read(BYTE))

    def unsubscribe(self, topic):
        output = self.parent.execute(
            MANAGE_OPCODE, BYTE(self.UNSUBSCRIBE), BYTE(topic.getID()))

        return bool(output.read(BYTE))

    def add(self, topic):
        if(topic.getID() < TOPIC_MAX_OPCODE):
            self.parent.bind(topic.getID(), topic.getHandler())
