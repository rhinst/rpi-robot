from itertools import cycle
import shlex

from app.message_bus import Connection, CommandMessage
from app.logging import logger

PROMPT = "rpibot> "


def process_input(user_input: str):
    command_parts = shlex.split(user_input)
    command = command_parts[0]
    arguments = command_parts[1:]
    logger.debug("Received command from CLI: '%s'", command)
    return CommandMessage(channel="core.command", command=command, arguments=arguments)


def start_cli_controller(message_bus: Connection):
    while cycle([True]):
        user_input = input(PROMPT).strip()
        if len(user_input) == 0:
            continue
        message = process_input(user_input)
        message_bus.publish(message)
