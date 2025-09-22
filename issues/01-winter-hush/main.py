#!/usr/bin/env python3
"""
Winter Hush - Issue #1
A quiet, contemplative experience of ASCII snow drifting down the terminal.
Catch snowflakes to reveal fragments of text.
"""

import sys
import os
import time
import random
import threading
from dataclasses import dataclass
from typing import List, Optional

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tinykit import Canvas, ArtisticThemes, clear_screen, hide_cursor, show_cursor, get_terminal_size, SimpleInput


@dataclass
class Snowflake:
    x: float
    y: float
    char: str
    speed: float
    drift: float
    fragment: Optional[str] = None


class WinterHush:
    def __init__(self):
        self.running = False
        self.terminal_size = get_terminal_size()
        self.canvas = Canvas(self.terminal_size.columns, self.terminal_size.lines - 1, ArtisticThemes.WINTER)
        self.snowflakes: List[Snowflake] = []
        self.caught_fragments = []
        self.cursor_x = self.terminal_size.columns // 2
        
        # Text fragments hidden in snowflakes
        self.fragments = [
            "winter whispers secrets",
            "silence falls like snow",
            "each flake a memory",
            "cold breath on glass",
            "footprints fade away",
            "the world sleeps white",
            "stars hide behind clouds",
            "time moves slowly here",
            "everything is hushed",
            "beauty in the quiet",
            "snow covers all wounds",
            "peace in the falling",
            "white blanket of dreams",
            "winter's gentle touch",
            "stillness speaks volumes"
        ]
        
        # Snowflake characters
        self.snow_chars = ["❄", "❅", "❆", "*", "·", "•", "○"]
    
    def create_snowflake(self):
        """Create a new snowflake at the top of the screen."""
        x = random.uniform(0, self.terminal_size.columns - 1)
        char = random.choice(self.snow_chars)
        speed = random.uniform(0.1, 0.3)
        drift = random.uniform(-0.1, 0.1)
        
        # Some snowflakes carry text fragments
        fragment = None
        if random.random() < 0.25 and self.fragments:  # 25% chance
            fragment = random.choice(self.fragments)
        
        return Snowflake(x, 0, char, speed, drift, fragment)
    
    def update_snowflakes(self):
        """Update snowflake positions."""
        # Remove snowflakes that have fallen off screen
        self.snowflakes = [s for s in self.snowflakes if s.y < self.terminal_size.lines]
        
        # Update positions
        for flake in self.snowflakes:
            flake.y += flake.speed
            flake.x += flake.drift
            
            # Wrap around horizontally
            if flake.x < 0:
                flake.x = self.terminal_size.columns - 1
            elif flake.x >= self.terminal_size.columns:
                flake.x = 0
    
    def check_catches(self):
        """Check if cursor caught any snowflakes."""
        caught = []
        remaining = []
        
        cursor_y = self.terminal_size.lines - 3  # Cursor position
        
        for flake in self.snowflakes:
            # Check if snowflake is near cursor (expanded collision area)
            # Use a larger collision area and account for floating point positions
            x_distance = abs(flake.x - self.cursor_x)
            y_distance = abs(flake.y - cursor_y)
            
            if (x_distance <= 2.0 and y_distance <= 1.5):
                caught.append(flake)
                if flake.fragment:
                    self.caught_fragments.append(flake.fragment)
                    # Remove from available fragments
                    if flake.fragment in self.fragments:
                        self.fragments.remove(flake.fragment)
            else:
                remaining.append(flake)
        
        self.snowflakes = remaining
        return len(caught) > 0
    
    def render_frame(self):
        """Render a single frame."""
        self.canvas.clear()
        
        # Draw snowflakes
        for flake in self.snowflakes:
            if 0 <= int(flake.x) < self.terminal_size.columns and 0 <= int(flake.y) < self.terminal_size.lines - 1:
                color = self.canvas.theme.accent if flake.fragment else self.canvas.theme.primary
                self.canvas.put_char(int(flake.x), int(flake.y), flake.char, color)
        
        # Draw cursor (a small shelter)
        cursor_y = self.terminal_size.lines - 3
        if 0 <= self.cursor_x < self.terminal_size.columns:
            self.canvas.put_char(self.cursor_x, cursor_y, "^", self.canvas.theme.text)
        
        # Draw caught fragments at bottom
        if self.caught_fragments:
            y_pos = self.terminal_size.lines - 2
            text = " • ".join(self.caught_fragments[-5:])  # Show last 5
            if len(text) > self.terminal_size.columns - 2:
                text = text[:self.terminal_size.columns - 5] + "..."
            self.canvas.put_text(1, y_pos, text, self.canvas.theme.secondary)
        
        # Instructions
        if not self.caught_fragments:
            instruction = "Move with ← → to catch snowflakes. Press 'q' to quit."
            if len(instruction) <= self.terminal_size.columns:
                self.canvas.put_text(
                    (self.terminal_size.columns - len(instruction)) // 2,
                    self.terminal_size.lines - 2,
                    instruction,
                    self.canvas.theme.secondary
                )
        
        return self.canvas.render()
    
    def handle_input(self):
        """Handle keyboard input in a separate thread."""
        try:
            while self.running:
                try:
                    key = SimpleInput.get_key()
                    if key == 'q' or key == '\x03':  # q or Ctrl+C
                        self.running = False
                    elif key == '\x1b':  # Escape sequence
                        next1 = SimpleInput.get_key()
                        if next1 == '[':
                            next2 = SimpleInput.get_key()
                            if next2 == 'D':  # Left arrow
                                self.cursor_x = max(0, self.cursor_x - 1)
                            elif next2 == 'C':  # Right arrow
                                self.cursor_x = min(self.terminal_size.columns - 1, self.cursor_x + 1)
                except:
                    pass
        except:
            pass
    
    def run(self):
        """Main game loop."""
        clear_screen()
        hide_cursor()
        
        print(f"{ArtisticThemes.WINTER.accent}Winter Hush{ArtisticThemes.WINTER.reset}")
        print(f"{ArtisticThemes.WINTER.secondary}Issue #1 - A TinyTUI Experience{ArtisticThemes.WINTER.reset}")
        print()
        time.sleep(2)
        
        self.running = True
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        last_snowflake = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Create new snowflakes periodically
                if current_time - last_snowflake > random.uniform(0.1, 0.5):
                    self.snowflakes.append(self.create_snowflake())
                    last_snowflake = current_time
                
                # Update simulation
                self.update_snowflakes()
                caught = self.check_catches()
                
                # Render frame
                clear_screen()
                print(self.render_frame())
                
                # Brief pause for animation
                time.sleep(0.05)
                
        except KeyboardInterrupt:
            pass
        finally:
            show_cursor()
            clear_screen()
            
            # Show final message
            print(f"{ArtisticThemes.WINTER.accent}Winter Hush{ArtisticThemes.WINTER.reset}")
            print()
            if self.caught_fragments:
                print(f"{ArtisticThemes.WINTER.primary}You caught these whispers:{ArtisticThemes.WINTER.reset}")
                for fragment in self.caught_fragments:
                    print(f"{ArtisticThemes.WINTER.secondary}  • {fragment}{ArtisticThemes.WINTER.reset}")
            else:
                print(f"{ArtisticThemes.WINTER.secondary}The snow falls silently...{ArtisticThemes.WINTER.reset}")
            print()


if __name__ == "__main__":
    game = WinterHush()
    game.run()