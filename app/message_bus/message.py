from typing import Dict
from dataclasses import dataclass


@dataclass
class Message:
    channel: str


@dataclass
class CommandMessage(Message):
    command: str
    arguments: Dict[str, str]


