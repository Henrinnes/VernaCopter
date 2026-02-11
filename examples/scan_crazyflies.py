import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.swarm import CachedCfFactory, Swarm

# Initialize low-level drivers
cflib.crtp.init_drivers(enable_debug_driver=False)

# Scan for available Crazyflies
print("Scanning for Crazyflies...")
available = cflib.crtp.scan_interfaces()

if not available:
    print("No Crazyflies found. Check radio dongle and power.")
else:
    print("Found Crazyflies:")
    for uri in available:
        print(uri)
