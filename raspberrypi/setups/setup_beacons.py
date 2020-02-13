from beacons.global_sync import ClientGS
from logs.log_manager import *

LogManager().start()

try:
    beacons1 = ClientGS(1, ip ='127.0.0.1')
    beacons1.connect()
    beacons1.reset_ressources()
except TimeoutError:
    pass

try:
    beacons2 = ClientGS(2, ip ='127.0.0.1')
    beacons2.connect()
    beacons2.reset_ressources()
except TimeoutError:
    pass

