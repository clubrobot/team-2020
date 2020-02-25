#!/usr/bin/env python3
# coding: utf-8

STARTING_POINT = (935, 2670)
DESTINATION_POINT = (935, 670)

PATH = [STARTING_POINT, DESTINATION_POINT]

if __name__ == "__main__":

    from setups.setup_wheeledbase import *
    from setups.setup_beacons import *
    from behaviours.avoidance_behaviour import AviodanceBehaviour
    from time import sleep

    behaviour = AviodanceBehaviour(wheeledbase, beacon)

    input('Place robot and press touch to start')
    wheeledbase.set_position(*STARTING_POINT, -pi/2)

    if behaviour.movement_authorized():
        wheeledbase.purepursuit(*PATH, finalangle=-pi/2)
        while not wheeledbase.isarrived():
            sleep(0.1)
            if not behaviour.movement_authorized():
                print('/!\\ Avoidance behavior taking control !')