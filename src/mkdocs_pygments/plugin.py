"""Configuration options for the MkDocs Manpage plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import Type as MkType
from mkdocs.plugins import BasePlugin, get_plugin_logger

if TYPE_CHECKING:
    from mkdocs.config.defaults import MkDocsConfig


logger = get_plugin_logger("mkdocs_pygments")


class PygmentsConfig(BaseConfig):
    """Configuration options for the plugin."""

    light = MkType(str, default="material")
    dark = MkType(str, default="material")
    respect_light_background = MkType(bool, default=True)
    respect_dark_background = MkType(bool, default=True)


class PygmentsPlugin(BasePlugin[PygmentsConfig]):
    """The MkDocs plugin to inject Pygments style sheets."""

    def on_config(self, config: MkDocsConfig) -> None:  # noqa: D102
        if "pygments" in config.plugins:
            logger.info("The public version of the mkdocs-pygments plugin is a no-op.")
