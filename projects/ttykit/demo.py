from blessed import Terminal
from components import render_button, render_modal, render_progress_bar
from themes import make_style

term = Terminal()

def main():
    """TTYKit demo with proper navigation."""
    selected = True  # Initial button state

    with term.fullscreen(), term.cbreak():  # Fullscreen with key input
        while True:
            print(term.clear)  # Clear screen
            
            # Show title
            print(term.move_y(2) + term.center("TTYKit Demo - Press arrow keys to navigate, 'q' to quit"))
            
            # Render components
            render_button("Click Me", 10, 5, selected)  # Render button
            render_modal("Welcome to TTYKit", 40)  # Render modal
            render_progress_bar(0.75, 20, 10, 10)  # Render progress bar
            
            # Handle input
            key = term.inkey()  # Wait for keypress (blocking)
            
            if key.name == "KEY_UP":
                selected = False  # Toggle off
            elif key.name == "KEY_DOWN":
                selected = True  # Toggle on
            elif key.name in ("q", "Q", "KEY_ESCAPE"):  # Exit condition
                break

if __name__ == "__main__":
    main()