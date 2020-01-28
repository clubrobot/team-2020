#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from time import sleep

from multiprocessing import Process, Pipe, Lock, Event
from common.parallel import Thread

from logs.log_manager import *
from tracking.libs.utils import *
from tracking.libs.camera import *
from tracking.libs.trackingCore import *


class TrackingWorker(Process):

    # Worker Command
    SETUP = 0
    START_TRACKING = 1
    STOP_TRACKING = 2
    RECALIBRATE = 3
    GET_CALIBRATION_FLAG = 4
    GET_POS = 5
    GET_FRAME = 6

    def __init__(self, exec_param=Logger.SHOW, log_level=INFO):
        """
            Init all Tracker Components
        """
        Process.__init__(self)

        # Terminate with the main process.
        self.daemon = True

        # Communication pipe.
        self.pipe = PipeType(*Pipe())

        # Lock
        self.lock = Lock()

        # Stop Event
        self.stop = Event()
        self.stop.clear()

        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        self.logger(INFO, 'TrackingWorker Initialisation Success !')

    def run(self):
        """
            Main process
        """
        while not self.stop.is_set():
            # get the last message
            msg = self._recv()

            if msg.cmd == self.SETUP:
                self._setup(msg.args.refMarker,
                            msg.args.markerList, msg.args.debug, msg.args.dictionnary)
                self._send(True)

            if msg.cmd == self.START_TRACKING:
                if hasattr(self, 'tracking'):
                    self.tracking.start()
                    if self.tracking.isAlive():
                        self._send(True)
                    else:
                        self._send(False)
                else:
                    self._send(False)

            if msg.cmd == self.STOP_TRACKING:
                if hasattr(self, 'tracking'):
                    if self.tracking.isAlive():
                        self.tracking.terminate()
                    self._send(True)
                else:
                    self._send(False)

            if msg.cmd == self.RECALIBRATE:
                self.tracking.recalibrate()
                self._send(True)

            if msg.cmd == self.GET_CALIBRATION_FLAG:
                self._send(self.tracking.is_calibrated())

            if msg.cmd == self.GET_POS:
                pass

            if msg.cmd == self.GET_FRAME:
                self._send(self.tracking.get_current_frame())

            # delete message
            del msg

    def _setup(self, refMarker, markerList, debug, dictionnary):
        """
            Internal method to initialise proces dependent components.
        """
        self.logger(INFO, 'TrackingWorker Setup...')
        # Creating camera component
        self.camera = Camera()
        self.camera.start()

        # Creating Tracker component
        self.tracking = TrackingCore(
            self.camera, refMarker, markerList, debug, dictionnary)

    def _recv(self, timeout=None):
        """
            Blocking recieve that permit to avoid some Pipe polling limitation
        """
        if select([self.pipe.parent], [], [], None)[0]:
            return self.pipe.parent.recv()
        else:
            return None

    def _send(self, obj):
        """
            Send Method
        """
        self.pipe.parent.send(obj)

    def terminate(self):
        self.stop.set()
