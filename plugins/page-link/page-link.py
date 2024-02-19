import os
import re
from flask import Flask
from config import WikmdConfig


class Plugin:
    def __init__(self, flask_app: Flask, config: WikmdConfig, web_dep):
        self.name = "page-link"
        self.plugname = "page-link"
        self.flask_app = flask_app
        self.config = config
        self.this_location = os.path.dirname(__file__)
        self.web_dep = web_dep
        self.reserved_names = ["[[info]]", "[[warning]]", "[[danger]]", "[[success]]", "[[draw]]"]
        """Reserved names from other plugins."""

    def get_plugin_name(self) -> str:
        """Returns the name of the plugin."""
        return self.name

    def process_html(self, html: str) -> str:
        """Receives the HTML and replaces all occurrences of [[NAME]] with a link to a document with that name"""
        pages = re.findall(r"(\[\[([^:]*?)]])", html)
        result = html
        for match, link_name in pages:
            if match in self.reserved_names:
                continue
            href_link = f'<a href="{link_name.strip()}">{link_name.strip()}</a>'
            result = result.replace(match, href_link)

        return result

