import os
from tempfile import NamedTemporaryFile

from gtts import gTTS

from app.logging import logger
from app.subsystem import Subsystem


class Talker(Subsystem):


    def say(self, phrase: str):
        logger.debug("Saying '%s'", phrase)
        f = NamedTemporaryFile(delete=False)
        filename = f.name
        f.close()
        tts = gTTS(phrase)
        tts.save(f.name)
        os.system(f"mpg123 -q {filename}")
        os.unlink(filename)
