import sys
from time import sleep
import numpy as np
import cv2
import cv2.aruco as aruco
from collections import namedtuple

from logs.log_manager import *
from tracking.libs.utils import *


class RobotsTracker:
    """
        This class purpose is to track robots positions on a map

        (3000,3000) +---------------------------------------+ x
                    |                                       |
                    |                     ref: id 42        |
                    |        (1250, 1500)+                  |
                    |                                       |
                    |                                       |
                    |                                       |
                y   +---------------------------------------+ (0,0)
                                        ^
                                        Camera
    """

    def __init__(self, camera, refMarker, markerList=None, dictionnary=aruco.DICT_4X4_100, exec_param=Logger.SHOW, log_level=INFO):
        """
            Init all Tracker Components
        """
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)

        try:
            # File storage in OpenCV
            cv_file = cv2.FileStorage(
                "../calibration.yaml", cv2.FILE_STORAGE_READ)

            self.camera_matrix = cv_file.getNode("camera_matrix").mat()
            self.dist_matrix = cv_file.getNode("dist_coeff").mat()

            # release file
            cv_file.release()
        except:
            self.logger(ERROR, 'No calibration file found, try to run calibration script before')
            sleep(0.2)
            sys.exit(1)

        # Get aruco dict
        self.dict = aruco.Dictionary_get(dictionnary)

        # Get detection parameters
        self.parameters = aruco.DetectorParameters_create()
        self.parameters.adaptiveThreshConstant = 10

        self.camera = camera
        self.refMarker = refMarker
        self.markerList = markerList

        self.calibrationMatrix = None

        self.display = ArucoDisplay(
            self.camera_matrix, self.dist_matrix, wait=1)

        self.logger(INFO, 'RobotsTracker Initialisation Success !')

    def calibrateFromExternalFrame(self, frame):
        """
            Calibrate method to get calibration matrix from external Frame
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        # Detect Markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, self.dict, parameters=self.parameters)

        index = self._getMarkerIndex(ids, self.refMarker.identifier)

        if index is not None:
            self.calibrationMatrix = self._getCalibrationMatrix(corners, index)

            if self.calibrationMatrix is not None:
                return True
        else:
            return False

    def calibrate(self):
        """
            Calibrate method to get calibration matrix from camera
        """
        # Get frames
        frame, gray = self._getFrame()

        # Detect Markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, self.dict, parameters=self.parameters)

        index = self._getMarkerIndex(ids, self.refMarker.identifier)

        if index is not None:
            self.calibrationMatrix = self._getCalibrationMatrix(corners, index)

            if self.calibrationMatrix is not None:
                return True
        else:
            return False

    def computeFromExternalFrame(self, frame):
        """
            ComputeFromExternalFrame method to print estimated position for each tag
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        self.display.wait = 0
        # Detect Markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, self.dict, parameters=self.parameters)

        if np.all(ids != None):
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                corners, self.refMarker.size, self.camera_matrix, self.dist_matrix)

            self.display.drawDetectedMarkers(frame, corners)

            for i in range(0, ids.size):
                p = self._getPointMilimeters(rvec[i], tvec[i])
                self.logger(INFO,'id :', ids[i], '| pos : ', p)

            if not self.display.show(frame):
                self.camera.stop()
                sleep(0.5)
                sys.exit(0)

    def compute(self):
        """
            Compute method to print estimated position for each tag
        """
        # Get frame
        frame, gray = self._getFrame()
        # Detect Markers
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            gray, self.dict, parameters=self.parameters)

        if np.all(ids != None):
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                corners, self.refMarker.size, self.camera_matrix, self.dist_matrix)

            self.display.drawDetectedMarkers(frame, corners)

            for i in range(0, ids.size):
                if ids[i] != self.refMarker.identifier:
                    p = self._getPointMilimeters(rvec[i], tvec[i])
                    self.logger(INFO,'id :', ids[i], '| pos : ', p)

            if not self.display.show(frame):
                self.camera.stop()
                sleep(0.5)
                sys.exit(0)

    def _getPointMilimeters(self, rvec, tvec):
        """
            Internal method to get milimeters pos from rvec and tvec.

            1. Get rotation matrix from Rvec by rodrigues func:

                R = Rodrigues(rvec)

            2. Compose 4x4 matrix with R and Tvec:

                                    | Rxx  Rxy  Rxz tvecx |
                Rmarker = |R|t| =   | Ryx  Ryy  Ryz tvecy |
                                    | Rzx  Rzy  Rzz tvecz |
                                    |  0    0    0    1   |

            3. Project coordinates of detected marker:

                | x |                                 | 0 |
                | y |   = ((Rref * Rcal) * Rmarker) * | 0 |
                | z |                                 | 0 |
                | 1 |                                 | 1 |

                Note: marker coordinates is always Zero on marker world

            4. Convert point to millimeters, round it and return it
        """
        try:
            R = np.float32(cv2.Rodrigues(rvec)[0])
            t = np.float32(tvec[0]).reshape(3,1)

            Rmarker = np.concatenate((R, t), axis = 1)
            Rmarker = np.vstack([Rmarker, np.float32([0,0,0,1])])

            point = (np.matmul(np.matmul(self.refMarker.matrix,
                                        self.calibrationMatrix), Rmarker)).dot([0, 0, 0, 1])

            return round(point[0]*1000), round(point[1]*1000), round(point[2]*1000)
        except:
            return None

    def _getMarkerIndex(self, idList, requestId):
        """
            Internal method to get marker index on ids list
        """
        try:
            return np.where(idList == np.array(requestId))[0][0]
        except:
            return None

    def _getFrame(self):
        """
            Internal method to get camera frame.
            It retrun color and gray frame
        """
        frame = self.camera.read(width=800)
        return (frame, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))

    def _getCalibrationMatrix(self, corners, index):
        """
            Internal method to retreive map calibration matrix from reference marker on map.

            1. Get rotation matrix from Rvec by rodrigues func:

                R = Rodrigues(rvec)

            2. Compose 4x4 Calibration matrix with R and Tvec:

                                | Rxx  Rxy  Rxz tvecx |
                Rcal  = |R|t| = | Ryx  Ryy  Ryz tvecy |
                                | Rzx  Rzy  Rzz tvecz |
                                |  0    0    0    1   |
            3. And invert it:

                Rcal = inv(Rcal)

            Return None if error occur
        """
        try:
            rvec, tvec, _ = aruco.estimatePoseSingleMarkers(
                corners[index], self.refMarker.size, self.camera_matrix, self.dist_matrix)

            R = np.float32(cv2.Rodrigues(rvec)[0])
            t = np.float32(tvec[0][0]).reshape(3,1)

            Rcal = np.concatenate((R, t), axis = 1)
            Rcal = np.vstack([Rcal, np.float32([0,0,0,1])])

            return np.linalg.inv(Rcal)
        except:
            return None
