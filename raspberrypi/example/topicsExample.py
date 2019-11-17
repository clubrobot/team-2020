#!/usr/bin/python3
# -*- coding: utf-8 -*-

from common.serialtalks import *
from common.serialtopics import *
from topics import *


class Arduino(SerialTalks):
    def __init__(self, uuid="/dev/tty.SLAB_USBtoUART"):
        SerialTalks.__init__(self, uuid)
        self.topics = SerialTopics(self)

        # create specific topic instance
        self.counter = CounterTopic()

        # add topic
        self.topics.add(self.counter)

    def on(self):
        self.send(0x10)

    def off(self):
        self.send(0x11)

    def subscribeCounter(self):
        return self.topics.subscribe(self.counter)

    def unsubscribeCounter(self):
        return self.topics.unsubscribe(self.counter)

    def getCounter(self):
        return self.counter.getRessource()


if __name__ == "__main__":

    # Create object
    arduino = Arduino()

    # Connect
    arduino.connect()

    # Get name
    print("uuid : ", arduino.getuuid())

    # topic subscription
    if(arduino.subscribeCounter()):
        print("Subscription succes")
    else:
        print("Subscription error")
    # Send some instruction
    # Activate sensors
    for i in range(0, 10):
        print("res = " + str(arduino.getCounter()))
        arduino.on()  # ON
        time.sleep(0.5)
        arduino.off()  # 0FF
        time.sleep(0.5)

if(arduino.unsubscribeCounter()):
    print("Unsubscription succes")
else:
    print("Unsubscription error")
