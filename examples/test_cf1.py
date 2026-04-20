import time
import cflib.crtp
from cflib.crazyflie import Crazyflie

URI = "radio://0/80/2M/E7E7E7E701"

def connected(uri):
    print("Connected to", uri)

def disconnected(uri):
    print("Disconnected")

cflib.crtp.init_drivers(enable_debug_driver=False)

cf = Crazyflie(rw_cache="./cache")
cf.connected.add_callback(connected)
cf.disconnected.add_callback(disconnected)

print("Connecting...")
cf.open_link(URI)

time.sleep(3)

cf.close_link()
print("Done")
