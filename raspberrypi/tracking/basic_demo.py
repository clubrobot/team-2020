
from imutils.video import VideoStream
from imutils.video import FPS
import imutils
import numpy as np
import cv2
import cv2.aruco as aruco

from logs.log_manager import *
from camera import Camera
from markers import *

NUM_FRAMES = 100

if __name__ == "__main__":

    # Start logger
    LogManager().start()

    cam = Camera()
    cam.start()

    detector = MarkersDetector(display=True)

    while cam.fps._numFrames < NUM_FRAMES:

        image = cam.read(800)

        markers = detector.getMarkers(image)

    # Release cam
    cam.stop()
    cv2.destroyAllWindows()
