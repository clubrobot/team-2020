#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
import sys

from beacons.global_sync import *

_BEACON_PORT = 25568

try:
    from tracking.libs.manager import *
    from tracking.libs.utils import *
    from tracking.libs.markers import *

    _CENTRAL_MARKER_ID          = 42
    _CENTRAL_MARKER_SIZE        = 0.10 # meters
    _CENTRAL_MARKER_COORDINATES = Point(0.125, 0.150, 0.0) # (x, y, z) meters
    _CENTRAL_MARKER_Z_ROTATION  = 90 # Degrees

    _BLUE_MARKERS_RANGE   = [1, 2 ,3, 4, 5 ]
    _YELLOW_MARKERS_RANGE = [6, 7, 8, 9, 10]

    _ROBOTS_MARKERS_SIZE  = 0.07 # meters

    _BLUE_MARKERS   = MarkerList(_BLUE_MARKERS_RANGE, _ROBOTS_MARKERS_SIZE)
    _YELLOW_MARKERS = MarkerList(_YELLOW_MARKERS_RANGE, _ROBOTS_MARKERS_SIZE)
except:
    pass


class SupervisorServer(ServerGS):
    def __init__(self):
        ServerGS.__init__(self)
        self.logger = LogManager().getlogger("Server", Logger.SHOW, level_disp=INFO)

        # Ressources to lock
        self.ressources = {'Dispenser1': -1, 'Dispenser2': -1}

        self.ihm = None          # TODO : Handle IHM here

        try:
            #                     id| size | Coords(x,y,z)  |    flip aroud Z
            self.reference = ReferenceMarker(_CENTRAL_MARKER_ID, _CENTRAL_MARKER_SIZE,_CENTRAL_MARKER_COORDINATES , _CENTRAL_MARKER_Z_ROTATION)

        except:
            self.logger(WARNING, "You should probably check your opencv package first")
            self.logger(WARNING, "Tracking can't work in this configuration")
            self.logger(WARNING, "But all others components works fine ! :)")

        self.tracking = TrackingManager()
        self.tracking.start()

        self.logger(INFO, "Server succefully initialised")

    def init_tracking(self, camera=VideoStream.JETSONCAMERA):
        while not self.tracking.setup(self.reference, camera=camera):
            pass

        self.tracking.startTracking()

    def get_opponents_pos(self):
        return self.tracking.getPos()
