from app.message_bus import Connection, CommandMessage
from app.logging import logger

PROMPT = "rpibot> "


class CliController:
    message_bus: Connection

    def __init__(self, message_bus: Connection):
        self.message_bus = message_bus

    def start(self):
        while True:
            user_input = input(PROMPT).strip()
            if len(user_input) == 0:
                continue
            # TODO: more sophisticated command parsing (strings can be quoted with spaces in them)
            command_parts = user_input.split()
            command = command_parts[0]
            arguments = command_parts[1:]
            logger.debug("Received command from CLI: '%s'", command)
            self.message_bus.publish(
                CommandMessage(
                    channel="core.command", command=command, arguments=arguments
                )
            )
