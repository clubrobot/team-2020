from setups.setup_wheeledbase import *
import random
from math import pi

startPoint = (935, 2670)

Zone1 = [(1000, 1700), (2000, 2700)]
Zone2 = [(300, 1000), (1000, 2000)]
Zone3 = [(1000, 1700), (300, 1000)]
Zone4 = [(300, 1000), (2000, 2700)]
Zone5 = [(1000, 1700), (1000, 2000)]
Zone6 = [(300, 1000), (300, 1000)]

point1 = (random.randint(Zone1[0][0], Zone1[0][1]),
          random.randint(Zone1[1][0], Zone1[1][1]))

point2 = (random.randint(Zone2[0][0], Zone2[0][1]),
          random.randint(Zone2[1][0], Zone2[1][1]))

point3 = (random.randint(Zone3[0][0], Zone3[0][1]),
          random.randint(Zone3[1][0], Zone3[1][1]))

point4 = (random.randint(Zone4[0][0], Zone4[0][1]),
          random.randint(Zone4[1][0], Zone4[1][1]))

point5 = (random.randint(Zone5[0][0], Zone5[0][1]),
          random.randint(Zone5[1][0], Zone5[1][1]))

point6 = (random.randint(Zone6[0][0], Zone6[0][1]),
          random.randint(Zone6[1][0], Zone6[1][1]))

path = [point1, point2, point3, point4, point5, point6]

input('palace robot and press touch to start')
wheeledbase.set_position(*startPoint, -pi/2)
print(path)

for point in path:
    wheeledbase.goto(*point)
    while not wheeledbase.isarrived():
        pass

wheeledbase.goto(*startPoint, -pi/2)
while not wheeledbase.isarrived():
    pass
