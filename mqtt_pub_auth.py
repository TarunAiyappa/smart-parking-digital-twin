import time
import random
import csv
import paho.mqtt.client as mqtt
from sensor_utils import UltrasonicSensor
from datetime import datetime
import os

BROKER = "localhost"
TOPIC = "parking/sensor"

log_dir = "/home/tarun/Research/test3/logs"
os.makedirs(log_dir, exist_ok=True)
csv_file = open(f"{log_dir}/sensor_log.csv", mode="a", newline="")
csv_writer = csv.writer(csv_file)
csv_writer.writerow(["timestamp", "sensor_id", "status", "distance_cm"])

sensor1 = UltrasonicSensor()
client = mqtt.Client()
client.username_pw_set("admin", "admin")  # Added auth here
client.connect(BROKER, 1883, 60)

try:
    while True:
        distance1 = sensor1.get_distance_cm()
        status1 = "Occupied" if sensor1.is_occupied() else "Available"
        message1 = f"1,{status1}"
        client.publish(TOPIC, message1)
        print(f"Sensor 1 (Real): {status1} (Distance: {distance1:.2f} cm)")
        csv_writer.writerow([datetime.now(), 1, status1, distance1])

        for sensor_id in range(2, 5):
            distance = random.uniform(5, 50)
            status = "Occupied" if distance < 10 else "Available"
            message = f"{sensor_id},{status}"
            client.publish(TOPIC, message)
            print(f"Sensor {sensor_id} (Simulated): {status} (Distance: {distance:.2f} cm)")
            csv_writer.writerow([datetime.now(), sensor_id, status, distance])

        csv_file.flush()
        time.sleep(1)
except KeyboardInterrupt:
    print("\nMQTT Publisher stopped by user.")
finally:
    sensor1.cleanup()
    csv_file.close()
    print("Sensor cleaned up and CSV file closed.")
