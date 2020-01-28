from tracking.libs.videostream import VideoStream
from imutils.video import FPS
import imutils

from logs.log_manager import *


class Camera(VideoStream):
    """
        The purpose of this class is to provide a camera abstraction layer to handle
        all camera types including picamera.
        It also compute the FPS rate.
    """

    def __init__(self, src=0, usePiCamera=False, resolution=(320, 240), framerate=32, exec_param=Logger.SHOW, log_level=INFO):
        """
            Init camera videostream and FPS class.
        """
        VideoStream.__init__(self, src, usePiCamera, resolution, framerate)
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)
        self.fps = FPS().start()

        self.logger(INFO, 'Camera Initialisation Success !')

    def start(self):
        """
            Strating camera process
        """
        self.logger(INFO, 'Starting Camera !')
        super().start()

    def read(self, width=None):
        """
            Read one frame and resize it if desired
        """
        image = super().read()
        if width is not None:
            image = imutils.resize(image, width=width)
        self.fps.update()
        return image.copy()

    def stop(self):
        """
            Stopping camera process.
            Show elapsed time and FPS approximation.
        """
        super().stop()
        self.fps.stop()
        self.logger(INFO, "elasped time: {:.2f}".format(self.fps.elapsed()))
        self.logger(INFO, "approx. FPS: {:.2f}".format(self.fps.fps()))
