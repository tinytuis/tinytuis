# TinyTUIs Issues

This directory contains all the terminal-based zine issues. Each issue is a self-contained Python program that creates an interactive experience in your terminal.

## Running Issues

Each issue can be run independently:

```bash
# From the project root directory
python issues/01-winter-hush/main.py
python issues/02-fragments/main.py
python issues/03-gutter/main.py
python issues/04-echo-chamber/main.py
python issues/05-amber-light/main.py
python issues/06-caret-cuts/main.py
```

Or use the catalog browser:

```bash
python tools/rack.py
```

## Issue Structure

Each issue follows this structure:

```
issues/XX-issue-name/
├── main.py          # The main program
├── README.md        # Issue-specific documentation
└── assets/          # Any additional files (optional)
```

## Requirements

- Python 3.7+
- Terminal with Unicode support
- No external dependencies

## Controls

Most issues use these common controls:

- **Arrow keys**: Navigation
- **Space/Enter**: Interaction
- **q**: Quit
- **Ctrl+C**: Force quit

Specific controls are shown when you run each issue.

## Philosophy

Each issue is designed to be:

- **Experiential**: More than just a program, it's an experience
- **Narrative**: Tells a story or creates a mood
- **Terminal-native**: Embraces the constraints and aesthetics of text interfaces
- **Self-contained**: No external dependencies or complex setup

Enjoy exploring these small digital zines!