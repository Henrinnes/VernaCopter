import sys
import time
import numpy as np

# Ensure pycrazyswarm is in the Python path
sys.path.append("/home/henri/crazyswarm/ros_ws/src/crazyswarm/scripts")
from pycrazyswarm.crazyswarm_py import Crazyswarm

# Parameters
FLIGHT_HEIGHT = 0.5  # meters
RETURN_HOME = True   # Return to initial point after waypoints
LAUNCH_FILE = "/home/henri/crazyswarm/ros_ws/src/crazyswarm/launch/crazyflies.yaml"
def fly_waypoints(waypoints):
    if not waypoints:
        print("[ERROR] No waypoints provided.")
        return
    
    # Initialize swarm (uses default ../launch/crazyflies.yaml)
    swarm = Crazyswarm()

    

    timeHelper = swarm.timeHelper

    # Assumes only one CF is defined in crazyflies.yaml, like "cf9"
    cf = swarm.allcfs.crazyflies[0]
    start_pos = np.array(waypoints[0])

    # Takeoff
    print("[INFO] Taking off")
    cf.takeoff(targetHeight=FLIGHT_HEIGHT, duration=2.0)
    timeHelper.sleep(3.0)

    # Fly through waypoints
    for i, wp in enumerate(waypoints):
        print(f"[INFO] Flying to waypoint {i+1}: {wp}")
        cf.goTo(np.array(wp), yaw=0.0, duration=3.0)
        timeHelper.sleep(3.0)

    # Return to start
    if RETURN_HOME:
        print("[INFO] Returning to start")
        cf.goTo(start_pos, yaw=0.0, duration=3.0)
        timeHelper.sleep(3.0)

    # Land
    print("[INFO] Landing")
    cf.land(targetHeight=0.02, duration=2.0)
    timeHelper.sleep(3.0)

    print("[INFO] Mission complete")

   

