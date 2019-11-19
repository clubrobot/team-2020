from common.serialtalks import *
from allclass import *


# Connect 
arduino.connect()


#Get name
print("uuid : ", arduino.getuuid())

        
p1 = LED(arduino)

i=0
while i<1:
    p1.led_on()
    time.sleep(1)
    p1.led_off()
    time.sleep(1)
    i= i+1


#  Get mesure and deserial it

#while i<10:
   # result = arduino.execute(0x11)
   # x,y,z = result.read(FLOAT,FLOAT,FLOAT)
   # print("y ", x , "  x ", y, " z", z)
   # i=i+1
   # time.sleep(0.1)



