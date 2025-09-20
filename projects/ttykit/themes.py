from blessed import Terminal
term = Terminal()

THEMES = {
    "gruvbox_light": {
        "button_text": term.black_on_lightyellow,
        "button_selected": term.bold + term.orange,
        "modal_border": term.orange,
        "progress_fill": term.orange
    },
    "solarized_dark": {
        "button_text": term.white_on_darkgray,
        "button_selected": term.bold + term.green,
        "modal_border": term.green,
        "progress_fill": term.green
    }
}

def make_style(theme_name: str = "gruvbox_light"):
    """Return a style function for the given theme."""
    theme = THEMES.get(theme_name, THEMES["gruvbox_light"])  # Get theme or default
    def style(role: str, text: str):
        color = theme.get(role, term.normal)  # Default to normal if role missing
        return f"{color}{text}{term.normal}"  # Apply color and reset
    return style