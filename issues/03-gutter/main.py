#!/usr/bin/env python3
"""
Gutter - Issue #3
An ASCII comic reader with panel layouts and navigation.
Experience sequential art in the terminal.
"""

import sys
import os
import time
import threading
from dataclasses import dataclass
from typing import List, Optional

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tinykit import Canvas, ArtisticThemes, clear_screen, hide_cursor, show_cursor, get_terminal_size, SimpleInput


@dataclass
class Panel:
    x: int
    y: int
    width: int
    height: int
    content: List[str]
    dialogue: str = ""
    highlighted: bool = False


class ComicPage:
    def __init__(self, title: str, panels: List[Panel]):
        self.title = title
        self.panels = panels
        self.current_panel = 0


class GutterReader:
    def __init__(self):
        self.running = False
        self.terminal_size = get_terminal_size()
        self.canvas = Canvas(self.terminal_size.columns, self.terminal_size.lines - 3, ArtisticThemes.MINIMAL)
        self.pages = self.create_comic_pages()
        self.current_page = 0
        self.reading_mode = "page"  # "page" or "panel"
        
    def create_comic_pages(self):
        """Create a weird experimental comic in the spirit of FRANK/Annie Koyama."""
        
        # Page 1: TEETH
        page1_panels = [
            Panel(2, 2, 25, 5, [
                "┌───────────────────────┐",
                "│ WWWWWWWWWWWWWWWWWWWWW │",
                "│ W W W W W W W W W W W │",
                "│ WWWWWWWWWWWWWWWWWWWWW │",
                "└───────────────────────┘"
            ], "TEETH TEETH TEETH"),
            
            Panel(30, 2, 25, 5, [
                "┌───────────────────────┐",
                "│ ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ │",
                "│ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ ▼ │",
                "│ ▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼▼ │",
                "└───────────────────────┘"
            ], "GROWING DOWNWARD"),
            
            Panel(2, 9, 53, 7, [
                "┌───────────────────────────────────────────────────┐",
                "│                                                   │",
                "│ I FORGOT TO BRUSH MY TEETH FOR 47 YEARS          │",
                "│ NOW THEY HAVE THEIR OWN ECOSYSTEM                │",
                "│ SMALL BIRDS NEST IN MY MOLARS                    │",
                "│                                                   │",
                "└───────────────────────────────────────────────────┘"
            ], "The narrator explains calmly.")
        ]
        
        # Page 2: THE BIRDS
        page2_panels = [
            Panel(2, 2, 30, 8, [
                "┌────────────────────────────┐",
                "│                            │",
                "│    ^   ^   ^   ^   ^       │",
                "│   ( ) ( ) ( ) ( ) ( )      │",
                "│    v   v   v   v   v       │",
                "│                            │",
                "│ TWEET TWEET TWEET TWEET    │",
                "└────────────────────────────┘"
            ], "The birds are very small."),
            
            Panel(35, 2, 30, 8, [
                "┌────────────────────────────┐",
                "│ THEY SING OPERA            │",
                "│                            │",
                "│ ♪ LA LA LA LA LA ♪         │",
                "│ ♫ DO RE MI FA SO ♫         │",
                "│                            │",
                "│ BUT ONLY WAGNER            │",
                "│ EXCLUSIVELY WAGNER         │",
                "└────────────────────────────┘"
            ], "This is a problem."),
            
            Panel(2, 12, 63, 4, [
                "┌─────────────────────────────────────────────────────────────┐",
                "│ MY DENTIST SAYS THIS IS 'HIGHLY IRREGULAR'                 │",
                "│ I SAY 'WHAT ABOUT THE BEAUTY OF INTERSPECIES COOPERATION?' │",
                "│ SHE DOES NOT APPRECIATE ART                                 │",
                "└─────────────────────────────────────────────────────────────┘"
            ], "Conflict arises.")
        ]
        
        # Page 3: RESOLUTION?
        page3_panels = [
            Panel(2, 2, 66, 14, [
                "┌────────────────────────────────────────────────────────────────┐",
                "│                                                                │",
                "│ I HAVE DECIDED TO BECOME A PERFORMANCE ARTIST                 │",
                "│                                                                │",
                "│ MY MOUTH IS NOW A VENUE                                        │",
                "│                                                                │",
                "│ TICKETS: $47 (CASH ONLY)                                      │",
                "│                                                                │",
                "│ SHOWTIMES:                                                     │",
                "│ - TUESDAYS: THE RING CYCLE (FULL 15 HOURS)                    │",
                "│ - WEDNESDAYS: EXPERIMENTAL JAZZ FUSION                        │",
                "│ - THURSDAYS: BIRD POETRY SLAM                                  │",
                "│                                                                │",
                "└────────────────────────────────────────────────────────────────┘"
            ], "The end. Or is it?")
        ]
        
        return [
            ComicPage("TEETH", page1_panels),
            ComicPage("THE BIRDS", page2_panels),
            ComicPage("RESOLUTION?", page3_panels)
        ]

    def render_page(self):
        """Render the current page."""
        self.canvas.clear()
        
        current_page_obj = self.pages[self.current_page]
        
        # Draw title
        title = f"Page {self.current_page + 1}: {current_page_obj.title}"
        self.canvas.put_text(2, 0, title, self.canvas.theme.accent)
        
        # Draw panels
        for i, panel in enumerate(current_page_obj.panels):
            # Highlight current panel in panel mode
            border_color = self.canvas.theme.accent if (self.reading_mode == "panel" and i == current_page_obj.current_panel) else self.canvas.theme.border
            
            # Draw panel content
            for j, line in enumerate(panel.content):
                if panel.y + j < self.terminal_size.lines - 3:
                    self.canvas.put_text(panel.x, panel.y + j, line, border_color)
            
            # Draw dialogue if in panel mode and this is the current panel
            if self.reading_mode == "panel" and i == current_page_obj.current_panel and panel.dialogue:
                dialogue_y = self.terminal_size.lines - 5
                dialogue_text = f"💬 {panel.dialogue}"
                if len(dialogue_text) <= self.terminal_size.columns - 4:
                    self.canvas.put_text(2, dialogue_y, dialogue_text, self.canvas.theme.secondary)
        
        # Draw navigation info
        nav_y = self.terminal_size.lines - 3
        if self.reading_mode == "page":
            nav_text = f"Page {self.current_page + 1}/{len(self.pages)} | ← → to navigate | SPACE for panel mode | Q to quit"
        else:
            current_panel = current_page_obj.current_panel + 1
            total_panels = len(current_page_obj.panels)
            nav_text = f"Panel {current_panel}/{total_panels} | ← → to navigate | SPACE for page mode | Q to quit"
        
        if len(nav_text) <= self.terminal_size.columns:
            self.canvas.put_text(0, nav_y, nav_text, self.canvas.theme.secondary)
        
        return self.canvas.render()

    def handle_input(self):
        """Handle keyboard input in a separate thread."""
        try:
            while self.running:
                try:
                    key = SimpleInput.get_key()
                    if key == 'q' or key == '\x03':  # q or Ctrl+C
                        self.running = False
                    elif key == ' ':  # Space to toggle mode
                        if self.reading_mode == "page":
                            self.reading_mode = "panel"
                            self.pages[self.current_page].current_panel = 0
                        else:
                            self.reading_mode = "page"
                    elif key == '\x1b':  # Escape sequence
                        next1 = SimpleInput.get_key()
                        if next1 == '[':
                            next2 = SimpleInput.get_key()
                            if next2 == 'D':  # Left arrow
                                if self.reading_mode == "page":
                                    self.current_page = max(0, self.current_page - 1)
                                else:
                                    current_page_obj = self.pages[self.current_page]
                                    current_page_obj.current_panel = max(0, current_page_obj.current_panel - 1)
                            elif next2 == 'C':  # Right arrow
                                if self.reading_mode == "page":
                                    self.current_page = min(len(self.pages) - 1, self.current_page + 1)
                                else:
                                    current_page_obj = self.pages[self.current_page]
                                    current_page_obj.current_panel = min(len(current_page_obj.panels) - 1, current_page_obj.current_panel + 1)
                except:
                    pass
        except:
            pass

    def run(self):
        """Main reader loop."""
        clear_screen()
        hide_cursor()
        
        print(f"{ArtisticThemes.MINIMAL.accent}Gutter{ArtisticThemes.MINIMAL.reset}")
        print(f"{ArtisticThemes.MINIMAL.secondary}Issue #3 - ASCII Comic Reader{ArtisticThemes.MINIMAL.reset}")
        print()
        time.sleep(2)
        
        self.running = True
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        try:
            while self.running:
                # Render frame
                clear_screen()
                print(self.render_page())
                
                # Brief pause for smooth updates
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            show_cursor()
            clear_screen()
            
            # Show final message
            print(f"{ArtisticThemes.MINIMAL.accent}Gutter{ArtisticThemes.MINIMAL.reset}")
            print()
            print(f"{ArtisticThemes.MINIMAL.primary}Thanks for reading about the tooth birds!{ArtisticThemes.MINIMAL.reset}")
            print()
            print(f"{ArtisticThemes.MINIMAL.secondary}Sequential art in the terminal - where every character counts.{ArtisticThemes.MINIMAL.reset}")
            print()


if __name__ == "__main__":
    reader = GutterReader()
    reader.run()