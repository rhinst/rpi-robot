from threading import Thread
from typing import Dict, Any
from queue import Queue, Empty
from app.message_bus import MessageBus, Message
from app.logging import logger


class Plugin(Thread):

    config: Dict
    queue: Queue
    message_bus: MessageBus

    def __init__(self, config: Dict, message_bus: MessageBus):
        super().__init__()
        self.config = config
        self.message_bus = message_bus
        self.queue = Queue()

    def receive_message(self, msg: Message):
        self.queue.put(msg)

    def on_load(self):
        pass

    def on_unload(self):
        pass

    def on_msg_received(self, msg: Message):
        pass

    def main_loop(self):
        pass

    def run(self) -> None:
        logger.debug("Running main loop for plugin: %s", self.__class__.__name__)
        while True:
            try:
                msg = self.queue.get(False)
            except Empty:
                pass
            else:
                self.on_msg_received(msg)
            self.main_loop()

