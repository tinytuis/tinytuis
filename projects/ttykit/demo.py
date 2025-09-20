from blessed import Terminal
from components import render_button, render_modal, render_progress_bar
from themes import make_style

term = Terminal()

def main():
    style_light = make_style("gruvbox_light")  # Create light theme style
    style_dark = make_style("solarized_dark")  # Create dark theme style
    selected = True  # Initial button state

    with term.fullscreen(), term.cbreak():  # Fullscreen with key input
        while True:
            print(term.clear)  # Clear screen
            render_button("Click Me", 10, 5, selected)  # Render button
            render_modal("Welcome to TTYKit")  # Render modal with light border
            render_progress_bar(0.75, 20, 10, 10)  # Render progress bar
            key = term.inkey(timeout=0.1)  # Check for keypress
            if key.name == "KEY_UP" and selected:
                selected = False  # Toggle off
            elif key.name == "KEY_DOWN" and not selected:
                selected = True  # Toggle on
            elif key.name in ("q", "Q", "KEY_ESCAPE"):  # Exit condition
                break

if __name__ == "__main__":
    main()