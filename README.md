# 5-Layer IoT Environment & Network Monitor
**Developer:** Sarvansh Raj (CMS Lucknow)
**Target:** Engineering Systems & Computer Science

## 🏗️ Technical Architecture
This project implements a high-availability monitoring system across 5 logical layers:

* **Layer 1 (Sensing):** Arduino Uno reading DHT11 (Primary), NTC Thermistor (Failover), and HL-01 Light Sensor.
* **Layer 2 (Collection):** Python-based validation on RPi 3B+. Implements logic to prioritize DHT11 and use NTC for cross-validation.
* **Layer 3 (Network):** Autonomous background services for ISP latency (Multiping) and hourly Speedtests.
* **Layer 4 (Storage):** InfluxDB 2.x with the engine path mapped to a **931.5GB External HDD** to prevent SD card wear.
* **Layer 5 (Visualization):** Grafana dashboards for real-time analytics.

## 🛠️ Features
- **Sensor Failover:** Logic-based temperature selection (DHT11 > NTC).
- **Data Integrity:** Discards incomplete readings if humidity data is missing.
- **Production-Ready:** All components run as `systemd` background services.


<img width="572" height="629" alt="image" src="https://github.com/SarvanshRaj/sensor_project/blob/main/image.png?raw=true" />
