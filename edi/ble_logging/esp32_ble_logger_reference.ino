/*
  EDI Week 2 - Module C: ESP32 BLE Contact Logger (REFERENCE TEMPLATE)
  -----------------------------------------------------------------------
  STATUS: NOT TESTED - hardware not available yet.

  This is a template for when your ESP32 boards arrive. It uses the
  ESP32's built-in BLE scanning to do the SAME job as ble_logger.py
  (the laptop version you're actually using this week): for every nearby
  BLE device, note its address, signal strength (RSSI), and how long
  you've continuously seen it.
*/

#include <BLEDevice.h>
#include <BLEScan.h>
#include <BLEAdvertisedDevice.h>

int scanTime = 2;  // seconds per scan cycle - matches SCAN_INTERVAL in ble_logger.py
BLEScan* pBLEScan;

class MyAdvertisedDeviceCallbacks : public BLEAdvertisedDeviceCallbacks {
    void onResult(BLEAdvertisedDevice advertisedDevice) {
      String mac = advertisedDevice.getAddress().toString().c_str();
      int rssi = advertisedDevice.getRSSI();

      // TODO (before this is a real deliverable, not just a template):
      // Replace the raw MAC address with a hashed pseudonymous ID, the
      // same idea as make_pseudo_id() in ble_logger.py. On the ESP32 you
      // can use the built-in mbedtls SHA-256 functions, or simplest of
      // all: send the raw MAC over Serial to a laptop, and let a small
      // Python script do the hashing + CSV writing (re-using
      // make_pseudo_id() and log_row() from ble_logger.py almost as-is).
      Serial.print("mac(TEMP-not-hashed-yet)=");
      Serial.print(mac);
      Serial.print("  rssi=");
      Serial.println(rssi);

      // TODO: write pseudonymous_id, rssi, timestamp, duration_seconds
      // to the SAME CSV format ble_logger.py uses, either onto an SD
      // card or streamed to a laptop, so Week 5's pipeline can consume
      // ESP32 data and laptop-prototype data identically.
    }
};

void setup() {
  Serial.begin(115200);
  BLEDevice::init("");
  pBLEScan = BLEDevice::getScan();
  pBLEScan->setAdvertisedDeviceCallbacks(new MyAdvertisedDeviceCallbacks());
  pBLEScan->setActiveScan(true);
}

void loop() {
  BLEScanResults foundDevices = pBLEScan->start(scanTime, false);
  pBLEScan->clearResults();
  delay(100);
}