#!/usr/bin/python3
# -*- coding: utf-8 -*-

from robots.bornibus.setup_bornibus import *
from common.automaton import Automaton
from managers.sensors_manager import *
import traceback
from managers.wheeledbase_manager import PositionUnreachable


COLOR = Automaton.YELLOW
COLOR = Automaton.PURPLE
PREPARATION = False


class Bornibus(Automaton):

    def __init__(self):
        Automaton.__init__(self)
        pass

    def set_side(self, side):
        pass

    def set_position(self):
        pass

    def positioning(self):
        pass

    def stop_match(self):
        pass

    def run(self):
        pass


if __name__ == '__main__':
    if PREPARATION:
        Bornibus().start_preparation()
    else:
        auto = Bornibus()
        auto.set_side(COLOR)
        init_robot()
        auto.set_position()
        print("ready")
        input()
        auto.run()
