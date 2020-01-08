import numpy as np
import cv2
import cv2.aruco as aruco
from collections import namedtuple

from logs.log_manager import *

Markers = namedtuple('Markers', ['corners', 'ids', 'rejectedImgPoints'])


class MakersDisplay():
    def __init__(self, exec_param=Logger.SHOW, log_level=INFO):
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        self.logger(INFO, 'MarkersDetection Initialisation Success !')

    def draw(self, image, markers):
        if markers is not None:
            if(markers.ids is not None and len(markers.ids) > 0):
                self.logger(INFO, 'Found', len(markers.ids),
                            'Markers | ids : ', markers.ids)

            self.logger(DEBUG, 'corners : ', markers.corners,
                        'rejectedImgPoints : ', markers.rejectedImgPoints)
            # Draw detected maker in green
            aruco.drawDetectedMarkers(image, markers.corners, markers.ids)
            # Draw rejected maker in red
            aruco.drawDetectedMarkers(
                image, markers.rejectedImgPoints, borderColor=(100, 0, 240))

            # Show image result in real time
            cv2.imshow('result', image)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                return False
        return True


class MarkersDetector():
    def __init__(self, display=False, exec_param=Logger.SHOW, log_level=INFO):
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        self.logger(INFO, 'MarkersDetector Initialisation Success !')

        # Get aruco dict
        self.dict = aruco.Dictionary_get(aruco.DICT_4X4_100)

        # Get detection parameters
        self.parameters = aruco.DetectorParameters_create()

        if display:
            self.display = MakersDisplay(exec_param, log_level)
        else:
            self.display = None

    def getMarkers(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        markers = Markers(
            *aruco.detectMarkers(gray, self.dict, parameters=self.parameters))

        if self.display is not None:
            self.display.draw(gray, markers)
        return markers


class MarkersPosEstimator():
    def __init__(self, exec_param=Logger.SHOW, log_level=INFO):
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        self.logger(INFO, 'MarkersPosEstimator Initialisation Success !')
