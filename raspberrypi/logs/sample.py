#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from logs.log_manager import *

if __name__ == "__main__":

    log = LogManager()
    log.start()
    loggerWheeledbase = log.getlogger('Wheeledbase', exec_param=Logger.BOTH)
    loggerSensors = log.getlogger('Sensors')

    loggerWheeledbase("b", level=Logger.CRITICAL)
    loggerWheeledbase("c", level=Logger.ERROR)
    loggerWheeledbase("d", level=Logger.WARNING)
    loggerWheeledbase("e", level=Logger.INFO)
    loggerWheeledbase("f", level=Logger.DEBUG)

    loggerSensors("b", level=Logger.CRITICAL)
    loggerSensors("c", level=Logger.ERROR)
    loggerSensors("d", level=Logger.WARNING)
    loggerSensors("e", level=Logger.INFO)
    loggerSensors("f", level=Logger.DEBUG)

    sleep(1)
    log.terminate()
