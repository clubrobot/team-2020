from imutils.video import VideoStream
from imutils.video import FPS
import imutils

from logs.log_manager import *


class Camera(VideoStream):
    def __init__(self, src=0, usePiCamera=False, resolution=(320, 240), framerate=32, exec_param=Logger.SHOW, log_level=INFO):
        VideoStream.__init__(self, src, usePiCamera, resolution, framerate)
        self.logger = LogManager().getlogger(
            self.__class__.__name__, exec_param, log_level)
        self.fps = FPS().start()

        self.logger(INFO, 'Camera Initialisation Success !')

    def start(self):
        self.logger(INFO, 'Starting Camera !')
        super().start()

    def read(self, width=400):
        image = imutils.resize(super().read(), width=width)
        self.fps.update()
        return image.copy()

    def stop(self):
        super().stop()
        self.fps.stop()
        self.logger(INFO, "elasped time: {:.2f}".format(self.fps.elapsed()))
        self.logger(INFO, "approx. FPS: {:.2f}".format(self.fps.fps()))
