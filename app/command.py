from typing import List
from dataclasses import dataclass


@dataclass
class Argument:
    name: str
    required: bool
    type: type


@dataclass
class Command:
    name: str
    arguments: List[Argument]
