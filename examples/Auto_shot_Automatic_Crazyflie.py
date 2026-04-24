"""
Auto_shot_Automatic_Crazyflie.py

Runs the full VernaCopter pipeline and then deploys the trajectory on a
Crazyflie drone.  Works on Windows and Linux with just a Flow deck.

Usage:
    python -m examples.Auto_shot_Automatic_Crazyflie
"""

from basics.config import One_shot_parameters
from main import main
from experiments.save_results import save_results
from examples.fly_trajectory import fly_trajectory

scenario_name = "reach_avoid"   # or "treasure_hunt"
pars = One_shot_parameters(scenario_name=scenario_name)

try:
    # Step 1: Plan trajectory via VernaCopter
    messages, task_accomplished, all_x = main(pars)

    # Step 2: Deploy on drone if task succeeded
    if task_accomplished and pars.deploy_on_drone:
        fly_trajectory(
            all_x,
            uri=pars.drone_uri,                   # None = auto-scan
            scale_factor=pars.scale_factor,
            waypoint_duration=pars.waypoint_duration,
            takeoff_height=pars.takeoff_height,
        )
    elif not task_accomplished:
        print("[WARNING] Task was not accomplished — skipping flight.")

except Exception as e:
    print("[ERROR]", e)
    task_accomplished = False
    messages = []

# Step 3: Save experiment results
if pars.save_results:
    save_results(pars, messages, task_accomplished, [])
