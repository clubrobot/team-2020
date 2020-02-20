#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event
from collections import namedtuple
from time import sleep
from math import hypot

from common.sync_flag_signal import Signal

Positions = namedtuple('Positions', ['brother', 'opponentA', 'oppenentB'])


class Positions:
    def __init__(self, brother=(-1000, -1000), opponentA=(-1000, -1000), oppenentB=(-1000, -1000)):
        self.brother = brother
        self.opponentA = opponentA
        self.oppenentB = oppenentB

class PositionListener(Thread):
    def __init__(self, brother_getter, opponents_getter, timestep=0.1, threshold=10):
        Thread.__init__(self)

        # Signals for each robots
        self.bro_signal = Signal()
        self.oppA_signal = Signal()
        self.oppB_signal = Signal()

        # Brother and opponents getter
        self.bro_getter = brother_getter
        self.opp_getter = opponents_getter

        # Timestep
        self.timestep = timestep

        # Stopping event
        self.stop = Event()

        # Position threshold
        self.threshold = threshold

        # Position error
        self.error = 0
        self.positions = Positions()   # Brother # opponentA #oppenentB

        # Atomatically start
        self.start()

    def _handle_brother_pos(self):
        bro_x, bro_y = self.bro_getter()

        if (hypot(bro_y - self.positions.brother[1], bro_x - self.positions.brother[0]) + self.error) > self.threshold:
            self.bro_signal.ping()

            self.error = 0
        else:
            self.error += hypot(bro_y - self.self.positions.brother[1], bro_x - self.self.positions.brother[0])

        return (bro_x, bro_y)

    def _handle_opponentA_pos(self):
        oppA_x, oppA_y = self.opp_getter()[0]

        if (hypot(oppA_y - self.positions.opponentA[1], oppA_x - self.positions.opponentA[0]) + self.error) > self.threshold:
            self.oppA_signal.ping()

            self.error = 0
        else:
            self.error += hypot(oppA_y - self.self.positions.opponentA[1], oppA_x - self.self.positions.opponentA[0])

        return (oppA_x, oppA_y)

    def _handle_opponentB_pos(self):
        oppB_x, oppB_y = self.opp_getter()[1]

        if (hypot(oppB_y - self.positions.oppenentB[1], oppB_x - self.positions.oppenentB[0]) + self.error) > self.threshold:
            self.oppB_signal.ping()

            self.error = 0
        else:
            self.error += hypot(oppB_y - self.self.positions.oppenentB[1], oppB_x - self.self.positions.oppenentB[0])

        return (oppB_x, oppB_y)

    def run(self):
        while not self.stop.is_set():
            sleep(self.timestep)

            # handle brother pos
            self.positions.brother = self._handle_brother_pos()

            # handle opponentA pos
            self.positions.opponentA = self._handle_opponentA_pos()

            # handle opponentB pos
            self.positions.opponentB = self._handle_opponentB_pos()
