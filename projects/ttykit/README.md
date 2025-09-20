# TTYKit

A TUI UI kit designed to make Linux terminals inviting for designers and new users.  
Pre-styled primitives (buttons, modals, progress bars) with switchable themes.

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

- **gruvbox_light**: Default light theme with orange accents.
- **solarized_dark**: Dark theme with green accents.

## Demo
Run: `python -m ttykit.demo`

[Insert GIF link here]

## Goal
Design pre-styled TUI components to make Linux terminals appealing for designers.

## Lessons Learned
[To be added after testing]