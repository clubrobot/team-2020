#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from logs.log_manager import *
from random import choice, random
from time import time, sleep
from threading import Thread
from logs.log_manager import DEBUG, WARNING, ERROR, INFO

# Create default message with associeted level
WHEELEDBASE_MSG =  [(DEBUG, "position 10, 20"), (ERROR, "spin error"), (DEBUG, "purpursuit"), (INFO, "arrived"),
                   (INFO, "set position 20 , 20"), (WARNING, "reset"), (INFO, "turnonthe spot 3.14")]

DISPLAY_MSG = [(DEBUG, "display time"), (WARNING, "print error msg"), (ERROR, "reset screen"), (INFO, "add point")]

SENSORS_MSG = [(WARNING, "Front robot detected"), (WARNING, "Back robot detected"), (WARNING, "Lat robot detected"),
               (INFO, "Wall detected"),(ERROR, "no obstacle detected")]

# Generation duration 
GEN_TIME = 20  #s

# Max time between 2 log
MAX_D_TIME = 1 #s

# Create and start logger
log = LogManager()
log.start()

# Create log topic
wheeledbase_log = log.getlogger("WheeledBase", Logger.WRITE, DEBUG)
display_log = log.getlogger("Display", Logger.WRITE, DEBUG)
sensors_log = log.getlogger("Sensors", Logger.WRITE, DEBUG)


# Create thread main function per topic
def wheeledbase_generator(wheeledbase_log, start_time):
    while time()<GEN_TIME+start_time:
        wheeledbase_log(*choice(WHEELEDBASE_MSG))
        sleep(random()*MAX_D_TIME)

def display_generator(display_log, start_time):
    while time()<GEN_TIME+start_time:
        display_log(*choice(DISPLAY_MSG))
        sleep(random()*MAX_D_TIME)

def sensors_generator(sensors_log, start_time):
    while time()<GEN_TIME+start_time:
        sensors_log(*choice(SENSORS_MSG))
        sleep(random()*MAX_D_TIME)

# Init time
start_time = time()

# Instantiate all threads
wheeledbase_thread = Thread(target=wheeledbase_generator, args=(wheeledbase_log, start_time))
display_thread = Thread(target=display_generator, args=(display_log, start_time))
sensors_thread = Thread(target=sensors_generator, args=(sensors_log, start_time))

# Start threads
wheeledbase_thread.start()
display_thread.start()
sensors_thread.start()

# Wait end
wheeledbase_thread.join()
display_thread.join()
sensors_thread.join()

# Close files
log.stop()
