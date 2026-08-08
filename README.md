HEAD
# USB Threat Detector

A real-time USB device monitoring tool for Windows that detects device
connect/disconnect events as they happen and flags any device not on a
trusted whitelist.

## How it works

- Uses Windows Management Instrumentation (WMI) to subscribe to live
  device-change events -- no polling, detection happens the instant a
  device connects or disconnects.
- Compares each newly connected device's name against a configurable
  whitelist. Unrecognized devices are flagged; disconnects are logged too.
- Every event (allowed, flagged, or disconnected) is written to a CSV
  audit log with a timestamp for later review.

## Tech stack

- Python 3
- wmi / pywin32 for Windows device event access

## Setup

pip install pywin32 wmi
python usb_threat_detector.py

Edit the WHITELIST list in usb_threat_detector.py with your own trusted
device names before running.

## Status

Actively used and tested with live connect/disconnect cycles on Windows 11.


