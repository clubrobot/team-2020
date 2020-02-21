#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event
from time import sleep
from math import hypot

from common.sync_flag_signal import Signal, Flag


class SensorListener(Thread):

    FRONT = 0
    LEFT  = 1
    RIGHT = 2

    def __init__(self, front_getter, left_getter, right_getter, timestep=0.1, threshold=220):
        Thread.__init__(self)
        self.daemon = True

        # Sensors list
        self.sensors_list = [LEFT, FRONT, RIGHT]

        # Signals for each sensors
        self.__setattr__("signal"+str(self.FRONT) , Signal())
        self.__setattr__("signal"+str(self.LEFT)  , Signal())
        self.__setattr__("signal"+str(self.RIGHT) , Signal())

        # Sensors getter
        self.__setattr__("getter"+str(self.FRONT) , front_getter)
        self.__setattr__("getter"+str(self.LEFT)  , left_getter)
        self.__setattr__("getter"+str(self.RIGHT) , left_getter)

        # Timestep
        self.timestep = timestep

        # Stopping event
        self.stop = Event()

        # Position threshold
        self.threshold = threshold

        # Atomatically start
        self.start()

    def bind(self, idx, func):
        self.__setattr__("flag"+str(idx), Flag(func))
        self.__getattribute__("flag"+str(idx)).bind(self.__getattribute__("signal"+str(idx)))

    def _handle_sensor(self, idx):
        try:
            a, b = self.__getattribute__("getter"+str(idx))
        except TimeoutError:
            pass

        if a < self.threshold or b < self.threshold:
            self.__getattribute__("signal"+str(idx)).ping()


    def run(self):
        while not self.stop.is_set():
            # Handle each sensors
            for sensor in self.sensors_list:
                self._handle_sensor(sensor)

            sleep(self.timestep)
