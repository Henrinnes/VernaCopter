import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie

URI = "radio://0/80/2M/E7E7E7E701"

cflib.crtp.init_drivers(enable_debug_driver=False)

with SyncCrazyflie(URI, cf=Crazyflie(rw_cache="./cache")) as scf:
    print("Connected.")
    time.sleep(1)

    deck = scf.cf.param.get_value("deck.bcFlow2")
    print("Flow deck detected:", deck)
