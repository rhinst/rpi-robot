from abc import ABC
from typing import Dict, Union
import speech_recognition as sr

from app.logging import logger

ENGINES = ["google", "google_cloud", "ibm", "sphinx"]


class Engine(sr.Recognizer, ABC):
    engine: str
    options: Dict[str, str]

    def __init__(self, engine: str, options: Union[Dict[str, str], None] = None):
        super().__init__()
        self.engine = engine
        self.options = options if options is not None else {}
        if self.engine not in ENGINES:
            raise ValueError(f"Unrecognized speech engine: {self.engine}")
        logger.debug("Using speech recognition engine: %s", self.engine)
        self.options = options

    def recognize(self, audio: sr.AudioSource) -> str:
        method_name = f"recognize_{self.engine}"
        options = self.options
        options.update(
            {
                "audio_data": audio,
            }
        )
        return getattr(self, method_name)(**options)
