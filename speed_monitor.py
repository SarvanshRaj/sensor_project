import speedtest
import time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

# --- CONFIGURATION ---
TOKEN = "uKtBrVVhiyW0C_HVXmQxQTC-wQc8qLmrHz_yXAJH48uIYpcWq5RnEoucDi5g2vbZ9X6JuUw_7wEqnugQ935vJA=="
ORG = "home_lab"
BUCKET = "sensor_data"
URL = "http://localhost:8086"

client = InfluxDBClient(url=URL, token=TOKEN, org=ORG)
write_api = client.write_api(write_options=SYNCHRONOUS)

def run_speedtest():
    print("Starting Hourly Speedtest Monitor...")
    st = speedtest.Speedtest()

    while True:
        try:
            print("Testing speed (this takes a minute)...")
            st.get_best_server()
            download = st.download() / 1_000_000  # Convert to Mbps
            upload = st.upload() / 1_000_000      # Convert to Mbps
            ping = st.results.ping

            point = (
                Point("network_speed")
                .field("download_mbps", float(download))
                .field("upload_mbps", float(upload))
                .field("isp_ping", float(ping))
                .time(time.time_ns(), WritePrecision.NS)
            )

            write_api.write(bucket=BUCKET, record=point)
            print(f"Speed Logged: Down {download:.2f} Mbps | Up {upload:.2f} Mbps")

            # Wait 1 hour (3600 seconds)
            time.sleep(3600)

        except Exception as e:
            print(f"Speedtest Error: {e}")
            time.sleep(60)

if __name__ == "__main__":
    run_speedtest()
