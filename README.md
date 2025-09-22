# TinyTUIs

**A small press for the terminal.**

TinyTUIs treats text user interfaces as creative artifacts — like zines or indie comics — rather than just developer tools. We curate and publish a series of small, narrative-like TUIs that explore the terminal as a medium for expression.

## Vision

Each TUI is an *issue*: short, self-contained, expressive, and meant to be run and experienced in the terminal. We position ourselves at the intersection of:

- **Software as expression** (TUIs as art objects)
- **Zine culture** (small, shareable, personal publishing)  
- **Indie comics** (issues, panels, narratives, collective voice)

## The Catalog

Our current anthology includes:

### Issue #1: Winter Hush
ASCII snow drifting down the terminal. Catch snowflakes to reveal fragments of text. Quiet, contemplative, seasonal.

### Issue #2: Fragments.txt
A scrolling stack of notes, quotes, or diary lines. Users can stitch fragments together into their own narrative. Collage-like, text as material.

### Issue #3: Gutter
A comic reader in the terminal. Panels drawn in ASCII or box art, navigated with arrow keys. Evokes the feel of photocopied mini-comics.

### Issue #4: Echo Chamber
Anything typed echoes back distorted: reversed, scattered, glitched. Creates a strange dialogue between user and machine. Poetic, eerie.

### Issue #5: Amber Light
Retro amber terminal theme. Simulates logs from a fictional machine, or diary entries from a sci-fi world. A nod to the history of terminals as storytelling devices.

### Issue #6: Caret Cuts
A set of very short one-shot TUIs (like one-page comics). Examples: typing a word and watching it unravel, ASCII constellations that redraw, or an overheard conversation scrolling past.

## Running the Issues

Each issue is self-contained and can be run independently:

```bash
python issues/01-winter-hush/main.py
python issues/02-fragments/main.py
python issues/03-gutter/main.py
python issues/04-echo-chamber/main.py
python issues/05-amber-light/main.py
python issues/06-caret-cuts/main.py
```

Or browse the full catalog:

```bash
python tools/rack.py
```

## Web Catalog

View the complete catalog with descriptions and visual previews:

```bash
# Serve the site locally
python -m http.server 8000 --directory site
# Then visit http://localhost:8000
```

## Philosophy

The long-term goal isn't mass adoption or utility — it's creating a **recognizable body of work** that sits at the edge of art, code, and publishing.

## Requirements

- Python 3.7+
- Terminal with Unicode support
- No external dependencies (uses only Python standard library)

## Contributing

We encourage remixing, sharing, and community contributions. Each issue should be:

- **Small**: Focus drives progress, keeps it expressive
- **Narrative**: Tell a story, create an experience  
- **Self-contained**: Runnable as a single experience
- **Expressive**: Explore the terminal as creative medium

See [`docs/CONTRIBUTING.md`](docs/CONTRIBUTING.md) for detailed guidelines.

---

*TinyTUIs - where code meets zine culture*
