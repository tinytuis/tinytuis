#!/usr/bin/env python3
"""
Echo Chamber - Issue #4
Type words and watch them echo, distort, and transform in the digital void.
Explore how meaning changes through repetition and digital decay.
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
class Echo:
    text: str
    x: int
    y: int
    age: int
    distortion: float
    fade: float


class EchoChamber:
    def __init__(self):
        self.running = False
        self.terminal_size = get_terminal_size()
        self.canvas = Canvas(self.terminal_size.columns, self.terminal_size.lines - 4, ArtisticThemes.MINIMAL)
        self.echoes: List[Echo] = []
        self.input_text = ""
        self.cursor_pos = 0
        self.echo_count = 0
        
        # Distortion characters for glitch effects
        self.distortion_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?~`"
        
        # Predefined responses that the chamber might echo back
        self.chamber_responses = [
            "hello... hello... hello...",
            "is anyone there?",
            "the void stares back",
            "your words dissolve here",
            "echo... echo... echo...",
            "silence speaks louder",
            "digital ghosts whisper",
            "fragments of meaning",
            "lost in translation",
            "the chamber remembers",
            "words become noise",
            "meaning fades away",
            "only echoes remain"
        ]

    def distort_text(self, text: str, distortion_level: float) -> str:
        """Apply distortion effects to text."""
        if distortion_level <= 0:
            return text
            
        result = ""
        for char in text:
            if random.random() < distortion_level:
                if char == ' ':
                    result += ' '
                else:
                    result += random.choice(self.distortion_chars)
            else:
                result += char
        return result

    def add_echo(self, text: str, delay: int = 0):
        """Add a new echo to the chamber."""
        if not text.strip():
            return
            
        # Calculate position for the echo
        base_y = 5 + len(self.echoes) * 2
        if base_y >= self.terminal_size.lines - 6:
            # Remove oldest echoes if we're running out of space
            self.echoes = self.echoes[-10:]
            base_y = 5 + len(self.echoes) * 2
        
        x = random.randint(2, max(2, self.terminal_size.columns - len(text) - 2))
        
        echo = Echo(
            text=text,
            x=x,
            y=base_y + delay,
            age=0,
            distortion=0.0,
            fade=1.0
        )
        
        self.echoes.append(echo)

    def update_echoes(self):
        """Update all echoes - aging, distortion, fading."""
        for echo in self.echoes[:]:
            echo.age += 1
            
            # Increase distortion over time
            if echo.age > 20:
                echo.distortion = min(0.8, (echo.age - 20) * 0.02)
            
            # Start fading after some time
            if echo.age > 50:
                echo.fade = max(0, 1.0 - (echo.age - 50) * 0.05)
            
            # Remove completely faded echoes
            if echo.fade <= 0:
                self.echoes.remove(echo)

    def process_input(self, text: str):
        """Process user input and create echoes."""
        if not text.strip():
            return
            
        # Add the original input
        self.add_echo(f"> {text}")
        
        # Create multiple echoes with variations
        variations = [
            text.lower(),
            text.upper(),
            text[::-1],  # reversed
            " ".join(text.split()[::-1]),  # word order reversed
        ]
        
        for i, variation in enumerate(variations):
            if variation != text:
                self.add_echo(f"  {variation}", i + 1)
        
        # Sometimes add a chamber response
        if random.random() < 0.3:
            response = random.choice(self.chamber_responses)
            self.add_echo(f"    [{response}]", len(variations) + 1)
        
        self.echo_count += 1

    def render_frame(self):
        """Render the current frame."""
        self.canvas.clear()
        
        # Title
        title = "ECHO CHAMBER"
        self.canvas.put_text((self.terminal_size.columns - len(title)) // 2, 1, title, self.canvas.theme.accent)
        
        # Subtitle
        subtitle = "Type and press ENTER to echo into the void"
        if len(subtitle) <= self.terminal_size.columns:
            self.canvas.put_text((self.terminal_size.columns - len(subtitle)) // 2, 2, subtitle, self.canvas.theme.secondary)
        
        # Render echoes
        for echo in self.echoes:
            if 0 <= echo.y < self.terminal_size.lines - 4:
                # Apply distortion
                display_text = self.distort_text(echo.text, echo.distortion)
                
                # Apply fading by adjusting color intensity
                if echo.fade < 0.5:
                    color = self.canvas.theme.secondary
                elif echo.fade < 0.8:
                    color = self.canvas.theme.text
                else:
                    color = self.canvas.theme.primary
                
                # Ensure text fits on screen
                if echo.x + len(display_text) > self.terminal_size.columns:
                    display_text = display_text[:self.terminal_size.columns - echo.x - 1]
                
                self.canvas.put_text(echo.x, echo.y, display_text, color)
        
        # Input area
        input_y = self.terminal_size.lines - 4
        prompt = "Say something: "
        self.canvas.put_text(0, input_y, prompt, self.canvas.theme.accent)
        
        # Current input with cursor
        input_display = self.input_text
        if len(input_display) > self.terminal_size.columns - len(prompt) - 2:
            input_display = input_display[-(self.terminal_size.columns - len(prompt) - 2):]
        
        self.canvas.put_text(len(prompt), input_y, input_display, self.canvas.theme.text)
        
        # Cursor
        cursor_x = len(prompt) + len(input_display)
        if cursor_x < self.terminal_size.columns:
            self.canvas.put_text(cursor_x, input_y, "_", self.canvas.theme.primary)
        
        # Stats
        stats = f"Echoes created: {self.echo_count} | Active: {len(self.echoes)} | 'q' to quit"
        if len(stats) <= self.terminal_size.columns:
            self.canvas.put_text(0, self.terminal_size.lines - 2, stats, self.canvas.theme.secondary)
        
        return self.canvas.render()

    def handle_input(self):
        """Handle keyboard input in a separate thread."""
        try:
            while self.running:
                try:
                    key = SimpleInput.get_key()
                    if key == 'q' or key == '\x03':  # q or Ctrl+C
                        self.running = False
                    elif key == '\r' or key == '\n':  # Enter
                        self.process_input(self.input_text)
                        self.input_text = ""
                    elif key == '\x7f' or key == '\b':  # Backspace
                        if self.input_text:
                            self.input_text = self.input_text[:-1]
                    elif key == '\x1b':  # Escape sequences (ignore for now)
                        try:
                            SimpleInput.get_key()  # consume next char
                            SimpleInput.get_key()  # consume next char
                        except:
                            pass
                    elif len(key) == 1 and ord(key) >= 32:  # Printable characters
                        if len(self.input_text) < 100:  # Limit input length
                            self.input_text += key
                except:
                    pass
        except:
            pass

    def run(self):
        """Main loop."""
        clear_screen()
        hide_cursor()
        
        print(f"{ArtisticThemes.MINIMAL.accent}Echo Chamber{ArtisticThemes.MINIMAL.reset}")
        print(f"{ArtisticThemes.MINIMAL.secondary}Issue #4 - A TinyTUI Experience{ArtisticThemes.MINIMAL.reset}")
        print()
        time.sleep(2)
        
        self.running = True
        
        # Add some initial echoes to set the mood
        self.add_echo("Welcome to the echo chamber...")
        self.add_echo("  Your words will be transformed here")
        self.add_echo("    Speak into the digital void")
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        try:
            while self.running:
                # Update echoes
                self.update_echoes()
                
                # Render frame
                clear_screen()
                print(self.render_frame())
                
                # Brief pause for animation
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            pass
        finally:
            show_cursor()
            clear_screen()
            
            # Show final message
            print(f"{ArtisticThemes.MINIMAL.accent}Echo Chamber{ArtisticThemes.MINIMAL.reset}")
            print()
            print(f"{ArtisticThemes.MINIMAL.primary}Your words have joined the eternal echo...{ArtisticThemes.MINIMAL.reset}")
            print()
            if self.echo_count > 0:
                print(f"{ArtisticThemes.MINIMAL.secondary}You created {self.echo_count} echoes in the digital void.{ArtisticThemes.MINIMAL.reset}")
                print(f"{ArtisticThemes.MINIMAL.secondary}Each one a fragment of meaning, transformed by repetition.{ArtisticThemes.MINIMAL.reset}")
            else:
                print(f"{ArtisticThemes.MINIMAL.secondary}The chamber remains silent, waiting for your voice...{ArtisticThemes.MINIMAL.reset}")
            print()


if __name__ == "__main__":
    chamber = EchoChamber()
    chamber.run()