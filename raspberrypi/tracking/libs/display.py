import sys
import numpy as np
import cv2
import cv2.aruco as aruco

class ArucoDisplay:
    def __init__(self, camera_matrix, dist_matrix, wait=1):
        self.wait = wait
        self.camera_matrix = camera_matrix
        self.dist_matrix = dist_matrix

    def drawDetectedMarkers(self, frame, corners, ids=None):
        try:
            aruco.drawDetectedMarkers(frame, corners, ids)
        except:
            pass

    def drawRejectedMarkers(self, frame, corners):
        try:
            aruco.drawDetectedMarkers(frame, corners, borderColor=(0, 0, 255))
        except:
            pass

    def drawAxis(self, frame, rvec, tvec):
        try:
            aruco.drawAxis(frame, self.camera_matrix, self.dist_matrix, rvec, tvec, 0.05)
        except:
            pass

    def show(self, frame):
        # Get frames
        cv2.imshow('frame', frame)
        if cv2.waitKey(self.wait) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return False
        return True
