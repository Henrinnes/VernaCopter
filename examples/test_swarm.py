# import cflib.crtp
# from cflib.crazyflie.swarm import Swarm

# uris = [
#     "radio://0/80/2M/E7E7E7E701",
#     "radio://0/80/2M/E7E7E7E702",
#     "radio://0/80/2M/E7E7E7E703",
#     "radio://0/80/2M/E7E7E7E704",
# ]

# cflib.crtp.init_drivers(enable_debug_driver=False)

# def log_connection(scf):
#     print("Connected to", scf._link_uri)

# with Swarm(uris) as swarm:
#     swarm.parallel_safe(log_connection)

# print("All drones connected successfully.")

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.swarm import Swarm, CachedCfFactory

uris = [
    "radio://0/80/2M/E7E7E7E701",
    "radio://0/80/2M/E7E7E7E702",
    "radio://0/80/2M/E7E7E7E703",
    "radio://0/80/2M/E7E7E7E704",
]

cflib.crtp.init_drivers(enable_debug_driver=False)

# This is the correct way to provide cache to all CF instances
factory = CachedCfFactory(rw_cache="./cache")

def log_connection(scf):
    print("Connected to", scf._link_uri)

with Swarm(uris, factory=factory) as swarm:
    swarm.parallel_safe(log_connection)

print("All drones connected successfully.")


