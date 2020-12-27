from dataclasses import dataclass
from enum import Enum

import RPi.GPIO as GPIO

from app.subsystem import Subsystem
from app.command import Command, Argument
from app.message_bus.connection import Connection
from app.message_bus.message import CommandMessage


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

    def __init__(self, message_bus: Connection, pins: MotorPins):
        super().__init__(message_bus)
        self.pins = pins
        GPIO.setmode(GPIO.BOARD)

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
        print("DRIVE THE MOTORS!")

    def on_stop_command(self, command: CommandMessage):
        print("STOP THE MOTORS!")

    def drive(self, front_left: MotorState, front_right: MotorState, rear_left: MotorState, rear_right: MotorState):
        pass


