from gpiozero import DistanceSensor

class UltrasonicSensor:
    def __init__(self, trigger_pin=23, echo_pin=24, max_distance=2):
        self.sensor = DistanceSensor(echo=echo_pin, trigger=trigger_pin, max_distance=max_distance)

    def get_distance_cm(self):
        return round(self.sensor.distance * 100, 2)

    def is_occupied(self, threshold_cm=10):
        return self.get_distance_cm() < threshold_cm

    def cleanup(self):
        self.sensor.close()
