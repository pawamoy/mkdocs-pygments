# mkdocs_pygments

MkDocs Pygments package.

Highlighting themes for code blocks.

Classes:

- **`PygmentsConfig`** – Configuration options for the plugin.
- **`PygmentsPlugin`** – The MkDocs plugin to inject Pygments style sheets.

## PygmentsConfig

Bases: `Config`

Configuration options for the plugin.

Attributes:

- **`dark`** – A Pygments theme to use with dark mode.
- **`light`** – A Pygments theme to use with light mode.
- **`respect_dark_background`** – Whether to respect the background color of the dark theme.
- **`respect_light_background`** – Whether to respect the background color of the light theme.

### dark

```
dark = Type(str, default='material')
```

A Pygments theme to use with dark mode.

### light

```
light = Type(str, default='material')
```

A Pygments theme to use with light mode.

### respect_dark_background

```
respect_dark_background = Type(bool, default=True)
```

Whether to respect the background color of the dark theme.

### respect_light_background

```
respect_light_background = Type(bool, default=True)
```

Whether to respect the background color of the light theme.

## PygmentsPlugin

```
PygmentsPlugin()
```

Bases: `BasePlugin[PygmentsConfig]`

The MkDocs plugin to inject Pygments style sheets.

Methods:

- **`on_config`** – Inject dark and light style sheets in extra_css.
- **`on_post_build`** – Write the CSS contents to the injected style sheets.

Attributes:

- **`css_filename`** – The name of the CSS file to write.
- **`styles`** – A mapping of available Pygments styles.

Source code in `src/mkdocs_pygments/_internal/plugin.py`

```
def __init__(self):
    """Initialize the plugin."""
    self.styles = None
    """A mapping of available Pygments styles."""
```

### css_filename

```
css_filename = 'pygments.css'
```

The name of the CSS file to write.

### styles

```
styles = None
```

A mapping of available Pygments styles.

### on_config

```
on_config(config: MkDocsConfig) -> MkDocsConfig | None
```

Inject dark and light style sheets in `extra_css`.

Parameters:

- **`config`** (`MkDocsConfig`) – The MkDocs config object.

Returns:

- `MkDocsConfig | None` – The config.

Source code in `src/mkdocs_pygments/_internal/plugin.py`

```
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
```

### on_post_build

```
on_post_build(config: MkDocsConfig, **kwargs: Any) -> None
```

Write the CSS contents to the injected style sheets.

Parameters:

- **`config`** (`MkDocsConfig`) – MkDocs configuration.

Source code in `src/mkdocs_pygments/_internal/plugin.py`

```
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
```
