# TTYKit

A comprehensive TUI UI kit designed to make Linux terminals inviting for designers and new users.  
Pre-styled, customizable components with multiple themes and styles for beautiful terminal interfaces.

## Install
```bash
pip install -r requirements.txt
```

## Quick Start
```python
from ttykit.components import render_button, render_modal, render_progress_bar
from ttykit.themes import make_style

# Basic usage with default theme
render_button("Save File", 10, 5, selected=True)
render_modal("Welcome to TTYKit!", 40)
render_progress_bar(0.75, 30, 10, 8)

# Custom theme and style
render_button("Save", 10, 5, theme="cyberpunk", style="rounded")
render_modal("Alert", theme="minimal", style="double", title="Warning")
```

## Components

### Buttons
- **Styles**: `default`, `rounded`, `minimal`, `boxed`
- **Features**: Selection states, keyboard navigation, theme integration
```python
render_button("Click Me", x=10, y=5, selected=True, theme="gruvbox_light", style="rounded")
```

### Modals
- **Styles**: `default`, `double`, `rounded`
- **Features**: Auto-centering, titles, multi-line content, borders
```python
render_modal("Content here", width=40, theme="solarized_dark", style="double", title="Dialog")
```

### Progress Bars
- **Styles**: `default`, `blocks`, `dots`, `arrows`
- **Features**: Percentage display, labels, animations
```python
render_progress_bar(0.5, width=30, x=10, y=8, theme="cyberpunk", style="blocks", label="Loading")
```

### Lists
- **Styles**: `default`, `arrows`, `bullets`, `numbers`
- **Features**: Selection highlighting, keyboard navigation
```python
items = ["File", "Edit", "View", "Help"]
render_list(items, x=10, y=5, selected=1, theme="minimal", style="arrows")
```

### Tables
- **Styles**: `default`, `minimal`
- **Features**: Auto-sizing columns, headers, borders
```python
headers = ["Name", "Size", "Date"]
rows = [["file.txt", "2KB", "2024-01-15"]]
render_table(headers, rows, x=10, y=5, theme="gruvbox_light", style="minimal")
```

### Status Bars
- **Types**: `info`, `success`, `warning`, `error`
- **Features**: Full-width, bottom positioning, status colors
```python
render_status_bar("File saved successfully", status="success", theme="solarized_dark")
```

## Themes

### Built-in Themes
- **`gruvbox_light`**: Warm light theme with orange accents (default)
- **`solarized_dark`**: Professional dark theme with green accents
- **`cyberpunk`**: Futuristic theme with cyan and magenta
- **`minimal`**: Clean monochrome theme with white accents

### Theme Usage
```python
from ttykit.themes import list_themes, get_theme_colors

# List all available themes
themes = list_themes()  # ['gruvbox_light', 'solarized_dark', 'cyberpunk', 'minimal']

# Get theme colors for custom components
colors = get_theme_colors("cyberpunk")
print(f"{colors['accent']}Accent text{term.normal}")
```

### Creating Custom Themes
Add new themes to `themes.py`:
```python
THEMES["my_theme"] = {
    "button_text": term.white_on_blue,
    "button_selected": term.bold + term.yellow,
    "button_border": term.yellow,
    "modal_border": term.yellow,
    "modal_background": term.white_on_blue,
    "progress_fill": term.yellow,
    "progress_empty": term.darkgray,
    "text_primary": term.white,
    "text_secondary": term.lightgray,
    "accent": term.yellow,
    "success": term.green,
    "warning": term.orange,
    "error": term.red
}
```

## Customization

### Adding Component Styles
Extend existing components with new visual styles:
```python
def render_button(text, x=0, y=0, selected=False, theme="gruvbox_light", style="default"):
    colors = get_theme_colors(theme)
    
    if style == "my_style":
        # Your custom button style here
        button = f"{colors['accent']}◆ {text} ◆{term.normal}"
    # ... existing styles
```

### Creating New Components
Follow the TTYKit pattern for consistency:
```python
def render_my_component(content, x=0, y=0, theme="gruvbox_light", style="default"):
    """Render a custom component with theme support."""
    colors = get_theme_colors(theme)
    
    # Use theme colors for consistency
    styled_content = f"{colors['accent']}{content}{term.normal}"
    
    with term.location(x, y):
        print(styled_content)
```

## Demo
Run the comprehensive demo to see all components and themes:
```bash
cd projects/ttykit
python demo.py
```

The demo showcases:
- All 4 built-in themes
- Every component style variation
- Interactive examples
- Customization guide

## Examples

### File Manager Interface
```python
# Header
render_status_bar("TTY File Manager v1.0", "info", "gruvbox_light")

# File list
files = ["document.txt", "image.png", "script.py"]
render_list(files, 5, 3, selected=1, theme="gruvbox_light", style="arrows")

# Action buttons
render_button("Open", 5, 8, theme="gruvbox_light", style="default")
render_button("Delete", 15, 8, theme="gruvbox_light", style="default")

# Progress for operations
render_progress_bar(0.6, 25, 5, 10, theme="gruvbox_light", style="blocks", label="Copying")
```

### Settings Dialog
```python
# Modal dialog
render_modal("Choose your preferred theme:\n\n1. Gruvbox Light\n2. Solarized Dark\n3. Cyberpunk\n4. Minimal", 
             width=50, theme="solarized_dark", style="double", title="Settings")

# Confirmation buttons
render_button("Apply", 20, 15, selected=True, theme="solarized_dark", style="rounded")
render_button("Cancel", 30, 15, theme="solarized_dark", style="rounded")
```

## Goal
Design pre-styled TUI components to make Linux terminals appealing and accessible for designers, with comprehensive theming and customization options.

## Architecture
- **`components.py`**: All UI components with style variations
- **`themes.py`**: Color themes and styling functions
- **`demo.py`**: Comprehensive demonstration of all features
- **Extensible**: Easy to add new themes, styles, and components

## Lessons Learned
- Theme consistency across components is crucial for professional UIs
- Multiple style options provide flexibility without complexity
- Interactive demos are essential for showcasing TUI capabilities
- Proper separation of styling and logic enables easy customization