from blessed import Terminal
term = Terminal()

THEMES = {
    "solarized_dark": {
        "button_text": term.white_on_darkgray,
        "button_selected": term.bold + term.bright_black,
        "modal_border": term.green,
        "progress_fill": term.green
    },
    "gruvbox_light": {
        "button_text": term.black_on_lightyellow,
        "button_selected": term.bold + term.aquamarine,
        "modal_border": term.orange,
        "progress_fill": term.orange
    }
}

def make_style(theme_name: str = "solarized_dark"):
    """Return a style function for a given theme."""
    pass  # Placeholder: Return a function applying theme colors