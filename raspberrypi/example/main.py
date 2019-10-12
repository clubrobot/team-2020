from common.serialtalks import *

# Create object
arduino = SerialTalks("/dev/ttyUSB0")


# Connect 
arduino.connect()


#Get name
print("uuid : ", arduino.getuuid())

#Send some instruction
#Activate sensors
arduino.send(0x11)


#  Get mesure and deserial it
result = arduino.execute(0x10)
left, right = result.read(INT, INT)
print("left : ", left)
print("right : ", right)


