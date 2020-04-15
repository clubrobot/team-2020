#!/usr/bin/python3
# -*- coding: utf-8 -*-

from robots.bornibus.setup_bornibus import *
from behaviours.robot_behaviour import RobotBehavior
from behaviours.avoidance_behaviour import AviodanceBehaviour
from robots.bornibus.strategy import BornibusStrategy

from math import pi
COLOR = RobotBehavior.YELLO_SIDE
PREPARATION = False

class Bornibus(RobotBehavior):
    def __init__(self, *args, timelimit=None, **kwargs):
        RobotBehavior.__init__(self, manager, *args, timelimit=timelimit, **kwargs)

        self.avoidance_behaviour = AviodanceBehaviour(wheeledbase, roadmap, robot_beacon)

        self.strategy = BornibusStrategy(geogebra)

        self.automate = self.strategy.get_automate()

        self.wheeledbase = wheeledbase
        self.cup_collector = cup_collector

        self.automatestep = 0

    def make_decision(self):
        if(self.automatestep < len(self.automate)):
            action = self.automate[self.automatestep]
        else:
            self.stop_event.set()
            return None, (self,), {}, (None, None)

        return action.procedure, (self,), {}, (action.actionpoint + (action.orientation,), (action.actionpoint_precision, None))

    def goto_procedure(self, destination, thresholds=(None, None)):
        if self.avoidance_behaviour.move(destination, thresholds):
            self.automatestep += 1
            return True
        else:
            return False

    def set_side(self, side):
        pass

    def set_position(self):
        self.wheeledbase.set_position(*geogebra.get('StartYellow'), -pi/2)

    def positioning(self):
        pass

    def stop_procedure(self):
        self.wheeledbase.stop()

if __name__ == '__main__':
    if PREPARATION:
        Bornibus().start_preparation()
    else:
        robot = Bornibus(timelimit=100)
        robot.set_side(COLOR)
        init_robot()
        robot.set_position()
        input()
        robot.start()
