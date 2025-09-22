#!/usr/bin/env python3
"""
Caret Cuts - Issue #6
Symbol constellation experiments with rotating symbols and micro-interactions.
Watch as ASCII symbols dance in patterns, creating ephemeral constellations.
"""

import sys
import os
import time
import random
import math
import threading
from dataclasses import dataclass
from typing import List, Tuple

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tinykit import Canvas, ArtisticThemes, clear_screen, hide_cursor, show_cursor, get_terminal_size, SimpleInput


@dataclass
class Symbol:
    char: str
    x: float
    y: float
    rotation: float
    rotation_speed: float
    pulse: float
    pulse_speed: float
    age: int = 0
    constellation_id: int = -1


@dataclass
class Constellation:
    symbols: List[Symbol]
    center_x: float
    center_y: float
    rotation: float
    rotation_speed: float
    lifetime: int
    age: int = 0


class CaretCuts:
    def __init__(self):
        self.running = False
        self.terminal_size = get_terminal_size()
        self.canvas = Canvas(self.terminal_size.columns, self.terminal_size.lines - 2, ArtisticThemes.MINIMAL)
        self.symbols: List[Symbol] = []
        self.constellations: List[Constellation] = []
        self.experiment_mode = 0  # 0: free symbols, 1: constellations, 2: micro-interactions
        self.mode_names = ["Free Symbols", "Constellations", "Micro-Interactions"]
        
        # Symbol sets for different experiments
        self.symbol_sets = {
            'basic': ['*', '+', 'x', 'o', '.', '·', '•', '◦', '○', '●'],
            'geometric': ['△', '▲', '▽', '▼', '◇', '◆', '□', '■', '◯', '◉'],
            'arrows': ['↑', '↓', '←', '→', '↖', '↗', '↘', '↙', '↕', '↔'],
            'math': ['∞', '∑', '∆', '∇', '∂', '∫', '√', '±', '≈', '≠'],
            'misc': ['^', 'v', '<', '>', '~', '`', "'", '"', '|', '-']
        }
        
        self.current_symbol_set = 'basic'

    def create_random_symbol(self):
        """Create a random symbol."""
        symbols = self.symbol_sets[self.current_symbol_set]
        return Symbol(
            char=random.choice(symbols),
            x=random.uniform(2, self.terminal_size.columns - 3),
            y=random.uniform(2, self.terminal_size.lines - 5),
            rotation=random.uniform(0, 2 * math.pi),
            rotation_speed=random.uniform(-0.1, 0.1),
            pulse=random.uniform(0, 2 * math.pi),
            pulse_speed=random.uniform(0.05, 0.15)
        )

    def create_constellation(self):
        """Create a constellation of symbols."""
        center_x = random.uniform(10, self.terminal_size.columns - 10)
        center_y = random.uniform(5, self.terminal_size.lines - 8)
        num_symbols = random.randint(3, 7)
        
        constellation_symbols = []
        symbols = self.symbol_sets[self.current_symbol_set]
        
        for i in range(num_symbols):
            angle = (2 * math.pi * i) / num_symbols
            radius = random.uniform(3, 8)
            
            symbol = Symbol(
                char=random.choice(symbols),
                x=center_x + radius * math.cos(angle),
                y=center_y + radius * math.sin(angle),
                rotation=angle,
                rotation_speed=random.uniform(-0.05, 0.05),
                pulse=random.uniform(0, 2 * math.pi),
                pulse_speed=random.uniform(0.03, 0.08),
                constellation_id=len(self.constellations)
            )
            constellation_symbols.append(symbol)
        
        constellation = Constellation(
            symbols=constellation_symbols,
            center_x=center_x,
            center_y=center_y,
            rotation=0,
            rotation_speed=random.uniform(-0.02, 0.02),
            lifetime=random.randint(200, 500)
        )
        
        return constellation

    def update_symbols(self):
        """Update symbol positions and properties."""
        for symbol in self.symbols:
            # Update rotation
            symbol.rotation += symbol.rotation_speed
            
            # Update pulse
            symbol.pulse += symbol.pulse_speed
            
            # Age the symbol
            symbol.age += 1
            
            # Gentle drift
            if random.random() < 0.1:
                symbol.x += random.uniform(-0.5, 0.5)
                symbol.y += random.uniform(-0.3, 0.3)
            
            # Keep symbols in bounds
            symbol.x = max(1, min(self.terminal_size.columns - 2, symbol.x))
            symbol.y = max(1, min(self.terminal_size.lines - 3, symbol.y))
        
        # Remove old symbols
        self.symbols = [s for s in self.symbols if s.age < 300]

    def update_constellations(self):
        """Update constellation positions and properties."""
        for constellation in self.constellations:
            constellation.age += 1
            constellation.rotation += constellation.rotation_speed
            
            # Update constellation symbols
            for i, symbol in enumerate(constellation.symbols):
                angle = constellation.rotation + (2 * math.pi * i) / len(constellation.symbols)
                radius = 3 + 2 * math.sin(constellation.age * 0.02)  # Breathing effect
                
                symbol.x = constellation.center_x + radius * math.cos(angle)
                symbol.y = constellation.center_y + radius * math.sin(angle)
                symbol.rotation += symbol.rotation_speed
                symbol.pulse += symbol.pulse_speed
                symbol.age += 1
        
        # Remove expired constellations
        self.constellations = [c for c in self.constellations if c.age < c.lifetime]

    def create_micro_interaction(self, x: int, y: int):
        """Create a micro-interaction at the given position."""
        # Create a small burst of symbols
        for _ in range(random.randint(3, 6)):
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(1, 4)
            
            symbol = Symbol(
                char=random.choice(self.symbol_sets[self.current_symbol_set]),
                x=x + distance * math.cos(angle),
                y=y + distance * math.sin(angle),
                rotation=angle,
                rotation_speed=random.uniform(-0.2, 0.2),
                pulse=0,
                pulse_speed=random.uniform(0.1, 0.3)
            )
            self.symbols.append(symbol)

    def render_frame(self):
        """Render the current frame."""
        self.canvas.clear()
        
        # Header
        title = f"Caret Cuts - {self.mode_names[self.experiment_mode]}"
        self.canvas.put_text((self.terminal_size.columns - len(title)) // 2, 0, title, self.canvas.theme.accent)
        
        # Render symbols
        all_symbols = self.symbols[:]
        for constellation in self.constellations:
            all_symbols.extend(constellation.symbols)
        
        for symbol in all_symbols:
            if 0 <= symbol.x < self.terminal_size.columns and 0 <= symbol.y < self.terminal_size.lines - 2:
                # Calculate intensity based on pulse
                pulse_intensity = (math.sin(symbol.pulse) + 1) / 2
                
                # Choose color based on intensity and age
                if pulse_intensity > 0.7:
                    color = self.canvas.theme.accent
                elif pulse_intensity > 0.4:
                    color = self.canvas.theme.primary
                else:
                    color = self.canvas.theme.secondary
                
                # Apply age fading
                if symbol.age > 200:
                    color = self.canvas.theme.secondary
                
                self.canvas.put_text(int(symbol.x), int(symbol.y), symbol.char, color)
        
        # Status line
        status_y = self.terminal_size.lines - 2
        status_parts = [
            f"Mode: {self.mode_names[self.experiment_mode]}",
            f"Symbols: {len(self.symbols)}",
            f"Constellations: {len(self.constellations)}",
            f"Set: {self.current_symbol_set}"
        ]
        status = " | ".join(status_parts)
        
        if len(status) <= self.terminal_size.columns:
            self.canvas.put_text(0, status_y, status, self.canvas.theme.text)
        
        # Controls
        controls_y = self.terminal_size.lines - 1
        controls = "SPACE: mode | S: symbol set | CLICK: interact | Q: quit"
        if len(controls) <= self.terminal_size.columns:
            self.canvas.put_text(0, controls_y, controls, self.canvas.theme.secondary)
        
        return self.canvas.render()

    def handle_input(self):
        """Handle keyboard input in a separate thread."""
        try:
            while self.running:
                try:
                    key = SimpleInput.get_key()
                    if key == 'q' or key == '\x03':  # q or Ctrl+C
                        self.running = False
                    elif key == ' ':  # Space - change mode
                        self.experiment_mode = (self.experiment_mode + 1) % len(self.mode_names)
                        # Clear existing symbols when changing modes
                        self.symbols.clear()
                        self.constellations.clear()
                    elif key == 's':  # S - change symbol set
                        symbol_sets = list(self.symbol_sets.keys())
                        current_index = symbol_sets.index(self.current_symbol_set)
                        self.current_symbol_set = symbol_sets[(current_index + 1) % len(symbol_sets)]
                    # Ignore other keys for this demo
                except:
                    pass
        except:
            pass

    def run(self):
        """Main loop."""
        clear_screen()
        hide_cursor()
        
        print(f"{ArtisticThemes.MINIMAL.accent}Caret Cuts{ArtisticThemes.MINIMAL.reset}")
        print(f"{ArtisticThemes.MINIMAL.secondary}Issue #6 - Symbol Constellation Experiments{ArtisticThemes.MINIMAL.reset}")
        print()
        time.sleep(2)
        
        self.running = True
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        last_spawn_time = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Spawn new elements based on mode
                if current_time - last_spawn_time > random.uniform(0.5, 2.0):
                    if self.experiment_mode == 0:  # Free symbols
                        if len(self.symbols) < 20:
                            self.symbols.append(self.create_random_symbol())
                    elif self.experiment_mode == 1:  # Constellations
                        if len(self.constellations) < 3:
                            self.constellations.append(self.create_constellation())
                    elif self.experiment_mode == 2:  # Micro-interactions
                        if len(self.symbols) < 15:
                            # Create interaction at random position
                            x = random.randint(5, self.terminal_size.columns - 5)
                            y = random.randint(3, self.terminal_size.lines - 5)
                            self.create_micro_interaction(x, y)
                    
                    last_spawn_time = current_time
                
                # Update elements
                self.update_symbols()
                self.update_constellations()
                
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
            print(f"{ArtisticThemes.MINIMAL.accent}Caret Cuts{ArtisticThemes.MINIMAL.reset}")
            print()
            print(f"{ArtisticThemes.MINIMAL.primary}Symbol constellation experiments complete.{ArtisticThemes.MINIMAL.reset}")
            print()
            print(f"{ArtisticThemes.MINIMAL.secondary}Patterns explored: {self.experiment_mode + 1}/3{ArtisticThemes.MINIMAL.reset}")
            print(f"{ArtisticThemes.MINIMAL.secondary}Symbols manifested: {len(self.symbols) + sum(len(c.symbols) for c in self.constellations)}{ArtisticThemes.MINIMAL.reset}")
            print()
            print(f"{ArtisticThemes.MINIMAL.text}The constellations fade, but their patterns remain in memory...{ArtisticThemes.MINIMAL.reset}")
            print()


if __name__ == "__main__":
    caret_cuts = CaretCuts()
    caret_cuts.run()