import os
from tempfile import TemporaryFile
from time import sleep

from gtts import gTTS
from pyglet.media import load, Player

from app.logging import logger
from app.subsystem import Subsystem
from app.command import Command, Argument
from app.message_bus.message import CommandMessage


class Talker(Subsystem):
    def register_commands(self):
        return [
            Command(
                name="say",
                arguments=[Argument(name="phrase", type=str, required=True)],
                callback=self.on_say_command,
            )
        ]

    def on_say_command(self, command: CommandMessage):
        self.say(" ".join(command.arguments))

    def say(self, phrase):
        logger.debug("Saying '%s'", phrase)
        tts = gTTS(phrase)
        f = TemporaryFile(mode="wb", delete=False)
        tts.write_to_fp(f)
        player = Player()
        f = open(f.name, mode="rb")
        music = load("blah", file=f, streaming=False)
        player.queue(music)
        player.play()
        sleep(music.duration)
        player.delete()
        f.close()
        os.unlink(f.name)
