#!/usr/bin/python3
# -*- coding: utf-8 -*-

from robots.bornibus.setup_bornibus import *
from behaviours.robot_behaviour import RobotBehavior
import traceback


COLOR = RobotBehavior.BLUE_SIDE
PREPARATION = False


class Bornibus(RobotBehavior):
    def __init__(self, manager, *args, timelimit=None, **kwargs):
        RobotBehavior.__init__(self, manager, *args, timelimit=timelimit, **kwargs)

        self.automate = list()

        self.automatestep = 0

    def make_decision(self):
        if(self.automatestep < len(self.automate)):
            action = self.automate[self.automatestep]
        else:
            return None, (self,), {}, (None, None)
            self.stop_event.set()

        return action.procedure, (self,), {}, (action.actionpoint + (action.orientation,), (action.actionpoint_precision, None))

    def goto_procedure(self, destination, thresholds=(None, None)):
        self.automatestep += 1
        sleep(1)
        return True

    def set_side(self, side):
        pass

    def set_position(self):
        pass

    def positioning(self):
        pass


if __name__ == '__main__':
    if PREPARATION:
        Bornibus().start_preparation()
    else:
        robot = Bornibus(manager)
        robot.set_side(COLOR)
        init_robot()
        robot.set_position()
        input()
        robot.start()
