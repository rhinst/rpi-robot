import time
from itertools import cycle

from app.subsystem import Subsystem
from app.message_bus.connection import Connection
from app.subsystem.GPIO import GPIO
from app.logging import logger


SPEED_OF_LIGHT = 34300


class Sonar(Subsystem):
    trigger_pin: int
    echo_pin: int
    distance: float

    def __init__(self, message_bus: Connection, trigger_pin: int, echo_pin: int):
        super().__init__(message_bus)
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self) -> float:
        return self.distance

    def measure_distance(self):
        GPIO.output(self.trigger_pin, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(self.trigger_pin, GPIO.LOW)
        pulse_start = time.time()
        while GPIO.input(self.echo_pin) == GPIO.LOW:
            pulse_start = time.time()
        pulse_end = time.time()
        while GPIO.input(self.echo_pin) == GPIO.HIGH:
            pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        self.distance = round(pulse_duration * (SPEED_OF_LIGHT / 2), 2)
        time.sleep(0.001)

    def run(self):
        GPIO.output(self.trigger_pin, GPIO.LOW)
        # wait for sensor to settle
        time.sleep(2)
        while cycle([True]):
            self.measure_distance()

    def cleanup(self):
        logger.debug("Sonar subsystem terminating")
        GPIO.cleanup()
