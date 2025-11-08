---
title: Overview
hide:
- feedback
---

--8<-- "README.md"

## Themes

The left column respects the theme's background color. The right column ignores it and uses the background color of the current color scheme (default or slate). You will notice that some themes work well with both schemes, while others do not. To fix a specific theme, we invite users to create light or dark variants for this theme and send pull requests to [Pygments][] (please read their [contributing instructions][]).

You will also notice that for some themes, names, punctuation, operators or other kinds of tokens are very hard to see depending on the current color scheme (default or slate): it's because these themes do not define colors for names, punctuation, operators, etc., and these unstyled tokens then take the color set by the current color scheme and the selected theme of our own docs pages. To fix a specific theme, we invite users to open issues on [Pygments][] (please read their [contributing instructions][]) to ask whether this theme could be improved by styling additional tokens, and to send pull requests if maintainers accept them.

````python exec="1" idprefix=""
import textwrap
from mkdocs_pygments.plugin import _get_styles, _pygments_css, _theme_css

styles = _get_styles()

broken = ("algol", "algol_nu", "bw")
for style in broken:
    styles.pop(style)

for style in styles.values():
    print(f"### {style.name}\n")
    print('<div class="grid" markdown>\n')
    for respect_background in (True, False):
        style_css_class = style.name
        if respect_background:
            style_css_class += "--respectbg"
        theme_css = _theme_css(style, f".{style_css_class}", respect_background=respect_background)
        print(f'<div class="{style_css_class}" markdown>\n')
        print(f"<style>{theme_css}</style>\n")
        print(
            textwrap.dedent(
                '''
                ```python
                from typing import Iterator

                # This is an example
                class Math:
                    @staticmethod
                    def fib(n: int) -> Iterator[int]:
                        """Fibonacci series up to n."""
                        a, b = 0, 1
                        while a < n:
                            yield a
                            a, b = b, a + b

                result = sum(Math.fib(42))
                print(f"The answer is {result}")
                ```
                '''
            )
        )
        print("\n</div>")
    print("\n</div>")
````

[Pygments]: https://github.com/pygments/pygments?tab=readme-ov-file
[contributing instructions]: https://pygments.org/docs/contributing/
