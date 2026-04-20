# # crazy_controller.py

# import time
# import logging
# from cflib.crazyflie import Crazyflie
# import cflib.crtp  # Initialize the low-level drivers
# from cflib.crazyflie.commander import Commander

# # Crazyflie radio URI
# URI = "radio://0/80/2M"

# # Flight behavior settings
# FLIGHT_HEIGHT = 0.5  # meters (used for takeoff hover)
# FLIGHT_SPEED = 0.5   # m/s
# RETURN_HOME = True   # Go back to start after mission

# logging.basicConfig(level=logging.ERROR)


# def fly_waypoints(waypoints):
#     if not waypoints:
#         print("[ERROR] No waypoints to fly.")
#         return

#     cflib.crtp.init_drivers(enable_debug_driver=False)
#     cf = Crazyflie(rw_cache="./cache")

#     def connect_callback(link_uri):
#         print(f"[INFO] Connected to {link_uri}")

#     def disconnect_callback(link_uri):
#         print(f"[INFO] Disconnected from {link_uri}")

#     cf.connected.add_callback(connect_callback)
#     cf.disconnected.add_callback(disconnect_callback)

#     print("[INFO] Connecting to Crazyflie...")
#     cf.open_link(URI)
#     time.sleep(2)

#     commander = cf.commander
#     start = waypoints[0]

#     try:
#         print("[INFO] Taking off...")
#         commander.send_hover_setpoint(0, 0, 0, FLIGHT_HEIGHT)
#         time.sleep(2)

#         for i, wp in enumerate(waypoints):
#             x, y, z = wp[:3]
#             commander.send_position_setpoint(x, y, z, 0)
#             print(f"[INFO] Flying to waypoint {i+1}: ({x:.2f}, {y:.2f}, {z:.2f})")
#             time.sleep(1.5)

#         if RETURN_HOME:
#             print("[INFO] Returning to home...")
#             x, y, z = start
#             commander.send_position_setpoint(x, y, z, 0)
#             time.sleep(2)

#         print("[INFO] Landing...")
#         commander.send_hover_setpoint(0, 0, 0, 0)
#         time.sleep(2)

#     finally:
#         cf.close_link()
#         print("[INFO] Mission complete.")

import time
import logging
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

logging.basicConfig(level=logging.ERROR)

DEFAULT_HEIGHT = 0.35   # keep your proven value
SEGMENT_TIME = 1.0      # seconds per waypoint segment (tune)

def fly_waypoints(waypoints, uri, default_height=DEFAULT_HEIGHT, segment_time=SEGMENT_TIME):
    """
    Fly a list of (x, y, z) waypoints using MotionCommander (Flow deck).
    - uri: full URI e.g. radio://0/80/2M/E7E7E7E701
    Waypoints are assumed to be in meters in the Flow-deck horizontal frame.
    """
    if not waypoints:
        print("[ERROR] No waypoints to fly.")
        return

    cflib.crtp.init_drivers(enable_debug_driver=False)
    cf = Crazyflie(rw_cache="./cache")

    # Start from current position assumption: first waypoint is "near" origin.
    # We'll fly by commanding relative velocities between successive waypoints.
    with SyncCrazyflie(uri, cf=cf) as scf:
        print(f"[INFO] Connected to {uri}")

        with MotionCommander(scf, default_height=default_height) as mc:
            print("[INFO] Takeoff/hover established.")

            # Fly waypoint-to-waypoint using constant velocity over segment_time
            prev = waypoints[0]
            time.sleep(0.5)

            for i, wp in enumerate(waypoints[1:], start=2):
                x0, y0, z0 = prev
                x1, y1, z1 = wp

                vx = (x1 - x0) / segment_time
                vy = (y1 - y0) / segment_time
                vz = (z1 - z0) / segment_time

                print(f"[INFO] Segment to wp{i}: v=({vx:.2f},{vy:.2f},{vz:.2f}) for {segment_time:.2f}s")
                mc.start_linear_motion(vx, vy, vz)
                time.sleep(segment_time)
                mc.start_linear_motion(0.0, 0.0, 0.0)
                time.sleep(0.1)

                prev = wp

            print("[INFO] Finished waypoints, hovering briefly...")
            time.sleep(1.0)

        print("[INFO] Landed.")
