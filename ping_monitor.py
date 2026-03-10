import time
from icmplib import multiping
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- CONFIGURATION ---
TOKEN = "uKtBrVVhiyW0C_HVXmQxQTC-wQc8qLmrHz_yXAJH48uIYpcWq5RnEoucDi5g2vbZ9X6JuUw_7wEqnugQ935vJA=="
ORG = "home_lab"
BUCKET = "sensor_data"
URL = "http://localhost:8086"

# The 10 servers you want to monitor
SERVERS = [
    '8.8.8.8',          # Google DNS
    '1.1.1.1',          # Cloudflare DNS
    '9.9.9.9',          # Quad9
    'github.com',       # GitHub
    'amazon.com',       # Amazon
    'raspberrypi.org',  # Raspberry Pi
    'google.com',       # Google Search
    'wikipedia.org',    # Wikipedia
    'discord.com',      # Discord
    'netflix.com'       # Netflix
]

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def run_ping_monitor():
    print(f"Starting Network Ping Monitor for {len(SERVERS)} servers...")
    while True:
        try:
            # Ping all servers at once
            results = multiping(SERVERS, count=3, interval=0.2, timeout=2)
            
            for result in results:
                point = (
                    Point("network_ping")
                    .tag("target", result.address)
                    .field("latency_ms", float(result.avg_rtt))
                    .field("packet_loss", float(result.packet_loss))
                    .time(time.time_ns(), WritePrecision.NS)
                )
                write_api.write(bucket=BUCKET, record=point)
            
            print(f"Network Latency Logged at {time.ctime()}")
            time.sleep(300)  # Wait 5 minutes (300 seconds)
            
        except Exception as e:
            print(f"Ping Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_ping_monitor()
