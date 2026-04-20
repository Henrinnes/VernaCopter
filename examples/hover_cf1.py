import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.high_level_commander import HighLevelCommander

URI = "radio://0/80/2M/E7E7E7E701"

# Conservative flight parameters
TAKEOFF_Z = 0.3     # meters
TAKEOFF_T = 2.0     # seconds
HOVER_T = 3.0       # seconds
LAND_T = 2.5        # seconds

cflib.crtp.init_drivers(enable_debug_driver=False)

# Create Crazyflie object with a writable cache directory
cf = Crazyflie(rw_cache="./cache")

with SyncCrazyflie(URI, cf=cf) as scf:
    hlc = HighLevelCommander(scf.cf)

    print("Taking off...")
    hlc.takeoff(TAKEOFF_Z, TAKEOFF_T)
    time.sleep(TAKEOFF_T + 0.5)

    print("Hovering...")
    time.sleep(HOVER_T)

    print("Landing...")
    hlc.land(0.0, LAND_T)
    time.sleep(LAND_T + 0.5)

    print("Stopping...")
    hlc.stop()
    time.sleep(0.2)

print("Done.")
