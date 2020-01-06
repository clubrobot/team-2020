import numpy as np
import cv2
import cv2.aruco as aruco

from logs.log_manager import *

WAITING_TIME = 10
MAKER_LEN = 0.1
DICT_ID = aruco.DICT_4X4_100


if __name__ == "__main__":

    # Start logger
    LogManager().start()
    logger = LogManager().getlogger('aruco_demo', Logger.SHOW, DEBUG)

    logger(INFO, 'Init Video Capture')
    videoIn = cv2.VideoCapture(0)

    # Get aruco dict
    aruco_dict = aruco.Dictionary_get(DICT_ID)

    # Get detection parameters
    parameters = aruco.DetectorParameters_create()

    logger(INFO, 'Starting Tag Detection')
    while(videoIn.grab()):
        ret, image = videoIn.retrieve()

        # Detect detection parameters
        corners, ids, rejectedImgPoints = aruco.detectMarkers(
            image, aruco_dict, parameters=parameters)

        if(ids is not None and len(ids) > 0):
            logger(INFO, 'Found', len(ids), 'Markers | ids : ', ids)

        # Draw detected maker in green
        aruco.drawDetectedMarkers(image, corners, ids)
        # Draw rejected maker in red
        aruco.drawDetectedMarkers(
            image, rejectedImgPoints, borderColor=(100, 0, 240))

        # Show image result in real time
        cv2.imshow('result', image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release cam
    videoIn.release()
    cv2.destroyAllWindows()
