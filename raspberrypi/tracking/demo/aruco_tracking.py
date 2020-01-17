import numpy as np
import cv2
import cv2.aruco as aruco
import glob
import imutils

from logs.log_manager import *
from tracking.libs.camera import *
from tracking.libs.tracking import *
from tracking.libs.utils import *

if __name__ == "__main__":
    # Start logger
    LogManager().start()

    cap = Camera()
    cap.start()

    #                     id| size | Coords(x,y,z)  |    flip aroud Z
    ref = ReferenceMarker(42, 0.02, Point(0.125, 0.150, 0.0), 90)

    tracker = RobotsTracker(cap, ref)
    images = glob.glob('Pictures/*.jpg')

    # ------------------ ARUCO TRACKER ---------------------------
    # For each pictures
    for fname in images:
        # Read frame and reshape at 800 pix
        frame = cv2.imread(fname)
        frame = imutils.resize(frame, 800)

        if tracker.calibrateFromExternalFrame(frame):
            tracker.computeFromExternalFrame(frame)

    # When everything done, release the capture
    cap.stop()
    cv2.destroyAllWindows()
