#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from logs.log_manager import *
from setups.setup_logger import *
from setups.setup_serialtalks import *
from setups.setup_wheeledbase import *
from setups.setup_roadmap import *
from setups.setup_display import *
#from setups.setup_sensors import *
from setups.setup_beacons import *


def init_robot():
    setup_logger(INFO, "Intialize robot !")
    pass


if __name__ == "__main__":
    init_robot()
