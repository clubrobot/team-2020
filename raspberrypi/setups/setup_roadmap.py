#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from common.geogebra import Geogebra

from setups.setup_logger import *
from setups.setup_robot_name import *

if ROBOT_ID == BORNIBUS_ID:
    setup_logger(INFO ,"Bornibus")
    os.chdir("/home/pi/git/clubrobot/team-2020")

elif ROBOT_ID == R128_ID:
    setup_logger(INFO ,"R128")
    os.chdir("/home/pi/git/clubrobot/team-2020")
else:
    setup_logger(INFO ,"Not on a robot !")

roadmap = None
for root, dirs, files in os.walk("."):
    for file in files:
        if ROBOT_ID == BORNIBUS_ID:
            if file == "Bornibus.ggb":
                roadmap = os.path.join(root, file)
        elif ROBOT_ID == R128_ID:
            if file == "128.ggb":
                roadmap = os.path.join(root, file)

if roadmap:
    geo = Geogebra(roadmap)
