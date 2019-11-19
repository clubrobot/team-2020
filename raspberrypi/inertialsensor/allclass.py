from common.serialtalks import *

arduino = SerialTalks("/dev/ttyS0")

#Send some instruction

class LED(SerialTalks):
    def __init__(self,uuid='led'):
        SerialTalks.__init__(self,uuid)

    def led_on(self):
        arduino.send(0x10,BYTE(0))

    def led_off(self):
        arduino.send(0x10,BYTE(1))