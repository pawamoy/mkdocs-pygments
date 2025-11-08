"""Tests for the plugin."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from mkdocs_pygments._internal.plugin import _get_styles, _theme_css

if TYPE_CHECKING:
    from pygments.style import Style

styles = _get_styles()


@pytest.mark.parametrize("style", styles.values())
def test_building_css(style: type[Style]) -> None:
    """Build CSS from a style class."""
    assert _theme_css(style, "", respect_background=True)
