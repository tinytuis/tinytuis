from blessed import Terminal
from components import render_button, render_modal, render_progress_bar, render_list, render_table, render_status_bar
from themes import list_themes, get_theme_colors
import time

term = Terminal()

def demo_themes():
    """Demo all available themes."""
    themes = list_themes()
    
    for theme in themes:
        print(term.clear)
        colors = get_theme_colors(theme)
        
        print(term.move_y(1) + term.center(f"TTYKit Theme: {theme.upper()}"))
        print(term.move_y(3) + term.center("All components automatically adapt to the theme"))
        
        # Show theme colors
        print(term.move_xy(10, 5) + f"{colors['text_primary']}Primary Text{term.normal}")
        print(term.move_xy(10, 6) + f"{colors['text_secondary']}Secondary Text{term.normal}")
        print(term.move_xy(10, 7) + f"{colors['accent']}Accent Color{term.normal}")
        print(term.move_xy(10, 8) + f"{colors['success']}Success{term.normal}")
        print(term.move_xy(10, 9) + f"{colors['warning']}Warning{term.normal}")
        print(term.move_xy(10, 10) + f"{colors['error']}Error{term.normal}")
        
        # Show components with this theme
        render_button("Sample Button", 30, 5, selected=True, theme=theme)
        render_progress_bar(0.7, 20, 30, 7, theme=theme)
        render_modal("Theme Preview", 30, theme=theme, title="Modal")
        
        print(term.move_y(term.height - 3) + term.center(f"Theme: {theme} | Press any key for next theme..."))
        term.inkey()

def demo_button_styles():
    """Demo all button styles."""
    styles = ["default", "rounded", "minimal", "boxed"]
    
    for style in styles:
        print(term.clear)
        print(term.move_y(1) + term.center(f"TTYKit Button Styles: {style.upper()}"))
        print(term.move_y(3) + term.center("Press UP/DOWN to see selected state"))
        
        selected = False
        while True:
            # Clear button area
            for line in range(6, 15):
                print(term.move_xy(0, line) + " " * term.width)
            
            print(term.move_xy(10, 6) + f"Style: {style}")
            print(term.move_xy(10, 8) + "Normal:")
            render_button("Save File", 20, 8, selected=False, style=style)
            
            print(term.move_xy(10, 12) + "Selected:")
            render_button("Save File", 20, 12, selected=True, style=style)
            
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
    """Demo all progress bar styles."""
    styles = ["default", "blocks", "dots", "arrows"]
    
    for style in styles:
        print(term.clear)
        print(term.move_y(1) + term.center(f"TTYKit Progress Styles: {style.upper()}"))
        print(term.move_y(3) + term.center("Watch the animated progress bars"))
        
        for i in range(101):
            progress = i / 100.0
            
            # Clear progress area
            for line in range(6, 12):
                print(term.move_xy(0, line) + " " * term.width)
            
            print(term.move_xy(10, 6) + f"Style: {style}")
            render_progress_bar(progress, 30, 10, 8, style=style, label="Download")
            render_progress_bar(progress * 0.7, 30, 10, 10, style=style, label="Install")
            
            time.sleep(0.02)
        
        print(term.move_y(15) + term.center("Press any key for next style..."))
        term.inkey()

def demo_modal_styles():
    """Demo all modal styles."""
    styles = ["default", "double", "rounded"]
    
    for style in styles:
        print(term.clear)
        print(term.move_y(1) + term.center(f"TTYKit Modal Styles: {style.upper()}"))
        
        modals = [
            ("Simple Modal", "This is a basic modal dialog"),
            ("Modal with Title", "This modal has a title bar\nand multiple lines of content"),
            ("Confirmation", "Are you sure you want to\ndelete this file?\n\nThis action cannot be undone.")
        ]
        
        for title, content in modals:
            print(term.clear)
            print(term.move_y(1) + term.center(f"Modal Style: {style.upper()}"))
            
            if title == "Simple Modal":
                render_modal(content, 40, style=style)
            else:
                render_modal(content, 50, style=style, title=title)
            
            print(term.move_y(term.height - 3) + term.center("Press any key for next modal..."))
            term.inkey()

def demo_lists():
    """Demo list components."""
    styles = ["default", "arrows", "bullets", "numbers"]
    items = ["New File", "Open File", "Save File", "Save As...", "Exit"]
    
    for style in styles:
        print(term.clear)
        print(term.move_y(1) + term.center(f"TTYKit List Styles: {style.upper()}"))
        print(term.move_y(3) + term.center("Use UP/DOWN arrows to navigate"))
        
        selected = 0
        while True:
            # Clear list area
            for line in range(6, 15):
                print(term.move_xy(0, line) + " " * term.width)
            
            print(term.move_xy(10, 6) + f"File Menu (Style: {style}):")
            render_list(items, 10, 8, selected, style=style)
            
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
    """Demo table components."""
    styles = ["default", "minimal"]
    headers = ["Name", "Size", "Modified"]
    rows = [
        ["document.txt", "2.4 KB", "2024-01-15"],
        ["image.png", "156 KB", "2024-01-14"],
        ["script.py", "8.1 KB", "2024-01-13"],
        ["data.json", "45 KB", "2024-01-12"]
    ]
    
    for style in styles:
        print(term.clear)
        print(term.move_y(1) + term.center(f"TTYKit Table Styles: {style.upper()}"))
        print(term.move_y(3) + term.center("File listing example"))
        
        render_table(headers, rows, 10, 6, style=style)
        
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
        print(term.move_y(7) + term.center("Status bars appear at the bottom of the screen"))
        print(term.move_y(9) + term.center(f"Current status: {status}"))
        
        render_status_bar(text, status)
        
        print(term.move_y(12) + term.center("Press any key for next status..."))
        term.inkey()

def demo_customization():
    """Demo how to customize TTYKit."""
    print(term.clear)
    print(term.move_y(2) + term.center("TTYKit Customization Guide"))
    print(term.move_y(4) + term.center("How to modify styling and create new patterns"))
    
    customization_info = [
        "1. THEMES - Modify colors in themes.py:",
        "   • Add new themes to THEMES dictionary",
        "   • Define colors for each component role",
        "   • Use blessed Terminal color methods",
        "",
        "2. COMPONENT STYLES - Add new styles:",
        "   • Modify render functions in components.py",
        "   • Add new style parameters",
        "   • Create custom visual patterns",
        "",
        "3. NEW COMPONENTS - Create new UI elements:",
        "   • Follow the render_* function pattern",
        "   • Accept theme and style parameters",
        "   • Use get_theme_colors() for consistency",
        "",
        "4. USAGE EXAMPLES:",
        "   render_button('Save', theme='cyberpunk', style='rounded')",
        "   render_modal('Alert', theme='minimal', style='double')",
        "   render_progress_bar(0.5, theme='solarized_dark', style='blocks')"
    ]
    
    for i, line in enumerate(customization_info):
        if line.startswith(("1.", "2.", "3.", "4.")):
            print(term.move_xy(5, 6 + i) + term.orange + line + term.normal)
        elif line.startswith("   render_"):
            print(term.move_xy(5, 6 + i) + term.cyan + line + term.normal)
        else:
            print(term.move_xy(5, 6 + i) + line)
    
    print(term.move_y(term.height - 3) + term.center("Press any key to continue..."))
    term.inkey()

def main():
    """Comprehensive TTYKit demo showcasing all patterns and customization."""
    with term.fullscreen(), term.cbreak():
        print(term.clear)
        print(term.move_y(3) + term.center("TTYKit - Complete Pattern Library"))
        print(term.move_y(5) + term.center("A comprehensive TUI UI kit for designer-friendly terminals"))
        print(term.move_y(7) + term.center("This demo showcases:"))
        print(term.move_y(9) + term.center("• 4 Built-in Themes (gruvbox_light, solarized_dark, cyberpunk, minimal)"))
        print(term.move_y(10) + term.center("• Multiple Component Styles (buttons, modals, progress bars)"))
        print(term.move_y(11) + term.center("• Advanced Components (lists, tables, status bars)"))
        print(term.move_y(12) + term.center("• Complete Customization Guide"))
        print(term.move_y(14) + term.center("Ready to explore the full breadth of TTYKit?"))
        print(term.move_y(16) + term.center("Press any key to start..."))
        term.inkey()
        
        # Run all demos
        demo_themes()
        demo_button_styles()
        demo_progress_styles()
        demo_modal_styles()
        demo_lists()
        demo_tables()
        demo_status_bars()
        demo_customization()
        
        # Final screen
        print(term.clear)
        print(term.move_y(6) + term.center("TTYKit Complete Demo Finished!"))
        print(term.move_y(8) + term.center("You've seen the full breadth of TTYKit:"))
        print(term.move_y(10) + term.center("✓ 4 Themes with full color customization"))
        print(term.move_y(11) + term.center("✓ 6 Component types with multiple styles each"))
        print(term.move_y(12) + term.center("✓ Advanced UI patterns (lists, tables, status bars)"))
        print(term.move_y(13) + term.center("✓ Complete customization and extension guide"))
        print(term.move_y(15) + term.center("TTYKit: Making Linux terminals beautiful and accessible!"))
        print(term.move_y(17) + term.center("Press any key to exit..."))
        term.inkey()

if __name__ == "__main__":
    main()