from blessed import Terminal
term = Terminal()

def render_button(text: str, x: int = 0, y: int = 0, selected: bool = False) -> None:
    """Render a styled button at (x,y). Default: gruvbox_light theme."""
    with term.location(x, y):  # Set position
        if selected:
            print(term.black_on_lightyellow + term.bold + f"[ {text} ]" + term.orange + ">" + term.normal)  # Selected state
        else:
            print(term.black_on_lightyellow + f"[ {text} ]" + term.normal)  # Normal state

def render_modal(content: str, width: int = 40) -> None:
    """Render a centered modal with gruvbox_light orange border."""
    border_top = term.orange + "┌" + "─" * (width - 2) + "┐" + term.normal  # Top border
    border_bottom = term.orange + "└" + "─" * (width - 2) + "┘" + term.normal  # Bottom border
    body = term.black_on_lightyellow + "│ " + content.ljust(width - 4) + " │" + term.normal  # Body with content
    modal = f"{border_top}\n{body}\n{border_bottom}"  # Assemble modal
    print(term.center(modal))  # Center on screen

def render_progress_bar(progress: float = 0.5, width: int = 20, x: int = 0, y: int = 0) -> None:
    """Render a progress bar with gruvbox_light orange fill."""
    filled = int(progress * width)  # Calculate filled portion
    bar = term.orange + "#" * filled + term.normal + " " * (width - filled)  # Build bar
    percent = int(progress * 100)  # Calculate percentage
    with term.location(x, y):  # Set position
        print(f"[ {bar} ] {percent}%")  # Render bar and percent