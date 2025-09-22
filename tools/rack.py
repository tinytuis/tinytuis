#!/usr/bin/env python3
"""
Rack of Zines - The TinyTUIs Catalog Browser
Issue #10 - A launcher that displays all TinyTUIs like issues on a spinner rack.
"""

import sys
import os
import subprocess
from dataclasses import dataclass
from typing import List, Optional

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))
from tinykit import Canvas, ArtisticThemes, clear_screen, SimpleInput, typewriter_effect


@dataclass
class Issue:
    number: int
    title: str
    description: str
    path: str
    status: str = "available"  # available, coming_soon, prototype


class RackOfZines:
    def __init__(self):
        self.theme = ArtisticThemes.MINIMAL
        self.selected_index = 0
        
        # Define the catalog of issues
        self.issues = [
            Issue(1, "Winter Hush", 
                  "ASCII snow drifting down the terminal. Catch snowflakes to reveal fragments of text.",
                  "issues/winter-hush/main.py"),
            Issue(2, "Fragments.txt", 
                  "A scrolling stack of notes, quotes, diary lines. Stitch fragments into narrative.",
                  "issues/fragments-txt/main.py", "coming_soon"),
            Issue(3, "Gutter", 
                  "A comic reader in the terminal. ASCII panels navigated with arrow keys.",
                  "issues/gutter/main.py", "coming_soon"),
            Issue(4, "Echo Chamber", 
                  "Anything typed echoes back distorted. Strange dialogue between user and machine.",
                  "issues/echo-chamber/main.py", "coming_soon"),
            Issue(5, "Amber Light", 
                  "Retro amber terminal theme. Logs from a fictional machine, sci-fi diary entries.",
                  "issues/amber-light/main.py", "coming_soon"),
            Issue(6, "Caret Cuts", 
                  "Very short one-shot TUIs. Words unraveling, ASCII constellations, conversations.",
                  "issues/caret-cuts/main.py", "coming_soon"),
            Issue(7, "Exquisite Pane", 
                  "Collaborative exquisite-corpse comic. Contributors add panels to surreal zine.",
                  "issues/exquisite-pane/main.py", "coming_soon"),
            Issue(8, "The Prompt", 
                  "TUI asks questions. Your answers shape the story. Interactive fiction meets diary.",
                  "issues/the-prompt/main.py", "coming_soon"),
            Issue(9, "Monospace Dreams", 
                  "Dreamlike text fragments drift and recombine. Surreal, generative dream zine.",
                  "issues/monospace-dreams/main.py", "coming_soon"),
        ]
    
    def draw_header(self):
        """Draw the rack header."""
        print(f"{self.theme.accent}╔══════════════════════════════════════════════════════════════════════════════╗{self.theme.reset}")
        print(f"{self.theme.accent}║{self.theme.primary}                              TinyTUIs Rack                                {self.theme.accent}║{self.theme.reset}")
        print(f"{self.theme.accent}║{self.theme.secondary}                        A Small Press for the Terminal                       {self.theme.accent}║{self.theme.reset}")
        print(f"{self.theme.accent}╚══════════════════════════════════════════════════════════════════════════════╝{self.theme.reset}")
        print()
    
    def draw_issue_spine(self, issue: Issue, is_selected: bool, width: int = 76):
        """Draw an issue as a spine on the rack."""
        if is_selected:
            bg = "\033[7m"  # Reverse video
            border_char = "█"
            color = self.theme.accent
        else:
            bg = ""
            border_char = "│"
            if issue.status == "available":
                color = self.theme.primary
            elif issue.status == "coming_soon":
                color = self.theme.secondary
            else:
                color = self.theme.text
        
        # Status indicator
        if issue.status == "available":
            status_icon = "●"
        elif issue.status == "coming_soon":
            status_icon = "○"
        else:
            status_icon = "◐"
        
        # Format the spine
        number_str = f"#{issue.number:02d}"
        title_space = width - len(number_str) - 8  # Account for borders and status
        
        if len(issue.title) > title_space:
            display_title = issue.title[:title_space-3] + "..."
        else:
            display_title = issue.title.ljust(title_space)
        
        spine = f"{bg}{color}{border_char} {number_str} {status_icon} {display_title} {border_char}{self.theme.reset}"
        print(spine)
    
    def draw_issue_details(self, issue: Issue):
        """Draw detailed information about the selected issue."""
        print()
        print(f"{self.theme.accent}┌─ Issue Details ─────────────────────────────────────────────────────────────┐{self.theme.reset}")
        print(f"{self.theme.accent}│{self.theme.reset}")
        
        # Title and number
        title_line = f"  Issue #{issue.number}: {issue.title}"
        padding = 78 - len(title_line)
        print(f"{self.theme.accent}│{self.theme.primary}{title_line}{' ' * padding}{self.theme.accent}│{self.theme.reset}")
        print(f"{self.theme.accent}│{' ' * 78}{self.theme.accent}│{self.theme.reset}")
        
        # Description (word wrap)
        words = issue.description.split()
        lines = []
        current_line = "  "
        
        for word in words:
            if len(current_line + word + " ") <= 76:
                current_line += word + " "
            else:
                lines.append(current_line.rstrip())
                current_line = "  " + word + " "
        
        if current_line.strip():
            lines.append(current_line.rstrip())
        
        for line in lines:
            padding = 78 - len(line)
            print(f"{self.theme.accent}│{self.theme.text}{line}{' ' * padding}{self.theme.accent}│{self.theme.reset}")
        
        print(f"{self.theme.accent}│{' ' * 78}{self.theme.accent}│{self.theme.reset}")
        
        # Status
        if issue.status == "available":
            status_text = f"  Status: {self.theme.primary}Available - Press ENTER to run{self.theme.text}"
        elif issue.status == "coming_soon":
            status_text = f"  Status: {self.theme.secondary}Coming Soon{self.theme.text}"
        else:
            status_text = f"  Status: {self.theme.secondary}Prototype{self.theme.text}"
        
        padding = 78 - len(status_text) + len(self.theme.primary) + len(self.theme.text)  # Account for color codes
        print(f"{self.theme.accent}│{status_text}{' ' * (padding - len(self.theme.primary) - len(self.theme.text))}{self.theme.accent}│{self.theme.reset}")
        
        print(f"{self.theme.accent}└─────────────────────────────────────────────────────────────────────────────┘{self.theme.reset}")
    
    def draw_controls(self):
        """Draw control instructions."""
        print()
        print(f"{self.theme.secondary}Controls: ↑↓ Navigate • ENTER Run Issue • q Quit{self.theme.reset}")
    
    def run_issue(self, issue: Issue):
        """Run the selected issue."""
        if issue.status != "available":
            print(f"\n{self.theme.secondary}This issue is not yet available.{self.theme.reset}")
            input(f"{self.theme.text}Press ENTER to continue...{self.theme.reset}")
            return
        
        if not os.path.exists(issue.path):
            print(f"\n{self.theme.secondary}Issue file not found: {issue.path}{self.theme.reset}")
            input(f"{self.theme.text}Press ENTER to continue...{self.theme.reset}")
            return
        
        clear_screen()
        print(f"{self.theme.accent}Launching {issue.title}...{self.theme.reset}")
        print()
        
        try:
            # Run the issue
            subprocess.run([sys.executable, issue.path], check=True)
        except subprocess.CalledProcessError as e:
            print(f"\n{self.theme.secondary}Error running issue: {e}{self.theme.reset}")
        except KeyboardInterrupt:
            print(f"\n{self.theme.secondary}Issue interrupted.{self.theme.reset}")
        
        print()
        input(f"{self.theme.text}Press ENTER to return to the rack...{self.theme.reset}")
    
    def show_intro(self):
        """Show the intro sequence."""
        clear_screen()
        
        # Animated intro
        typewriter_effect("TinyTUIs", 0.1, self.theme.accent)
        typewriter_effect("A Small Press for the Terminal", 0.05, self.theme.secondary)
        print()
        typewriter_effect("Where code meets zine culture...", 0.03, self.theme.text)
        print()
        
        input(f"{self.theme.secondary}Press ENTER to browse the rack...{self.theme.reset}")
    
    def run(self):
        """Main program loop."""
        self.show_intro()
        
        while True:
            clear_screen()
            self.draw_header()
            
            # Draw all issue spines
            for i, issue in enumerate(self.issues):
                self.draw_issue_spine(issue, i == self.selected_index)
            
            # Draw details for selected issue
            if 0 <= self.selected_index < len(self.issues):
                self.draw_issue_details(self.issues[self.selected_index])
            
            self.draw_controls()
            
            # Get input
            try:
                key = SimpleInput.get_key()
                
                if key == 'q' or key == '\x03':  # q or Ctrl+C
                    break
                elif key == '\r' or key == '\n':  # Enter
                    if 0 <= self.selected_index < len(self.issues):
                        self.run_issue(self.issues[self.selected_index])
                elif key == '\x1b':  # Escape sequence (arrow keys)
                    next1 = SimpleInput.get_key()
                    if next1 == '[':
                        next2 = SimpleInput.get_key()
                        if next2 == 'A':  # Up arrow
                            self.selected_index = max(0, self.selected_index - 1)
                        elif next2 == 'B':  # Down arrow
                            self.selected_index = min(len(self.issues) - 1, self.selected_index + 1)
                
            except KeyboardInterrupt:
                break
        
        clear_screen()
        print(f"{self.theme.accent}Thank you for browsing TinyTUIs{self.theme.reset}")
        print(f"{self.theme.secondary}Where terminal interfaces become art{self.theme.reset}")
        print()


if __name__ == "__main__":
    rack = RackOfZines()
    rack.run()