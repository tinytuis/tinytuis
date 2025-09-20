from blessed import Terminal
from components import render_button, render_modal, render_progress_bar, render_list, render_table, render_status_bar
from themes import list_themes, get_theme_colors, make_style
import time

term = Terminal()

def demo_themes():
    """Demo the three selected themes with styled components."""
    themes = ["gruvbox_light", "solarized_dark", "functional"]  # Limited to three for launch
    for theme in themes:
        print(term.clear)
        colors = get_theme_colors(theme)
        style = make_style(theme) if theme != "functional" else make_style("functional")
        if theme == "functional":
            print(term.move_y(1) + term.center(f"TTYKit Theme: FUNCTIONAL"))
            print(term.move_y(3) + term.center("Clean, purposeful design focused on usability"))
        else:
            print(term.move_y(1) + term.center(f"TTYKit Theme: {theme.upper()}"))
            print(term.move_y(3) + term.center("All components adapt to the theme"))
        print(term.move_xy(10, 5) + f"{colors['text_primary']}Primary Text{term.normal}")
        print(term.move_xy(10, 6) + f"{colors['text_secondary']}Secondary Text{term.normal}")
        print(term.move_xy(10, 7) + f"{colors['accent']}Accent Color{term.normal}")
        print(term.move_xy(10, 8) + f"{colors['success']}Success{term.normal}")
        print(term.move_xy(10, 9) + f"{colors['warning']}Warning{term.normal}")
        print(term.move_xy(10, 10) + f"{colors['error']}Error{term.normal}")
        render_button("Sample Button", 30, 5, selected=True, theme=theme, style="default")
        render_progress_bar(0.7, 20, 30, 7, theme=theme, style="default")
        render_modal("Theme Preview", 30, theme=theme, style="default", title="Modal")
        print(term.move_y(term.height - 3) + term.center(f"Theme: {theme} | Press any key for next..."))
        term.inkey()

def demo_button_styles():
    """Demo all button styles including functional."""
    styles = ["default", "rounded", "minimal", "boxed", "functional"]
    for style in styles:
        print(term.clear)
        if style == "functional":
            print(term.move_y(1) + term.center(f"TTYKit Button Style: FUNCTIONAL"))
            print(term.move_y(3) + term.center("Clean design focused on usability"))
        else:
            print(term.move_y(1) + term.center(f"TTYKit Button Styles: {style.upper()}"))
            print(term.move_y(3) + term.center("Press UP/DOWN to see selected state"))
        selected = False
        while True:
            for line in range(6, 15):
                print(term.move_xy(0, line) + " " * term.width)
            print(term.move_xy(10, 6) + f"Style: {style}")
            print(term.move_xy(10, 8) + "Normal:")
            theme = "functional" if style == "functional" else "gruvbox_light"
            render_button("Save File", 20, 8, selected=False, theme=theme, style=style)
            print(term.move_xy(10, 12) + "Selected:")
            render_button("Save File", 20, 12, selected=True, theme=theme, style=style)
            print(term.move_xy(10, 16) + f"Current: {'SELECTED' if selected else 'NORMAL'}")
            print(term.move_xy(10, 18) + "UP/DOWN to toggle, ENTER for next style")
            key = term.inkey()
            if key.name in ("KEY_UP", "KEY_DOWN"):
                selected = not selected
            elif key.name == "KEY_ENTER":
                break
            elif key.lower() == 'q':
                return

def demo_progress_styles():
    """Demo all progress bar styles including functional with frame cap."""
    styles = ["default", "blocks", "dots", "arrows", "functional"]
    for style in styles:
        print(term.clear)
        if style == "functional":
            print(term.move_y(1) + term.center(f"TTYKit Progress Style: FUNCTIONAL"))
            print(term.move_y(3) + term.center("Minimal visual noise, maximum clarity"))
        else:
            print(term.move_y(1) + term.center(f"TTYKit Progress Styles: {style.upper()}"))
            print(term.move_y(3) + term.center("Animated progress bars"))
        for i in range(101):
            progress = i / 100.0
            for line in range(6, 12):
                print(term.move_xy(0, line) + " " * term.width)
            print(term.move_xy(10, 6) + f"Style: {style}")
            theme = "functional" if style == "functional" else "gruvbox_light"
            render_progress_bar(progress, 30, 10, 8, theme=theme, style=style, label="Download")
            render_progress_bar(progress * 0.7, 30, 10, 10, theme=theme, style=style, label="Install")
            time.sleep(1 / 20)  # Cap at 20 FPS
        print(term.move_y(15) + term.center("Press any key for next style..."))
        term.inkey()

def demo_modal_styles():
    """Demo all modal styles including functional."""
    styles = ["default", "double", "rounded", "functional"]
    for style in styles:
        print(term.clear)
        if style == "functional":
            print(term.move_y(1) + term.center(f"TTYKit Modal Style: FUNCTIONAL"))
            print(term.move_y(3) + term.center("No borders, pure content focus"))
        else:
            print(term.move_y(1) + term.center(f"TTYKit Modal Styles: {style.upper()}"))
        modals = [
            ("Simple Modal", "This is a basic modal dialog"),
            ("Modal with Title", "This modal has a title bar\nand multiple lines of content"),
            ("Confirmation", "Are you sure you want to\ndelete this file?\n\nThis action cannot be undone.")
        ]
        for title, content in modals:
            print(term.clear)
            if style == "functional":
                print(term.move_y(1) + term.center(f"Modal Style: FUNCTIONAL - Clean content"))
            else:
                print(term.move_y(1) + term.center(f"Modal Style: {style.upper()}"))
            theme = "functional" if style == "functional" else "gruvbox_light"
            if title == "Simple Modal":
                render_modal(content, 40, theme=theme, style=style)
            else:
                render_modal(content, 50, theme=theme, style=style, title=title)
            print(term.move_y(term.height - 3) + term.center("Press any key for next modal..."))
            term.inkey()

def demo_lists():
    """Demo list components including functional."""
    styles = ["default", "arrows", "bullets", "numbers", "functional"]
    items = ["New File", "Open File", "Save File", "Save As...", "Exit"]
    for style in styles:
        print(term.clear)
        if style == "functional":
            print(term.move_y(1) + term.center(f"TTYKit List Style: FUNCTIONAL"))
            print(term.move_y(3) + term.center("Selection through contrast, not decoration"))
        else:
            print(term.move_y(1) + term.center(f"TTYKit List Styles: {style.upper()}"))
            print(term.move_y(3) + term.center("Use UP/DOWN arrows to navigate"))
        selected = 0
        while True:
            for line in range(6, 15):
                print(term.move_xy(0, line) + " " * term.width)
            print(term.move_xy(10, 6) + f"File Menu (Style: {style}):")
            theme = "functional" if style == "functional" else "gruvbox_light"
            render_list(items, 10, 8, selected, theme=theme, style=style)
            print(term.move_xy(10, 15) + "UP/DOWN to navigate, ENTER for next style")
            key = term.inkey()
            if key.name == "KEY_UP" and selected > 0:
                selected -= 1
            elif key.name == "KEY_DOWN" and selected < len(items) - 1:
                selected += 1
            elif key.name == "KEY_ENTER":
                break
            elif key.lower() == 'q':
                return

def demo_tables():
    """Demo table components including functional."""
    styles = ["default", "minimal", "functional"]
    headers = ["Name", "Size", "Modified"]
    rows = [
        ["document.txt", "2.4 KB", "2024-01-15"],
        ["image.png", "156 KB", "2024-01-14"],
        ["script.py", "8.1 KB", "2024-01-13"],
        ["data.json", "45 KB", "2024-01-12"]
    ]
    for style in styles:
        print(term.clear)
        if style == "functional":
            print(term.move_y(1) + term.center(f"TTYKit Table Style: FUNCTIONAL"))
            print(term.move_y(3) + term.center("No borders, pure data alignment"))
        else:
            print(term.move_y(1) + term.center(f"TTYKit Table Styles: {style.upper()}"))
            print(term.move_y(3) + term.center("File listing example"))
        theme = "functional" if style == "functional" else "gruvbox_light"
        render_table(headers, rows, 10, 6, theme=theme, style=style)
        print(term.move_y(term.height - 3) + term.center("Press any key for next style..."))
        term.inkey()

def demo_status_bars():
    """Demo status bar components."""
    statuses = [
        ("Ready", "info"),
        ("File saved successfully", "success"),
        ("Warning: Unsaved changes", "warning"),
        ("Error: Connection failed", "error")
    ]
    for text, status in statuses:
        print(term.clear)
        print(term.move_y(5) + term.center("TTYKit Status Bars"))
        print(term.move_y(7) + term.center("Status bars appear at the bottom"))
        print(term.move_y(9) + term.center(f"Current status: {status}"))
        render_status_bar(text, status)
        print(term.move_y(12) + term.center("Press any key for next status..."))
        term.inkey()

def demo_customization():
    """Demo how to customize TTYKit with clean design principles."""
    print(term.clear)
    print(term.move_y(2) + term.center("TTYKit Customization Guide"))
    print(term.move_y(4) + term.center("How to create clean, functional TUI designs"))
    customization_info = [
        "CLEAN DESIGN PRINCIPLES FOR TTYKIT:",
        "",
        "1. REMOVE DECORATION - Use 'functional' style for pure usability",
        " render_button('Save', style='functional', theme='functional')",
        "",
        "2. CONTRAST OVER ORNAMENTATION - Selection through inversion",
        " Selected items use inverted colors, not arrows/bullets",
        "",
        "3. CONTENT HIERARCHY - Information, not decoration",
        " Status through text content: 'SUCCESS: File saved'",
        "",
        "4. CONSISTENT SPACING - Grid-based alignment",
        " All components respect consistent spacing rules",
        "",
        "5. PURPOSEFUL COLOR - Color only when functional",
        " 'functional' theme uses only essential colors",
        "",
        "Focus on usability and clarity over visual complexity."
    ]
    for i, line in enumerate(customization_info):
        if line.startswith(("1.", "2.", "3.", "4.", "5.")):
            print(term.move_xy(5, 6 + i) + term.orange + line + term.normal)
        elif line.startswith(" render_"):
            print(term.move_xy(5, 6 + i) + term.cyan + line + term.normal)
        elif line.startswith("Focus on"):
            print(term.move_xy(5, 6 + i) + term.white + line + term.normal)
        elif line.startswith("CLEAN DESIGN"):
            print(term.move_xy(5, 6 + i) + term.bold + term.white + line + term.normal)
        else:
            print(term.move_xy(5, 6 + i) + line)
    print(term.move_y(term.height - 3) + term.center("Press any key to continue..."))
    term.inkey()

def main():
    """Comprehensive TTYKit demo showcasing all patterns including functional design."""
    with term.fullscreen(), term.cbreak():
        print(term.clear)
        print(term.move_y(3) + term.center("TTYKit - Complete Pattern Library"))
        print(term.move_y(5) + term.center("A comprehensive TUI UI kit for designer-friendly terminals"))
        print(term.move_y(7) + term.center("Featuring clean, functional design:"))
        print(term.move_y(9) + term.center("• 3 Built-in Themes (including 'functional')"))
        print(term.move_y(10) + term.center("• Multiple Component Styles (including clean variants)"))
        print(term.move_y(11) + term.center("• Advanced Components (lists, tables, status bars)"))
        print(term.move_y(12) + term.center("• Focus on usability and clarity"))
        print(term.move_y(14) + term.center("Ready to explore functional beauty?"))
        print(term.move_y(16) + term.center("Press any key to start..."))
        term.inkey()
        demo_themes()
        demo_button_styles()
        demo_progress_styles()
        demo_modal_styles()
        demo_lists()
        demo_tables()
        demo_status_bars()
        demo_customization()
        print(term.clear)
        print(term.move_y(6) + term.center("TTYKit Complete Demo Finished!"))
        print(term.move_y(8) + term.center("You've seen the full breadth of TTYKit:"))
        print(term.move_y(10) + term.center("✓ 3 Themes including clean functional design"))
        print(term.move_y(11) + term.center("✓ 6 Component types with multiple styles each"))
        print(term.move_y(12) + term.center("✓ Advanced UI patterns (lists, tables, status bars)"))
        print(term.move_y(13) + term.center("✓ Focus on usability and clarity"))
        print(term.move_y(15) + term.center("TTYKit: Form follows function in terminal interfaces!"))
        print(term.move_y(17) + term.center("Press any key to exit..."))
        term.inkey()

if __name__ == "__main__":
    main()