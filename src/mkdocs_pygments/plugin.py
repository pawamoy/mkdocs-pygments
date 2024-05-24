"""Configuration options for the MkDocs Manpage plugin."""

from __future__ import annotations

from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import Type as MkType
from mkdocs.plugins import BasePlugin


class PygmentsConfig(BaseConfig):
    """Configuration options for the plugin."""

    light = MkType(str, default="material")
    dark = MkType(str, default="material")
    respect_light_background = MkType(bool, default=True)
    respect_dark_background = MkType(bool, default=True)


class PygmentsPlugin(BasePlugin[PygmentsConfig]):
    """The MkDocs plugin to inject Pygments style sheets."""
