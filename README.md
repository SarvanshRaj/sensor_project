# IoT Multi-Layer Sensor & Network Monitor

A 5-layer monitoring system built on Raspberry Pi 3B+ and Arduino Uno, logging data to a 1TB External HDD.

## 🏗️ Architecture
- **Layer 1 (Sensing):** Arduino Uno reading DHT11 (Temp/Hum), NTC Thermistor (Backup), and Light Sensor.
- **Layer 2 (Collection):** Python script on Pi validating data (DHT11 primary, NTC backup).
- **Layer 3 (Network):** Independent Python services for Ping (10 servers) and Hourly Speedtests.
- **Layer 4 (Storage):** InfluxDB 2.x with the data directory mapped to a 931.5G External HDD.
- **Layer 5 (Visualization):** Grafana Dashboards for real-time monitoring.

## 🚀 Setup
1. **Hardware:** Follow the wiring diagram for Arduino pins D2, A0, and A1.
2. **Database:** Install InfluxDB 2 and mount your external HDD to `/mnt/data`.
3. **Python:** ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt```
4. **Services:** Copy the .service files to /etc/systemd/system/ and enable them.
