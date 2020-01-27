#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
from time import sleep

import cv2
import cv2.aruco as aruco

from multiprocessing import Process, Pipe, Lock, Event
from common.parallel import Thread

from common.metaclass import Singleton

from logs.log_manager import *
from tracking.libs.utils import *
from tracking.libs.worker import *

class TrackingManager(metaclass=Singleton):

    #Worker Command
    SETUP                   = 0
    START_TRACKING          = 1
    STOP_TRACKING           = 2
    RECALIBRATE             = 3
    GET_CALIBRATION_FLAG    = 4
    GET_POS                 = 5

    def __init__(self, exec_param=Logger.SHOW, log_level=INFO):
        """
        Instanciate worker at the singleton creation
        """
        # Instantiate LogWorker
        self.worker = TrackingWorker(exec_param, log_level)

        # Lock
        self.lock = Lock()

        self.logger = LogManager().getlogger(self.__class__.__name__, exec_param, log_level)

        self.logger(INFO, 'TrackingManager Initialisation Success !')

    def setup(self, refMarker, markerList=None, dictionnary=aruco.DICT_4X4_100):
        """
        Send Init command to the Worker Process on the specific logger proxy creation
        """
        if self._check_pid():
            self._send(Command(self.SETUP, InitMsg(refMarker, markerList, dictionnary)))
            ret = self._recv(timeout=5)
            if ret:
                self.logger(INFO, 'Setup sucessful !')
                return True
        self.logger(INFO, 'Setup fail !')
        return False

    def startTracking(self):
        if self._check_pid():
            self._send(Command(self.START_TRACKING, None))
            ret = self._recv(timeout=1)
            if ret:
                self.logger(INFO, 'Starting success !')
                return True
        self.logger(INFO, 'Starting fail !')
        return False

    def stopTracking(self):
        if self._check_pid():
            self._send(Command(self.STOP_TRACKING, None))
            ret = self._recv(timeout=1)
            if ret:
                self.logger(INFO, 'Stopping success !')
                return True
        self.logger(INFO, 'Stopping fail !')
        return False

    def recalibrate(self):
        if self._check_pid():
            self._send(Command(self.RECALIBRATE, None))
            ret = self._recv(timeout=1)
            if ret:
                self.logger(INFO, 'Recalibration success !')
                return True
        self.logger(INFO, 'Recalibration fail !')
        return False

    def start(self):
        """
        Start Worker Process
        """
        try:
            self.logger(INFO, 'Tracking Worker Starting Success !')
            self.worker.start()
        except:
            self.logger(INFO, 'Tracking Worker Starting Fail !')

    def stop(self):
        """
        Stop Worker Process
        """
        try:
            self.worker.terminate()
        except:
            pass

    def _check_pid(self):
        """
        Check For the existence of a unix pid.
        """
        try:
            if self.worker.pid is not None:
                os.kill(self.worker.pid, 0)
            else:
                return False
        except OSError:
            return False
        else:
            return True

    def _recv(self, timeout = None):
        """
            Blocking recieve that permit to avoid some Pipe polling limitation
        """
        if select([self.worker.pipe.child], [], [], timeout)[0]:
            return self.worker.pipe.child.recv()
        else:
            return None

    def _send(self, obj):
        """
            Send Method
        """
        self.worker.pipe.child.send(obj)