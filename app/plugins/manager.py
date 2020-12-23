import os
from typing import List, Dict
from importlib import import_module

from app.plugins.plugin import Plugin
from app.logging import logger
from app.message_bus import MessageBus

BASE_PLUGINS = ["listening"]


class PluginManager:
    config: Dict
    loaded_plugins: List[Plugin]
    message_bus: MessageBus

    def __init__(self, config: Dict, message_bus: MessageBus):
        self.config = config
        self.message_bus = message_bus
        self.loaded_plugins = []

    @staticmethod
    def get_plugin_directory() -> str:
        return os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

    def _unload_plugins(self):
        for plugin in self.loaded_plugins:
            plugin.on_unload()
        self.loaded_plugins = []

    def load_plugins(self):
        logger.info("Loading plugins")
        plugin_dir = PluginManager.get_plugin_directory()
        self._unload_plugins()
        for pkg_name in os.listdir(plugin_dir):
            full_path = os.path.join(plugin_dir, pkg_name)
            if not os.path.isdir(full_path):
                continue
            filename = f"{full_path}/plugin.py"
            if not os.path.isfile(filename):
                logger.warning("Package %s missing plugin.py. Skipping it.", pkg_name)
                continue
            logger.info("Loading plugin: %s", pkg_name)
            class_name = f"{pkg_name.replace('_', ' ').title().replace(' ', '')}Plugin"
            module_name = f"app.plugins.{pkg_name}.plugin"
            cls = getattr(import_module(module_name), class_name)
            instance = cls(self.config, self.message_bus)
            instance.on_load()
            instance.start()
            self.loaded_plugins.append(instance)
