import os

def ensure_libusb_dll_on_path() -> str:
    """
    Force PyUSB/cflib to find libusb on Windows by prepending the DLL directory to PATH.
    Uses libusb_package.find_library(...) which is the most reliable across layouts.
    """
    import libusb_package  # installed in your venv

    # Different versions require different candidate strings
    candidates = ["usb-1.0", "libusb-1.0"]
    dll_path = None

    for c in candidates:
        try:
            dll_path = libusb_package.find_library(c)
        except TypeError:
            # Some versions have a different signature; try again with the same candidate
            dll_path = libusb_package.find_library(c)
        if dll_path:
            break

    if not dll_path:
        raise RuntimeError("libusb_package.find_library could not locate libusb DLL")

    dll_dir = os.path.dirname(dll_path)
    os.environ["PATH"] = dll_dir + os.pathsep + os.environ.get("PATH", "")
    return dll_dir