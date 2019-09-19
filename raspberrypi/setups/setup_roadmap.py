import os
from common.logger import *
from common.geogebra import Geogebra
from robots.get_robot_name import *

if ROBOT_ID == BORNIBUS_ID or ROBOT_ID == R128_ID:
    log = Logger(Logger.BOTH, file_name="/home/pi/logs/start.log")
else:
    log = Logger(Logger.SHOW)


if ROBOT_ID == BORNIBUS_ID:
    print("Bornibus")
    os.chdir("/home/pi/git/clubrobot/team-2020")

elif ROBOT_ID == R128_ID:
    print("R128")
    os.chdir("/home/pi/git/clubrobot/team-2020")

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
