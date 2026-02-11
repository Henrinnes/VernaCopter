#testcrazy.py
import time
import logging
from cflib.crazyflie import Crazyflie
import cflib.crtp

logging.basicConfig(level=logging.INFO)

# Initialize the low-level drivers
cflib.crtp.init_drivers()

# Scan common channels and speeds
channels = [80, 90, 100]
speeds = ['250K', '1M', '2M']

found_uri = None

for ch in channels:
    for speed in speeds:
        uri = f"radio://0/{ch}/{speed}"
        print(f"[INFO] Trying {uri}...")
        cf = Crazyflie()
        try:
            cf.open_link(uri)
            time.sleep(2.0)
            if cf.is_connected():
                print(f"[SUCCESS] Connected to Crazyflie on {uri}")
                found_uri = uri
                cf.close_link()
                break
        except Exception as e:
            print(f"[ERROR] Failed on {uri}: {e}")
        finally:
            cf.close_link()
        time.sleep(0.5)

    if found_uri:
        break  # exit outer loop too

if found_uri:
    print(f"[RESULT] Crazyflie found on {found_uri}")
else:
    print("[RESULT] No Crazyflie found on tested channels.")

print("[DONE]")

