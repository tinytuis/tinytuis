# TTYKit
A comprehensive TUI UI kit designed to make Linux terminals inviting for designers and new users.  
Pre-styled, customizable components with multiple themes and styles for beautiful terminal interfaces.  
**Now featuring clean, functional design focused on usability over decoration**

## Install
```bash
cd projects/ttykit
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

# Clean, functional design
render_button("Save", 10, 5, theme="functional", style="functional")
render_modal("Form follows function", theme="functional", style="functional")
```

## Components

### Buttons
- **Styles**: `default`, `rounded`, `minimal`, `boxed`, `functional`
- **Features**: Selection states, keyboard navigation, theme integration

```python
render_button("Click Me", x=10, y=5, selected=True, theme="gruvbox_light", style="rounded")
render_button("Save", x=10, y=5, selected=True, theme="functional", style="functional") # Clean, no decoration
```

### Modals
- **Styles**: `default`, `double`, `rounded`, `functional`
- **Features**: Auto-centering, titles, multi-line content, borders

```python
render_modal("Content here", width=40, theme="solarized_dark", style="double", title="Dialog")
render_modal("No decoration, pure content", theme="functional", style="functional") # No borders
```

### Progress Bars
- **Styles**: `default`, `blocks`, `dots`, `arrows`, `functional`
- **Features**: Percentage display, labels, animations

```python
render_progress_bar(0.5, width=30, x=10, y=8, theme="solarized_dark", style="blocks", label="Loading")
render_progress_bar(0.5, width=30, x=10, y=8, theme="functional", style="functional", label="Progress") # Minimal noise
```

### Lists
- **Styles**: `default`, `arrows`, `bullets`, `numbers`, `functional`
- **Features**: Selection highlighting, keyboard navigation

```python
items = ["File", "Edit", "View", "Help"]
render_list(items, x=10, y=5, selected=1, theme="gruvbox_light", style="arrows")
render_list(items, x=10, y=5, selected=1, theme="functional", style="functional") # Contrast over decoration
```

### Tables
- **Styles**: `default`, `minimal`, `functional`
- **Features**: Auto-sizing columns, headers, borders

```python
headers = ["Name", "Size", "Date"]
rows = [["file.txt", "2KB", "2024-01-15"]]
render_table(headers, rows, x=10, y=5, theme="gruvbox_light", style="minimal")
render_table(headers, rows, x=10, y=5, theme="functional", style="functional") # No borders, pure alignment
```

### Status Bars
- **Types**: `info`, `success`, `warning`, `error`
- **Features**: Full-width, bottom positioning, status colors

```python
render_status_bar("File saved successfully", status="success", theme="solarized_dark")
render_status_bar("SUCCESS: File saved", status="success", theme="functional") # Status in text, not color
```

## Themes

### Built-in Themes
- **`gruvbox_light`**: Warm light theme with orange accents (default)
- **`solarized_dark`**: Professional dark theme with green accents
- **`functional`**: Clean monochrome theme focused on usability

### Functional Theme Philosophy
The `functional` theme embodies clean design principles:
- **Monochrome palette**: Only black, white, and gray
- **No decoration**: Pure function over form
- **Contrast for selection**: High contrast inversion, no ornamental indicators
- **Status through content**: Information communicated through text, not color
- **Clarity over complexity**: Every element serves a purpose

### Theme Usage
```python
from ttykit.themes import list_themes, get_theme_colors

# List all available themes
themes = list_themes() # ['gruvbox_light', 'solarized_dark', 'functional']

# Get theme colors for custom components
colors = get_theme_colors("functional")
print(f"{colors['accent']}Functional text{term.normal}")
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

### Clean Design Guidelines
When creating custom components, follow these principles:

1. **Remove decoration**: Use `style="functional"` for pure usability
2. **Contrast over ornamentation**: Selection through inversion, not symbols
3. **Content hierarchy**: Information, not decoration
4. **Consistent spacing**: Grid-based alignment
5. **Purposeful color**: Color only when functional

```python
# Good: Clean, functional
render_button("Save", theme="functional", style="functional") # Clean, usable

# Avoid: Over-decorated
render_button("💾 Save File! ✨", theme="solarized_dark", style="boxed") # Too much visual noise
```

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
Run the comprehensive demo to see all components, themes, and design approaches:
```bash
cd projects/ttykit
python demo.py
```

The demo showcases:
- All 3 built-in themes (including functional)
- Every component style variation
- Interactive examples
- Complete customization guide
- Clean design principles

[Insert GIF link here]

## Goal
Design pre-styled TUI components to make Linux terminals appealing and accessible for designers, with comprehensive theming and customization options. Features both decorative and functional design approaches to suit different preferences and use cases.

## Architecture
- **`components.py`**: All UI components with style variations (including functional styles)
- **`themes.py`**: Color themes and styling functions (including functional theme)
- **`demo.py`**: Comprehensive demonstration of all features and design approaches
- **Extensible**: Easy to add new themes, styles, and components following established patterns

## Lessons Learned
- Theme consistency across components is crucial for professional UIs
- Multiple style options provide flexibility without complexity
- Interactive demos are essential for showcasing TUI capabilities
- Proper separation of styling and logic enables easy customization
- **Clean, functional design principles create more usable interfaces**
- **Contrast and clarity are more important than decoration**
- **Every visual element should serve a purpose**