import time
import cflib.crtp
from cflib.crazyflie.swarm import Swarm, CachedCfFactory

uris = [
    "radio://0/80/2M/E7E7E7E701",
    "radio://0/80/2M/E7E7E7E702",
    "radio://0/80/2M/E7E7E7E703",
    "radio://0/80/2M/E7E7E7E704",
]

cflib.crtp.init_drivers(enable_debug_driver=False)
factory = CachedCfFactory(rw_cache="./cache")

def check_flow(scf):
    time.sleep(0.5)
    try:
        v = scf.cf.param.get_value("deck.bcFlow2")
        print(scf._link_uri, "deck.bcFlow2 =", v)
    except Exception as e:
        print(scf._link_uri, "Flow check failed:", e)

with Swarm(uris, factory=factory) as swarm:
    swarm.parallel_safe(check_flow)

print("Done.")
