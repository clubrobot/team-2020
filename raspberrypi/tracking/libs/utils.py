import sys
import numpy as np
from time import sleep
import cv2
import cv2.aruco as aruco
from collections import namedtuple

Point = namedtuple('Point', ['x', 'y', 'z'])

class Marker:
    """
        The purpose of this class is to define a marker
    """

    def __init__(self, identifier, size, dictionnary=aruco.DICT_4X4_100):
        """
            Init with aruco tag ID, its size in mm
        """
        self.identifier = identifier
        self.size = size  # mm
        self.dictionnary = dictionnary

class MarkerList:
    def __init__(self, ids, size, dictionnary=aruco.DICT_4X4_100):
        self.markers = list()
        self.size = len(ids)

        for i in range(0, self.size):
            self.markers.append(Marker(ids[i], size, dictionnary))

class ReferenceMarker(Marker):
    def __init__(self, identifier, size, pos, rotAngle=None, dictionnary=aruco.DICT_4X4_100):
        """
            Init reference marker
        """
        Marker.__init__(self, identifier, size, dictionnary)
        self.pos = pos
        if rotAngle is None:
            self.matrix = np.float32([[1, 0, 0, self.pos.x],
                                      [0, 1, 0, self.pos.y],
                                      [0, 0, 1, self.pos.z],
                                      [0, 0, 0, 1]])
        else:
            th = np.radians(rotAngle)
            self.matrix = np.float32([[np.cos(th),  -np.sin(th), 0, self.pos.x],
                                      [np.sin(th), np.cos(th), 0, self.pos.y],
                                      [0, 0, 1, self.pos.z],
                                      [0, 0, 0, 1]])


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
            aruco.drawAxis(frame, self.camera_matrix,
                           self.dist_matrix, rvec, tvec, 0.05)
        except:
            pass

    def show(self, frame):
        # Get frames
        cv2.imshow('frame', frame)
        if cv2.waitKey(self.wait) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return False
        return True
