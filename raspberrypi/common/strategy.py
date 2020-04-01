#!/usr/bin/env python3
#-*- coding: utf-8 -*-

from time import monotonic, sleep

from logs.log_manager import *

class Action:
    """
        The purpose of this class is to define action object body
    """
    def procedure(self, robot):
        """
            The procedure method give the robot comportement to successfully acheive this action
        """
        raise RuntimeError("The 'procedure' method must be overriden")


class Strategy:
    """
        The purpose of this class is to define strategy object body.
        In this class, you can initialise all actions
    """
    def __init__(self, geogebra, strategy = None, exec_param=Logger.SHOW, log_level=INFO):
        # Init Logger
        self.logger = LogManager().getlogger(self.__class__.__name__, exec_param, log_level)

        self.automate = list()

    def get_automate(self):
        """
        This method return the selected automate required by strategy
        """
        if not self.automate:
            self.logger(WARNING, "Current automate is empty ")
        else:
            i = 0
            display_dict = dict()
            for action in self.automate:
                display_dict.update({str(i) + ' - ' +  action.__class__.__name__ : action.actionpoint})
                i += 1
            self.logger(INFO, "Current automate contain : ", **display_dict)
        return self.automate


if __name__ == "__main__":

    from math import pi

    class TakeCup(Action):
        def __init__(self, side):
            self.side = side
            self.action_point = (555, 666)# geogebra.get('Point name')
            self.orientation = pi
            self.actionpoint_precision = 10

        def procedure(self, robot):
            print(robot)


    take = TakeCup(0)

    print(take.side)
    print(take.action_point)
    print(take.orientation)