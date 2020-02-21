#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event

from listeners.position_listener import *
from listeners.sensor_listener import *

from logs.log_manager import *

class AviodanceBehaviour(Thread):

    BEHAVIOUR_STOPPING = 0
    # TODO : Add new behaviour here

    def __init__(self, wheeledbase, beacon_client, behaviour=BEHAVIOUR_STOPPING, exec_param=Logger.SHOW, log_level=INFO):
        """
            Init all internals components
        """
        Thread.__init__(self)
        self.daemon = True

        # Init Logger
        self.logger = LogManager().getlogger(self.__class__.__name__, exec_param, log_level)

        # Init internal events
        self.on_brother_moving_event = Event()
        self.on_opponentA_moving_event = Event()
        self.on_opponentB_moving_event = Event()

        # Stopping event
        self.stop = Event()

        # Clear all internal events
        self.on_brother_moving_event.clear()
        self.on_opponentA_moving_event.clear()
        self.on_opponentB_moving_event.clear()

        # Bind behaviour wheeledbase and beacon client
        self.wheeledbase = wheeledbase
        self.beacon_client = beacon_client
        self.behaviour = behaviour
        self.timestep = 0.1 # Seconds

        # Instanciate position listener
        self.position_listener = PositionListener(self.beacon_client.get_brother_pos , self.beacon_client.get_opponents_pos)

        # Bind internal event generator
        self.position_listener.bind(PositionListener.BROTHER, self._on_brother_moving)
        self.position_listener.bind(PositionListener.OPPONENTA, self._on_opponentA_moving)
        self.position_listener.bind(PositionListener.OPPONENTB, self._on_opponentB_moving)

        self.start()

    def _on_brother_moving(self):
        """
            Generate Event when Brother moving
        """
        self.on_brother_moving_event.set()

    def _on_opponentA_moving(self):
        """
            Generate Event when opponentA moving
        """
        self.on_opponentA_moving_event.set()

    def _on_opponentB_moving(self):
        """
            Generate Event when opponentA moving
        """
        self.on_opponentB_moving_event.set()

    def run(self):
        while not self.stop.is_set():
            if self.on_brother_moving_event.is_set():
                self.logger(INFO, "Brother is moving ...", pos=self.position_listener.get_position(PositionListener.BROTHER))
                self.on_brother_moving_event.clear()

            if self.on_opponentA_moving_event.is_set():
                self.logger(INFO, "OpponentA is moving ...", pos=self.position_listener.get_position(PositionListener.OPPONENTA))
                self.on_opponentA_moving_event.clear()

            if self.on_opponentB_moving_event.is_set():
                self.logger(INFO, "OpponentB is moving ...", pos=self.position_listener.get_position(PositionListener.OPPONENTB))
                self.on_opponentB_moving_event.clear()

            sleep(self.timestep)

if __name__ == "__main__":
    from beacons.global_sync import ClientGS

    LogManager().start()
    try:
        beacon = ClientGS(1, ip ='127.0.0.1')
        beacon.connect()
        beacon.reset_ressources()

        a = AviodanceBehaviour(None, beacon)
    except TimeoutError:
        pass