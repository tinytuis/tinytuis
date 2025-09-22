#!/usr/bin/env python3
"""
Fragments.txt - Issue #2
A stream of text fragments flowing down the terminal.
Catch fragments with spacebar to stitch them into coherent thoughts.
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
class Fragment:
    x: float
    y: float
    text: str
    speed: float
    caught: bool = False
    fade: float = 1.0


class FragmentsStream:
    def __init__(self):
        self.running = False
        self.terminal_size = get_terminal_size()
        self.canvas = Canvas(self.terminal_size.columns, self.terminal_size.lines - 3, ArtisticThemes.NEBULA)
        self.fragments: List[Fragment] = []
        self.caught_fragments = []
        self.catch_zone_y = self.terminal_size.lines - 8
        
        # Text fragments that flow down
        self.fragment_pool = [
            "memory", "fragments", "scattered", "thoughts", "broken", "pieces",
            "whispers", "echoes", "remnants", "traces", "shadows", "glimpses",
            "fleeting", "moments", "lost", "words", "fading", "dreams",
            "half", "remembered", "stories", "untold", "secrets", "hidden",
            "meanings", "between", "lines", "spaces", "silence", "speaks",
            "volumes", "unspoken", "truths", "buried", "deep", "within",
            "consciousness", "streams", "flowing", "endless", "rivers",
            "time", "carries", "everything", "away", "nothing", "remains",
            "except", "these", "small", "fragments", "of", "what", "was",
            "once", "whole", "now", "scattered", "like", "leaves", "in",
            "autumn", "wind", "gathering", "them", "together", "again",
            "piece", "by", "piece", "slowly", "rebuilding", "the", "story"
        ]
        
        # Catch zone indicator
        self.catch_indicator = "[ CATCH ZONE ]"

    def create_fragment(self):
        """Create a new fragment at the top of the screen."""
        text = random.choice(self.fragment_pool)
        x = random.uniform(0, max(0, self.terminal_size.columns - len(text) - 1))
        speed = random.uniform(0.2, 0.5)
        
        return Fragment(x, 0, text, speed)

    def update_fragments(self):
        """Update fragment positions and handle catching."""
        # Remove fragments that have fallen off screen
        self.fragments = [f for f in self.fragments if f.y < self.terminal_size.lines - 2]
        
        # Update positions
        for fragment in self.fragments:
            if not fragment.caught:
                fragment.y += fragment.speed
            else:
                # Caught fragments fade and move to collection
                fragment.fade -= 0.05
                if fragment.fade <= 0:
                    self.fragments.remove(fragment)

    def try_catch_fragment(self):
        """Try to catch fragments in the catch zone."""
        caught_any = False
        for fragment in self.fragments:
            if (not fragment.caught and 
                self.catch_zone_y - 1 <= fragment.y <= self.catch_zone_y + 1):
                fragment.caught = True
                self.caught_fragments.append(fragment.text)
                caught_any = True
                
                # Remove from pool to avoid repetition
                if fragment.text in self.fragment_pool:
                    self.fragment_pool.remove(fragment.text)
                    
        return caught_any

    def render_frame(self):
        """Render a single frame."""
        self.canvas.clear()
        
        # Draw fragments
        for fragment in self.fragments:
            if 0 <= int(fragment.y) < self.terminal_size.lines - 3:
                if fragment.caught:
                    # Caught fragments glow and fade
                    color = f"\033[38;2;{int(100*fragment.fade)};{int(255*fragment.fade)};{int(150*fragment.fade)}m"
                else:
                    color = self.canvas.theme.primary
                    
                self.canvas.put_text(int(fragment.x), int(fragment.y), fragment.text, color)
        
        # Draw catch zone
        catch_x = (self.terminal_size.columns - len(self.catch_indicator)) // 2
        if catch_x >= 0:
            self.canvas.put_text(catch_x, self.catch_zone_y, self.catch_indicator, self.canvas.theme.accent)
        
        # Draw caught fragments at bottom
        if self.caught_fragments:
            # Show last few caught fragments
            recent = self.caught_fragments[-8:]  # Show last 8
            text = " → ".join(recent)
            if len(text) > self.terminal_size.columns - 2:
                text = "..." + text[-(self.terminal_size.columns - 5):]
            
            self.canvas.put_text(1, self.terminal_size.lines - 4, "Caught:", self.canvas.theme.secondary)
            self.canvas.put_text(1, self.terminal_size.lines - 3, text, self.canvas.theme.text)
        
        # Instructions
        if not self.caught_fragments:
            instruction = "Press SPACE to catch fragments in the catch zone. 'q' to quit."
            if len(instruction) <= self.terminal_size.columns:
                self.canvas.put_text(
                    (self.terminal_size.columns - len(instruction)) // 2,
                    self.terminal_size.lines - 2,
                    instruction,
                    self.canvas.theme.secondary
                )
        else:
            count_text = f"Fragments caught: {len(self.caught_fragments)}"
            self.canvas.put_text(
                self.terminal_size.columns - len(count_text) - 1,
                self.terminal_size.lines - 2,
                count_text,
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
                    elif key == ' ':  # Space to catch
                        self.try_catch_fragment()
                except:
                    pass
        except:
            pass

    def run(self):
        """Main game loop."""
        clear_screen()
        hide_cursor()
        
        print(f"{ArtisticThemes.NEBULA.accent}Fragments.txt{ArtisticThemes.NEBULA.reset}")
        print(f"{ArtisticThemes.NEBULA.secondary}Issue #2 - A TinyTUI Experience{ArtisticThemes.NEBULA.reset}")
        print()
        time.sleep(2)
        
        self.running = True
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        last_fragment = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Create new fragments periodically
                if current_time - last_fragment > random.uniform(0.3, 0.8):
                    if self.fragment_pool:  # Only if we have fragments left
                        self.fragments.append(self.create_fragment())
                    last_fragment = current_time
                
                # Update simulation
                self.update_fragments()
                
                # Render frame
                clear_screen()
                print(self.render_frame())
                
                # Brief pause for animation
                time.sleep(0.08)
                
        except KeyboardInterrupt:
            pass
        finally:
            show_cursor()
            clear_screen()
            
            # Show final message
            print(f"{ArtisticThemes.NEBULA.accent}Fragments.txt{ArtisticThemes.NEBULA.reset}")
            print()
            if self.caught_fragments:
                print(f"{ArtisticThemes.NEBULA.primary}You stitched together these fragments:{ArtisticThemes.NEBULA.reset}")
                
                # Show the complete story
                story = " ".join(self.caught_fragments)
                words = story.split()
                
                # Format into lines
                lines = []
                current_line = []
                for word in words:
                    if len(" ".join(current_line + [word])) <= 60:
                        current_line.append(word)
                    else:
                        if current_line:
                            lines.append(" ".join(current_line))
                        current_line = [word]
                
                if current_line:
                    lines.append(" ".join(current_line))
                
                for line in lines:
                    print(f"{ArtisticThemes.NEBULA.secondary}  {line}{ArtisticThemes.NEBULA.reset}")
                    
                print()
                print(f"{ArtisticThemes.NEBULA.text}Total fragments: {len(self.caught_fragments)}{ArtisticThemes.NEBULA.reset}")
            else:
                print(f"{ArtisticThemes.NEBULA.secondary}The fragments scattered in the wind...{ArtisticThemes.NEBULA.reset}")
            
            print()


if __name__ == "__main__":
    stream = FragmentsStream()
    stream.run()