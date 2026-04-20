import time
import cflib.crtp
from cflib.crazyflie import Crazyflie

URI = "radio://0/80/2M/E7E7E7E7E7"

def connected(link_uri):
    print("Connected to", link_uri)

def connection_failed(link_uri, msg):
    print("Connection failed:", msg)

def disconnected(link_uri):
    print("Disconnected")

print("Initializing drivers...")
cflib.crtp.init_drivers(enable_debug_driver=False)

cf = Crazyflie(rw_cache="./cache")

cf.connected.add_callback(connected)
cf.connection_failed.add_callback(connection_failed)
cf.disconnected.add_callback(disconnected)

print("Opening link...")
cf.open_link(URI)

time.sleep(5)

cf.close_link()
print("Done")
