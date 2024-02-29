import importlib

from flask import Flask
from wikmd.config import WikmdConfig


class PluginManager:
    """Load all plugins inside "plugins" folder.

    A plugin needs to be a package with a module with the same name.
    """
    def __init__(self, flask_app: Flask, config: WikmdConfig, web_deps=None):
        self.plugins = {}

        self.config = config
        self.flask_app = flask_app
        self.web_deps = web_deps

    def send(self, plugin, slot, data):
        """Send a message to a single plugin and get the result."""
        if plugin not in self.plugins:
            return data
        if slot in dir(self.plugins[plugin]):
            self.flask_app.logger.info("Plugin %s ran on %s", plugin, slot)
            plugin_obj = self.plugins[plugin]
            data = getattr(plugin_obj, slot)(data)
        return data

    def broadcast(self, slot, data):
        """Broadcast the message to each plugin.

        Pass the data to them in turn, augment the data with the plugins and return it.
        """
        for name in self.plugins:
            data = self.send(name, slot, data)
        return data

    def load_plugin(self, plugin):
        self.plugins[plugin] = (importlib.import_module(
            f"wikmd.plugins.{plugin}.{plugin}", ".")
                .Plugin(self.flask_app, self.config, self.web_deps))
