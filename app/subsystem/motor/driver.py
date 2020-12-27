from app.subsystem import Subsystem
from app.command import Command, Argument
from app.message_bus.message import CommandMessage


class Driver(Subsystem):
    def register_commands(self):
        return [
            Command(
                name="drive",
                arguments=[
                    Argument(name="fl_speed", type=float, required=True),
                    Argument(name="fr_speed", type=float, required=True),
                    Argument(name="rl_speed", type=float, required=True),
                    Argument(name="rr_speed", type=float, required=True)
                ],
                callback=self.on_drive_command,
            ),
            Command(
                name="stop",
                arguments=[],
                callback=self.on_stop_command,
            )
        ]

    def on_drive_command(self, command: CommandMessage):
        print("DRIVE THE MOTORS!")

    def on_stop_command(self, command: CommandMessage):
        print("STOP THE MOTORS!")

