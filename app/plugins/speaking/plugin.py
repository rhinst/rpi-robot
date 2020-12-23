import os
from tempfile import NamedTemporaryFile

from gtts import gTTS

from app.plugins.plugin import Plugin
from app.message_bus import Message
from app.logging import logger


class SpeakingPlugin(Plugin):

    def say(self, phrase: str):
        logger.debug("Saying '%s'", phrase)
        f = NamedTemporaryFile(delete=False)
        filename = f.name
        f.close()
        tts = gTTS(phrase)
        tts.save(f.name)
        os.system(f"mpg123 -q {filename}")
        os.unlink(filename)

    def on_load(self):
        logger.debug("Subscribing to plugin.listening.recognized_words")
        self.message_bus.subscribe(self, "plugin.listening.recognized_words")

    def on_msg_received(self,  msg: Message):
        logger.debug("Received a phrase from the plugin.listening.recognized_words queue!")
        self.say(str(msg.data))
