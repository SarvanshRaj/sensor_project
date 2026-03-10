import serial
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- CONFIGURATION ---
TOKEN = "uKtBrVVhiyW0C_HVXmQxQTC-wQc8qLmrHz_yXAJH48uIYpcWq5RnEoucDi5g2vbZ9X6JuUw_7wEqnugQ935vJA==" 
ORG = "home_lab"
BUCKET = "sensor_data"
URL = "http://localhost:8086"
SERIAL_PORT = '/dev/ttyACM0'
BAUD_RATE = 9600

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def run_collector():
    print(f"Connecting to Arduino on {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
        time.sleep(2)
        ser.flush()
        
        while True:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').strip()
                if not line or line.startswith('#'): continue
                
                parts = line.split(',')
                if len(parts) == 5:
                    dht_t, hum, light, ntc_t = parts[1], parts[2], parts[3], parts[4]

                    # 1. DISCARD logic: Humidity is mandatory
                    if hum == "ERR":
                        print("Discarded: Humidity is ERR")
                        continue

                    # 2. FAILOVER logic: DHT11 is Primary, NTC is Backup
                    if dht_t != "ERR":
                        final_temp = float(dht_t)
                        source = "DHT11"
                    elif ntc_t != "ERR":
                        final_temp = float(ntc_t)
                        source = "NTC"
                    else:
                        print("Discarded: No temperature source available")
                        continue

                    # 3. Save to InfluxDB (using parentheses to avoid IndentationError)
                    point = (
                        Point("room_environment")
                        .tag("temp_source", source)
                        .field("temperature", float(final_temp))
                        .field("humidity", float(hum))
                        .field("light", int(light))
                        .time(time.time_ns(), WritePrecision.NS)
                    )
                    
                    write_api.write(bucket=BUCKET, record=point)
                    print(f"[{source}] Stored: {final_temp}°C | {hum}% Hum | Light {light}")
                    
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run_collector()
