#!/usr/bin/python3
# -*- coding: utf-8 -*-
from time import sleep
from math import pi

from behaviours.action.action import *
from logs.log_manager import *
from daughter_cards.cupcollector import *

class PutCup(Action):
    BLUE_SIDE       = 0
    YELLO_SIDE      = 1
    UNDEFINED_SIDE  = -1

    def __init__(self, geo, side):

        self.logger = LogManager().getlogger(self.__class__.__name__, Logger.SHOW, INFO)

        self.side = side
        self.actionpoint = geo.get('Put'+str(self.side))
        if(self.side == self.BLUE_SIDE):
            self.orientation = pi/2
        else:
            self.orientation = -pi/2

        self.actionpoint_precision = 1

        self.red = geo.get('Red1')
        self.green = geo.get('Green1')

    def procedure(self, robot):
        self.logger(INFO, 'Action is launch on', robot.__class__.__name__)
        self.logger(INFO, 'Put Cup')

        robot.wheeledbase.turnonthespot(pi)
        robot.wheeledbase.wait()

        robot.wheeledbase.goto(*self.red)

        if robot.cup_collector.get_color(GRIPPER_FRONT_LEFT) == 'red':
            robot.cup_collector.put(GRIPPER_FRONT_LEFT)
        if robot.cup_collector.get_color(GRIPPER_FRONT_CENTER) == 'red':
            robot.cup_collector.put(GRIPPER_FRONT_CENTER)
        if robot.cup_collector.get_color(GRIPPER_FRONT_RIGHT) == 'red':
            robot.cup_collector.put(GRIPPER_FRONT_RIGHT)

        robot.wheeledbase.goto(*self.green)

        if robot.cup_collector.get_color(GRIPPER_BACK_LEFT) == 'green':
            robot.cup_collector.put(GRIPPER_BACK_LEFT)
        if robot.cup_collector.get_color(GRIPPER_BACK_CENTER) == 'green':
            robot.cup_collector.put(GRIPPER_BACK_CENTER)
        if robot.cup_collector.get_color(GRIPPER_BACK_RIGHT) == 'green':
            robot.cup_collector.put(GRIPPER_BACK_RIGHT)
