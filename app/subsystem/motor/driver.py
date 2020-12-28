from dataclasses import dataclass
from enum import Enum

from app.subsystem import Subsystem
from app.command import Command, Argument
from app.message_bus.connection import Connection
from app.message_bus.message import CommandMessage
from app.subsystem.GPIO import GPIO


class MotorDirection(Enum):
    FORWARD = 1
    BACKWARD = 2


@dataclass
class MotorState:
    speed: float
    direction: MotorDirection


@dataclass
class MotorPins:
    front_left_dir: int
    front_left_speed: int
    front_right_dir: int
    front_right_speed: int
    rear_left_dir: int
    rear_left_speed: int
    rear_right_dir: int
    rear_right_speed: int


class Driver(Subsystem):
    pins: MotorPins
    fl_pwm: GPIO.PWM
    fr_pwm: GPIO.PWM
    rl_pwm: GPIO.PWM
    rr_pwm: GPIO.PWM

    def __init__(self, message_bus: Connection, pins: MotorPins):
        super().__init__(message_bus)
        self.pins = pins
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(
            [
                pins.front_left_dir,
                pins.front_left_speed,
                pins.front_right_dir,
                pins.front_right_speed,
                pins.rear_left_dir,
                pins.rear_left_speed,
                pins.rear_right_dir,
                pins.rear_right_speed,
            ],
            GPIO.OUT
        )
        self.fl_pwm = GPIO.PWM(pins.front_left_speed, 1000)
        self.fr_pwm = GPIO.PWM(pins.front_right_speed, 1000)
        self.rl_pwm = GPIO.PWM(pins.rear_left_speed, 1000)
        self.rr_pwm = GPIO.PWM(pins.rear_right_speed, 1000)

    def register_commands(self):
        return [
            Command(
                name="drive",
                arguments=[
                    Argument(name="fl_speed", type=float, required=True),
                    Argument(name="fr_speed", type=float, required=True),
                    Argument(name="rl_speed", type=float, required=True),
                    Argument(name="rr_speed", type=float, required=True),
                ],
                callback=self.on_drive_command,
            ),
            Command(
                name="stop",
                arguments=[],
                callback=self.on_stop_command,
            ),
        ]

    def on_drive_command(self, command: CommandMessage):
        motors = [
            MotorState(
                speed=abs(int(arg)),
                direction=MotorDirection.FORWARD if int(arg) > 0 else MotorDirection.BACKWARD
            )
            for arg in command.arguments
        ]
        self.drive(*motors)

    def on_stop_command(self, _):
        self.stop()

    def drive(self, front_left: MotorState, front_right: MotorState, rear_left: MotorState, rear_right: MotorState):
        self.fl_pwm.start(front_left.speed*100)
        GPIO.output(self.pins.front_left_dir, GPIO.HIGH if front_left.direction == MotorDirection.FORWARD else GPIO.LOW)
        self.fr_pwm.start(front_right.speed*100)
        GPIO.output(self.pins.front_right_dir, GPIO.HIGH if front_right.direction == MotorDirection.FORWARD else GPIO.LOW)
        self.rl_pwm.start(rear_left.speed*100)
        GPIO.output(self.pins.rear_left_dir, GPIO.HIGH if rear_left.direction == MotorDirection.FORWARD else GPIO.LOW)
        self.rr_pwm.start(rear_right.speed*100)
        GPIO.output(self.pins.rear_right_dir, GPIO.HIGH if rear_right.direction == MotorDirection.FORWARD else GPIO.LOW)

    def stop(self):
        self.fl_pwm.stop()
        self.fr_pwm.stop()
        self.rl_pwm.stop()
        self.rr_pwm.stop()

