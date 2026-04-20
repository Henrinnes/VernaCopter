import usb.core
import usb.backend.libusb1
import libusb_package

# Force PyUSB to use the libusb DLL that comes with libusb-package
backend = usb.backend.libusb1.get_backend(find_library=libusb_package.find_library)

print("Backend is None?", backend is None)
print("Backend:", backend)

if backend is None:
    raise SystemExit("ERROR: libusb backend not found. (PyUSB cannot access libusb-1.0.dll)")

devs = list(usb.core.find(find_all=True, backend=backend))
print("USB devices found:", len(devs))

# Show a few device IDs to confirm it is working
for d in devs[:10]:
    print(f"VID={hex(d.idVendor)} PID={hex(d.idProduct)}")
