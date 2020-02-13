#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import sys

from beacons.global_sync import *

_BEACON_PORT = 25568


class SupervisorServer(ServerGS):
    def __init__(self):
        ServerGS.__init__(self)
        self.logger = LogManager().getlogger("Server", Logger.SHOW, level_disp=INFO)
        self.logger(INFO, "Server succefully initialised")

        self.ihm = None          # TODO : Handle IHM here
        self.tracking = None     # TODO : Handle tracking here


    def get_opponents_pos(self):
        return [(-1000, -1000),(-1000, -1000)]
