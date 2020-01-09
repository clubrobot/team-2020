import numpy as np
import cv2
import cv2.aruco as aruco
from collections import namedtuple

from logs.log_manager import *

Markers = namedtuple('Markers', ['corners', 'ids', 'rejectedImgPoints'])
PosSingleMarker = namedtuple(
    'PosSingleMarker', ['rvecs', 'tvecs', 'objPoints'])


class MarkersDetector():
    def __init__(self, dictionnary=aruco.DICT_4X4_100, exec_param=Logger.SHOW, log_level=INFO):
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        self.logger(INFO, 'MarkersDetector Initialisation Success !')

        # Get aruco dict
        self.dict = aruco.Dictionary_get(dictionnary)

        # Get detection parameters
        self.parameters = aruco.DetectorParameters_create()
        self.parameters.adaptiveThreshConstant = 10

    def getMarkers(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return Markers(*aruco.detectMarkers(gray, self.dict, parameters=self.parameters))


class MarkersPositioning():
    def __init__(self, exec_param=Logger.SHOW, log_level=INFO):
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        # File storage in OpenCV
        cv_file = cv2.FileStorage("../calibration.yaml", cv2.FILE_STORAGE_READ)

        # Note : we also have to specify the type
        # to retrieve otherwise we only get a 'None'
        # FileNode object back instead of a matrix
        self.camera_matrix = cv_file.getNode("camera_matrix").mat()
        self.dist_matrix = cv_file.getNode("dist_coeff").mat()

        cv_file.release()

        self.logger(INFO, 'camera_matrix : ', self.camera_matrix.tolist())
        self.logger(INFO, 'dist_matrix : ', self.dist_matrix.tolist())

        cv_file.release()

        self.logger(INFO, 'MarkersPositioning Initialisation Success !')

    def getPositionsFromMarkers(self, markers):
        # estimate pose of each marker and return the values
        # rvet and tvec-different from camera coefficients
        return PosSingleMarker(*aruco.estimatePoseSingleMarkers(
            markers.corners, 0.05, self.camera_matrix, self.dist_matrix))
        # (rvec-tvec).any() # get rid of that nasty numpy value array error


class MarkersPosEstimator():
    def __init__(self, exec_param=Logger.SHOW, log_level=INFO):
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        self.cameraMatrix = None
        self.distCoefs = None

        self.rvec = None
        self.tvec = None

        self.logger(INFO, 'MarkersPosEstimator Initialisation Success !')
