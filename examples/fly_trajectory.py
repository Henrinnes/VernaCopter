"""
fly_trajectory.py

Deploys a VernaCopter trajectory on a Crazyflie drone using HighLevelCommander.
Works on Windows and Linux with just a Flow deck (no motion capture needed).

Usage:
    Import fly_trajectory() and call it with the all_x array from main().
    URI is auto-discovered if not provided.
"""

import os
import sys
import time
import logging
import numpy as np

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.high_level_commander import HighLevelCommander
from cflib.utils.reset_estimator import reset_estimator

logging.basicConfig(level=logging.ERROR)


def _ensure_libusb():
    """Prepend the libusb DLL directory to PATH on Windows so cflib can find it."""
    if sys.platform != "win32":
        return
    try:
        import libusb_package
        dll_path = None
        for candidate in ["usb-1.0", "libusb-1.0"]:
            try:
                dll_path = libusb_package.find_library(candidate)
            except TypeError:
                dll_path = libusb_package.find_library(candidate)
            if dll_path:
                break
        if dll_path:
            dll_dir = os.path.dirname(dll_path)
            os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")
    except ImportError:
        pass  # libusb_package not installed; cflib will try its own fallback


def scan_for_drone():
    """Scan radio interfaces and return the URI of the first Crazyflie found."""
    print("[INFO] Scanning for Crazyflies...")
    raw = cflib.crtp.scan_interfaces()

    def _flatten(x):
        out = []
        for item in x:
            if isinstance(item, (list, tuple)):
                out.extend(_flatten(item))
            else:
                out.append(item)
        return out

    uris = [s for s in _flatten(raw) if isinstance(s, str) and s.startswith("radio://")]
    if not uris:
        raise RuntimeError(
            "No Crazyflie found. Make sure the Crazyradio is plugged in and the drone is powered on."
        )
    print(f"[INFO] Found: {uris}")
    return uris[0]


def prepare_waypoints(all_x, scale_factor, takeoff_height, max_waypoints=30):
    """
    Convert a VernaCopter trajectory (6xN) to a list of (x, y, z) tuples.

    - Subsamples to at most max_waypoints
    - Normalises so the drone starts at (0, 0) in x/y
    - Scales by scale_factor to fit the physical space
    - Clamps z to at least takeoff_height so the drone never tries to land mid-flight
    """
    positions = all_x[:3].T.copy()  # (N, 3)

    # Subsample evenly
    if len(positions) > max_waypoints:
        idx = np.linspace(0, len(positions) - 1, max_waypoints, dtype=int)
        positions = positions[idx]

    # Shift so the trajectory starts at the origin in x/y
    positions[:, 0] -= positions[0, 0]
    positions[:, 1] -= positions[0, 1]
    positions[:, 2] -= positions[0, 2]

    # Scale down to physical dimensions
    positions *= scale_factor

    # Floor z at takeoff height (drone must stay airborne)
    positions[:, 2] = np.clip(positions[:, 2], takeoff_height, None)

    return [tuple(float(v) for v in wp) for wp in positions]


def fly_trajectory(
    all_x,
    uri=None,
    scale_factor=0.3,
    waypoint_duration=2.5,
    takeoff_height=0.4,
):
    """
    Fly a VernaCopter trajectory on a Crazyflie.

    Parameters
    ----------
    all_x : np.ndarray, shape (6, N)
        Full state trajectory from VernaCopter (rows 0-2 are x, y, z positions).
    uri : str or None
        Radio URI of the target drone, e.g. "radio://0/80/2M/E7E7E7E701".
        Pass None to auto-discover the first available drone.
    scale_factor : float
        Multiplier applied to the trajectory so it fits the physical room.
        0.3 maps a 10 m simulated range to 3 m physical range.
    waypoint_duration : float
        Seconds allowed for each waypoint-to-waypoint move.
    takeoff_height : float
        Altitude (m) to hover at before the trajectory starts.
    """
    _ensure_libusb()
    cflib.crtp.init_drivers(enable_debug_driver=False)

    if uri is None:
        uri = scan_for_drone()

    waypoints = prepare_waypoints(all_x, scale_factor, takeoff_height)

    print(f"[INFO] Connecting to {uri}")
    print(f"[INFO] Trajectory: {len(waypoints)} waypoints, scale={scale_factor}")
    for i, wp in enumerate(waypoints):
        print(f"       wp{i+1:02d}: ({wp[0]:+.2f}, {wp[1]:+.2f}, {wp[2]:+.2f})")

    with SyncCrazyflie(uri, cf=Crazyflie(rw_cache="./cache")) as scf:
        cf = scf.cf

        try:
            bat = cf.param.get_value("pm.vbat")
            print(f"[INFO] Battery: {bat} V")
        except Exception:
            pass

        # Reset position estimator so (0,0,0) matches where the drone is sitting
        reset_estimator(cf)
        time.sleep(0.5)

        hlc = HighLevelCommander(cf)

        print(f"[INFO] Taking off to {takeoff_height:.2f} m...")
        hlc.takeoff(takeoff_height, duration_s=2.0)
        time.sleep(2.5)

        try:
            for i, (x, y, z) in enumerate(waypoints):
                print(f"[INFO] Waypoint {i+1}/{len(waypoints)}: ({x:+.2f}, {y:+.2f}, {z:+.2f})")
                hlc.go_to(x, y, z, yaw=0.0, duration_s=waypoint_duration)
                time.sleep(waypoint_duration + 0.3)

        except Exception as e:
            print(f"[ERROR] During flight: {e}")

        finally:
            print("[INFO] Landing...")
            hlc.land(0.0, duration_s=2.5)
            time.sleep(3.0)
            hlc.stop()

    print("[INFO] Mission complete.")
