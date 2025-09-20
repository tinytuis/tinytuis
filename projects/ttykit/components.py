from blessed import Terminal
from themes import get_theme_colors

term = Terminal()

def render_button(text: str, x: int = 0, y: int = 0, selected: bool = False, theme: str = "gruvbox_light", style: str = "default") -> None:
    """Render a styled button at (x,y) with customizable themes and styles."""
    colors = get_theme_colors(theme)
    
    if style == "functional":
        # Functional style: Pure function, no decoration
        if selected:
            button = f"{colors['button_selected']} {text} {term.normal}"  # Inverted, no brackets
        else:
            button = f"{colors['button_text']} {text} {term.normal}"  # Clean text only
    elif style == "rounded":
        # Rounded button style
        if selected:
            button = f"{colors['button_selected']}( {text} ){colors['accent']}◄{term.normal}"
        else:
            button = f"{colors['button_text']}( {text} ){term.normal}"
    elif style == "minimal":
        # Minimal button style
        if selected:
            button = f"{colors['button_selected']}> {text}{term.normal}"
        else:
            button = f"{colors['text_primary']}  {text}{term.normal}"
    elif style == "boxed":
        # Boxed button style
        if selected:
            button = f"{colors['button_border']}┌{'─' * (len(text) + 2)}┐{term.normal}\n"
            button += f"{colors['button_border']}│{colors['button_selected']} {text} {colors['button_border']}│{colors['accent']}◄{term.normal}\n"
            button += f"{colors['button_border']}└{'─' * (len(text) + 2)}┘{term.normal}"
        else:
            button = f"{colors['button_border']}┌{'─' * (len(text) + 2)}┐{term.normal}\n"
            button += f"{colors['button_border']}│{colors['button_text']} {text} {colors['button_border']}│{term.normal}\n"
            button += f"{colors['button_border']}└{'─' * (len(text) + 2)}┘{term.normal}"
    else:
        # Default button style
        if selected:
            button = f"{colors['button_text']}[ {text} ]{colors['accent']}>{term.normal}"
        else:
            button = f"{colors['button_text']}[ {text} ]{term.normal}"
    
    with term.location(x, y):
        if style == "boxed":
            for i, line in enumerate(button.split('\n')):
                with term.location(x, y + i):
                    print(line)
        else:
            print(button)

def render_modal(content: str, width: int = 40, theme: str = "gruvbox_light", style: str = "default", title: str = "") -> None:
    """Render a centered modal with customizable themes and styles."""
    colors = get_theme_colors(theme)
    lines = content.split('\n')
    max_content_width = max(len(line) for line in lines) if lines else 0
    box_width = max(width, max_content_width + 4, len(title) + 4 if title else 0)
    
    # Calculate center position
    center_x = (term.width - box_width) // 2
    center_y = (term.height - len(lines) - (4 if title else 2)) // 2
    
    if style == "functional":
        # Functional style: No borders, just content with spacing
        if title:
            with term.location(center_x, center_y):
                print(f"{colors['accent']}{title.center(box_width)}{term.normal}")
            content_start = center_y + 2
        else:
            content_start = center_y
        
        # Content lines with minimal formatting
        for i, line in enumerate(lines):
            with term.location(center_x, content_start + i):
                print(f"{colors['text_primary']}{line.center(box_width)}{term.normal}")
        return
    
    if style == "double":
        # Double-line border
        top_char, bottom_char, side_char = "╔╗", "╚╝", "║"
        horizontal_char = "═"
    elif style == "rounded":
        # Rounded corners
        top_char, bottom_char, side_char = "╭╮", "╰╯", "│"
        horizontal_char = "─"
    else:
        # Default single-line border
        top_char, bottom_char, side_char = "┌┐", "└┘", "│"
        horizontal_char = "─"
    
    # Top border
    with term.location(center_x, center_y):
        print(f"{colors['modal_border']}{top_char[0]}{horizontal_char * (box_width - 2)}{top_char[1]}{term.normal}")
    
    # Title if provided
    if title:
        with term.location(center_x, center_y + 1):
            title_padding = (box_width - 2 - len(title)) // 2
            print(f"{colors['modal_border']}{side_char}{colors['accent']}{' ' * title_padding}{title}{' ' * (box_width - 2 - len(title) - title_padding)}{colors['modal_border']}{side_char}{term.normal}")
        
        # Separator
        with term.location(center_x, center_y + 2):
            print(f"{colors['modal_border']}├{horizontal_char * (box_width - 2)}┤{term.normal}")
        content_start = center_y + 3
    else:
        content_start = center_y + 1
    
    # Content lines
    for i, line in enumerate(lines):
        with term.location(center_x, content_start + i):
            padding = (box_width - 2 - len(line)) // 2
            print(f"{colors['modal_border']}{side_char}{colors['modal_background']}{' ' * padding}{line}{' ' * (box_width - 2 - len(line) - padding)}{colors['modal_border']}{side_char}{term.normal}")
    
    # Bottom border
    with term.location(center_x, content_start + len(lines)):
        print(f"{colors['modal_border']}{bottom_char[0]}{horizontal_char * (box_width - 2)}{bottom_char[1]}{term.normal}")

def render_progress_bar(progress: float = 0.5, width: int = 20, x: int = 0, y: int = 0, theme: str = "gruvbox_light", style: str = "default", label: str = "") -> None:
    """Render a progress bar with customizable themes and styles."""
    colors = get_theme_colors(theme)
    filled = int(progress * width)
    percent = int(progress * 100)
    
    if style == "functional":
        # Functional style: Pure function, minimal visual noise
        bar = f"{colors['progress_fill']}{'█' * filled}{colors['progress_empty']}{'·' * (width - filled)}{term.normal}"
        with term.location(x, y):
            if label:
                print(f"{colors['text_primary']}{label} {bar} {percent}%{term.normal}")
            else:
                print(f"{bar} {percent}%")
        return
    
    if style == "blocks":
        # Block-style progress bar
        bar = f"{colors['progress_fill']}{'█' * filled}{colors['progress_empty']}{'░' * (width - filled)}{term.normal}"
    elif style == "dots":
        # Dot-style progress bar
        bar = f"{colors['progress_fill']}{'●' * filled}{colors['progress_empty']}{'○' * (width - filled)}{term.normal}"
    elif style == "arrows":
        # Arrow-style progress bar
        bar = f"{colors['progress_fill']}{'►' * filled}{colors['progress_empty']}{'▷' * (width - filled)}{term.normal}"
    else:
        # Default hash-style progress bar
        bar = f"{colors['progress_fill']}{'#' * filled}{colors['progress_empty']}{' ' * (width - filled)}{term.normal}"
    
    with term.location(x, y):
        if label:
            print(f"{colors['text_primary']}{label}: {term.normal}[ {bar} ] {percent}%")
        else:
            print(f"[ {bar} ] {percent}%")

def render_list(items: list, x: int = 0, y: int = 0, selected: int = 0, theme: str = "gruvbox_light", style: str = "default") -> None:
    """Render a selectable list with customizable themes and styles."""
    colors = get_theme_colors(theme)
    
    for i, item in enumerate(items):
        is_selected = (i == selected)
        
        if style == "functional":
            # Functional style: No decoration, just inversion for selection
            item_color = colors['button_selected'] if is_selected else colors['text_primary']
            prefix = ""
        elif style == "arrows":
            prefix = f"{colors['accent']}► {term.normal}" if is_selected else "  "
        elif style == "bullets":
            prefix = f"{colors['accent']}• {term.normal}" if is_selected else "  "
        elif style == "numbers":
            prefix = f"{colors['accent']}{i+1}. {term.normal}" if is_selected else f"{colors['text_secondary']}{i+1}. {term.normal}"
        else:
            # Default style
            prefix = f"{colors['accent']}> {term.normal}" if is_selected else "  "
        
        if style != "functional":
            item_color = colors['button_selected'] if is_selected else colors['text_primary']
        
        with term.location(x, y + i):
            print(f"{prefix}{item_color}{item}{term.normal}")

def render_table(headers: list, rows: list, x: int = 0, y: int = 0, theme: str = "gruvbox_light", style: str = "default") -> None:
    """Render a table with customizable themes and styles."""
    colors = get_theme_colors(theme)
    
    # Calculate column widths
    col_widths = [len(header) for header in headers]
    for row in rows:
        for i, cell in enumerate(row):
            if i < len(col_widths):
                col_widths[i] = max(col_widths[i], len(str(cell)))
    
    # Add padding
    col_widths = [w + 2 for w in col_widths]
    
    if style == "functional":
        # Functional style: No borders, just aligned columns
        with term.location(x, y):
            header_line = " ".join(f"{colors['accent']}{header.ljust(col_widths[i])}{term.normal}" for i, header in enumerate(headers))
            print(header_line)
        
        # Subtle separator line
        with term.location(x, y + 1):
            separator = " ".join(f"{colors['text_secondary']}{'─' * col_widths[i]}{term.normal}" for i in range(len(headers)))
            print(separator)
        
        for i, row in enumerate(rows):
            with term.location(x, y + i + 2):
                row_line = " ".join(f"{colors['text_primary']}{str(cell).ljust(col_widths[j])}{term.normal}" for j, cell in enumerate(row))
                print(row_line)
        return
    
    if style == "minimal":
        # Minimal table style
        with term.location(x, y):
            header_line = " ".join(f"{colors['accent']}{header.ljust(col_widths[i])}{term.normal}" for i, header in enumerate(headers))
            print(header_line)
        
        for i, row in enumerate(rows):
            with term.location(x, y + i + 1):
                row_line = " ".join(f"{colors['text_primary']}{str(cell).ljust(col_widths[j])}{term.normal}" for j, cell in enumerate(row))
                print(row_line)
    else:
        # Default bordered table style
        total_width = sum(col_widths) + len(headers) - 1
        
        # Top border
        with term.location(x, y):
            print(f"{colors['modal_border']}┌{'─' * total_width}┐{term.normal}")
        
        # Headers
        with term.location(x, y + 1):
            header_line = f"{colors['modal_border']}│{term.normal}"
            for i, header in enumerate(headers):
                header_line += f"{colors['accent']}{header.ljust(col_widths[i])}{term.normal}"
                if i < len(headers) - 1:
                    header_line += f"{colors['modal_border']}│{term.normal}"
            header_line += f"{colors['modal_border']}│{term.normal}"
            print(header_line)
        
        # Header separator
        with term.location(x, y + 2):
            print(f"{colors['modal_border']}├{'─' * total_width}┤{term.normal}")
        
        # Rows
        for i, row in enumerate(rows):
            with term.location(x, y + 3 + i):
                row_line = f"{colors['modal_border']}│{term.normal}"
                for j, cell in enumerate(row):
                    row_line += f"{colors['text_primary']}{str(cell).ljust(col_widths[j])}{term.normal}"
                    if j < len(row) - 1:
                        row_line += f"{colors['modal_border']}│{term.normal}"
                row_line += f"{colors['modal_border']}│{term.normal}"
                print(row_line)
        
        # Bottom border
        with term.location(x, y + 3 + len(rows)):
            print(f"{colors['modal_border']}└{'─' * total_width}┘{term.normal}")

def render_status_bar(text: str, status: str = "info", theme: str = "gruvbox_light") -> None:
    """Render a status bar at the bottom of the screen."""
    colors = get_theme_colors(theme)
    
    if theme == "functional":
        # Functional style: Status through text content, not color
        bg_color = colors['text_primary']
        if status in ["success", "warning", "error"]:
            text = f"{status.upper()}: {text}"  # Explicit status in text
    else:
        if status == "success":
            bg_color = colors['success']
        elif status == "warning":
            bg_color = colors['warning']
        elif status == "error":
            bg_color = colors['error']
        else:
            bg_color = colors['accent']
    
    with term.location(0, term.height - 1):
        status_line = f"{bg_color}{text.ljust(term.width)}{term.normal}"
        print(status_line)