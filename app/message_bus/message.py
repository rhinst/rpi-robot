from typing import List, Dict, Any
from dataclasses import dataclass


@dataclass
class Message:
    channel: str

    def __repr__(self):
        return None


@dataclass
class GenericMessage(Message):
    data: Any

    def __repr__(self):
        return self.data


@dataclass
class CommandMessage(Message):
    command: str
    arguments: List[str]

    def __repr__(self):
        return f"{self.command} {' '.join(self.arguments)}"


class MessageFactory:
    @staticmethod
    def _create_command_message(redis_msg: Dict) -> CommandMessage:
        command_parts = redis_msg["data"].split()
        command = command_parts[0].decode("utf-8")
        arguments = [argument.decode("utf-8") for argument in command_parts[1:]]
        return CommandMessage(
            channel=redis_msg["channel"].decode("utf-8"),
            command=command,
            arguments=arguments,
        )

    @staticmethod
    def from_redis_msg(redis_msg: Dict) -> Message:
        message_handlers = {"core.command": MessageFactory._create_command_message}
        try:
            return message_handlers[redis_msg["channel"].decode("utf-8")](redis_msg)
        except KeyError:
            return GenericMessage(
                channel=redis_msg["channel"].decode("utf-8"), data=redis_msg["data"]
            )
