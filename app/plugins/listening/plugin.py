from typing import Dict

import speech_recognition as sr

from app.message_bus import MessageBus
from app.plugins.plugin import Plugin
from app.plugins.listening.exception import DeviceNotFoundException
from app.logging import logger

ENGINES = ["google", "google_cloud", "ibm", "sphinx"]


def get_microphone_index(device_name: str):
    available_devices = sr.Microphone.list_microphone_names()
    try:
        return available_devices.index(device_name)
    except ValueError:
        print(sr.Microphone.list_microphone_names())
        raise DeviceNotFoundException(f"Microphone named {device_name} not found")


class ListeningPlugin(Plugin):
    recognizer: sr.Recognizer
    mic: sr.Microphone
    engine: str
    engine_options: Dict

    def __init__(self, config: Dict, message_bus: MessageBus):
        super().__init__(config, message_bus)
        self.message_bus = message_bus
        try:
            self.engine = config["plugins"]["listening"]["engine"]["name"].lower()
        except KeyError:
            # fall back to sphinx as default, since it doesn't require an Internet connection
            self.engine = "sphinx"
        if self.engine not in ENGINES:
            raise ValueError(f"Unrecognized speech engine: {self.engine}")
        logger.debug("Using speech recognition engine: %s", self.engine)
        self.engine_options = config["plugins"]["listening"]["engine"]["options"]
        self.recognizer = sr.Recognizer()
        try:
            device_name = config["plugins"]["listening"]["microphone"]["device_name"]
        except KeyError:
            device_name = "default"
        logger.debug("Using microphone: %s", device_name)
        self.mic = sr.Microphone(device_index=get_microphone_index(device_name))

    def recognize_speech(self) -> str:
        with self.mic as source:
            self.recognizer.adjust_for_ambient_noise(source)
            audio = self.recognizer.listen(source, timeout=1)
        method_name = f"recognize_{self.engine}"
        options = self.engine_options
        options.update(
            {
                "audio_data": audio,
            }
        )
        return getattr(self.recognizer, method_name)(**options)

    def on_load(self):
        logger.info("Speech recognition plugin starting up")

    def main_loop(self):
        try:
            logger.debug("Listening for words")
            spoken_words = self.recognize_speech()
        except sr.UnknownValueError as e:
            logger.debug("Unrecognized audio")
        except sr.WaitTimeoutError as e:
            logger.debug("Timed out waiting for speech input")
        else:
            logger.debug("Recognized audio: '%s'", spoken_words)
            self.message_bus.publish("plugin.listening.recognized_words", spoken_words)
