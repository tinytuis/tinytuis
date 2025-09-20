from blessed import Terminal
from components import render_button, render_modal, render_progress_bar
from themes import make_style
import time

term = Terminal()

def demo_buttons():
    """Demo showing button states and navigation."""
    print(term.clear)
    print(term.move_y(1) + term.center("TTYKit Demo: BUTTONS"))
    print(term.move_y(3) + term.center("Buttons can be selected/unselected with arrow keys"))
    print(term.move_y(4) + term.center("Press UP/DOWN arrows to see the difference"))
    print()
    
    selected = False
    while True:
        # Clear button area
        print(term.move_xy(0, 7) + " " * term.width)
        print(term.move_xy(0, 8) + " " * term.width)
        print(term.move_xy(0, 9) + " " * term.width)
        
        # Show both states
        print(term.move_xy(10, 7) + "Normal button:")
        render_button("Save File", 25, 7, selected=False)
        
        print(term.move_xy(10, 9) + "Selected button:")
        render_button("Save File", 25, 9, selected=True)
        
        print(term.move_xy(10, 11) + f"Current state: {'SELECTED' if selected else 'NORMAL'}")
        print(term.move_xy(10, 13) + "Press UP/DOWN to toggle, ENTER to continue")
        
        key = term.inkey()
        if key.name in ("KEY_UP", "KEY_DOWN"):
            selected = not selected
        elif key.name == "KEY_ENTER":
            break
        elif key.lower() == 'q':
            return

def demo_progress():
    """Demo showing animated progress bars."""
    print(term.clear)
    print(term.move_y(1) + term.center("TTYKit Demo: PROGRESS BARS"))
    print(term.move_y(3) + term.center("Progress bars show completion status"))
    print(term.move_y(4) + term.center("Watch them fill up!"))
    
    for i in range(101):
        progress = i / 100.0
        
        # Clear progress area
        for line in range(7, 12):
            print(term.move_xy(0, line) + " " * term.width)
        
        print(term.move_xy(10, 7) + "File Download:")
        render_progress_bar(progress, 30, 25, 7)
        
        print(term.move_xy(10, 9) + "Installation:")
        render_progress_bar(progress * 0.7, 30, 25, 9)
        
        print(term.move_xy(10, 11) + "Backup:")
        render_progress_bar(progress * 0.4, 30, 25, 11)
        
        time.sleep(0.03)
    
    print(term.move_y(15) + term.center("Press any key to continue..."))
    term.inkey()

def demo_modal():
    """Demo showing modal dialogs."""
    print(term.clear)
    print(term.move_y(1) + term.center("TTYKit Demo: MODAL DIALOGS"))
    print(term.move_y(3) + term.center("Modals display important messages"))
    print(term.move_y(4) + term.center("They're centered and styled with borders"))
    
    modals = [
        "Welcome to TTYKit!",
        "File saved successfully",
        "Are you sure you want to delete this file?",
        "Error: Connection failed\nPlease try again later"
    ]
    
    for i, content in enumerate(modals):
        print(term.clear)
        print(term.move_y(1) + term.center(f"TTYKit Demo: MODAL DIALOGS ({i+1}/{len(modals)})"))
        print(term.move_y(3) + term.center("Example modal:"))
        
        render_modal(content, 50)
        
        print(term.move_y(term.height - 3) + term.center("Press any key for next modal..."))
        term.inkey()

def demo_themes():
    """Demo showing different themes."""
    print(term.clear)
    print(term.move_y(1) + term.center("TTYKit Demo: THEMES"))
    print(term.move_y(3) + term.center("TTYKit supports multiple color themes"))
    print(term.move_y(4) + term.center("Currently showing: gruvbox_light (orange accents)"))
    print(term.move_y(6) + term.center("Components automatically use theme colors"))
    
    # Show all components with current theme
    render_button("Themed Button", 20, 8, selected=True)
    render_progress_bar(0.6, 25, 20, 10)
    render_modal("This modal uses\nthe current theme colors", 35)
    
    print(term.move_y(term.height - 3) + term.center("Press any key to continue..."))
    term.inkey()

def main():
    """Main demo showcasing all TTYKit components."""
    with term.fullscreen(), term.cbreak():
        print(term.clear)
        print(term.move_y(5) + term.center("Welcome to TTYKit!"))
        print(term.move_y(7) + term.center("A TUI UI kit for designer-friendly terminals"))
        print(term.move_y(9) + term.center("This demo will show you:"))
        print(term.move_y(11) + term.center("• Styled buttons with selection states"))
        print(term.move_y(12) + term.center("• Animated progress bars"))
        print(term.move_y(13) + term.center("• Centered modal dialogs"))
        print(term.move_y(14) + term.center("• Theme support"))
        print(term.move_y(16) + term.center("Press any key to start the demo..."))
        term.inkey()
        
        # Run each demo section
        demo_buttons()
        demo_progress()
        demo_modal()
        demo_themes()
        
        # Final screen
        print(term.clear)
        print(term.move_y(8) + term.center("TTYKit Demo Complete!"))
        print(term.move_y(10) + term.center("You've seen all the main components:"))
        print(term.move_y(12) + term.center("✓ Buttons with selection states"))
        print(term.move_y(13) + term.center("✓ Progress bars with animations"))
        print(term.move_y(14) + term.center("✓ Modal dialogs"))
        print(term.move_y(15) + term.center("✓ Theme support"))
        print(term.move_y(17) + term.center("Ready to build beautiful TUIs!"))
        print(term.move_y(19) + term.center("Press any key to exit..."))
        term.inkey()

if __name__ == "__main__":
    main()