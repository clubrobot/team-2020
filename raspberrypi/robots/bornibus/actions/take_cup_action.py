#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep
from math import pi

from behaviours.action.action import *
from logs.log_manager import *
from daughter_cards.cupcollector import *

class TakeCup(Action):
    def __init__(self, geo, idx):

        self.logger = LogManager().getlogger(self.__class__.__name__, Logger.SHOW, INFO)

        self.idx = idx
        self.actionpoint = geo.get('Cup'+str(self.idx))
        self.orientation = None
        self.actionpoint_precision = 10

    def procedure(self, robot):
        self.logger(INFO, 'Action is launch on', robot.__class__.__name__)
        self.logger(INFO, 'Taking Cup number ', self.idx)

        if self.idx == 1:
            robot.wheeledbase.turnonthespot(pi)
        if self.idx == 2:
            robot.wheeledbase.turnonthespot(0)

        robot.wheeledbase.wait()
        x = self.actionpoint[0] - 145
        y = self.actionpoint[1]
        robot.wheeledbase.goto(x,y)
        if self.idx == 1:
            robot.cup_collector.get(GRIPPER_FRONT_LEFT)
            robot.cup_collector.get(GRIPPER_FRONT_CENTER)
            robot.cup_collector.get(GRIPPER_FRONT_RIGHT)
        if self.idx == 2:
            robot.cup_collector.get(GRIPPER_BACK_RIGHT)
            robot.cup_collector.get(GRIPPER_BACK_CENTER)

        if self.idx == 1:
            robot.wheeledbase.goto(*self.actionpoint)
            robot.wheeledbase.turnonthespot(-pi/2)

            robot.wheeledbase.wait()

