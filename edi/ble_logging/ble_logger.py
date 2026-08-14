"""
EDI Week 2 - Module C: BLE Contact Logging
-------------------------------------------
WHAT THIS DOES (in plain words):
Your laptop already has a Bluetooth Low Energy (BLE) radio. Nearby devices
(phones, earbuds, smartwatches, other laptops) constantly "advertise"
themselves over BLE - they broadcast a small packet saying "I'm here."

This script listens for those broadcasts every couple of seconds and, for
every device it hears, writes down 4 things to a CSV file:
    1. pseudonymous_id   - a scrambled version of the device's address
                            (never the real address - this protects privacy)
    2. rssi_dbm          - signal strength (bigger/less-negative = closer)
    3. timestamp         - when we saw it
    4. duration_seconds  - how long we've been continuously seeing this
                            same device (resets if it disappears for a while)

WHY A LAPTOP AND NOT THE ESP32 YET?
The plan's real target device is an ESP32 (Module C's "flash devices" step).
Since the ESP32 boards haven't arrived, this script is a stand-in that
still produces REAL data from REAL nearby BLE devices - it just uses your
laptop's Bluetooth radio instead of the ESP32's. The CSV columns are kept
identical to what the ESP32 version will produce (see
esp32_ble_logger_reference.ino), so when the hardware arrives, you swap the
data source but nothing downstream (Week 5's DEAM pipeline, etc.) has to
change.

HOW TO RUN THIS (step by step):
1. Make sure you have Python 3.9 or newer:  python3 --version
2. Install the one library this needs:      pip install bleak
   (bleak = "BLE Agnostic Klient" - a cross-platform Python BLE library.
   Works on Windows, macOS, and Linux.)
3. Turn on Bluetooth on your laptop, and ideally have your phone nearby
   with its Bluetooth on too, so there's something to detect.
4. Run:  python ble_logger.py
5. Let it run for a few minutes. Walk around, bring your phone closer/
   farther away if you want to see the RSSI and duration change.
6. Press Ctrl+C to stop. Open ble_log.csv - that file is your Week 2
   deliverable: "at least one device logging real data."
"""

import asyncio
import csv
import hashlib
import time
from datetime import datetime

from bleak import BleakScanner

# ---- settings you can tweak -------------------------------------------
LOG_FILE = "ble_log.csv"
SESSION_TIMEOUT = 10   # seconds: if a device disappears for longer than
                        # this, we treat its next appearance as a NEW
                        # "encounter" (duration resets to 0). This mirrors
                        # the FSM's COOLDOWN -> IDLE idea from DEAM Module A.
SCAN_INTERVAL = 2       # seconds per scan cycle
# -------------------------------------------------------------------------

# Remembers, for each device we're currently "in contact with":
#   first_seen -> when this current encounter started
#   last_seen  -> the last time we heard from it
device_sessions = {}


def make_pseudo_id(mac_address: str) -> str:
    """
    Turn a real BLE MAC address into a short, one-way (non-reversible) ID.

    We run the MAC address through SHA-256 (a hashing function: same input
    always gives the same output, but you can't work backwards from the
    output to recover the input) and keep the first 12 hex characters.
    That's enough characters that two different nearby devices essentially
    never collide, but short enough to be readable in the CSV.

    We NEVER write the raw MAC address anywhere - only this hashed ID.
    """
    hashed = hashlib.sha256(mac_address.encode()).hexdigest()
    return hashed[:12]


def log_row(pseudo_id: str, rssi: int, timestamp: str, duration: float) -> None:
    """Append a single reading to the CSV file."""
    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([pseudo_id, rssi, timestamp, round(duration, 1)])


async def scan_loop() -> None:
    # Write the header row once, at the very start (this also clears any
    # old file from a previous run).
    with open(LOG_FILE, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["pseudonymous_id", "rssi_dbm", "timestamp", "duration_seconds"])

    print(f"Scanning for BLE devices every {SCAN_INTERVAL}s. Press Ctrl+C to stop.")
    print(f"Logging to: {LOG_FILE}\n")

    while True:
        # return_adv=True gives us both the device AND its advertisement
        # data (which is where RSSI actually lives in current bleak
        # versions) in one call.
        discovered = await BleakScanner.discover(timeout=SCAN_INTERVAL, return_adv=True)

        now = time.time()
        now_str = datetime.now().isoformat(timespec="seconds")

        for device, adv_data in discovered.values():
            pseudo_id = make_pseudo_id(device.address)
            rssi = adv_data.rssi

            session = device_sessions.get(pseudo_id)
            if session is None or (now - session["last_seen"]) > SESSION_TIMEOUT:
                # Either we've never seen this device before, or it's been
                # gone too long -> this counts as a brand-new encounter.
                device_sessions[pseudo_id] = {"first_seen": now, "last_seen": now}
            else:
                # Same ongoing encounter - just refresh last_seen.
                session["last_seen"] = now

            duration = now - device_sessions[pseudo_id]["first_seen"]

            log_row(pseudo_id, rssi, now_str, duration)
            print(f"[{now_str}] id={pseudo_id}  rssi={rssi} dBm  duration={duration:.1f}s")


if __name__ == "__main__":
    try:
        asyncio.run(scan_loop())
    except KeyboardInterrupt:
        print("\nStopped. Check ble_log.csv for your logged data.")