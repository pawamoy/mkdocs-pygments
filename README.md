# MkDocs Pygments

[![documentation](https://img.shields.io/badge/docs-mkdocs-708FCC.svg?style=flat)](https://pawamoy.github.io/mkdocs-pygments/)
[![gitpod](https://img.shields.io/badge/gitpod-workspace-708FCC.svg?style=flat)](https://gitpod.io/#https://github.com/pawamoy/mkdocs-pygments)
[![gitter](https://badges.gitter.im/join%20chat.svg)](https://app.gitter.im/#/room/#mkdocs-pygments:gitter.im)

Highlighting themes for code blocks.

## Installation

This project is available to sponsors only, through my Insiders program.
See Insiders [explanation](https://pawamoy.github.io/mkdocs-pygments/insiders/)
and [installation instructions](https://pawamoy.github.io/mkdocs-pygments/insiders/installation/).

## Usage

Configure it in `mkdocs.yml`:

```yaml
# mkdocs.yml
plugins:
- pygments:
    light: autumn
    dark: github-dark
```

To know which themes are available, you can either read our docs,
or use a theme that doesn't exist, to abort the build with an error
and a message listing the available themes:

```yaml
# mkdocs.yml
plugins:
- pygments:
    light: wodjweofijwqefd
    dark: github-dark
```

```console
$ mkdocs serve
INFO    -  Building documentation...
INFO    -  Cleaning site directory
ERROR   -  pygments: Unknown theme: 'wodjweofijwqefd'. Available themes:
           abap, algol, algol_nu, arduino, autumn, bw, borland, coffee,
           colorful, default, dracula, emacs, friendly_grayscale, friendly,
           fruity, github-dark, gruvbox-dark, gruvbox-light, igor, inkpot,
           lightbulb, lilypond, lovelace, manni, material, monokai, murphy,
           native, nord-darker, nord, one-dark, paraiso-dark, paraiso-light,
           pastie, perldoc, rainbow_dash, rrt, sas, solarized-dark,
           solarized-light, staroffice, stata-dark, stata-light,
           tango, trac, vim, vs, xcode, zenburn
```

---

It's possible to instruct MkDocs Pygments
to ignore the background color set by a theme,
in order to make it work for both light and dark
color schemes.

For example, to use the `autumn` style (which is a light theme),
for both light and dark schemes while adapting the background color:

```yaml
# mkdocs.yml
plugins:
- pygments:
    light: autumn
    respect_light_background: true  # default value
    dark: autumn
    respect_dark_background: false
```

To use the `github-dark` style (which is a dark theme),
for both light and dark schemes while adapting the background color:

```yaml
# mkdocs.yml
plugins:
- pygments:
    light: github-dark
    respect_light_background: false
    dark: github-dark
```

By default, the background color is respected,
so you don't have to actually specify `respect_<light/dark>_background: true`.
