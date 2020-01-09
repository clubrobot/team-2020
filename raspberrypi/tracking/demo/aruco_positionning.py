import numpy as np
import cv2
import cv2.aruco as aruco
import glob

from logs.log_manager import *
from tracking.libs.camera import Camera
from tracking.libs.markers import *

# Start logger
LogManager().start()

cap = Camera()
cap.start()

detector = MarkersDetector(dictionnary=aruco.DICT_5X5_1000)
positionning = MarkersPositioning()

# ------------------ ARUCO TRACKER ---------------------------
while (True):
    # Read frame and reshape at 800 pix
    frame = cap.read(800)

    # Markers detection
    markers = detector.getMarkers(frame)

    # check if the ids list is not empty
    # if no check is added the code will crash
    if np.all(markers.ids != None):
        # estimate pose of each marker and return the values
        pos = positionning.getPositionsFromMarkers(markers)

        for i in range(0, markers.ids.size):
            # draw axis for the aruco markers
            aruco.drawAxis(frame, positionning.camera_matrix,
                           positionning.dist_matrix, pos.rvecs[i], pos.tvecs[i], 0.1)

        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, markers.corners)

    # display the resulting frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.stop()
cv2.destroyAllWindows()
