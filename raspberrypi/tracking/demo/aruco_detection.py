import cv2
import cv2.aruco as aruco

from logs.log_manager import *
from tracking.libs.camera import Camera
from tracking.libs.markers import *

if __name__ == "__main__":

    # Start logger
    LogManager().start()

    cam = Camera()
    cam.start()

    detector = MarkersDetector()

    while (True):

        frame = cam.read(400)

        markers = detector.getMarkers(frame)

        # draw a square around the markers
        aruco.drawDetectedMarkers(frame, markers.corners)

        # display the resulting frame
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release cam
    cam.stop()
    cv2.destroyAllWindows()
