import paho.mqtt.client as mqtt
import time
from collections import defaultdict

BROKER = "10.0.0.165"  # ?? Replace with Pi's IP
TOPIC = "parking/sensor"

message_count = 0
sensor_stats = defaultdict(int)

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg):
    global message_count
    message_count += 1
    payload = msg.payload.decode()
    parts = payload.split(",")
    if len(parts) == 2:
        sensor_id = parts[0].strip()
        sensor_stats[sensor_id] += 1

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(BROKER, 1883, 60)
client.loop_start()

try:
    while True:
        time.sleep(1)
        print(f"[{time.strftime('%H:%M:%S')}] Messages received: {message_count}")
        for sid, count in sensor_stats.items():
            print(f"  - Sensor {sid}: {count} msgs/sec")
        message_count = 0
        sensor_stats.clear()
except KeyboardInterrupt:
    print("Logging stopped.")
    client.loop_stop()

