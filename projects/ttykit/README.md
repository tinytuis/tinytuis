# TTYKit

A tiny UI kit for the terminal.  
Reusable primitives (buttons, modals, progress bars) with switchable themes.

## Install
```bash
pip install -r requirements.txt
```

## Usage
```python
from ttykit.components import render_button
from ttykit.themes import make_style

style = make_style("solarized_dark")
render_button("Click me", 5, 2, selected=True, style=style("button_text"))
```

## Components

- **Button**: Selectable text box with arrow nav.
- **Modal**: Centered ASCII box.
- **Progress Bar**: Percentage indicator.

## Themes

- **solarized_dark**: Dark with green accents.
- **gruvbox_light**: Light with orange accents.

## Demo
Run: `python -m ttykit.demo`

[Insert GIF link here]

## Goal
Learn to design reusable TUI primitives with themes in a terminal.

## Lessons Learned
[To be added after testing]