"""
Auto_crazy_vcon.py

Runs the full VernaCopter + Crazyflie (via Crazyswarm) pipeline automatically.
"""
import sys
sys.path.append("/home/henri/crazyswarm/ros_ws/src/crazyswarm/scripts")
from pycrazyswarm.crazyswarm_py import Crazyswarm

from basics.config import One_shot_parameters
from main import main
from experiments.save_results import save_results
from examples.Control_Vcon import fly_waypoints
import numpy as np

scenario_name = "treasure_hunt"  # or "reach_avoid"
pars = One_shot_parameters(scenario_name=scenario_name)

try:
    # Step 1: Plan trajectory
    messages, task_accomplished, all_x = main(pars)

    # Step 2: Convert to list of (x, y, z) tuples
    waypoints = list(zip(all_x[0], all_x[1], all_x[2]))

    # Step 3: Scale for physical environment
    SCALE_FOR_REAL_ENV = True
    SCALE_FACTOR = 0.3
    if SCALE_FOR_REAL_ENV:
        waypoints = [(x * SCALE_FACTOR, y * SCALE_FACTOR, z * SCALE_FACTOR) for (x, y, z) in waypoints]

    # Step 4: Send to Crazyflie
    if task_accomplished:
        fly_waypoints(waypoints)
    else:
        print("[WARNING] Task failed — skipping flight.")

except Exception as e:
    print("[ERROR]", e)
    task_accomplished = False
    messages = []
    waypoints = []

# Step 5: Save logs
if pars.save_results:
    save_results(pars, messages, task_accomplished, waypoints)

print("[INFO] Auto mission complete. Results saved.")
