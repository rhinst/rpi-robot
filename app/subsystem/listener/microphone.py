import speech_recognition as sr

from app.subsystem.listener.exception import DeviceNotFoundException
from app.logging import logger


def get_microphone_index(device_name: str):
    available_devices = sr.Microphone.list_microphone_names()
    try:
        return available_devices.index(device_name)
    except ValueError:
        print(sr.Microphone.list_microphone_names())
        raise DeviceNotFoundException(f"Microphone named {device_name} not found")


class Microphone(sr.Microphone):
    def __init__(self, device_name: str = "default"):
        logger.debug("Using microphone: %s", device_name)
        super().__init__(device_index=get_microphone_index(device_name))
