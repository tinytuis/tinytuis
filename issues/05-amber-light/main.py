#!/usr/bin/env python3
"""
Amber Light - Issue #5
A retro amber terminal experience with glowing log entries.
Watch system messages stream by in nostalgic monochrome warmth.
"""

import sys
import os
import time
import random
import threading
from dataclasses import dataclass
from typing import List

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', 'lib'))
from tinykit import Canvas, ArtisticThemes, clear_screen, hide_cursor, show_cursor, get_terminal_size, SimpleInput


@dataclass
class LogEntry:
    timestamp: str
    level: str
    message: str
    age: int = 0
    glow: float = 1.0


class AmberTerminal:
    def __init__(self):
        self.running = False
        self.terminal_size = get_terminal_size()
        self.canvas = Canvas(self.terminal_size.columns, self.terminal_size.lines - 2, ArtisticThemes.AMBER)
        self.log_entries: List[LogEntry] = []
        self.log_count = 0
        
        # Retro system messages
        self.system_messages = [
            "System initialization complete",
            "Loading kernel modules...",
            "Network interface configured",
            "Memory check passed",
            "Disk subsystem ready",
            "User authentication enabled",
            "Process scheduler active",
            "File system mounted",
            "Device drivers loaded",
            "Security protocols engaged",
            "Background services started",
            "System ready for operation",
            "Monitoring processes...",
            "Cache optimization running",
            "Garbage collection cycle",
            "Buffer flush completed",
            "Connection pool refreshed",
            "Session cleanup performed",
            "Log rotation executed",
            "Backup verification passed",
            "Performance metrics updated",
            "Resource allocation adjusted",
            "Thread pool expanded",
            "Database connection stable",
            "SSL certificates validated",
            "Firewall rules updated",
            "Load balancer healthy",
            "Service mesh synchronized",
            "Container orchestration active",
            "Microservices responding",
            "API gateway operational",
            "Message queue processing",
            "Event stream flowing",
            "Data pipeline active",
            "Analytics engine running",
            "Machine learning model trained",
            "Neural network converged",
            "Pattern recognition enabled",
            "Anomaly detection active",
            "Predictive algorithms loaded",
            "Real-time processing online"
        ]
        
        self.log_levels = ["INFO", "DEBUG", "WARN", "ERROR", "TRACE"]

    def generate_timestamp(self):
        """Generate a retro-style timestamp."""
        import datetime
        now = datetime.datetime.now()
        return now.strftime("%H:%M:%S.%f")[:-3]

    def add_log_entry(self):
        """Add a new log entry."""
        timestamp = self.generate_timestamp()
        level = random.choice(self.log_levels)
        message = random.choice(self.system_messages)
        
        # Add some variation to messages
        if random.random() < 0.3:
            variations = [
                f"{message} [{random.randint(1000, 9999)}]",
                f"{message} (PID: {random.randint(100, 9999)})",
                f"{message} - {random.choice(['OK', 'DONE', 'READY', 'ACTIVE'])}",
                f"{message} in {random.randint(1, 999)}ms"
            ]
            message = random.choice(variations)
        
        entry = LogEntry(timestamp, level, message)
        self.log_entries.append(entry)
        self.log_count += 1
        
        # Keep only recent entries to prevent memory issues
        if len(self.log_entries) > 100:
            self.log_entries = self.log_entries[-50:]

    def update_log_entries(self):
        """Update log entry aging and glow effects."""
        for entry in self.log_entries:
            entry.age += 1
            # Fade glow over time
            entry.glow = max(0.3, 1.0 - (entry.age * 0.02))

    def render_frame(self):
        """Render the current frame."""
        self.canvas.clear()
        
        # Header with retro styling
        header = "AMBER TERMINAL v2.1 - SYSTEM LOG MONITOR"
        self.canvas.put_text((self.terminal_size.columns - len(header)) // 2, 0, header, self.canvas.theme.accent)
        
        # Separator line
        separator = "=" * min(60, self.terminal_size.columns - 2)
        self.canvas.put_text((self.terminal_size.columns - len(separator)) // 2, 1, separator, self.canvas.theme.border)
        
        # Render log entries
        visible_entries = self.log_entries[-(self.terminal_size.lines - 5):]  # Show recent entries
        
        for i, entry in enumerate(visible_entries):
            y_pos = 3 + i
            if y_pos >= self.terminal_size.lines - 2:
                break
            
            # Format log line
            level_color = self.canvas.theme.accent if entry.level in ["ERROR", "WARN"] else self.canvas.theme.primary
            
            # Timestamp
            self.canvas.put_text(1, y_pos, f"[{entry.timestamp}]", self.canvas.theme.secondary)
            
            # Level
            level_x = 14
            self.canvas.put_text(level_x, y_pos, f"{entry.level:>5}", level_color)
            
            # Message
            msg_x = 21
            max_msg_len = self.terminal_size.columns - msg_x - 1
            message = entry.message
            if len(message) > max_msg_len:
                message = message[:max_msg_len - 3] + "..."
            
            # Apply glow effect by choosing color intensity
            if entry.glow > 0.8:
                msg_color = self.canvas.theme.text
            elif entry.glow > 0.5:
                msg_color = self.canvas.theme.primary
            else:
                msg_color = self.canvas.theme.secondary
            
            self.canvas.put_text(msg_x, y_pos, message, msg_color)
        
        # Status line
        status_y = self.terminal_size.lines - 2
        status = f"LOG ENTRIES: {self.log_count} | ACTIVE: {len(self.log_entries)} | PRESS 'q' TO EXIT"
        if len(status) <= self.terminal_size.columns:
            self.canvas.put_text(0, status_y, status, self.canvas.theme.accent)
        
        # Cursor simulation
        cursor_x = self.terminal_size.columns - 1
        cursor_y = self.terminal_size.lines - 3
        cursor_char = "█" if int(time.time() * 2) % 2 else " "
        self.canvas.put_text(cursor_x, cursor_y, cursor_char, self.canvas.theme.accent)
        
        return self.canvas.render()

    def handle_input(self):
        """Handle keyboard input in a separate thread."""
        try:
            while self.running:
                try:
                    key = SimpleInput.get_key()
                    if key == 'q' or key == '\x03':  # q or Ctrl+C
                        self.running = False
                    # Ignore other keys for this demo
                except:
                    pass
        except:
            pass

    def run(self):
        """Main loop."""
        clear_screen()
        hide_cursor()
        
        print(f"{ArtisticThemes.AMBER.accent}Amber Light{ArtisticThemes.AMBER.reset}")
        print(f"{ArtisticThemes.AMBER.secondary}Issue #5 - Retro Terminal Experience{ArtisticThemes.AMBER.reset}")
        print()
        time.sleep(2)
        
        self.running = True
        
        # Start input handler thread
        input_thread = threading.Thread(target=self.handle_input, daemon=True)
        input_thread.start()
        
        last_log_time = time.time()
        
        try:
            while self.running:
                current_time = time.time()
                
                # Add new log entries periodically
                if current_time - last_log_time > random.uniform(0.5, 2.0):
                    self.add_log_entry()
                    last_log_time = current_time
                
                # Update log entries
                self.update_log_entries()
                
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
            print(f"{ArtisticThemes.AMBER.accent}Amber Light{ArtisticThemes.AMBER.reset}")
            print()
            print(f"{ArtisticThemes.AMBER.primary}System log monitoring session complete.{ArtisticThemes.AMBER.reset}")
            print()
            print(f"{ArtisticThemes.AMBER.secondary}Total log entries processed: {self.log_count}{ArtisticThemes.AMBER.reset}")
            print(f"{ArtisticThemes.AMBER.secondary}The amber glow fades, but the memories remain...{ArtisticThemes.AMBER.reset}")
            print()


if __name__ == "__main__":
    terminal = AmberTerminal()
    terminal.run()