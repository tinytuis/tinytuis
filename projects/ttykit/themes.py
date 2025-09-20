from blessed import Terminal
term = Terminal()

# Keeping three themes for launch: gruvbox_light (warm), solarized_dark (professional), functional (usability-focused)
THEMES = {
    "gruvbox_light": {
        "button_text": term.black_on_lightyellow,
        "button_selected": term.bold + term.orange,
        "button_border": term.orange,
        "modal_border": term.orange,
        "modal_background": term.black_on_lightyellow,
        "progress_fill": term.orange,
        "progress_empty": term.darkgray,
        "text_primary": term.black,
        "text_secondary": term.darkgray,
        "accent": term.orange,
        "success": term.green,
        "warning": term.yellow,
        "error": term.red
    },
    "solarized_dark": {
        "button_text": term.white_on_darkgray,
        "button_selected": term.bold + term.green,
        "button_border": term.green,
        "modal_border": term.green,
        "modal_background": term.white_on_darkgray,
        "progress_fill": term.green,
        "progress_empty": term.darkgray,
        "text_primary": term.white,
        "text_secondary": term.lightgray,
        "accent": term.green,
        "success": term.cyan,
        "warning": term.yellow,
        "error": term.red
    },
    "functional": {
        # Clean, functional design - monochrome with single accent for clarity
        "button_text": term.white_on_black,
        "button_selected": term.black_on_white,  # High contrast inversion
        "button_border": term.white,
        "modal_border": term.white,
        "modal_background": term.white_on_black,
        "progress_fill": term.white,
        "progress_empty": term.darkgray,
        "text_primary": term.white,
        "text_secondary": term.darkgray,
        "accent": term.white,  # No decoration, pure function
        "success": term.white,  # Status through text, not color
        "warning": term.white,
        "error": term.white
    }
}

def make_style(theme_name: str = "gruvbox_light"):
    """Return a style function for the given theme."""
    theme = THEMES.get(theme_name, THEMES["gruvbox_light"])  # Get theme or default
    def style(role: str, text: str = ""):
        color = theme.get(role, term.normal)  # Default to normal if role missing
        if text:
            return f"{color}{text}{term.normal}"  # Apply color and reset
        else:
            return color  # Return just the color for direct use
    return style

def get_theme_colors(theme_name: str = "gruvbox_light"):
    """Get raw theme colors for direct access."""
    return THEMES.get(theme_name, THEMES["gruvbox_light"])

def list_themes():
    """List all available themes."""
    return list(THEMES.keys())