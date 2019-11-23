#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from logs.log_manager import *
import threading


def thread_wheeledbase():
    loggerWheeledbase = log.getlogger(
        'Wheeledbase', exec_param=Logger.BOTH, level_disp=Logger.CRITICAL)
    loggerWheeledbase("b", level=Logger.CRITICAL)
    sleep(2)
    loggerWheeledbase("c", level=Logger.ERROR)
    sleep(2)
    loggerWheeledbase("d", level=Logger.WARNING)
    loggerWheeledbase("e", level=Logger.INFO)
    loggerWheeledbase("f", level=Logger.DEBUG)


def thread_sensors():
    loggerSensors = log.getlogger(
        'Sensors', exec_param=Logger.BOTH, level_disp=Logger.CRITICAL)

    loggerSensors("b", level=Logger.CRITICAL)
    loggerSensors("c", level=Logger.ERROR)
    loggerSensors("d", level=Logger.WARNING)
    sleep(2)
    loggerSensors("e", level=Logger.INFO)
    loggerSensors("f", level=Logger.DEBUG)


if __name__ == "__main__":

    log = LogManager()
    log.start()

    x1 = threading.Thread(target=thread_wheeledbase)
    x2 = threading.Thread(target=thread_sensors)

    x1.start()
    x2.start()

    x1.join()
    x2.join()

    sleep(1)
    log.terminate()
