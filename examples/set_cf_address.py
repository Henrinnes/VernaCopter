import sys
import time
import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.syncLogger import SyncLogger

DEFAULT_URI = "radio://0/80/2M/E7E7E7E7E7"

def set_address(new_addr_hex: str):
    # new_addr_hex must be like "E7E7E7E701"
    if len(new_addr_hex) != 10:
        raise ValueError("Address must be 10 hex chars, e.g., E7E7E7E701")

    # Convert hex string to 5 bytes
    addr_bytes = bytes.fromhex(new_addr_hex)

    cflib.crtp.init_drivers(enable_debug_driver=False)

    with SyncCrazyflie(DEFAULT_URI, cf=Crazyflie(rw_cache="./cache")) as scf:
        print(f"Connected to default URI. Setting address to {new_addr_hex} ...")
        # Set radio address parameter (stored in CF persistent memory)
        scf.cf.param.set_value("radio.address", str(int.from_bytes(addr_bytes, byteorder="little")))
        time.sleep(0.5)

        # Read back to confirm
        val = scf.cf.param.get_value("radio.address")
        print("radio.address (raw):", val)

    print("Done. Power-cycle the drone now.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python examples/set_cf_address.py E7E7E7E701")
        sys.exit(1)
    set_address(sys.argv[1])
