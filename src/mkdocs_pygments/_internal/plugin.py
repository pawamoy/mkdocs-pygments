from __future__ import annotations

import os
from importlib import import_module
from typing import TYPE_CHECKING, Any

from mkdocs.config.base import Config as BaseConfig
from mkdocs.config.config_options import Type as MkType
from mkdocs.config.defaults import MkDocsConfig
from mkdocs.exceptions import PluginError
from mkdocs.plugins import BasePlugin, get_plugin_logger
from mkdocs.utils import write_file
from pygments.styles import STYLES
from pygments.token import STANDARD_TYPES

if TYPE_CHECKING:
    from collections.abc import Iterator

    from mkdocs.config.defaults import MkDocsConfig
    from pygments.style import Style


_logger = get_plugin_logger(__name__)


def _get_styles() -> dict[str, type[Style]]:
    result = {}
    for class_name, (module_name, *_) in STYLES.items():
        style_class = getattr(import_module(module_name), class_name)
        result[style_class.name] = style_class
    return result


def _yield_css_colors(style_class: type[Style]) -> Iterator[tuple[str, str]]:
    for token_type, color_data in style_class:
        if (css_class := STANDARD_TYPES.get(token_type, None)) and (color := color_data.get("color", None)):
            yield css_class, f"#{color}"


def _pygments_css(style: str | None = None) -> str:
    style_class = f".{style} " if style else ""
    pygments_variables = [
        f"{style_class}.highlight .{css_class} {{ color: var(--pygments-{css_class}); }}"
        for css_class in sorted(STANDARD_TYPES.values())
        if css_class
    ]
    return "\n".join(pygments_variables)


def _theme_css(style_class: type[Style], prefix: str, *, respect_background: bool = True) -> str:
    css_variables = sorted(_yield_css_colors(style_class))
    css_lines = [f"--pygments-{css_class}: {color};" for css_class, color in css_variables]
    if respect_background:
        css_lines.insert(0, f"--md-code-bg-color: {style_class.background_color};")
    css_lines.append("}")
    return f"{prefix} {{\n" + "\n".join(css_lines)


class PygmentsConfig(BaseConfig):
    """Configuration options for the plugin."""

    light = MkType(str, default="material")
    """A Pygments theme to use with light mode."""
    dark = MkType(str, default="material")
    """A Pygments theme to use with dark mode."""
    respect_light_background = MkType(bool, default=True)
    """Whether to respect the background color of the light theme."""
    respect_dark_background = MkType(bool, default=True)
    """Whether to respect the background color of the dark theme."""


class PygmentsPlugin(BasePlugin[PygmentsConfig]):
    """The MkDocs plugin to inject Pygments style sheets."""

    css_filename = "pygments.css"
    """The name of the CSS file to write."""

    def __init__(self):
        """Initialize the plugin."""
        self.styles = None
        """A mapping of available Pygments styles."""

    def on_config(self, config: MkDocsConfig) -> MkDocsConfig | None:
        """Inject dark and light style sheets in `extra_css`.

        Arguments:
            config: The MkDocs config object.

        Returns:
            The config.
        """
        self.styles = _get_styles()
        config.extra_css.insert(0, self.css_filename)
        return config

    def on_post_build(self, config: MkDocsConfig, **kwargs: Any) -> None:  # noqa: ARG002
        """Write the CSS contents to the injected style sheets.

        Parameters:
            config: MkDocs configuration.
        """
        try:
            light_css = _theme_css(
                self.styles[self.config.light],
                '[data-md-color-scheme="default"]',
                respect_background=self.config.respect_light_background,
            )
            dark_css = _theme_css(
                self.styles[self.config.dark],
                '[data-md-color-scheme="slate"]',
                respect_background=self.config.respect_dark_background,
            )
        except KeyError as error:
            available = ", ".join(self.styles.keys())
            raise PluginError(f"pygments: Unknown theme: {error}. Available themes: {available}") from error
        css_contents = f"{light_css}\n\n{dark_css}\n\n{_pygments_css()}"
        write_file(
            css_contents.encode("utf-8"),
            os.path.join(config.site_dir, self.css_filename.format(theme="base")),
        )
