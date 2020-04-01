#!/usr/bin/python3
# -*- coding: utf-8 -*-
from logs.log_manager import *
from common.strategy import Strategy
from robots.bornibus.actions.take_cup_action import TakeCup
from robots.bornibus.actions.put_cup_action import PutCup

class BornibusStrategy(Strategy):
    STRATEGY_1 = 0
    STRATEGY_2 = 1
    def __init__(self, geogebra, strategy = STRATEGY_1, exec_param=Logger.SHOW, log_level=INFO):
        Strategy.__init__(self, geogebra, strategy, exec_param, log_level)
        # Init actions
        take1 = TakeCup(geogebra, 1)
        take2 = TakeCup(geogebra, 2)
        put1  = PutCup(geogebra, 1)

        # Init Stragtegy
        if strategy == self.STRATEGY_1:

            self.automate = [
                take1,
                take2,
                put1,
                ]

        elif strategy == self.STRATEGY_2:
            pass