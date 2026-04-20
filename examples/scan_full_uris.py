import cflib.crtp

cflib.crtp.init_drivers(enable_debug_driver=False)

print("Scanning for Crazyflies (raw output)...")
raw = cflib.crtp.scan_interfaces()
print("RAW:", raw)

# Flatten helper
def flatten(x):
    out = []
    for item in x:
        if isinstance(item, (list, tuple)):
            out.extend(flatten(item))
        else:
            out.append(item)
    return out

flat = [s for s in flatten(raw) if isinstance(s, str) and s.strip()]
print("\nFLAT:", flat)

# Keep only radio URIs
uris = sorted({s for s in flat if s.startswith("radio://")})
print("\n==== RADIO URIs ====")
if not uris:
    print("No URIs found. Make sure at least one Crazyflie is powered on.")
else:
    for u in uris:
        print(u)
