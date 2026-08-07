"""
USB Threat Detector
--------------------
Monitors USB device connect/disconnect events in real time on Windows
and flags any device not on the trusted whitelist.

Install requirements first:
    pip install pywin32 wmi

Run with:
    python usb_threat_detector.py
(Run as Administrator for best results — WMI event access sometimes needs it.)
"""

import wmi
import csv
import os
from datetime import datetime

LOG_FILE = "usb_activity_log.csv"

# Add the Device IDs (or partial name matches) of USB devices you trust.
# You can find a device's ID in Device Manager -> right click device -> Properties -> Details -> Device Instance Path
WHITELIST = [
    "Integrated Camera",
    "Intel(R) Wireless Bluetooth(R)",
    "USB Root Hub",
    "USB Input Device",
    "VendorCo ProductCode USB Device",  # your USB drive
]

def is_trusted(device_name: str) -> bool:
    if not device_name:
        return False
    return any(trusted.lower() in device_name.lower() for trusted in WHITELIST)


def log_event(device_name: str, status: str):
    file_exists = os.path.isfile(LOG_FILE)
    with open(LOG_FILE, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Device Name", "Status"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), device_name, status])


def monitor_usb():
    print("[*] USB Threat Detector running. Watching for device changes...")
    print(f"[*] Logging to {LOG_FILE}\n")

    c = wmi.WMI()
    watcher = c.Win32_DeviceChangeEvent.watch_for()

    previous_devices = set()  # device IDs connected last time we checked

    while True:
        try:
            event = watcher()
            devices = c.Win32_PnPEntity(ConfigManagerErrorCode=0)
            usb_devices = [d for d in devices if d.PNPDeviceID and "USB" in d.PNPDeviceID]

            current_devices = {d.PNPDeviceID: d.Name for d in usb_devices}
            current_ids = set(current_devices.keys())

            # Devices that are new since last check = just connected
            newly_connected = current_ids - previous_devices
            # Devices that were there before but aren't now = just disconnected
            disconnected = previous_devices - current_ids

            for device_id in newly_connected:
                name = current_devices.get(device_id, "Unknown Device")
                if is_trusted(name):
                    status = "ALLOWED"
                    print(f"[OK]    {name}")
                else:
                    status = "FLAGGED - UNTRUSTED DEVICE"
                    print(f"[ALERT] Unrecognized USB device connected: {name}")
                log_event(name, status)

            for device_id in disconnected:
                print(f"[INFO]  Device disconnected: {device_id}")
                log_event(device_id, "DISCONNECTED")

            previous_devices = current_ids

        except KeyboardInterrupt:
            print("\n[*] Stopping USB Threat Detector.")
            break
        except Exception as e:
            print(f"[!] Error: {e}")


if __name__ == "__main__":
    monitor_usb()