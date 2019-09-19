from beacons.global_sync import ClientGS

try:
    beacons = ClientGS(1)
    beacons.connect()
    beacons.reset_ressources()
except TimeoutError:
    pass
