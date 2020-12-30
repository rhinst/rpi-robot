from time import sleep
from itertools import cycle

import speech_recognition as sr

from app.logging import logger
from app.subsystem import Subsystem
from app.subsystem.listener.microphone import Microphone
from app.subsystem.listener.engine import Engine
from app.message_bus.connection import Connection


class Listener(Subsystem):
    mic: Microphone
    engine: Engine

    def __init__(self, message_bus: Connection, engine: Engine, microphone: Microphone):
        super().__init__(message_bus)
        self.mic = microphone
        self.engine = engine

    def listen_for_duration(self, duration: float) -> sr.AudioData:
        return self.engine.record(source=self.mic, duration=duration)

    def listen_for_phrase(self) -> str:
        while cycle([True]):
            try:
                logger.debug("Listening for a phrase")
                self.engine.adjust_for_ambient_noise(self.mic)
                audio = self.engine.listen(source=self.mic, timeout=1)
                return self.engine.recognize(audio)
            except sr.UnknownValueError:
                logger.debug("Unrecognized audio")
            except sr.WaitTimeoutError:
                logger.debug("Timed out waiting for speech input")

    def wait_for_wake_word(self, wake_word: str):
        while cycle([True]):
            phrase = self.listen_for_phrase()
            if phrase.lower() == wake_word.lower():
                break
            sleep(0.001)
