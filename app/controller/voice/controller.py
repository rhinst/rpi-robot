from time import sleep
import itertools

from app.message_bus import Connection


def start_voice_controller(message_bus: Connection):
    while itertools.cycle([True]):
        sleep(0.001)
