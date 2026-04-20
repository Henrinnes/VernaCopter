# import time
# import cflib.crtp
# from cflib.crazyflie import Crazyflie
# from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# from cflib.positioning.motion_commander import MotionCommander

# URI = "radio://0/80/2M/E7E7E7E701"

# cflib.crtp.init_drivers(enable_debug_driver=False)

# cf = Crazyflie(rw_cache="./cache")

# with SyncCrazyflie(URI, cf=cf) as scf:
#     # MotionCommander will handle takeoff/hover/land using setpoints
#     print("Starting MotionCommander...")
#     with MotionCommander(scf, default_height=0.3) as mc:
#         print("Hovering...")
#         time.sleep(3)

#     print("Landed.")

# import time
# import cflib.crtp
# from cflib.crazyflie import Crazyflie
# from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# from cflib.positioning.motion_commander import MotionCommander

# URI = "radio://0/80/2M/E7E7E7E703"

# cflib.crtp.init_drivers(enable_debug_driver=False)
# cf = Crazyflie(rw_cache="./cache")

# with SyncCrazyflie(URI, cf=cf) as scf:
#     with MotionCommander(scf, default_height=0.3) as mc:
#         print("Hovering...")
#         time.sleep(5)          # longer hover
#         print("Preparing to land...")
#         time.sleep(0.5)          # settle before landing

# print("Done.")

# import time
# import cflib.crtp
# from cflib.crazyflie import Crazyflie
# from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
# from cflib.positioning.motion_commander import MotionCommander

# URI = "radio://0/80/2M/E7E7E7E703"

# cflib.crtp.init_drivers(enable_debug_driver=False)
# cf = Crazyflie(rw_cache="./cache")

# with SyncCrazyflie(URI, cf=cf) as scf:
#     with MotionCommander(scf, default_height=0.3) as mc:
#         print("Hovering...")
#         time.sleep(3)

#         print("Descending slowly...")
#         # slow vertical descent (m/s). Keep it small.
#         mc.start_linear_motion(0.0, 0.0, -0.15)
#         time.sleep(2.0)

#         print("Stop motion...")
#         mc.start_linear_motion(0.0, 0.0, 0.0)
#         time.sleep(0.5)

# print("Done.")



import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.positioning.motion_commander import MotionCommander

from _usb_backend_fix import ensure_libusb_dll_on_path
print("Using libusb DLL from:", ensure_libusb_dll_on_path())

URI = "radio://0/80/2M/E7E7E7E701"

cflib.crtp.init_drivers(enable_debug_driver=False)
cf = Crazyflie(rw_cache="./cache")

with SyncCrazyflie(URI, cf=cf) as scf:
    print("Connected:", URI)

    # Battery check
    try:
        bat = scf.cf.param.get_value("pm.vbat")
        print("Battery (V):", bat)
    except Exception as e:
        print("Battery read failed:", e)

    # Optional: reset Kalman estimator (if enabled)
    try:
        scf.cf.param.set_value("kalman.resetEstimation", "1")
        time.sleep(0.1)
        scf.cf.param.set_value("kalman.resetEstimation", "0")
        time.sleep(1.0)
        print("Estimator reset done.")
    except Exception as e:
        print("Estimator reset skipped:", e)

    print("Starting MotionCommander...")
    with MotionCommander(scf, default_height=0.35) as mc:
        print("Hovering...")
        time.sleep(5)

    print("Landed.")


