import time
import glob

from logs.log_manager import *
from tracking.libs.camera import *
from tracking.libs.manager import *
from tracking.libs.utils import *
from tracking.libs.markers import *

if __name__ == "__main__":
    # Start logger
    LogManager().start()

    #                     id| size | Coords(x,y,z)  |    flip aroud Z
    ref = ReferenceMarker(42, 0.02, Point(0.125, 0.150, 0.0), 90)

    markerList = MarkerList([1, 2, 3, 4, 5], 0.02)

    man = TrackingManager()
    man.start()

    while not man.setup(ref, markerList, debug=True):
        pass

    man.startTracking()

    while True:
        man.show()

    man.stopTracking()

    input()
