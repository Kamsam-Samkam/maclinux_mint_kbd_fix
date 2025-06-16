#!/usr/bin/env python3

import os
import sys
import time
import evdev
from evdev import InputDevice, categorize, ecodes
import subprocess

def find_mac_keyboard_event():
    for path in evdev.list_devices():
        dev = evdev.InputDevice(path)
        if "Mac" in dev.name and "Keyboard" in dev.name:
            return path
    return None
"""
def run_evtest(device_path):
    # Run evtest silently, just enough to trigger reinitialization
    subprocess.Popen(['evtest', device_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # Let it run briefly, then kill it
    subprocess.run(['sleep', '1'])
    subprocess.run(['pkill', '-f', f'evtest {device_path}'])
"""
def run_evtest(device_path):
    # First run (immediate)
    subprocess.Popen(['evtest', device_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sleep', '0.5'])
    subprocess.run(['pkill', '-f', f'evtest {device_path}'])

    # Second run (delayed) to ensure state applies
    subprocess.Popen(['evtest', device_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['sleep', '0.5'])
    subprocess.run(['pkill', '-f', f'evtest {device_path}'])

def wait_for_keyboard():
    print("⏳ Waiting for Mac keyboard to become available...")
    for _ in range(30):  # wait up to 30 seconds
        path = find_mac_keyboard_event()
        if path:
            print(f"✅ Found Mac keyboard at: {path}")
            return path
        time.sleep(1)
    print("❌ Mac keyboard not found after waiting.")
    return None


def main():
    event_path = wait_for_keyboard() # earlier is was  event_path = find_mac_keyboard_event()
    if not event_path:
        # print("❌ Mac keyboard not found.")
        return

    dev = evdev.InputDevice(event_path)
    print(f"✅ Listening for Caps Lock presses on: {event_path}")

    for event in dev.read_loop():
        if (
            event.type == evdev.ecodes.EV_KEY and
            event.code == evdev.ecodes.KEY_CAPSLOCK and
            event.value == 1  # Only key *presses*, not releases or repeats
        ):
            print("⚠️ Caps Lock pressed — fixing layout now.")
            run_evtest(event_path)
"""
def main():
    event_path = find_mac_keyboard_event()
    if not event_path:
        print("❌ Mac keyboard not found.")
        return

    dev = evdev.InputDevice(event_path)
    print(f"✅ Listening for Caps Lock on: {event_path}")

    for event in dev.read_loop():
        if event.type == evdev.ecodes.EV_KEY and event.code == evdev.ecodes.KEY_CAPSLOCK:
            if event.value == 1:  # Key press
                print("⚠️ Caps Lock pressed — fixing layout now.")
                run_evtest(event_path)
"""
main()

