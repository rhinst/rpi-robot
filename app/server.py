from threading import Thread
from typing import Dict

from app.plugins.manager import PluginManager
from app.logging import logger
from app.message_bus import MessageBus


class RobotServer(Thread):

    config: Dict
    plugin_manager: PluginManager
    message_bus: MessageBus

    def __init__(self, config: Dict):
        super().__init__()
        self.config = config
        self.message_bus = MessageBus()
        self.plugin_manager = PluginManager(config, self.message_bus)

    def run(self):
        logger.info("Started Robot server")
        self.plugin_manager.load_plugins()
