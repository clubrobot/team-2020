#!/usr/bin/env python3
# coding: utf-8

from threading import Thread, Event

from listeners.position_listener import *
from listeners.sensor_listener import *

from logs.log_manager import *
import math
class AviodanceBehaviour(Thread):

    # Avoiding behaviour
    BEHAVIOUR_STOPPING              = 0
    BEHAVIOUR_AVOID_ROADMAP         = 1
    BEHAVIOUR_AVOID_POTENTIAL_FIELD = 2
    # TODO : Add new behaviour here

    # Avoiding detection style
    BEHAVIOUR_DETECT_NEAR_TO_ME = 0
    BEHAVIOUR_DETECT_ON_MY_PATH = 1

    def __init__(self, wheeledbase, roadmap, beacon_client, behaviour=BEHAVIOUR_STOPPING, detection_style=BEHAVIOUR_DETECT_NEAR_TO_ME, timestep=0.1, exec_param=Logger.SHOW, log_level=INFO):
        """
            Init all internals components
        """
        Thread.__init__(self)
        self.daemon = True

        # Init Logger
        self.logger = LogManager().getlogger(self.__class__.__name__, exec_param, log_level)

        # Init internal events
        self.on_brother_moving_event    = Event()
        self.on_opponentA_moving_event  = Event()
        self.on_opponentB_moving_event  = Event()
        # TODO Sensors event

        self.movement_in_progress       = Event()

        # Stopping event
        self.stop = Event()

        # Clear all internal events
        self.on_brother_moving_event.clear()
        self.on_opponentA_moving_event.clear()
        self.on_opponentB_moving_event.clear()

        self.movement_in_progress.clear()

        # Bind behaviour wheeledbase and beacon client
        self.wheeledbase        = wheeledbase
        self.roadmap            = roadmap
        self.beacon_client      = beacon_client
        self.behaviour          = behaviour
        self.detection_style    = detection_style
        self.timestep           = timestep # Seconds

        # Instanciate position listener
        self.position_listener = PositionListener(self.beacon_client.get_brother_pos , self.beacon_client.get_opponents_pos)

        # Instanciate Sensors listener
        # TODO

        # Bind internal event generator
        self.position_listener.bind(PositionListener.BROTHER, self._on_brother_moving)
        self.position_listener.bind(PositionListener.OPPONENTA, self._on_opponentA_moving)
        self.position_listener.bind(PositionListener.OPPONENTB, self._on_opponentB_moving)

        # TODO Sensors events

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

    def move(self, destination, thresholds=(None, None)):
        linpos_threshold, angpos_threshold = thresholds
        default_linpos_threshold = 3
        default_angpos_threshold = 0.1

        # Pathfinding
        path_not_found = False
        x_in, y_in, theta_in = self.wheeledbase.get_position()
        x_sp, y_sp, theta_sp = destination

        try:
            path = [(x_in, y_in), (x_sp, y_sp)]
            self.logger(INFO, 'follow path: [{}]'.format(', '.join('({0[0]:.0f}, {0[1]:.0f})'.format(waypoint) for waypoint in path)))
        except RuntimeError:
            path_not_found = True

        # Return there is no path available
        if path_not_found:
            self.logger(ERROR, 'No path found !')
            sleep(1)
            return False

        # Pure Pursuit configuration
        if math.cos(math.atan2(path[1][1] - path[0][1], path[1][0] - path[0][0]) - theta_in) >= 0:
            direction = 1
        else:
            direction = -1

        if math.hypot(path[1][0] - path[0][0], path[1][1] - path[0][1]) < 5 and theta_sp is not None:
            finalangle = theta_sp - (direction - 1) * math.pi
        else:
            finalangle = None

        self.wheeledbase.lookahead.set(150)
        self.wheeledbase.lookaheadbis.set(150)
        self.wheeledbase.max_linvel.set(500)
        self.wheeledbase.max_angvel.set(6.0)
        self.wheeledbase.linpos_threshold.set(linpos_threshold or default_linpos_threshold)
        self.wheeledbase.angpos_threshold.set(angpos_threshold or default_angpos_threshold)

        # Trajectory
        self.wheeledbase.purepursuit(path, direction={1:'forward', -1:'backward'}[direction], finalangle=finalangle)

        # Robot moving event
        self.movement_in_progress.set()

        # Wait until destination is reached
        isarrived = False
        blocked = False
        while not isarrived:
            try:
                isarrived = self.wheeledbase.isarrived()
            except RuntimeError:
                self.logger(WARNING, 'Blocked while following path')
                blocked = True

            if blocked:
                self.logger(INFO, 'Go backward a little')
                self.wheeledbase.set_velocities(-direction * 100, 0)
                sleep(1)
                self.logger(INFO, 'Resume path')
                wheeledbase.purepursuit(path, direction={1:'forward', -1:'backward'}[direction])
                blocked = False

        return True

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